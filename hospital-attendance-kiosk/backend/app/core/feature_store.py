"""功能開關的持久化與執行期快取。

規則 (CLAUDE.md §5)：
- 執行期可切換，不需重啟；
- 關閉時對應 API 回 404、前端隱藏入口；
- **既有資料不得刪除**——關閉開關只影響讀寫入口，不動資料。
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, select
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.core.database import Base, TimestampMixin, utcnow
from app.core.features import DEFAULT_FLAGS, Feature


class FeatureFlagRecord(Base, TimestampMixin):
    """功能開關的權威狀態。DEFAULT_FLAGS 僅作為 seed 與 fallback。"""

    __tablename__ = "feature_flag"

    key: Mapped[str] = mapped_column(String(64), primary_key=True)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    updated_by: Mapped[str | None] = mapped_column(String(36), nullable=True)
    updated_reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
    last_toggled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class FeatureFlagService:
    """讀取走記憶體快取，寫入即失效。單體部署下足夠。

    TODO(open-decision): 若日後水平擴充為多個 app instance，
    此快取需改為 pub/sub 或短 TTL，否則各 instance 狀態會不一致。
    """

    _cache: dict[str, bool] | None = None

    @classmethod
    def invalidate(cls) -> None:
        cls._cache = None

    @classmethod
    def all_flags(cls, db: Session) -> dict[str, bool]:
        if cls._cache is not None:
            return cls._cache

        rows = db.execute(select(FeatureFlagRecord)).scalars().all()
        stored = {row.key: row.enabled for row in rows}
        # 資料庫未涵蓋的開關（例如新增需求）以預設值補上。
        cls._cache = {
            feature.value: stored.get(feature.value, default)
            for feature, default in DEFAULT_FLAGS.items()
        }
        return cls._cache

    @classmethod
    def is_enabled(cls, db: Session, feature: Feature) -> bool:
        return cls.all_flags(db).get(feature.value, DEFAULT_FLAGS.get(feature, False))

    @classmethod
    def set_enabled(
        cls,
        db: Session,
        feature: Feature,
        enabled: bool,
        *,
        actor_id: str,
        reason: str,
    ) -> FeatureFlagRecord:
        """切換開關。呼叫端負責寫入 audit_log。"""
        record = db.get(FeatureFlagRecord, feature.value)
        if record is None:
            record = FeatureFlagRecord(key=feature.value)
            db.add(record)

        record.enabled = enabled
        record.updated_by = actor_id
        record.updated_reason = reason
        record.last_toggled_at = utcnow()

        db.flush()
        cls.invalidate()
        return record

    @classmethod
    def seed_defaults(cls, db: Session) -> None:
        """啟動時補齊缺少的開關列，不覆寫既有設定。"""
        existing = {
            key for key in db.execute(select(FeatureFlagRecord.key)).scalars().all()
        }
        for feature, default in DEFAULT_FLAGS.items():
            if feature.value not in existing:
                db.add(FeatureFlagRecord(key=feature.value, enabled=default))
        db.flush()
        cls.invalidate()
