"""Audit 模組公開介面。

其他模組**只能**透過本檔的函式寫稽核，不得直接操作 AuditLog ORM
(CLAUDE.md §4 模組邊界規則)。
"""

from __future__ import annotations

import json
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import utcnow
from app.core.enums import AuditAction
from app.modules.audit.models import AuditLog


def _dump(value: Any) -> str | None:
    if value is None:
        return None
    return json.dumps(value, ensure_ascii=False, default=str)


def record(
    db: Session,
    *,
    action: AuditAction,
    entity_type: str,
    entity_id: str | None = None,
    actor_id: str | None = None,
    before: Any = None,
    after: Any = None,
    reason: str | None = None,
    ip_address: str | None = None,
    station_id: str | None = None,
) -> AuditLog:
    """寫入一筆稽核紀錄（append-only）。"""
    entry = AuditLog(
        actor_id=actor_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        before_value=_dump(before),
        after_value=_dump(after),
        reason=reason,
        occurred_at=utcnow(),
        ip_address=ip_address,
        station_id=station_id,
    )
    db.add(entry)
    db.flush()
    return entry


def record_export(
    db: Session,
    *,
    actor_id: str,
    report_type: str,
    file_format: str,
    filters: dict[str, Any],
) -> AuditLog:
    """報表下載必須記錄 (CLAUDE.md §9)。"""
    return record(
        db,
        action=AuditAction.EXPORT,
        entity_type="report",
        entity_id=report_type,
        actor_id=actor_id,
        after={"format": file_format, "filters": filters},
        reason="報表匯出",
    )


def history_for(
    db: Session, entity_type: str, entity_id: str, limit: int = 100
) -> list[AuditLog]:
    """查詢某筆資料的完整變更歷程。"""
    stmt = (
        select(AuditLog)
        .where(AuditLog.entity_type == entity_type, AuditLog.entity_id == entity_id)
        .order_by(AuditLog.occurred_at.desc())
        .limit(limit)
    )
    return list(db.execute(stmt).scalars().all())
