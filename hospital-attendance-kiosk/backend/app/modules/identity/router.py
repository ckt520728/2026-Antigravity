"""Identity API：WebAuthn 註冊／驗證與例外路徑。"""

from __future__ import annotations

import base64

from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel, Field

from app.core.deps import AuthedStaff, DbSession, require_feature
from app.core.features import Feature
from app.modules.identity import service

router = APIRouter(prefix="/identity", tags=["identity"])

# 需求 a：整個生物驗證流程受 BIOMETRIC_PRESENCE 開關控制。
biometric_gate = Depends(require_feature(Feature.BIOMETRIC_PRESENCE))


class RegistrationFinish(BaseModel):
    credential_json: str = Field(description="瀏覽器回傳的 attestation JSON")
    station_id: str | None = None
    device_label: str | None = None


class AuthenticationStart(BaseModel):
    employee_no: str


class AuthenticationFinish(BaseModel):
    employee_no: str
    credential_json: str
    credential_id_b64: str = Field(description="base64url 編碼的 credential id")
    station_id: str | None = None


class ManualOverride(BaseModel):
    staff_id: str
    reason: str = Field(min_length=1, description="例外打卡必填理由")
    station_id: str | None = None


@router.post("/webauthn/register/start", dependencies=[biometric_gate])
def register_start(db: DbSession, staff: AuthedStaff) -> Response:
    """產生註冊 options。回傳原始 JSON 供瀏覽器 API 直接使用。"""
    return Response(
        content=service.start_registration(db, staff_id=staff.staff_id),
        media_type="application/json",
    )


@router.post("/webauthn/register/finish", dependencies=[biometric_gate])
def register_finish(payload: RegistrationFinish, db: DbSession, staff: AuthedStaff):
    credential = service.finish_registration(
        db,
        staff_id=staff.staff_id,
        credential_json=payload.credential_json,
        station_id=payload.station_id,
        device_label=payload.device_label,
    )
    return {"credential_id": credential.id, "device_label": credential.device_label}


@router.post("/webauthn/authenticate/start", dependencies=[biometric_gate])
def authenticate_start(payload: AuthenticationStart, db: DbSession) -> Response:
    return Response(
        content=service.start_authentication(db, employee_no=payload.employee_no),
        media_type="application/json",
    )


@router.post("/webauthn/authenticate/finish", dependencies=[biometric_gate])
def authenticate_finish(payload: AuthenticationFinish, db: DbSession):
    """驗證成功後回傳 access token 與 verification_id。

    verification_id 需在後續打卡時帶上，作為生物驗證背書。
    """
    raw_id = base64.urlsafe_b64decode(payload.credential_id_b64 + "==")
    event, token = service.finish_authentication(
        db,
        employee_no=payload.employee_no,
        credential_json=payload.credential_json,
        raw_credential_id=raw_id,
        station_id=payload.station_id,
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "verification_id": event.id,
    }


@router.post("/verification/manual-override", status_code=201)
def manual_override(payload: ManualOverride, db: DbSession, staff: AuthedStaff):
    """受治理的非生物辨識例外路徑 (CLAUDE.md §8)。

    TODO(open-decision): 目前僅擋掉「自己核准自己」。
    完整的主管層級檢查需等角色權限矩陣定案。
    """
    event = service.record_manual_override(
        db,
        staff_id=payload.staff_id,
        approved_by=staff.staff_id,
        reason=payload.reason,
        station_id=payload.station_id,
    )
    return {"verification_id": event.id}
