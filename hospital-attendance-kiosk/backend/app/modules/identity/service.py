"""Identity 模組公開介面：WebAuthn 註冊／驗證與 token 簽發。

CLAUDE.md §8 / R1：
- 使用院內 kiosk 的 platform authenticator（Windows Hello 指紋／臉部）；
- 伺服器只收到**簽章**，生物特徵從未離開 kiosk 的 TPM；
- 本檔沒有、也不得新增任何處理原始生物特徵的程式碼。
"""

from __future__ import annotations

from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from webauthn import (
    generate_authentication_options,
    generate_registration_options,
    options_to_json,
    verify_authentication_response,
    verify_registration_response,
)
from webauthn.helpers.structs import (
    AuthenticatorAttachment,
    AuthenticatorSelectionCriteria,
    PublicKeyCredentialDescriptor,
    ResidentKeyRequirement,
    UserVerificationRequirement,
)

from app.core.config import settings
from app.core.database import utcnow
from app.core.enums import AuditAction, VerificationMethod
from app.modules.audit import service as audit
from app.modules.identity.models import Staff, VerificationEvent, WebAuthnCredential


class _ChallengeStore:
    """暫存 WebAuthn challenge。

    TODO(open-decision): 目前為單機記憶體實作，僅適用單一 app instance。
    正式部署若有多台 instance，需改為 Redis 或資料表並設定 TTL。
    """

    _store: dict[str, tuple[bytes, datetime]] = {}
    _ttl = timedelta(minutes=5)

    @classmethod
    def put(cls, key: str, challenge: bytes) -> None:
        cls._store[key] = (challenge, utcnow() + cls._ttl)

    @classmethod
    def take(cls, key: str) -> bytes:
        entry = cls._store.pop(key, None)
        if entry is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="challenge 不存在或已使用"
            )
        challenge, expires_at = entry
        if utcnow() > expires_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="challenge 已過期"
            )
        return challenge


def start_registration(db: Session, *, staff_id: str) -> str:
    """產生註冊 options（回傳 JSON 字串給前端）。"""
    staff = _get_staff(db, staff_id)

    options = generate_registration_options(
        rp_id=settings.webauthn_rp_id,
        rp_name=settings.webauthn_rp_name,
        user_id=staff.id.encode(),
        user_name=staff.employee_no,
        user_display_name=staff.name,
        authenticator_selection=AuthenticatorSelectionCriteria(
            # 限定平台驗證器：綁定院內 kiosk 的 TPM，不允許自帶手機。
            authenticator_attachment=AuthenticatorAttachment.PLATFORM,
            resident_key=ResidentKeyRequirement.PREFERRED,
            # 強制使用者驗證（指紋／臉部／PIN），否則只是「裝置在場」。
            user_verification=UserVerificationRequirement.REQUIRED,
        ),
    )
    _ChallengeStore.put(f"reg:{staff.id}", options.challenge)
    return options_to_json(options)


def finish_registration(
    db: Session,
    *,
    staff_id: str,
    credential_json: str,
    station_id: str | None = None,
    device_label: str | None = None,
) -> WebAuthnCredential:
    """驗證註冊回應，只儲存 credential_id、公鑰、計數器 (R1)。"""
    staff = _get_staff(db, staff_id)
    challenge = _ChallengeStore.take(f"reg:{staff.id}")

    verification = verify_registration_response(
        credential=credential_json,
        expected_challenge=challenge,
        expected_rp_id=settings.webauthn_rp_id,
        expected_origin=settings.webauthn_origin,
        require_user_verification=True,
    )

    credential = WebAuthnCredential(
        staff_id=staff.id,
        credential_id=verification.credential_id,
        public_key=verification.credential_public_key,
        signature_counter=verification.sign_count,
        method=VerificationMethod.WEBAUTHN_PLATFORM,
        registered_station_id=station_id,
        device_label=device_label,
    )
    db.add(credential)
    db.flush()

    audit.record(
        db,
        action=AuditAction.CREATE,
        entity_type="webauthn_credential",
        entity_id=credential.id,
        actor_id=staff.id,
        after={"station_id": station_id, "device_label": device_label},
        reason="註冊生物驗證憑證",
        station_id=station_id,
    )
    return credential


def start_authentication(db: Session, *, employee_no: str) -> str:
    staff = _get_staff_by_employee_no(db, employee_no)
    credentials = _active_credentials(db, staff.id)
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="此員工尚未註冊生物驗證憑證"
        )

    options = generate_authentication_options(
        rp_id=settings.webauthn_rp_id,
        allow_credentials=[
            PublicKeyCredentialDescriptor(id=c.credential_id) for c in credentials
        ],
        user_verification=UserVerificationRequirement.REQUIRED,
    )
    _ChallengeStore.put(f"auth:{staff.id}", options.challenge)
    return options_to_json(options)


def finish_authentication(
    db: Session,
    *,
    employee_no: str,
    credential_json: str,
    raw_credential_id: bytes,
    station_id: str | None = None,
) -> tuple[VerificationEvent, str]:
    """驗證登入回應，寫入 VerificationEvent 並簽發 token。

    回傳 (verification_event, access_token)。
    verification_event.id 之後會被 attendance 事件引用，
    作為「這筆打卡有生物驗證背書」的證據。
    """
    staff = _get_staff_by_employee_no(db, employee_no)
    challenge = _ChallengeStore.take(f"auth:{staff.id}")

    credential = db.execute(
        select(WebAuthnCredential).where(
            WebAuthnCredential.credential_id == raw_credential_id,
            WebAuthnCredential.staff_id == staff.id,
            WebAuthnCredential.revoked_at.is_(None),
        )
    ).scalar_one_or_none()
    if credential is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="憑證不存在或已註銷"
        )

    verification = verify_authentication_response(
        credential=credential_json,
        expected_challenge=challenge,
        expected_rp_id=settings.webauthn_rp_id,
        expected_origin=settings.webauthn_origin,
        credential_public_key=credential.public_key,
        credential_current_sign_count=credential.signature_counter,
        require_user_verification=True,
    )

    # 防重放：計數器必須遞增。倒退代表憑證可能已被複製。
    credential.signature_counter = verification.new_sign_count

    event = VerificationEvent(
        staff_id=staff.id,
        method=credential.method,
        credential_id=credential.credential_id,
        signature_counter=verification.new_sign_count,
        verified_at=utcnow(),
        station_id=station_id,
    )
    db.add(event)
    db.flush()

    audit.record(
        db,
        action=AuditAction.LOGIN,
        entity_type="verification_event",
        entity_id=event.id,
        actor_id=staff.id,
        station_id=station_id,
        reason="生物驗證成功",
    )
    return event, issue_token(staff)


def record_manual_override(
    db: Session,
    *,
    staff_id: str,
    approved_by: str,
    reason: str,
    station_id: str | None = None,
) -> VerificationEvent:
    """受治理的非生物辨識例外路徑 (CLAUDE.md §8)。

    需主管核准並填寫理由，且一律寫入稽核。
    """
    if not reason.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="例外路徑必須填寫理由"
        )
    if approved_by == staff_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="不得自行核准例外打卡"
        )

    event = VerificationEvent(
        staff_id=staff_id,
        method=VerificationMethod.MANUAL_OVERRIDE,
        verified_at=utcnow(),
        station_id=station_id,
        override_reason=reason,
        override_approved_by=approved_by,
    )
    db.add(event)
    db.flush()

    audit.record(
        db,
        action=AuditAction.CREATE,
        entity_type="verification_event",
        entity_id=event.id,
        actor_id=approved_by,
        after={"method": VerificationMethod.MANUAL_OVERRIDE.value},
        reason=reason,
        station_id=station_id,
    )
    return event


def issue_token(staff: Staff) -> str:
    payload = {
        "sub": staff.id,
        "employee_no": staff.employee_no,
        "role": staff.role.value if hasattr(staff.role, "value") else staff.role,
        "unit": staff.unit.value if hasattr(staff.unit, "value") else staff.unit,
        "exp": utcnow() + timedelta(minutes=settings.jwt_expire_minutes),
        "iat": utcnow(),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def staff_directory(db: Session) -> dict[str, dict[str, str]]:
    """供 reporting 模組取用的員工基本資料對照表（唯讀 dict）。

    只回傳報表所需欄位，避免其他模組拿到完整 ORM 物件後改動名冊。
    """
    rows = db.execute(select(Staff)).scalars().all()
    return {
        s.id: {
            "employee_no": s.employee_no,
            "name": s.name,
            "unit": s.unit.value if hasattr(s.unit, "value") else str(s.unit),
            "role": s.role.value if hasattr(s.role, "value") else str(s.role),
        }
        for s in rows
    }


def list_active_staff_summary(db: Session, unit: str | None = None) -> list[dict[str, Any]]:
    """供 Kiosk 畫面與打卡快速選擇的員工摘要清單。"""
    stmt = select(Staff).where(Staff.active.is_(True))
    if unit:
        stmt = stmt.where(Staff.unit == unit)
    stmt = stmt.order_by(Staff.role, Staff.employee_no)
    rows = db.execute(stmt).scalars().all()
    return [
        {
            "id": s.id,
            "employee_no": s.employee_no,
            "name": s.name,
            "unit": s.unit.value if hasattr(s.unit, "value") else str(s.unit),
            "role": s.role.value if hasattr(s.role, "value") else str(s.role),
            "employment_type": s.employment_type.value if hasattr(s.employment_type, "value") else str(s.employment_type),
        }
        for s in rows
    ]


def get_staff_by_no(db: Session, employee_no: str) -> dict[str, Any]:
    """供 attendance 模組依工號查詢員工公開資訊。"""
    staff = _get_staff_by_employee_no(db, employee_no)
    return {
        "id": staff.id,
        "employee_no": staff.employee_no,
        "name": staff.name,
        "unit": staff.unit.value if hasattr(staff.unit, "value") else str(staff.unit),
        "role": staff.role.value if hasattr(staff.role, "value") else str(staff.role),
        "employment_type": staff.employment_type.value if hasattr(staff.employment_type, "value") else str(staff.employment_type),
    }


def record_kiosk_verification(
    db: Session,
    *,
    staff_id: str,
    station_id: str | None = "YM-3F-KIOSK",
    reason: str = "護理站網頁打卡簽名",
) -> str:
    """護理站電腦網頁介面打卡驗證事件。"""
    event = VerificationEvent(
        staff_id=staff_id,
        method=VerificationMethod.MANUAL_OVERRIDE,
        verified_at=utcnow(),
        station_id=station_id,
        override_reason=reason,
    )
    db.add(event)
    db.flush()
    return event.id


def _active_credentials(db: Session, staff_id: str) -> list[WebAuthnCredential]:
    stmt = select(WebAuthnCredential).where(
        WebAuthnCredential.staff_id == staff_id,
        WebAuthnCredential.revoked_at.is_(None),
    )
    return list(db.execute(stmt).scalars().all())


def _get_staff(db: Session, staff_id: str) -> Staff:
    staff = db.get(Staff, staff_id)
    if staff is None or not staff.active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="找不到員工")
    return staff


def _get_staff_by_employee_no(db: Session, employee_no: str) -> Staff:
    staff = db.execute(
        select(Staff).where(Staff.employee_no == employee_no, Staff.active.is_(True))
    ).scalar_one_or_none()
    if staff is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="找不到員工")
    return staff

