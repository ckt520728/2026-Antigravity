"""Reporting API：Excel / Word / 統計圖下載 (CLAUDE.md §9)。

所有下載行為都必須寫入 audit_log。
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import AuthedStaff, DbSession, require_feature
from app.core.features import Feature
from app.modules.attendance import service as attendance_service
from app.modules.audit import service as audit
from app.modules.identity import service as identity
from app.modules.overtime import service as overtime
from app.modules.reporting import service as reporting

router = APIRouter(prefix="/reports", tags=["reporting"])

# 報表內容來自工時彙總，因此同受需求 j 的開關控制。
aggregation_gate = Depends(require_feature(Feature.OVERTIME_AGGREGATION))


def _build_rows(db: Session, period_start: date, period_end: date) -> list[dict]:
    """把工時彙總與員工基本資料合併成報表列。"""
    summaries = overtime.summaries_for_period(
        db, period_start=period_start, period_end=period_end
    )
    directory = identity.staff_directory(db)

    # 若特定期間內無打卡彙總，仍列出所有在職員工以供完整對照
    existing_staff_ids = {s.staff_id for s in summaries}
    rows: list[dict] = []
    
    for s in summaries:
        info = directory.get(s.staff_id, {})
        rows.append(
            {
                "employee_no": info.get("employee_no", ""),
                "name": info.get("name", ""),
                "unit": info.get("unit", ""),
                "role": info.get("role", ""),
                "first_check_in_at": s.first_check_in_at,
                "last_check_out_at": s.last_check_out_at,
                "total_out_count": s.total_out_count,
                "total_work_minutes": s.total_work_minutes,
                "regular_minutes": s.regular_minutes,
                "overtime_candidate_minutes": s.overtime_candidate_minutes,
                "night_duty_minutes": s.night_duty_minutes,
                "holiday_duty_minutes": s.holiday_duty_minutes,
                "unmatched_event_count": s.unmatched_event_count,
                "status": s.status,
            }
        )
        
    for staff_id, info in directory.items():
        if staff_id not in existing_staff_ids and info.get("active", True):
            rows.append(
                {
                    "employee_no": info.get("employee_no", ""),
                    "name": info.get("name", ""),
                    "unit": info.get("unit", ""),
                    "role": info.get("role", ""),
                    "first_check_in_at": None,
                    "last_check_out_at": None,
                    "total_out_count": 0,
                    "total_work_minutes": 0,
                    "regular_minutes": 0,
                    "overtime_candidate_minutes": 0,
                    "night_duty_minutes": 0,
                    "holiday_duty_minutes": 0,
                    "unmatched_event_count": 0,
                    "status": "未到勤",
                }
            )

    rows.sort(key=lambda r: r["employee_no"])
    return rows


@router.get("/kiosk/excel")
def kiosk_excel_export(
    db: DbSession,
    period_start: Optional[date] = Query(default=None),
    period_end: Optional[date] = Query(default=None),
    facility_name: str = Query(default="陽明醫院附設護理之家"),
):
    """護理站前台與主管一鍵匯出 Excel 報表 (包含多工作表：工時總表、打卡流水、醫師巡診)。"""
    today = date.today()
    start_d = period_start or today.replace(day=1)
    end_d = period_end or today

    rows = _build_rows(db, start_d, end_d)
    events = attendance_service.list_events_for_period(db, period_start=start_d, period_end=end_d)
    
    ctx = reporting.ReportContext(
        period_start=start_d,
        period_end=end_d,
        generated_by="護理站管理者",
        facility_name=facility_name,
    )
    content = reporting.build_excel(rows, ctx, events=events)

    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": (
                f'attachment; filename="attendance-report-{start_d}-{end_d}.xlsx"'
            )
        },
    )


@router.get("/kiosk/word")
def kiosk_word_export(
    db: DbSession,
    period_start: Optional[date] = Query(default=None),
    period_end: Optional[date] = Query(default=None),
    facility_name: str = Query(default="陽明醫院附設護理之家"),
):
    """護理站前台與主管一鍵匯出 Word 統計報表 (專業醫療文書排版與簽核區)。"""
    today = date.today()
    start_d = period_start or today.replace(day=1)
    end_d = period_end or today

    rows = _build_rows(db, start_d, end_d)
    events = attendance_service.list_events_for_period(db, period_start=start_d, period_end=end_d)
    
    ctx = reporting.ReportContext(
        period_start=start_d,
        period_end=end_d,
        generated_by="護理站管理者",
        facility_name=facility_name,
    )
    content = reporting.build_word(
        rows, ctx, title=f"{facility_name} 員工出勤與巡診統計月報", events=events
    )

    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition": (
                f'attachment; filename="attendance-summary-{start_d}-{end_d}.docx"'
            )
        },
    )


@router.get("/work-hours.xlsx", dependencies=[aggregation_gate])
def work_hours_excel(
    db: DbSession, staff: AuthedStaff, period_start: date, period_end: date
):
    rows = _build_rows(db, period_start, period_end)
    events = attendance_service.list_events_for_period(db, period_start=period_start, period_end=period_end)
    ctx = reporting.ReportContext(
        period_start=period_start,
        period_end=period_end,
        generated_by=staff.employee_no or staff.staff_id,
    )
    content = reporting.build_excel(rows, ctx, events=events)

    audit.record_export(
        db,
        actor_id=staff.staff_id,
        report_type="work_hours",
        file_format="xlsx",
        filters={"period_start": str(period_start), "period_end": str(period_end)},
    )
    return Response(
        content=content,
        media_type=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
        headers={
            "Content-Disposition": (
                f'attachment; filename="work-hours-{period_start}-{period_end}.xlsx"'
            )
        },
    )


@router.get("/work-hours.docx", dependencies=[aggregation_gate])
def work_hours_word(
    db: DbSession, staff: AuthedStaff, period_start: date, period_end: date
):
    rows = _build_rows(db, period_start, period_end)
    events = attendance_service.list_events_for_period(db, period_start=period_start, period_end=period_end)
    ctx = reporting.ReportContext(
        period_start=period_start,
        period_end=period_end,
        generated_by=staff.employee_no or staff.staff_id,
    )
    content = reporting.build_word(rows, ctx, title="員工工時與加班月報", events=events)

    audit.record_export(
        db,
        actor_id=staff.staff_id,
        report_type="work_hours",
        file_format="docx",
        filters={"period_start": str(period_start), "period_end": str(period_end)},
    )
    return Response(
        content=content,
        media_type=(
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ),
        headers={
            "Content-Disposition": (
                f'attachment; filename="work-hours-{period_start}-{period_end}.docx"'
            )
        },
    )


@router.get("/overtime-plot.png", dependencies=[aggregation_gate])
def overtime_plot(
    db: DbSession, staff: AuthedStaff, period_start: date, period_end: date
):
    rows = _build_rows(db, period_start, period_end)
    ctx = reporting.ReportContext(
        period_start=period_start,
        period_end=period_end,
        generated_by=staff.employee_no or staff.staff_id,
    )
    content = reporting.build_overtime_plot(rows, ctx)

    audit.record_export(
        db,
        actor_id=staff.staff_id,
        report_type="overtime_plot",
        file_format="png",
        filters={"period_start": str(period_start), "period_end": str(period_end)},
    )
    return Response(content=content, media_type="image/png")


@router.get("/unit-distribution.png", dependencies=[aggregation_gate])
def unit_distribution_plot(
    db: DbSession, staff: AuthedStaff, period_start: date, period_end: date
):
    rows = _build_rows(db, period_start, period_end)
    ctx = reporting.ReportContext(
        period_start=period_start,
        period_end=period_end,
        generated_by=staff.employee_no or staff.staff_id,
    )
    content = reporting.build_unit_distribution_plot(rows, ctx)

    audit.record_export(
        db,
        actor_id=staff.staff_id,
        report_type="unit_distribution",
        file_format="png",
        filters={"period_start": str(period_start), "period_end": str(period_end)},
    )
    return Response(content=content, media_type="image/png")
