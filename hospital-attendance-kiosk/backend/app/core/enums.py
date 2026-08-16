"""跨模組共用列舉。

術語定義見 CLAUDE.md §6 / CONTEXT.md。這裡的命名刻意與術語表一致，
避免「打卡」「簽到」「值班」在程式中混用。
"""

from __future__ import annotations

from enum import StrEnum


class StaffRole(StrEnum):
    """職務角色。涵蓋需求 c–i 的醫護與非醫護對象。"""

    DOCTOR = "DOCTOR"                      # 醫師
    NURSE = "NURSE"                        # 護理師
    NURSE_SPECIALIST = "NURSE_SPECIALIST"  # 專科護理師
    REGISTRATION = "REGISTRATION"          # 掛號
    ACCOUNTANT = "ACCOUNTANT"              # 會計
    MEDICAL_ADMIN = "MEDICAL_ADMIN"        # 醫務行政
    SUPERVISOR = "SUPERVISOR"              # 單位主管（核准關卡）
    HR = "HR"                              # 人事（確認關卡）
    SYSTEM_ADMIN = "SYSTEM_ADMIN"          # 系統管理者


class Unit(StrEnum):
    """工作單位。決定適用哪一組出勤規則。"""

    OPD = "OPD"                # 門診
    ER = "ER"                  # 急診
    INPATIENT = "INPATIENT"    # 住院病房
    ADMINISTRATION = "ADMINISTRATION"  # 行政
    OTHER = "OTHER"


class EmploymentType(StrEnum):
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    CONTRACT = "CONTRACT"
    LOCUM = "LOCUM"  # 代班／支援


class AttendanceEventType(StrEnum):
    """出勤事件型別。

    三種概念**不可混用** (CLAUDE.md §6)：
    - CHECK_IN / CHECK_OUT      → 一般上下班（需求 b, e, f, g）
    - ON_DUTY_SIGN_IN / _OUT    → 夜間、假日、on-call 到勤（需求 h, i）
    - CLINICAL_ROUND_SIGN_IN    → 病房層級醫師在場（需求 d）
    """

    CHECK_IN = "CHECK_IN"
    CHECK_OUT = "CHECK_OUT"
    BREAK_OUT = "BREAK_OUT"    # 外出（供「外出次數」指標）
    BREAK_IN = "BREAK_IN"      # 外出返回
    ON_DUTY_SIGN_IN = "ON_DUTY_SIGN_IN"
    ON_DUTY_SIGN_OUT = "ON_DUTY_SIGN_OUT"
    CLINICAL_ROUND_SIGN_IN = "CLINICAL_ROUND_SIGN_IN"


class EventSource(StrEnum):
    """事件來源。用於區分證據強度與稽核。"""

    KIOSK_WEBAUTHN = "KIOSK_WEBAUTHN"  # 院內 kiosk 生物驗證，證據最強
    WEB = "WEB"                        # 一般網頁登入
    SUPERVISOR_EXCEPTION = "SUPERVISOR_EXCEPTION"  # 非生物辨識例外路徑，需理由
    IMPORT = "IMPORT"                  # 由既有 HR/紙本匯入（影子模式對帳用）
    CORRECTION = "CORRECTION"          # 經完整更正流程產生


class VerificationMethod(StrEnum):
    """驗證方式。

    R1：無論何種方式，都**只存簽章與中繼資料**，
    絕不儲存原始指紋／臉部影像或可還原的生物特徵範本。
    """

    WEBAUTHN_PLATFORM = "WEBAUTHN_PLATFORM"  # Windows Hello 指紋／臉部
    WEBAUTHN_ROAMING = "WEBAUTHN_ROAMING"    # 實體安全金鑰
    MANUAL_OVERRIDE = "MANUAL_OVERRIDE"      # 受治理的例外路徑


class ShiftType(StrEnum):
    """班別。對應需求 c, h, i。"""

    DAY = "DAY"                    # 白班
    EVENING = "EVENING"            # 小夜
    NIGHT = "NIGHT"                # 大夜
    OPD_SESSION = "OPD_SESSION"    # 門診診次（需求 c）
    NIGHT_DUTY = "NIGHT_DUTY"      # 夜間值班（需求 h）
    HOLIDAY_DUTY = "HOLIDAY_DUTY"  # 假日值班（需求 i）
    OFF = "OFF"                    # 休假


class ShiftVersionState(StrEnum):
    """班表版本狀態。班表需經主管核准 (CLAUDE.md 決議 12)。"""

    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    APPROVED = "APPROVED"
    SUPERSEDED = "SUPERSEDED"


class CorrectionState(StrEnum):
    """更正流程狀態機 (CLAUDE.md §10)。

    DRAFT → SUBMITTED → SUPERVISOR_APPROVED → HR_CONFIRMED → APPLIED
                     ↘ REJECTED（任一關卡可退回，須填理由）
    """

    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    SUPERVISOR_APPROVED = "SUPERVISOR_APPROVED"
    HR_CONFIRMED = "HR_CONFIRMED"
    APPLIED = "APPLIED"
    REJECTED = "REJECTED"


class SummaryStatus(StrEnum):
    """工時彙總狀態。

    影子模式下加班一律先為 CANDIDATE，核准後才 APPROVED，
    且**絕不自動送薪資** (R4)。
    """

    DRAFT = "DRAFT"
    CANDIDATE = "CANDIDATE"
    APPROVED = "APPROVED"
    LOCKED = "LOCKED"


class AuditAction(StrEnum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    EXPORT = "EXPORT"          # 報表下載必須記錄 (CLAUDE.md §9)
    FEATURE_TOGGLE = "FEATURE_TOGGLE"
    LOGIN = "LOGIN"
