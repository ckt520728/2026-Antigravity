"""Overtime 模組公開介面：工時彙總與加班候選計算（需求 j）。

紅線 R4：本模組**只產生 Overtime Candidate**。
沒有任何函式會把時數送往薪資系統，也不得新增這種函式。
"""

from __future__ import annotations

import json
from datetime import date, datetime, time, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import utcnow
from app.core.enums import ShiftType, SummaryStatus
from app.modules.attendance import service as attendance
from app.modules.overtime.models import ComplianceFlag, WorkHourSummary
from app.modules.scheduling import service as scheduling


def _policy_snapshot() -> dict[str, int | bool]:
    """記錄計算當下的政策參數，讓日後政策異動不會改寫歷史彙總。"""
    labor = settings.labor
    return {
        "daily_regular_minutes": labor.daily_regular_minutes,
        "weekly_regular_minutes": labor.weekly_regular_minutes,
        "daily_max_minutes": labor.daily_max_minutes,
        "monthly_overtime_cap_minutes": labor.monthly_overtime_cap_minutes,
        "min_shift_interval_minutes": labor.min_shift_interval_minutes,
        "labor_rules_reviewed": labor.labor_rules_reviewed,
    }


def calculate_summary(
    db: Session,
    *,
    staff_id: str,
    period_start: date,
    period_end: date,
) -> WorkHourSummary:
    """計算某員工在期間內的工時彙總。

    流程：
    1. 取出配對後的工作區段（attendance 模組）；
    2. 取出預期班表（scheduling 模組）——**只讀，不覆寫** (R9)；
    3. 拆解為正常工時 / 加班候選 / 夜間值班 / 假日值班；
    4. 產生勞基法門檻提示（非違法認定）。
    """
    start_dt = datetime.combine(period_start, time.min).astimezone()
    end_dt = datetime.combine(period_end, time.max).astimezone()

    pairing = attendance.pair_for_period(
        db, staff_id=staff_id, start=start_dt, end=end_dt
    )
    shifts = scheduling.shifts_for_staff(
        db, staff_id=staff_id, start=period_start, end=period_end
    )
    shift_by_date = {s["shift_date"]: s for s in shifts}

    labor = settings.labor
    regular = 0
    overtime_candidate = 0
    night_duty = 0
    holiday_duty = 0

    for session in pairing.sessions:
        if not session.is_closed:
            continue

        minutes = session.worked_minutes
        session_date = session.start_at.date()
        shift = shift_by_date.get(session_date)
        shift_type = shift["shift_type"] if shift else None

        # 需求 h / i：夜間與假日值班另計時數桶。
        if shift_type == ShiftType.NIGHT_DUTY:
            night_duty += minutes
        elif shift_type == ShiftType.HOLIDAY_DUTY:
            holiday_duty += minutes

        # 超過每日正常工時的部分為加班候選。
        day_regular = min(minutes, labor.daily_regular_minutes)
        regular += day_regular
        overtime_candidate += max(0, minutes - labor.daily_regular_minutes)

        # 勞基法 §32：每日工時上限提示。
        if minutes > labor.daily_max_minutes:
            _flag(
                db,
                staff_id=staff_id,
                rule_code="LSA_32_DAILY_MAX",
                observed=minutes,
                threshold=labor.daily_max_minutes,
                occurred_on=session_date,
                note="單日工時超過上限（提示，非違法認定）",
            )

    # 勞基法 §32：每月加班上限提示。
    if overtime_candidate > labor.monthly_overtime_cap_minutes:
        _flag(
            db,
            staff_id=staff_id,
            rule_code="LSA_32_MONTHLY_OT_CAP",
            observed=overtime_candidate,
            threshold=labor.monthly_overtime_cap_minutes,
            occurred_on=period_end,
            note="期間加班時數超過上限（提示，非違法認定）",
        )

    # 勞基法 §34：輪班間隔提示。
    _check_shift_interval(db, staff_id=staff_id, pairing=pairing)

    summary = _upsert(db, staff_id=staff_id, start=period_start, end=period_end)
    summary.first_check_in_at = pairing.first_check_in_at
    summary.last_check_out_at = pairing.last_check_out_at
    summary.total_out_count = pairing.total_out_count
    summary.total_work_minutes = pairing.total_work_minutes
    summary.regular_minutes = regular
    summary.overtime_candidate_minutes = overtime_candidate
    summary.night_duty_minutes = night_duty
    summary.holiday_duty_minutes = holiday_duty
    summary.unmatched_event_count = pairing.unmatched_count
    summary.policy_snapshot = json.dumps(_policy_snapshot(), ensure_ascii=False)
    summary.policy_reviewed = labor.labor_rules_reviewed
    summary.calculated_at = utcnow()

    # 影子模式：加班永遠停在候選狀態，等待核准 (R4)。
    summary.status = (
        SummaryStatus.CANDIDATE if overtime_candidate > 0 else SummaryStatus.DRAFT
    )

    db.flush()
    return summary


def _check_shift_interval(db: Session, *, staff_id: str, pairing) -> None:
    """勞基法 §34：連續兩班之間應有 11 小時休息。"""
    closed = sorted(
        (s for s in pairing.sessions if s.is_closed), key=lambda s: s.start_at
    )
    threshold = settings.labor.min_shift_interval_minutes
    for previous, current in zip(closed, closed[1:], strict=False):
        gap = int((current.start_at - previous.end_at) / timedelta(minutes=1))
        if 0 <= gap < threshold:
            _flag(
                db,
                staff_id=staff_id,
                rule_code="LSA_34_SHIFT_INTERVAL",
                observed=gap,
                threshold=threshold,
                occurred_on=current.start_at.date(),
                note="輪班間隔不足（提示，非違法認定）",
            )


def _flag(
    db: Session,
    *,
    staff_id: str,
    rule_code: str,
    observed: int,
    threshold: int,
    occurred_on: date,
    note: str,
) -> None:
    db.add(
        ComplianceFlag(
            staff_id=staff_id,
            rule_code=rule_code,
            observed_value=observed,
            threshold_value=threshold,
            occurred_on=occurred_on,
            note=note,
        )
    )


def _upsert(
    db: Session, *, staff_id: str, start: date, end: date
) -> WorkHourSummary:
    stmt = select(WorkHourSummary).where(
        WorkHourSummary.staff_id == staff_id,
        WorkHourSummary.period_start == start,
        WorkHourSummary.period_end == end,
    )
    summary = db.execute(stmt).scalar_one_or_none()
    if summary is None:
        summary = WorkHourSummary(
            staff_id=staff_id, period_start=start, period_end=end
        )
        db.add(summary)
        db.flush()
    return summary


def summaries_for_period(
    db: Session, *, period_start: date, period_end: date
) -> list[WorkHourSummary]:
    """供 reporting 模組取用。"""
    stmt = select(WorkHourSummary).where(
        WorkHourSummary.period_start == period_start,
        WorkHourSummary.period_end == period_end,
    )
    return list(db.execute(stmt).scalars().all())
