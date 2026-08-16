"""Overtime API：工時彙總與加班候選（需求 j）。"""

from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.config import settings
from app.core.deps import AuthedStaff, DbSession, require_feature
from app.core.features import Feature
from app.modules.overtime import service

router = APIRouter(prefix="/overtime", tags=["overtime"])

aggregation_gate = Depends(require_feature(Feature.OVERTIME_AGGREGATION))


class CalculateRequest(BaseModel):
    staff_id: str
    period_start: date
    period_end: date


@router.post("/calculate", dependencies=[aggregation_gate])
def calculate(payload: CalculateRequest, db: DbSession, staff: AuthedStaff):
    """計算工時彙總。

    影子模式：結果永遠停在 CANDIDATE，**不會**也不得送往薪資 (R4)。
    """
    summary = service.calculate_summary(
        db,
        staff_id=payload.staff_id,
        period_start=payload.period_start,
        period_end=payload.period_end,
    )
    return {
        "id": summary.id,
        "first_check_in_at": summary.first_check_in_at,
        "last_check_out_at": summary.last_check_out_at,
        "total_out_count": summary.total_out_count,
        "total_work_minutes": summary.total_work_minutes,
        "regular_minutes": summary.regular_minutes,
        "overtime_candidate_minutes": summary.overtime_candidate_minutes,
        "night_duty_minutes": summary.night_duty_minutes,
        "holiday_duty_minutes": summary.holiday_duty_minutes,
        "unmatched_event_count": summary.unmatched_event_count,
        "status": summary.status,
        "shadow_mode": settings.shadow_mode,
        "policy_reviewed": summary.policy_reviewed,
        "warning": None
        if summary.policy_reviewed
        else "工時門檻尚未經人事室與勞動法規權責單位複核，僅供參考。",
    }


@router.get("/summaries", dependencies=[aggregation_gate])
def list_summaries(
    db: DbSession, staff: AuthedStaff, period_start: date, period_end: date
):
    summaries = service.summaries_for_period(
        db, period_start=period_start, period_end=period_end
    )
    return [
        {
            "staff_id": s.staff_id,
            "total_work_minutes": s.total_work_minutes,
            "overtime_candidate_minutes": s.overtime_candidate_minutes,
            "status": s.status,
        }
        for s in summaries
    ]
