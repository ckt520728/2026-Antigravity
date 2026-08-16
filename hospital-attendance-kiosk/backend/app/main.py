"""FastAPI 應用進入點（模組化單體）。

CLAUDE.md §3：架構為 modular monolith，不是微服務。
各模組以 router 掛載，模組間僅透過 service 介面互相呼叫。
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models  # noqa: F401  確保所有 ORM model 完成註冊
from app.core.config import settings
from app.core.database import Base, SessionLocal, engine
from app.core.feature_store import FeatureFlagService
from app.modules.attendance.router import router as attendance_router
from app.modules.audit.router import router as audit_router
from app.modules.governance.router import router as governance_router
from app.modules.identity.router import router as identity_router
from app.modules.overtime.router import router as overtime_router
from app.modules.reporting.router import router as reporting_router
from app.modules.scheduling.router import router as scheduling_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 確保資料表已建立 (開發與測試沙盒環境)
    Base.metadata.create_all(bind=engine)
    # 啟動時補齊功能開關列（不覆寫既有設定）。
    with SessionLocal() as db:
        FeatureFlagService.seed_defaults(db)
        db.commit()
    yield



app = FastAPI(
    title=settings.app_name,
    version="0.1.0-phase1",
    description=(
        "醫院員工出勤系統 Phase 1（沙盒試辦）。"
        "與現有 HIS/EMR 完全隔離；影子模式運作，加班為候選值，不自動送薪資。"
    ),
    lifespan=lifespan,
)

# TODO(open-decision): 正式部署的來源網域待定。
# 地端部署確認後改為明確清單，勿在 production 使用萬用字元。
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.webauthn_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for module_router in (
    identity_router,
    attendance_router,
    scheduling_router,
    overtime_router,
    reporting_router,
    audit_router,
    governance_router,
):
    app.include_router(module_router, prefix="/api/v1")


@app.get("/health", tags=["system"])
def health() -> dict[str, object]:
    return {
        "status": "ok",
        "environment": settings.environment,
        "shadow_mode": settings.shadow_mode,
        "labor_rules_reviewed": settings.labor.labor_rules_reviewed,
        # R8：在醫院 IT 與 HIS 廠商書面確認前，此值永遠為 False。
        "his_integrated": False,
    }
