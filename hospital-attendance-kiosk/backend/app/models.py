"""集中匯入所有 ORM model。

Alembic autogenerate 與建表都依賴這裡：
新增模組時**必須**在此加一行 import，否則該表不會出現在 migration 中。
"""

from app.core.feature_store import FeatureFlagRecord  # noqa: F401
from app.modules.attendance.models import (  # noqa: F401
    AttendanceEvent,
    CorrectionRequest,
)
from app.modules.audit.models import AuditLog  # noqa: F401
from app.modules.governance.models import (  # noqa: F401
    DeviationRecord,
    RubricCheck,
    UnknownItem,
)
from app.modules.identity.models import (  # noqa: F401
    Staff,
    VerificationEvent,
    WebAuthnCredential,
)
from app.modules.overtime.models import ComplianceFlag, WorkHourSummary  # noqa: F401
from app.modules.scheduling.models import (  # noqa: F401
    PlannedShift,
    ShiftChangeLog,
    ShiftVersion,
)

__all__ = [
    "AttendanceEvent",
    "AuditLog",
    "ComplianceFlag",
    "CorrectionRequest",
    "DeviationRecord",
    "FeatureFlagRecord",
    "PlannedShift",
    "RubricCheck",
    "ShiftChangeLog",
    "ShiftVersion",
    "Staff",
    "UnknownItem",
    "VerificationEvent",
    "WebAuthnCredential",
    "WorkHourSummary",
]
