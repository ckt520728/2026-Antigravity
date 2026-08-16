"""應用設定。

重要：勞基法參數一律為「可設定的政策參數」，不得寫死在計算程式中
(CLAUDE.md §7)。在權責單位書面確認前，`labor_rules_reviewed` 必須為 False，
所有報表需標示「未經法規複核」。
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class LaborPolicy(BaseSettings):
    """台灣勞基法預設參數 (CLAUDE.md §7)。

    TODO(open-decision): 權責單位（人事室）與勞動法規複核窗口尚未指定。
    在 `labor_rules_reviewed` 轉為 True 前，任何據此產生的加班時數
    只能是 Overtime Candidate，且報表必須帶警示浮水印。
    """

    model_config = SettingsConfigDict(env_prefix="LABOR_")

    # 勞基法 §30 — 每日正常工時 8 小時
    daily_regular_minutes: int = 480
    # 勞基法 §30 — 每週正常工時 40 小時
    weekly_regular_minutes: int = 2400
    # 勞基法 §32 — 每日工時上限（含加班）12 小時
    daily_max_minutes: int = 720
    # 勞基法 §32 — 每月加班上限 46 小時
    monthly_overtime_cap_minutes: int = 2760
    # 勞基法 §34 — 輪班間隔 11 小時
    min_shift_interval_minutes: int = 660

    # 未經人事室 / 勞動法規複核確認前一律 False
    labor_rules_reviewed: bool = False


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    app_name: str = "醫院員工出勤系統"
    environment: Literal["development", "test", "staging", "production"] = "development"
    debug: bool = True

    # 治理法域：中華民國（台灣）(CLAUDE.md §13)
    timezone: str = "Asia/Taipei"

    database_url: str = (
        "postgresql+psycopg://attendance:attendance@localhost:5432/attendance"
    )

    # --- Phase 1 影子模式 (CLAUDE.md §7, R4) ---
    # True = 與現有 HR/紙本平行運作，加班僅為候選，絕不送薪資。
    shadow_mode: bool = True

    # --- WebAuthn (CLAUDE.md §8) ---
    webauthn_rp_id: str = "localhost"
    webauthn_rp_name: str = "醫院員工出勤系統"
    webauthn_origin: str = "http://localhost:5173"

    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    labor: LaborPolicy = LaborPolicy()

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def allows_real_staff_data(self) -> bool:
        """CLAUDE.md R7：開發／測試環境僅可使用合成或不可逆去識別化資料。"""
        return self.environment in ("staging", "production")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
