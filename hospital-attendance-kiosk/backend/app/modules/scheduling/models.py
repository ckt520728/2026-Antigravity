"""Scheduling 模組資料模型：班表版本、預期班別、OPD 診次。

紅線 R9 (CLAUDE.md §2)：`PlannedShift` 是「預期」，`AttendanceEvent` 是「實際」。
兩者永遠分開儲存，任何寫入路徑都不得讓其中一方覆寫另一方。
比對兩者是 overtime 模組的工作，不是覆寫。
"""

from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TimestampMixin, UUIDPrimaryKey
from app.core.enums import ShiftType, ShiftVersionState, Unit


class ShiftVersion(Base, UUIDPrimaryKey, TimestampMixin):
    """班表版本。每次調整產生新版本，舊版標記 SUPERSEDED 而非刪除。

    來源：標準 Excel 範本匯入，或授權網頁編輯 (CLAUDE.md 決議 12)。
    """

    __tablename__ = "shift_version"

    unit: Mapped[Unit] = mapped_column(String(32), nullable=False)
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    state: Mapped[ShiftVersionState] = mapped_column(
        String(32), nullable=False, default=ShiftVersionState.DRAFT
    )
    version_no: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    created_by: Mapped[str] = mapped_column(ForeignKey("staff.id"), nullable=False)
    approved_by: Mapped[str | None] = mapped_column(
        ForeignKey("staff.id"), nullable=True
    )
    approved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    supersedes_id: Mapped[str | None] = mapped_column(
        ForeignKey("shift_version.id"), nullable=True
    )
    source_note: Mapped[str | None] = mapped_column(String(255), nullable=True)

    shifts: Mapped[list["PlannedShift"]] = relationship(back_populates="version")

    __table_args__ = (
        Index("ix_shift_version_unit_period", "unit", "period_start", "period_end"),
    )


class PlannedShift(Base, UUIDPrimaryKey, TimestampMixin):
    """已核准的預期班別。

    涵蓋需求 c（OPD 診次）、h（夜間值班）、i（假日值班），
    以 shift_type 區分。
    """

    __tablename__ = "planned_shift"

    staff_id: Mapped[str] = mapped_column(ForeignKey("staff.id"), nullable=False)
    version_id: Mapped[str] = mapped_column(
        ForeignKey("shift_version.id"), nullable=False
    )
    shift_date: Mapped[date] = mapped_column(Date, nullable=False)
    shift_type: Mapped[ShiftType] = mapped_column(String(32), nullable=False)
    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # 需求 c：門診診次專用欄位。
    clinic_code: Mapped[str | None] = mapped_column(String(32), nullable=True)
    room_code: Mapped[str | None] = mapped_column(String(32), nullable=True)
    # 需求 d：訪視醫師負責病房（病房層級，非病人 — R3）。
    ward_code: Mapped[str | None] = mapped_column(String(32), nullable=True)

    version: Mapped[ShiftVersion] = relationship(back_populates="shifts")

    __table_args__ = (
        Index("ix_planned_shift_staff_date", "staff_id", "shift_date"),
        Index("ix_planned_shift_type_date", "shift_type", "shift_date"),
    )


class ShiftChangeLog(Base, UUIDPrimaryKey):
    """換班／編輯歷程。

    CLAUDE.md 決議 12：每次 swap/edit 必須保留原值、操作者、時間戳記、理由。
    本表為 append-only。
    """

    __tablename__ = "shift_change_log"

    planned_shift_id: Mapped[str | None] = mapped_column(
        ForeignKey("planned_shift.id"), nullable=True
    )
    version_id: Mapped[str] = mapped_column(
        ForeignKey("shift_version.id"), nullable=False
    )
    actor_id: Mapped[str] = mapped_column(ForeignKey("staff.id"), nullable=False)
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    previous_value: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON
    new_value: Mapped[str | None] = mapped_column(Text, nullable=True)       # JSON
    reason: Mapped[str] = mapped_column(Text, nullable=False)

    __table_args__ = (Index("ix_shift_change_version", "version_id", "changed_at"),)
