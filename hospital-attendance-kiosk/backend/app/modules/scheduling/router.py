"""Scheduling API：班表版本、班別、OPD 診次（需求 c）。"""

from __future__ import annotations

from datetime import date, datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.core.deps import AuthedStaff, DbSession, require_feature
from app.core.enums import ShiftType, Unit
from app.core.features import Feature
from app.modules.scheduling import service

router = APIRouter(prefix="/scheduling", tags=["scheduling"])

# 需求 c：門診診次排程控制。
opd_gate = Depends(require_feature(Feature.OPD_SCHEDULE))


class VersionCreate(BaseModel):
    unit: Unit
    period_start: date
    period_end: date
    source_note: str | None = None


class ShiftCreate(BaseModel):
    staff_id: str
    shift_date: date
    shift_type: ShiftType
    start_at: datetime
    end_at: datetime
    clinic_code: str | None = None
    room_code: str | None = None
    ward_code: str | None = None


class ShiftEdit(BaseModel):
    reason: str = Field(min_length=1, description="換班或編輯必填理由")
    staff_id: str | None = None
    shift_type: ShiftType | None = None
    start_at: datetime | None = None
    end_at: datetime | None = None
    clinic_code: str | None = None
    ward_code: str | None = None


class ApprovalAction(BaseModel):
    note: str | None = None


@router.post("/versions", status_code=201, dependencies=[opd_gate])
def create_version(payload: VersionCreate, db: DbSession, staff: AuthedStaff):
    version = service.create_version(
        db,
        unit=payload.unit,
        period_start=payload.period_start,
        period_end=payload.period_end,
        created_by=staff.staff_id,
        source_note=payload.source_note,
    )
    return {"id": version.id, "version_no": version.version_no, "state": version.state}


@router.post("/versions/{version_id}/approve", dependencies=[opd_gate])
def approve_version(
    version_id: str, payload: ApprovalAction, db: DbSession, staff: AuthedStaff
):
    version = service.approve_version(
        db, version_id=version_id, approver_id=staff.staff_id, note=payload.note
    )
    return {"id": version.id, "state": version.state}


@router.post("/versions/{version_id}/shifts", status_code=201, dependencies=[opd_gate])
def add_shift(
    version_id: str, payload: ShiftCreate, db: DbSession, staff: AuthedStaff
):
    shift = service.add_shift(
        db,
        version_id=version_id,
        staff_id=payload.staff_id,
        shift_date=payload.shift_date,
        shift_type=payload.shift_type,
        start_at=payload.start_at,
        end_at=payload.end_at,
        actor_id=staff.staff_id,
        clinic_code=payload.clinic_code,
        room_code=payload.room_code,
        ward_code=payload.ward_code,
    )
    return {"id": shift.id}


@router.patch("/shifts/{shift_id}", dependencies=[opd_gate])
def edit_shift(shift_id: str, payload: ShiftEdit, db: DbSession, staff: AuthedStaff):
    """編輯／換班。原值、操作者、時間、理由一律寫入 ShiftChangeLog。"""
    changes = payload.model_dump(exclude={"reason"}, exclude_none=True)
    shift = service.edit_shift(
        db, shift_id=shift_id, actor_id=staff.staff_id, reason=payload.reason, **changes
    )
    return {"id": shift.id, "shift_type": shift.shift_type}


@router.get("/shifts", dependencies=[opd_gate])
def list_shifts(db: DbSession, staff: AuthedStaff, start: date, end: date):
    """查詢自己的班表。"""
    return service.shifts_for_staff(db, staff_id=staff.staff_id, start=start, end=end)


# TODO(open-decision): 標準 Excel 範本匯入 (CLAUDE.md 決議 12)。
# 範本欄位定義尚未與人事室確認，實作前需先取得實際使用中的班表檔案。
