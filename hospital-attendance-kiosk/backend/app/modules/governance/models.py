"""Unknown Governance 模組（thinking_unknown 治理層）資料模型。

CLAUDE.md §11：這是**治理與持續改善層**，不是臨床工具。
紅線 R10：絕不產生診斷、處方、醫囑、檢傷分級或原始臨床紀錄。
"""

from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, TimestampMixin, UUIDPrimaryKey


class UnknownItem(Base, UUIDPrimaryKey, TimestampMixin):
    """已知／未知對映表 (CLAUDE.md §11 步驟 1)。

    對應 handoff.md §14 的六項未決事項，以及開發過程中新發現的未知。
    """

    __tablename__ = "governance_unknown"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    # KNOWN / KNOWN_UNKNOWN / UNKNOWN_UNKNOWN
    category: Mapped[str] = mapped_column(String(32), nullable=False)
    # OPEN / INVESTIGATING / RESOLVED / ACCEPTED_RISK
    state: Mapped[str] = mapped_column(String(32), nullable=False, default="OPEN")
    impact: Mapped[str | None] = mapped_column(String(32), nullable=True)  # LOW/MED/HIGH
    owner_id: Mapped[str | None] = mapped_column(ForeignKey("staff.id"), nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    resolution: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (Index("ix_unknown_state", "state"),)


class DeviationRecord(Base, UUIDPrimaryKey, TimestampMixin):
    """偏離計畫紀錄 (CLAUDE.md §11 步驟 5)。

    偏離既定計畫時必須記錄，不得事後補寫成「本來就這樣規劃」。
    """

    __tablename__ = "governance_deviation"

    planned: Mapped[str] = mapped_column(Text, nullable=False)
    actual: Mapped[str] = mapped_column(Text, nullable=False)
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    recorded_by: Mapped[str | None] = mapped_column(
        ForeignKey("staff.id"), nullable=True
    )
    occurred_on: Mapped[date] = mapped_column(Date, nullable=False)
    # 是否需要補一份 ADR (docs/adr/)
    requires_adr: Mapped[bool] = mapped_column(default=False, nullable=False)


class RubricCheck(Base, UUIDPrimaryKey, TimestampMixin):
    """依預先定義評分表的驗收結果 (CLAUDE.md §11 步驟 6)。

    TODO(open-decision): 試辦成功評分表與 go/no-go 關卡尚未定案，
    rubric_code 的值域待使用者確認後才可固定。
    """

    __tablename__ = "governance_rubric_check"

    rubric_code: Mapped[str] = mapped_column(String(64), nullable=False)
    criterion: Mapped[str] = mapped_column(Text, nullable=False)
    # PASS / FAIL / NOT_APPLICABLE / BLOCKED
    result: Mapped[str] = mapped_column(String(32), nullable=False)
    evidence: Mapped[str | None] = mapped_column(Text, nullable=True)
    checked_by: Mapped[str | None] = mapped_column(
        ForeignKey("staff.id"), nullable=True
    )
    checked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    __table_args__ = (Index("ix_rubric_code_result", "rubric_code", "result"),)
