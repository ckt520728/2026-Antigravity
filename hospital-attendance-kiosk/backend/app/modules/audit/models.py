"""Audit 模組資料模型。

CLAUDE.md §10：稽核紀錄為 **append-only**，禁止刪除或修改。
本模組刻意不提供 update / delete 介面。
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, UUIDPrimaryKey
from app.core.enums import AuditAction


class AuditLog(Base, UUIDPrimaryKey):
    """稽核軌跡。

    寫入時機（至少）：
    - 任何出勤紀錄更正的每一個狀態轉換；
    - 班表換班／編輯；
    - 功能開關切換；
    - **報表下載** (CLAUDE.md §9)；
    - 非生物辨識例外路徑的代打卡。
    """

    __tablename__ = "audit_log"

    actor_id: Mapped[str | None] = mapped_column(ForeignKey("staff.id"), nullable=True)
    action: Mapped[AuditAction] = mapped_column(String(32), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    entity_id: Mapped[str | None] = mapped_column(String(64), nullable=True)

    # 變更前後快照（JSON 字串）。保留原值是決議 12 的硬性要求。
    before_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    after_value: Mapped[str | None] = mapped_column(Text, nullable=True)

    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    # 來源資訊，供資安事件調查。
    ip_address: Mapped[str | None] = mapped_column(String(64), nullable=True)
    station_id: Mapped[str | None] = mapped_column(String(64), nullable=True)

    __table_args__ = (
        Index("ix_audit_entity", "entity_type", "entity_id"),
        Index("ix_audit_actor_time", "actor_id", "occurred_at"),
        Index("ix_audit_action_time", "action", "occurred_at"),
    )
