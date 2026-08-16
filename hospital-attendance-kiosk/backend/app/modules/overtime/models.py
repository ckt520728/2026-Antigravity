"""Overtime 模組資料模型：工時彙總與加班候選。

紅線 R4 (CLAUDE.md §2)：加班一律先產生為 **Overtime Candidate**，
核准後才轉正式，且**絕不自動送入薪資系統**。
"""

from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, TimestampMixin, UUIDPrimaryKey
from app.core.enums import SummaryStatus


class WorkHourSummary(Base, UUIDPrimaryKey, TimestampMixin):
    """單一員工在某期間的工時彙總（需求 j）。

    四項核心指標沿用 reference/employer-checkin 的 SQL 邏輯：
    首次上班、最後下班、外出次數、總工時。
    """

    __tablename__ = "work_hour_summary"

    staff_id: Mapped[str] = mapped_column(ForeignKey("staff.id"), nullable=False)
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)

    # --- 參考實作的四項指標 ---
    first_check_in_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_check_out_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    total_out_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_work_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # --- 工時拆解 ---
    regular_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    overtime_candidate_minutes: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    night_duty_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    holiday_duty_minutes: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )

    status: Mapped[SummaryStatus] = mapped_column(
        String(32), nullable=False, default=SummaryStatus.DRAFT
    )

    # 計算當下所用的政策參數快照（JSON）。
    # 政策日後修改時，既有彙總仍能重現當時的計算依據。
    policy_snapshot: Mapped[str | None] = mapped_column(Text, nullable=True)
    # 計算時 labor_rules_reviewed 是否為 True。False 代表報表需帶警示浮水印。
    policy_reviewed: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )

    # 未配對的事件數（只有 check-in 沒有 check-out 等），供資料品質追蹤。
    unmatched_event_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )

    calculated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    __table_args__ = (
        Index("ix_summary_staff_period", "staff_id", "period_start", "period_end"),
        Index("ix_summary_status", "status"),
    )


class ComplianceFlag(Base, UUIDPrimaryKey, TimestampMixin):
    """勞基法門檻的觀察結果。

    刻意命名為 flag 而非 violation：在人事室完成法規複核前
    (settings.labor.labor_rules_reviewed)，系統只做「提示」，
    不做「違法認定」(CLAUDE.md §7)。
    """

    __tablename__ = "compliance_flag"

    staff_id: Mapped[str] = mapped_column(ForeignKey("staff.id"), nullable=False)
    summary_id: Mapped[str | None] = mapped_column(
        ForeignKey("work_hour_summary.id"), nullable=True
    )
    rule_code: Mapped[str] = mapped_column(String(64), nullable=False)
    observed_value: Mapped[int] = mapped_column(Integer, nullable=False)
    threshold_value: Mapped[int] = mapped_column(Integer, nullable=False)
    occurred_on: Mapped[date] = mapped_column(Date, nullable=False)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (Index("ix_compliance_staff_date", "staff_id", "occurred_on"),)
