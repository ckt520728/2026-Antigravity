"""Attendance API。

功能開關 (CLAUDE.md §5)：打卡端點的可用性同時取決於
**事件型別**與**呼叫者的單位／職務**，因此不能只掛一個 require_feature，
必須用 `_required_features()` 動態解析。關閉時一律回 404。
"""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.core.deps import AuthedStaff, DbSession
from app.core.enums import AttendanceEventType, EventSource, StaffRole, Unit
from app.core.feature_store import FeatureFlagService
from app.core.features import FEATURE_LABELS, Feature
from app.modules.attendance import service

router = APIRouter(prefix="/attendance", tags=["attendance"])


# --------------------------------------------------------------------------
# Schemas
# --------------------------------------------------------------------------


class CheckInRequest(BaseModel):
    event_type: AttendanceEventType
    occurred_at: datetime | None = Field(
        default=None, description="留空則以伺服器接收時間為準"
    )
    verification_id: str | None = Field(
        default=None, description="identity 驗證成功後回傳的 id"
    )
    station_id: str | None = None
    ward_code: str | None = Field(
        default=None, description="僅 CLINICAL_ROUND_SIGN_IN 使用；病房層級，非病人"
    )
    client_event_uid: str | None = Field(
        default=None, description="kiosk 離線補送用的冪等鍵"
    )


class AttendanceEventOut(BaseModel):
    id: str
    staff_id: str
    event_type: AttendanceEventType
    occurred_at: datetime
    source: EventSource
    ward_code: str | None = None
    is_corrected: bool

    model_config = {"from_attributes": True}


class CorrectionCreate(BaseModel):
    attendance_event_id: str | None = None
    requested_occurred_at: datetime
    requested_event_type: AttendanceEventType
    reason: str = Field(min_length=1, description="必填；空白理由一律拒絕")


class ApprovalAction(BaseModel):
    note: str | None = None


class RejectionAction(BaseModel):
    reason: str = Field(min_length=1)


# --------------------------------------------------------------------------
# 功能開關解析
# --------------------------------------------------------------------------

#: 單位／職務 → 對應的出勤功能開關（需求 e, f, g）。
_ROLE_UNIT_FEATURE: dict[tuple[Unit, StaffRole], Feature] = {
    (Unit.OPD, StaffRole.NURSE): Feature.OPD_NURSE,
    (Unit.OPD, StaffRole.NURSE_SPECIALIST): Feature.OPD_NURSE,
    (Unit.ER, StaffRole.NURSE): Feature.ER_INPATIENT_NURSE,
    (Unit.ER, StaffRole.NURSE_SPECIALIST): Feature.ER_INPATIENT_NURSE,
    (Unit.INPATIENT, StaffRole.NURSE): Feature.ER_INPATIENT_NURSE,
    (Unit.INPATIENT, StaffRole.NURSE_SPECIALIST): Feature.ER_INPATIENT_NURSE,
}

_NONMEDICAL_ROLES = {
    StaffRole.REGISTRATION,
    StaffRole.ACCOUNTANT,
    StaffRole.MEDICAL_ADMIN,
}


def _required_features(
    event_type: AttendanceEventType, role: str, unit: str | None
) -> list[Feature]:
    """解析此次打卡需要哪些功能開關同時為開。"""
    required: list[Feature] = []

    if event_type in (
        AttendanceEventType.CHECK_IN,
        AttendanceEventType.CHECK_OUT,
        AttendanceEventType.BREAK_IN,
        AttendanceEventType.BREAK_OUT,
    ):
        required.append(Feature.WORK_HOURS)  # 需求 b
    elif event_type in (
        AttendanceEventType.ON_DUTY_SIGN_IN,
        AttendanceEventType.ON_DUTY_SIGN_OUT,
    ):
        # 需求 h / i：夜間與假日值班共用端點，
        # 只要其中一個開關開啟即允許；由班表決定實際歸屬。
        required.append(Feature.NIGHT_DUTY)
    elif event_type is AttendanceEventType.CLINICAL_ROUND_SIGN_IN:
        required.append(Feature.WARD_ROUND_SIGNIN)  # 需求 d

    try:
        role_enum = StaffRole(role)
        unit_enum = Unit(unit) if unit else None
    except ValueError:
        return required

    if unit_enum is not None:
        specific = _ROLE_UNIT_FEATURE.get((unit_enum, role_enum))
        if specific is not None:
            required.append(specific)

    if role_enum in _NONMEDICAL_ROLES:
        required.append(Feature.NONMEDICAL_STAFF)  # 需求 g

    return required


def _assert_features(db, features: list[Feature]) -> None:
    for feature in features:
        if not FeatureFlagService.is_enabled(db, feature):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"功能未啟用：{FEATURE_LABELS.get(feature, feature.value)}",
            )


# --------------------------------------------------------------------------
# Endpoints
# --------------------------------------------------------------------------


@router.post("/events", response_model=AttendanceEventOut, status_code=201)
def record_event(payload: CheckInRequest, db: DbSession, staff: AuthedStaff):
    """打卡／簽到。唯一的事件寫入路徑。"""
    _assert_features(db, _required_features(payload.event_type, staff.role, staff.unit))

    # 需求 a：生物驗證開啟時，打卡必須附帶 verification_id。
    if (
        FeatureFlagService.is_enabled(db, Feature.BIOMETRIC_PRESENCE)
        and payload.verification_id is None
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="已啟用生物辨識在勤確認，打卡必須附帶 verification_id",
        )

    event = service.record_event(
        db,
        staff_id=staff.staff_id,
        event_type=payload.event_type,
        occurred_at=payload.occurred_at or datetime.now().astimezone(),
        source=EventSource.KIOSK_WEBAUTHN
        if payload.verification_id
        else EventSource.WEB,
        verification_id=payload.verification_id,
        station_id=payload.station_id,
        ward_code=payload.ward_code,
        client_event_uid=payload.client_event_uid,
    )
    return event


@router.get("/events", response_model=list[AttendanceEventOut])
def list_events(
    db: DbSession,
    staff: AuthedStaff,
    start: datetime,
    end: datetime,
    staff_id: str | None = None,
):
    """查詢出勤事件。

    TODO(open-decision): 角色權限矩陣未定案前，僅允許查詢自己的紀錄。
    主管／人事的跨員工查詢範圍待確認後開放。
    """
    target = staff_id or staff.staff_id
    if target != staff.staff_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="跨員工查詢權限尚未開放（角色權限矩陣待定案）",
        )
    return service.list_events(db, staff_id=target, start=start, end=end)


@router.post("/corrections", status_code=201)
def submit_correction(payload: CorrectionCreate, db: DbSession, staff: AuthedStaff):
    """提出更正申請 (CLAUDE.md §10)。"""
    request = service.submit_correction(
        db,
        staff_id=staff.staff_id,
        requested_by=staff.staff_id,
        requested_occurred_at=payload.requested_occurred_at,
        requested_event_type=payload.requested_event_type,
        reason=payload.reason,
        attendance_event_id=payload.attendance_event_id,
    )
    return {"id": request.id, "state": request.state}


@router.post("/corrections/{request_id}/supervisor-approve")
def supervisor_approve(
    request_id: str, payload: ApprovalAction, db: DbSession, staff: AuthedStaff
):
    request = service.supervisor_approve(
        db, request_id=request_id, supervisor_id=staff.staff_id, note=payload.note
    )
    return {"id": request.id, "state": request.state}


@router.post("/corrections/{request_id}/hr-confirm")
def hr_confirm(
    request_id: str, payload: ApprovalAction, db: DbSession, staff: AuthedStaff
):
    request = service.hr_confirm(
        db, request_id=request_id, hr_id=staff.staff_id, note=payload.note
    )
    return {"id": request.id, "state": request.state}


@router.post("/corrections/{request_id}/apply")
def apply_correction(request_id: str, db: DbSession, staff: AuthedStaff):
    event = service.apply_correction(
        db, request_id=request_id, actor_id=staff.staff_id
    )
    return {"resulting_event_id": event.id}


@router.post("/corrections/{request_id}/reject")
def reject_correction(
    request_id: str, payload: RejectionAction, db: DbSession, staff: AuthedStaff
):
    request = service.reject_correction(
        db, request_id=request_id, actor_id=staff.staff_id, reason=payload.reason
    )
    return {"id": request.id, "state": request.state}


# --------------------------------------------------------------------------
# 護理站電腦網頁版 Kiosk 打卡 API (滑鼠點擊 / 鍵盤輸入)
# --------------------------------------------------------------------------


class KioskStaffOut(BaseModel):
    id: str
    employee_no: str
    name: str
    unit: str
    role: str
    employment_type: str


class KioskPunchRequest(BaseModel):
    employee_no: str = Field(description="員工工號，如 YM-DOC-01, YM-NUR-01")
    event_type: AttendanceEventType
    station_id: str = Field(default="YM-3F-KIOSK", description="護理站終端編號")
    ward_code: str | None = Field(default=None, description="病房層級代碼，如 3F-NH")
    override_reason: str | None = Field(default=None, description="例外或手動打卡原因")
    client_event_uid: str | None = Field(default=None, description="前端離線補送 UUID")
    occurred_at: datetime | None = Field(default=None, description="打卡時間")


class KioskPunchOut(BaseModel):
    event_id: str
    employee_no: str
    name: str
    role: str
    event_type: AttendanceEventType
    occurred_at: datetime
    ward_code: str | None = None
    station_id: str | None = None
    message: str


class KioskPunchHistoryItem(BaseModel):
    id: str
    staff_id: str
    employee_no: str
    name: str
    role: str
    event_type: AttendanceEventType
    occurred_at: datetime
    ward_code: str | None = None
    source: EventSource


@router.get("/kiosk/staff", response_model=list[KioskStaffOut])
def get_kiosk_staff_list(db: DbSession, unit: str | None = None):
    """取得護理站 Kiosk 可供鍵盤/滑鼠快速選擇的在職同仁名單。"""
    from app.modules.identity import service as identity_service

    return identity_service.list_active_staff_summary(db, unit=unit)


@router.get("/kiosk/recent-punches", response_model=list[KioskPunchHistoryItem])
def get_kiosk_recent_punches(db: DbSession, limit: int = 30):
    """取得護理站 Kiosk 最新打卡流水清單（即時出勤看板）。"""
    from app.modules.identity import service as identity_service

    events = service.list_recent_events_all(db, limit=limit)
    directory = identity_service.staff_directory(db)

    result = []
    for ev in events:
        info = directory.get(ev.staff_id, {})
        result.append(
            KioskPunchHistoryItem(
                id=ev.id,
                staff_id=ev.staff_id,
                employee_no=info.get("employee_no", "UNKNOWN"),
                name=info.get("name", "未知"),
                role=info.get("role", "UNKNOWN"),
                event_type=ev.event_type,
                occurred_at=ev.occurred_at,
                ward_code=ev.ward_code,
                source=ev.source,
            )
        )
    return result


@router.post("/kiosk/punch", response_model=KioskPunchOut, status_code=201)
def kiosk_punch(payload: KioskPunchRequest, db: DbSession):
    """護理站電腦網頁版打卡簽到（支援鍵盤鍵入工號、滑鼠點擊、朱醫師巡診簽到、離線同步）。"""
    from app.modules.identity import service as identity_service

    # 1. 查詢員工
    staff_info = identity_service.get_staff_by_no(db, payload.employee_no.strip())
    staff_id = staff_info["id"]
    staff_name = staff_info["name"]
    staff_role = staff_info["role"]
    staff_unit = staff_info["unit"]

    # 2. 檢查功能開關
    _assert_features(db, _required_features(payload.event_type, staff_role, staff_unit))

    # 3. 建立驗證事件
    verification_id = identity_service.record_kiosk_verification(
        db,
        staff_id=staff_id,
        station_id=payload.station_id,
        reason=payload.override_reason or f"護理站網頁打卡 ({payload.event_type.value})",
    )

    # 4. 記錄出勤事件
    event_time = payload.occurred_at or datetime.now().astimezone()
    event = service.record_event(
        db,
        staff_id=staff_id,
        event_type=payload.event_type,
        occurred_at=event_time,
        source=EventSource.WEB,
        verification_id=verification_id,
        station_id=payload.station_id,
        ward_code=payload.ward_code if payload.event_type == AttendanceEventType.CLINICAL_ROUND_SIGN_IN else None,
        client_event_uid=payload.client_event_uid,
        actor_id=staff_id,
    )

    # 5. 格式化回應訊息
    msg_map = {
        AttendanceEventType.CHECK_IN: "上班簽到成功！",
        AttendanceEventType.CHECK_OUT: "下班簽退成功！",
        AttendanceEventType.CLINICAL_ROUND_SIGN_IN: "病房巡診簽到成功！",
        AttendanceEventType.BREAK_OUT: "外出登記成功！",
        AttendanceEventType.BREAK_IN: "外出返回簽到成功！",
        AttendanceEventType.ON_DUTY_SIGN_IN: "值班簽到成功！",
        AttendanceEventType.ON_DUTY_SIGN_OUT: "值班簽退成功！",
    }
    action_desc = msg_map.get(payload.event_type, f"{payload.event_type.value} 完成")
    user_msg = f"{staff_name} ({payload.employee_no}) {action_desc}"

    return KioskPunchOut(
        event_id=event.id,
        employee_no=staff_info["employee_no"],
        name=staff_name,
        role=staff_role,
        event_type=event.event_type,
        occurred_at=event.occurred_at,
        ward_code=event.ward_code,
        station_id=event.station_id,
        message=user_msg,
    )

