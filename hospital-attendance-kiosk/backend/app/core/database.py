"""資料庫連線與 ORM 基底。"""

from __future__ import annotations

import uuid
from collections.abc import Generator
from datetime import UTC, datetime

from sqlalchemy import DateTime, MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from app.core.config import settings

# 明確命名慣例，讓 Alembic autogenerate 產出穩定的 migration。
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)


def utcnow() -> datetime:
    """一律以 UTC 儲存；顯示時再依 settings.timezone 轉為 Asia/Taipei。"""
    return datetime.now(UTC)


def new_uuid() -> str:
    return str(uuid.uuid4())


class UUIDPrimaryKey:
    """共用主鍵 mixin。"""

    id: Mapped[str] = mapped_column(primary_key=True, default=new_uuid)


class TimestampMixin:
    """建立／更新時間 mixin。

    注意：稽核用途請勿只依賴這兩個欄位，正式稽核軌跡走 audit_log
    (append-only, CLAUDE.md §10)。
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )


engine = create_engine(
    settings.database_url,
    echo=settings.debug and settings.environment == "development",
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency：每個請求一個 session。"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
