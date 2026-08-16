"""共用 FastAPI dependencies：功能開關守門、身分、權限。"""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.feature_store import FeatureFlagService
from app.core.features import FEATURE_LABELS, Feature

DbSession = Annotated[Session, Depends(get_db)]


def require_feature(feature: Feature) -> Callable[..., None]:
    """功能開關守門。

    關閉時回 **404**（而非 403）——對外不揭露該功能存在，
    符合 CLAUDE.md §5「關閉時對應 API 回 404」。
    """

    def _guard(db: DbSession) -> None:
        if not FeatureFlagService.is_enabled(db, feature):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"功能未啟用：{FEATURE_LABELS.get(feature, feature.value)}",
            )

    return _guard


class CurrentStaff:
    """已驗證的呼叫者。

    Phase 1 由 HR 核可名冊另行開設試辦帳號，
    **不重用 HIS 密碼** (CLAUDE.md R5)。
    """

    def __init__(self, staff_id: str, employee_no: str, role: str, unit: str | None):
        self.staff_id = staff_id
        self.employee_no = employee_no
        self.role = role
        self.unit = unit


def get_current_staff(request: Request) -> CurrentStaff:
    """從 Bearer token 解出目前使用者。

    Token 由 identity 模組於 WebAuthn 驗證成功後簽發 (CLAUDE.md §8)。
    """
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="缺少驗證憑證",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = header.removeprefix("Bearer ").strip()
    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="憑證無效或已過期"
        ) from exc

    return CurrentStaff(
        staff_id=payload["sub"],
        employee_no=payload.get("employee_no", ""),
        role=payload.get("role", ""),
        unit=payload.get("unit"),
    )


AuthedStaff = Annotated[CurrentStaff, Depends(get_current_staff)]


def require_role(*roles: str) -> Callable[..., CurrentStaff]:
    """粗粒度角色守門。

    TODO(open-decision): 完整的角色權限矩陣與職責分離 (segregation of duties)
    尚未定案 (CLAUDE.md §14)。此處僅為骨架，實作前必須先與使用者確認矩陣，
    特別是「主管核准」與「人事確認」不得由同一人兼任的分離規則。
    """

    def _guard(staff: AuthedStaff) -> CurrentStaff:
        if staff.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="權限不足",
            )
        return staff

    return _guard
