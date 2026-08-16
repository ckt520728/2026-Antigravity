"""Attendance 模組資料模型：實際觀測到的出勤事件與更正申請。

紅線 (CLAUDE.md §2)：
- R9 `AttendanceEvent` 與 `PlannedShift` 是兩張獨立表，任一方都不得覆寫另一方。
      本模組**不 import** scheduling 的 ORM model，只透過其 service 介面查詢。
- R3 病房訪視只記錄病房層級，**沒有**病人姓名、病歷號、診斷欄位。
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, TimestampMixin, UUIDPrimaryKey
from app.core.enums import AttendanceEventType, CorrectionState, EventSource


class AttendanceEvent(Base, UUIDPrimaryKey, TimestampMixin):
    """觀測到的打卡／簽到證據。

    這是「事實紀錄」：一旦寫入就不直接 UPDATE 時間，
    任何修改都必須走 CorrectionRequest 狀態機 (CLAUDE.md §10)。
    """

    __tablename__ = "attendance_event"

    staff_id: Mapped[str] = mapped_column(ForeignKey("staff.id"), nullable=False)
    event_type: Mapped[AttendanceEventType] = mapped_column(String(32), nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    source: Mapped[EventSource] = mapped_column(String(32), nullable=False)

    # 指向 identity.VerificationEvent；為 None 代表此筆無生物驗證背書。
    verification_id: Mapped[str | None] = mapped_column(
        ForeignKey("verification_event.id"), nullable=True
    )
    station_id: Mapped[str | None] = mapped_column(String(64), nullable=True)

    # 需求 d：病房層級簽到只記病房代碼，絕不記病人 (R3)。
    ward_code: Mapped[str | None] = mapped_column(String(32), nullable=True)

    is_corrected: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    # 被更正後指向取代它的新事件，保留原紀錄不刪除。
    superseded_by_id: Mapped[str | None] = mapped_column(
        ForeignKey("attendance_event.id"), nullable=True
    )

    # 離線 kiosk 補送時，記錄實際送達伺服器的時間以供對帳。
    # TODO(open-decision): kiosk 離線佇列行為（暫存上限、補送順序、
    # 時鐘偏移容忍度）尚未定案 — 這是目前最高風險的未決項目。
    received_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    client_event_uid: Mapped[str | None] = mapped_column(
        String(64), unique=True, nullable=True
    )

    __table_args__ = (
        Index("ix_attendance_staff_time", "staff_id", "occurred_at"),
        Index("ix_attendance_type_time", "event_type", "occurred_at"),
    )


class CorrectionRequest(Base, UUIDPrimaryKey, TimestampMixin):
    """出勤更正申請 (CLAUDE.md §10)。

    狀態機：
        DRAFT → SUBMITTED → SUPERVISOR_APPROVED → HR_CONFIRMED → APPLIED
                         ↘ REJECTED（任一關卡可退回，須填理由）

    每次變更保留原值、操作者、時間戳記、理由。
    """

    __tablename__ = "correction_request"

    attendance_event_id: Mapped[str | None] = mapped_column(
        ForeignKey("attendance_event.id"), nullable=True
    )
    staff_id: Mapped[str] = mapped_column(ForeignKey("staff.id"), nullable=False)
    requested_by: Mapped[str] = mapped_column(ForeignKey("staff.id"), nullable=False)

    state: Mapped[CorrectionState] = mapped_column(
        String(32), nullable=False, default=CorrectionState.DRAFT
    )

    # 申請內容：原值與請求值並存，方便稽核比對。
    original_occurred_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    requested_occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    requested_event_type: Mapped[AttendanceEventType] = mapped_column(
        String(32), nullable=False
    )
    reason: Mapped[str] = mapped_column(Text, nullable=False)

    # 核准鏈。職責分離：supervisor_id 與 hr_id 不得為同一人。
    supervisor_id: Mapped[str | None] = mapped_column(
        ForeignKey("staff.id"), nullable=True
    )
    supervisor_acted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    hr_id: Mapped[str | None] = mapped_column(ForeignKey("staff.id"), nullable=True)
    hr_acted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    applied_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    # 核准後產生的取代事件。
    resulting_event_id: Mapped[str | None] = mapped_column(
        ForeignKey("attendance_event.id"), nullable=True
    )

    __table_args__ = (
        Index("ix_correction_state", "state"),
        Index("ix_correction_staff", "staff_id"),
    )
