"""Identity 模組資料模型：員工名冊、WebAuthn 憑證、驗證事件。

紅線 (CLAUDE.md §2)：
- R1 絕不儲存原始指紋／臉部影像或可還原的生物特徵範本；
- R5 不收集或重用 HIS 密碼——本表**沒有** password 欄位，這是刻意的；
- R8 在醫院 IT 與 HIS 廠商確認前，不得宣稱已整合 OIDC/LDAP。
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Index, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TimestampMixin, UUIDPrimaryKey
from app.core.enums import EmploymentType, StaffRole, Unit, VerificationMethod


class Staff(Base, UUIDPrimaryKey, TimestampMixin):
    """員工名冊。

    來源為 HR 核可名冊，Phase 1 另行開設試辦帳號 (CLAUDE.md §8)。
    刻意不含密碼欄位：驗證一律走 WebAuthn。
    """

    __tablename__ = "staff"

    employee_no: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    unit: Mapped[Unit] = mapped_column(String(32), nullable=False)
    role: Mapped[StaffRole] = mapped_column(String(32), nullable=False)
    employment_type: Mapped[EmploymentType] = mapped_column(
        String(32), nullable=False, default=EmploymentType.FULL_TIME
    )
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # 供主管核准鏈使用；完整權限矩陣待定 (見 deps.require_role 的 TODO)。
    supervisor_id: Mapped[str | None] = mapped_column(
        ForeignKey("staff.id"), nullable=True
    )

    credentials: Mapped[list["WebAuthnCredential"]] = relationship(
        back_populates="staff", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_staff_unit_role", "unit", "role"),
    )


class WebAuthnCredential(Base, UUIDPrimaryKey, TimestampMixin):
    """WebAuthn 公鑰憑證 (CLAUDE.md §8)。

    只存公開資訊：credential_id、公鑰、簽章計數器。
    生物特徵本身**從未離開 kiosk 的 TPM**，伺服器端無從取得也不需要 (R1)。
    """

    __tablename__ = "webauthn_credential"

    staff_id: Mapped[str] = mapped_column(ForeignKey("staff.id"), nullable=False)
    credential_id: Mapped[bytes] = mapped_column(
        LargeBinary, unique=True, nullable=False
    )
    public_key: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    # 防重放：每次驗證必須遞增，倒退代表憑證可能被複製。
    signature_counter: Mapped[int] = mapped_column(
        BigInteger, nullable=False, default=0
    )
    method: Mapped[VerificationMethod] = mapped_column(
        String(32), nullable=False, default=VerificationMethod.WEBAUTHN_PLATFORM
    )
    # 註冊此憑證的 kiosk；用於限制憑證只在院內終端可用。
    registered_station_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    device_label: Mapped[str | None] = mapped_column(String(100), nullable=True)
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    staff: Mapped[Staff] = relationship(back_populates="credentials")


class VerificationEvent(Base, UUIDPrimaryKey):
    """單次驗證的簽署後中繼資料。

    attendance_event 以 verification_id 指向本表，作為「這筆打卡有生物驗證背書」
    的證據。本表**不含**任何生物特徵資料 (R1)。
    """

    __tablename__ = "verification_event"

    staff_id: Mapped[str] = mapped_column(ForeignKey("staff.id"), nullable=False)
    method: Mapped[VerificationMethod] = mapped_column(String(32), nullable=False)
    credential_id: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    signature_counter: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    verified_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    station_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    # 例外路徑（MANUAL_OVERRIDE）必填理由 (CLAUDE.md §8)。
    override_reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
    override_approved_by: Mapped[str | None] = mapped_column(
        ForeignKey("staff.id"), nullable=True
    )

    __table_args__ = (
        Index("ix_verification_staff_time", "staff_id", "verified_at"),
    )
