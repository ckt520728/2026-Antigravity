"""功能開關 (CLAUDE.md §5)。

需求 a–j 各自對應一個開關，必須可獨立、於執行期開關（不需重啟）。
關閉時：對應 API 回 404、前端隱藏入口、既有資料不得刪除。
"""

from __future__ import annotations

from enum import StrEnum


class Feature(StrEnum):
    """需求 a–j 對應的功能開關。"""

    # a. 以 WebAuthn 生物驗證確認在／缺勤
    BIOMETRIC_PRESENCE = "FEATURE_BIOMETRIC_PRESENCE"
    # b. 上下班打卡與工時判定
    WORK_HOURS = "FEATURE_WORK_HOURS"
    # c. 醫師門診（OPD）診次排程控制
    OPD_SCHEDULE = "FEATURE_OPD_SCHEDULE"
    # d. 住院病房訪視醫師「病房層級」簽到
    WARD_ROUND_SIGNIN = "FEATURE_WARD_ROUND_SIGNIN"
    # e. 門診護理師上下班
    OPD_NURSE = "FEATURE_OPD_NURSE"
    # f. 急診與住院護理師上下班
    ER_INPATIENT_NURSE = "FEATURE_ER_INPATIENT_NURSE"
    # g. 非醫護（掛號、會計、醫務行政）
    NONMEDICAL_STAFF = "FEATURE_NONMEDICAL_STAFF"
    # h. 夜間值班醫師／專科護理師簽到退
    NIGHT_DUTY = "FEATURE_NIGHT_DUTY"
    # i. 假日值班醫師／專科護理師簽到退
    HOLIDAY_DUTY = "FEATURE_HOLIDAY_DUTY"
    # j. 工時與加班時數彙總
    OVERTIME_AGGREGATION = "FEATURE_OVERTIME_AGGREGATION"


#: 需求代號 → 功能開關，供後台 UI 與文件對照使用。
REQUIREMENT_MAP: dict[str, Feature] = {
    "a": Feature.BIOMETRIC_PRESENCE,
    "b": Feature.WORK_HOURS,
    "c": Feature.OPD_SCHEDULE,
    "d": Feature.WARD_ROUND_SIGNIN,
    "e": Feature.OPD_NURSE,
    "f": Feature.ER_INPATIENT_NURSE,
    "g": Feature.NONMEDICAL_STAFF,
    "h": Feature.NIGHT_DUTY,
    "i": Feature.HOLIDAY_DUTY,
    "j": Feature.OVERTIME_AGGREGATION,
}

#: 中文顯示名稱（後台切換頁使用）。
FEATURE_LABELS: dict[Feature, str] = {
    Feature.BIOMETRIC_PRESENCE: "生物辨識在勤確認",
    Feature.WORK_HOURS: "上下班打卡與工時",
    Feature.OPD_SCHEDULE: "醫師門診診次排程",
    Feature.WARD_ROUND_SIGNIN: "病房訪視醫師簽到",
    Feature.OPD_NURSE: "門診護理師出勤",
    Feature.ER_INPATIENT_NURSE: "急診與住院護理師出勤",
    Feature.NONMEDICAL_STAFF: "非醫護人員出勤",
    Feature.NIGHT_DUTY: "夜間值班簽到退",
    Feature.HOLIDAY_DUTY: "假日值班簽到退",
    Feature.OVERTIME_AGGREGATION: "工時與加班彙總",
}

#: 首次啟動時寫入資料庫的預設值。
#: 之後以資料庫 feature_flag 表為準，本表僅作為 seed 與 fallback。
DEFAULT_FLAGS: dict[Feature, bool] = {
    Feature.BIOMETRIC_PRESENCE: True,
    Feature.WORK_HOURS: True,
    Feature.OPD_SCHEDULE: True,
    Feature.WARD_ROUND_SIGNIN: True,
    Feature.OPD_NURSE: True,
    Feature.ER_INPATIENT_NURSE: True,
    Feature.NONMEDICAL_STAFF: True,
    Feature.NIGHT_DUTY: True,
    Feature.HOLIDAY_DUTY: True,
    Feature.OVERTIME_AGGREGATION: True,
}
