"""Unknown Governance API + 功能開關後台。

CLAUDE.md §5：功能開關必須可於**執行期**切換，不需重啟。
CLAUDE.md §11：thinking_unknown 為治理層，R10 禁止任何臨床輸出。
"""

from __future__ import annotations

from datetime import date

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.core.config import settings
from app.core.deps import AuthedStaff, DbSession
from app.core.enums import AuditAction
from app.core.feature_store import FeatureFlagService
from app.core.features import FEATURE_LABELS, REQUIREMENT_MAP, Feature
from app.modules.audit import service as audit
from app.modules.governance.models import DeviationRecord, UnknownItem

router = APIRouter(prefix="/governance", tags=["governance"])


class FeatureToggle(BaseModel):
    enabled: bool
    reason: str = Field(min_length=1, description="切換功能開關必填理由")


class UnknownCreate(BaseModel):
    title: str
    description: str
    category: str = Field(description="KNOWN / KNOWN_UNKNOWN / UNKNOWN_UNKNOWN")
    impact: str | None = None


class DeviationCreate(BaseModel):
    planned: str
    actual: str
    rationale: str
    occurred_on: date
    requires_adr: bool = False


@router.get("/features")
def list_features(db: DbSession, staff: AuthedStaff):
    """列出所有功能開關現況，附需求代號對照。"""
    flags = FeatureFlagService.all_flags(db)
    requirement_by_feature = {v: k for k, v in REQUIREMENT_MAP.items()}
    return [
        {
            "key": feature.value,
            "requirement": requirement_by_feature.get(feature),
            "label": FEATURE_LABELS[feature],
            "enabled": flags.get(feature.value, False),
        }
        for feature in Feature
    ]


@router.put("/features/{feature_key}")
def toggle_feature(
    feature_key: str, payload: FeatureToggle, db: DbSession, staff: AuthedStaff
):
    """開關某功能。

    關閉只影響入口，**既有資料不得刪除** (CLAUDE.md §5)。

    TODO(open-decision): 目前任何登入者皆可切換。
    角色權限矩陣定案後須限縮為系統管理者。
    """
    feature = Feature(feature_key)
    previous = FeatureFlagService.is_enabled(db, feature)

    FeatureFlagService.set_enabled(
        db,
        feature,
        payload.enabled,
        actor_id=staff.staff_id,
        reason=payload.reason,
    )
    audit.record(
        db,
        action=AuditAction.FEATURE_TOGGLE,
        entity_type="feature_flag",
        entity_id=feature.value,
        actor_id=staff.staff_id,
        before={"enabled": previous},
        after={"enabled": payload.enabled},
        reason=payload.reason,
    )
    return {"key": feature.value, "enabled": payload.enabled}


@router.get("/status")
def governance_status(db: DbSession, staff: AuthedStaff):
    """治理狀態總覽，供前端顯示紅色警示條。"""
    return {
        "shadow_mode": settings.shadow_mode,
        "labor_rules_reviewed": settings.labor.labor_rules_reviewed,
        "environment": settings.environment,
        "his_integration_claimed": False,  # R8：永遠為 False，直到書面確認
        "notices": [
            n
            for n in [
                "影子模式運作中：加班為候選值，不得作為薪資依據。"
                if settings.shadow_mode
                else None,
                "工時門檻尚未經勞動法規複核。"
                if not settings.labor.labor_rules_reviewed
                else None,
            ]
            if n
        ],
    }


@router.post("/unknowns", status_code=201)
def create_unknown(payload: UnknownCreate, db: DbSession, staff: AuthedStaff):
    """登錄一項未知 (CLAUDE.md §11 步驟 1)。"""
    item = UnknownItem(
        title=payload.title,
        description=payload.description,
        category=payload.category,
        impact=payload.impact,
        owner_id=staff.staff_id,
    )
    db.add(item)
    db.flush()
    return {"id": item.id, "state": item.state}


@router.post("/deviations", status_code=201)
def create_deviation(payload: DeviationCreate, db: DbSession, staff: AuthedStaff):
    """記錄偏離計畫 (CLAUDE.md §11 步驟 5)。"""
    record = DeviationRecord(
        planned=payload.planned,
        actual=payload.actual,
        rationale=payload.rationale,
        occurred_on=payload.occurred_on,
        requires_adr=payload.requires_adr,
        recorded_by=staff.staff_id,
    )
    db.add(record)
    db.flush()
    return {"id": record.id, "requires_adr": record.requires_adr}
