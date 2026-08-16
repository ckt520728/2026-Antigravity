"""Scheduling 模組公開介面。

R9：本模組**只回傳預期班表**。任何函式都不得依出勤事件回寫 PlannedShift，
也不得依班表產生 AttendanceEvent。
"""

from __future__ import annotations

import json
from datetime import date, datetime
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import utcnow
from app.core.enums import AuditAction, ShiftType, ShiftVersionState, Unit
from app.modules.audit import service as audit
from app.modules.scheduling.models import PlannedShift, ShiftChangeLog, ShiftVersion


def create_version(
    db: Session,
    *,
    unit: Unit,
    period_start: date,
    period_end: date,
    created_by: str,
    source_note: str | None = None,
) -> ShiftVersion:
    """建立新的班表版本（草稿）。"""
    previous = _latest_approved(db, unit=unit, start=period_start, end=period_end)
    version = ShiftVersion(
        unit=unit,
        period_start=period_start,
        period_end=period_end,
        created_by=created_by,
        version_no=(previous.version_no + 1) if previous else 1,
        supersedes_id=previous.id if previous else None,
        source_note=source_note,
    )
    db.add(version)
    db.flush()

    audit.record(
        db,
        action=AuditAction.CREATE,
        entity_type="shift_version",
        entity_id=version.id,
        actor_id=created_by,
        after={"unit": unit.value, "version_no": version.version_no},
        reason=source_note or "建立班表版本",
    )
    return version


def approve_version(
    db: Session, *, version_id: str, approver_id: str, note: str | None = None
) -> ShiftVersion:
    """主管核准班表版本，並將前一版標記為 SUPERSEDED（不刪除）。"""
    version = db.get(ShiftVersion, version_id)
    if version is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="找不到班表版本"
        )
    if version.state is ShiftVersionState.APPROVED:
        return version
    if version.created_by == approver_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="不得核准自己建立的班表版本"
        )

    version.state = ShiftVersionState.APPROVED
    version.approved_by = approver_id
    version.approved_at = utcnow()

    if version.supersedes_id:
        previous = db.get(ShiftVersion, version.supersedes_id)
        if previous is not None:
            previous.state = ShiftVersionState.SUPERSEDED

    db.flush()
    audit.record(
        db,
        action=AuditAction.APPROVE,
        entity_type="shift_version",
        entity_id=version.id,
        actor_id=approver_id,
        after={"state": version.state.value},
        reason=note or "核准班表版本",
    )
    return version


def add_shift(
    db: Session,
    *,
    version_id: str,
    staff_id: str,
    shift_date: date,
    shift_type: ShiftType,
    start_at: datetime,
    end_at: datetime,
    actor_id: str,
    clinic_code: str | None = None,
    room_code: str | None = None,
    ward_code: str | None = None,
) -> PlannedShift:
    shift = PlannedShift(
        version_id=version_id,
        staff_id=staff_id,
        shift_date=shift_date,
        shift_type=shift_type,
        start_at=start_at,
        end_at=end_at,
        clinic_code=clinic_code,
        room_code=room_code,
        ward_code=ward_code,
    )
    db.add(shift)
    db.flush()

    _log_change(
        db,
        version_id=version_id,
        planned_shift_id=shift.id,
        actor_id=actor_id,
        previous=None,
        new={"shift_type": shift_type.value, "start_at": start_at, "end_at": end_at},
        reason="新增班別",
    )
    return shift


def edit_shift(
    db: Session,
    *,
    shift_id: str,
    actor_id: str,
    reason: str,
    **changes: Any,
) -> PlannedShift:
    """編輯班別。決議 12：必須保留原值、操作者、時間戳記、理由。"""
    if not reason.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="換班或編輯必須填寫理由"
        )

    shift = db.get(PlannedShift, shift_id)
    if shift is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="找不到班別")

    previous = {
        "staff_id": shift.staff_id,
        "shift_type": shift.shift_type,
        "start_at": shift.start_at,
        "end_at": shift.end_at,
        "clinic_code": shift.clinic_code,
        "ward_code": shift.ward_code,
    }

    for field, value in changes.items():
        if value is not None and hasattr(shift, field):
            setattr(shift, field, value)
    db.flush()

    _log_change(
        db,
        version_id=shift.version_id,
        planned_shift_id=shift.id,
        actor_id=actor_id,
        previous=previous,
        new=changes,
        reason=reason,
    )
    return shift


def shifts_for_staff(
    db: Session, *, staff_id: str, start: date, end: date
) -> list[dict[str, Any]]:
    """供 overtime 模組取用的**唯讀** dict 檢視。

    刻意回傳 dict 而非 ORM 物件，讓跨模組呼叫端在型別上就無法回寫班表 (R9)。
    """
    stmt = (
        select(PlannedShift)
        .join(ShiftVersion, PlannedShift.version_id == ShiftVersion.id)
        .where(
            PlannedShift.staff_id == staff_id,
            PlannedShift.shift_date >= start,
            PlannedShift.shift_date <= end,
            ShiftVersion.state == ShiftVersionState.APPROVED,
        )
        .order_by(PlannedShift.shift_date)
    )
    return [
        {
            "id": s.id,
            "shift_date": s.shift_date,
            "shift_type": s.shift_type,
            "start_at": s.start_at,
            "end_at": s.end_at,
            "clinic_code": s.clinic_code,
            "ward_code": s.ward_code,
        }
        for s in db.execute(stmt).scalars().all()
    ]


def _latest_approved(
    db: Session, *, unit: Unit, start: date, end: date
) -> ShiftVersion | None:
    stmt = (
        select(ShiftVersion)
        .where(
            ShiftVersion.unit == unit,
            ShiftVersion.period_start == start,
            ShiftVersion.period_end == end,
            ShiftVersion.state == ShiftVersionState.APPROVED,
        )
        .order_by(ShiftVersion.version_no.desc())
        .limit(1)
    )
    return db.execute(stmt).scalar_one_or_none()


def _log_change(
    db: Session,
    *,
    version_id: str,
    planned_shift_id: str | None,
    actor_id: str,
    previous: dict[str, Any] | None,
    new: dict[str, Any] | None,
    reason: str,
) -> None:
    db.add(
        ShiftChangeLog(
            version_id=version_id,
            planned_shift_id=planned_shift_id,
            actor_id=actor_id,
            changed_at=utcnow(),
            previous_value=json.dumps(previous, ensure_ascii=False, default=str)
            if previous
            else None,
            new_value=json.dumps(new, ensure_ascii=False, default=str) if new else None,
            reason=reason,
        )
    )
