"""Audit API。

只提供查詢。刻意**不提供** update / delete 端點——稽核為 append-only
(CLAUDE.md §10)。
"""

from __future__ import annotations

from fastapi import APIRouter

from app.core.deps import AuthedStaff, DbSession
from app.modules.audit import service

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("/history/{entity_type}/{entity_id}")
def history(entity_type: str, entity_id: str, db: DbSession, staff: AuthedStaff):
    """查詢某筆資料的完整變更歷程。

    TODO(open-decision): 稽核查詢的存取權限與保留年限尚未定案 (CLAUDE.md §14)。
    """
    entries = service.history_for(db, entity_type, entity_id)
    return [
        {
            "id": e.id,
            "action": e.action,
            "actor_id": e.actor_id,
            "occurred_at": e.occurred_at,
            "before": e.before_value,
            "after": e.after_value,
            "reason": e.reason,
        }
        for e in entries
    ]
