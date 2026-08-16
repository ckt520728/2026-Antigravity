"""Attendance 模組公開介面。

其他模組只能呼叫本檔的函式，不得直接 import AttendanceEvent ORM
(CLAUDE.md §4)。
"""

from __future__ import annotations

from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import utcnow
from app.core.enums import (
    AttendanceEventType,
    AuditAction,
    CorrectionState,
    EventSource,
)
from app.modules.attendance.models import AttendanceEvent, CorrectionRequest
from app.modules.attendance.pairing import PairingResult, RawEvent, pair_events
from app.modules.audit import service as audit


def record_event(
    db: Session,
    *,
    staff_id: str,
    event_type: AttendanceEventType,
    occurred_at: datetime,
    source: EventSource,
    verification_id: str | None = None,
    station_id: str | None = None,
    ward_code: str | None = None,
    client_event_uid: str | None = None,
    actor_id: str | None = None,
) -> AttendanceEvent:
    """寫入一筆出勤事件。

    這是**唯一**的事件寫入路徑。事件寫入後不得直接 UPDATE 時間，
    任何修改都必須走 `submit_correction` 狀態機 (CLAUDE.md §10)。
    """
    if ward_code is not None and event_type is not AttendanceEventType.CLINICAL_ROUND_SIGN_IN:
        # ward_code 僅供病房層級簽到使用，避免被誤用來夾帶其他資訊。
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ward_code 僅適用於 CLINICAL_ROUND_SIGN_IN",
        )

    if client_event_uid:
        # 離線 kiosk 補送的冪等保護：同一 uid 只寫一次。
        existing = db.execute(
            select(AttendanceEvent).where(
                AttendanceEvent.client_event_uid == client_event_uid
            )
        ).scalar_one_or_none()
        if existing is not None:
            return existing

    event = AttendanceEvent(
        staff_id=staff_id,
        event_type=event_type,
        occurred_at=occurred_at,
        source=source,
        verification_id=verification_id,
        station_id=station_id,
        ward_code=ward_code,
        client_event_uid=client_event_uid,
        received_at=utcnow(),
    )
    db.add(event)
    db.flush()

    audit.record(
        db,
        action=AuditAction.CREATE,
        entity_type="attendance_event",
        entity_id=event.id,
        actor_id=actor_id or staff_id,
        after={
            "event_type": event_type.value,
            "occurred_at": occurred_at,
            "source": source.value,
        },
        station_id=station_id,
    )
    return event


def list_events(
    db: Session, *, staff_id: str, start: datetime, end: datetime
) -> list[AttendanceEvent]:
    """查詢期間內某員工的事件（不含已被更正取代者）。"""
    stmt = (
        select(AttendanceEvent)
        .where(
            AttendanceEvent.staff_id == staff_id,
            AttendanceEvent.occurred_at >= start,
            AttendanceEvent.occurred_at <= end,
            AttendanceEvent.superseded_by_id.is_(None),
        )
        .order_by(AttendanceEvent.occurred_at)
    )
    return list(db.execute(stmt).scalars().all())


def list_recent_events_all(
    db: Session, *, limit: int = 50
) -> list[AttendanceEvent]:
    """供 Kiosk 畫面即時顯示最新打卡流水紀錄。"""
    stmt = (
        select(AttendanceEvent)
        .where(AttendanceEvent.superseded_by_id.is_(None))
        .order_by(AttendanceEvent.occurred_at.desc())
        .limit(limit)
    )
    return list(db.execute(stmt).scalars().all())


def pair_for_period(
    db: Session, *, staff_id: str, start: datetime, end: datetime
) -> PairingResult:
    """供 overtime 模組取得配對結果的公開介面。"""
    events = list_events(db, staff_id=staff_id, start=start, end=end)
    return pair_events(
        [
            RawEvent(
                event_id=e.id, event_type=e.event_type, occurred_at=e.occurred_at
            )
            for e in events
        ]
    )


# --------------------------------------------------------------------------
# 更正流程狀態機 (CLAUDE.md §10)
# --------------------------------------------------------------------------

#: 合法的狀態轉換。任何不在表中的轉換一律拒絕。
_ALLOWED_TRANSITIONS: dict[CorrectionState, set[CorrectionState]] = {
    CorrectionState.DRAFT: {CorrectionState.SUBMITTED},
    CorrectionState.SUBMITTED: {
        CorrectionState.SUPERVISOR_APPROVED,
        CorrectionState.REJECTED,
    },
    CorrectionState.SUPERVISOR_APPROVED: {
        CorrectionState.HR_CONFIRMED,
        CorrectionState.REJECTED,
    },
    CorrectionState.HR_CONFIRMED: {
        CorrectionState.APPLIED,
        CorrectionState.REJECTED,
    },
    CorrectionState.APPLIED: set(),   # 終態
    CorrectionState.REJECTED: set(),  # 終態
}


def _assert_transition(current: CorrectionState, target: CorrectionState) -> None:
    if target not in _ALLOWED_TRANSITIONS[current]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"不允許的狀態轉換：{current.value} → {target.value}",
        )


def submit_correction(
    db: Session,
    *,
    staff_id: str,
    requested_by: str,
    requested_occurred_at: datetime,
    requested_event_type: AttendanceEventType,
    reason: str,
    attendance_event_id: str | None = None,
) -> CorrectionRequest:
    """員工提出更正申請。理由為必填。"""
    if not reason.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="更正申請必須填寫理由"
        )

    original = (
        db.get(AttendanceEvent, attendance_event_id) if attendance_event_id else None
    )

    request = CorrectionRequest(
        attendance_event_id=attendance_event_id,
        staff_id=staff_id,
        requested_by=requested_by,
        state=CorrectionState.SUBMITTED,
        original_occurred_at=original.occurred_at if original else None,
        requested_occurred_at=requested_occurred_at,
        requested_event_type=requested_event_type,
        reason=reason,
    )
    db.add(request)
    db.flush()

    audit.record(
        db,
        action=AuditAction.CREATE,
        entity_type="correction_request",
        entity_id=request.id,
        actor_id=requested_by,
        before={"occurred_at": request.original_occurred_at},
        after={"occurred_at": requested_occurred_at},
        reason=reason,
    )
    return request


def supervisor_approve(
    db: Session, *, request_id: str, supervisor_id: str, note: str | None = None
) -> CorrectionRequest:
    request = _get_request(db, request_id)
    _assert_transition(request.state, CorrectionState.SUPERVISOR_APPROVED)

    if supervisor_id == request.requested_by:
        # 職責分離：不得自己核准自己的申請。
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="不得核准自己提出的更正申請"
        )

    request.state = CorrectionState.SUPERVISOR_APPROVED
    request.supervisor_id = supervisor_id
    request.supervisor_acted_at = utcnow()
    db.flush()

    audit.record(
        db,
        action=AuditAction.APPROVE,
        entity_type="correction_request",
        entity_id=request.id,
        actor_id=supervisor_id,
        after={"state": request.state.value},
        reason=note or "主管核准",
    )
    return request


def hr_confirm(
    db: Session, *, request_id: str, hr_id: str, note: str | None = None
) -> CorrectionRequest:
    request = _get_request(db, request_id)
    _assert_transition(request.state, CorrectionState.HR_CONFIRMED)

    # 職責分離：主管與人事不得為同一人 (CLAUDE.md §10)。
    if hr_id in {request.requested_by, request.supervisor_id}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="人事確認者不得與申請人或核准主管為同一人",
        )

    request.state = CorrectionState.HR_CONFIRMED
    request.hr_id = hr_id
    request.hr_acted_at = utcnow()
    db.flush()

    audit.record(
        db,
        action=AuditAction.APPROVE,
        entity_type="correction_request",
        entity_id=request.id,
        actor_id=hr_id,
        after={"state": request.state.value},
        reason=note or "人事確認",
    )
    return request


def apply_correction(db: Session, *, request_id: str, actor_id: str) -> AttendanceEvent:
    """套用更正：產生新事件，原事件標記為已被取代但**不刪除**。"""
    request = _get_request(db, request_id)
    _assert_transition(request.state, CorrectionState.APPLIED)

    new_event = AttendanceEvent(
        staff_id=request.staff_id,
        event_type=request.requested_event_type,
        occurred_at=request.requested_occurred_at,
        source=EventSource.CORRECTION,
        received_at=utcnow(),
    )
    db.add(new_event)
    db.flush()

    if request.attendance_event_id:
        original = db.get(AttendanceEvent, request.attendance_event_id)
        if original is not None:
            original.is_corrected = True
            original.superseded_by_id = new_event.id

    request.state = CorrectionState.APPLIED
    request.applied_at = utcnow()
    request.resulting_event_id = new_event.id
    db.flush()

    audit.record(
        db,
        action=AuditAction.UPDATE,
        entity_type="attendance_event",
        entity_id=request.attendance_event_id or new_event.id,
        actor_id=actor_id,
        before={"occurred_at": request.original_occurred_at},
        after={"occurred_at": request.requested_occurred_at},
        reason=f"更正申請 {request.id} 套用",
    )
    return new_event


def reject_correction(
    db: Session, *, request_id: str, actor_id: str, reason: str
) -> CorrectionRequest:
    request = _get_request(db, request_id)
    _assert_transition(request.state, CorrectionState.REJECTED)

    if not reason.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="退回必須填寫理由"
        )

    previous = request.state
    request.state = CorrectionState.REJECTED
    request.rejection_reason = reason
    db.flush()

    audit.record(
        db,
        action=AuditAction.REJECT,
        entity_type="correction_request",
        entity_id=request.id,
        actor_id=actor_id,
        before={"state": previous.value},
        after={"state": request.state.value},
        reason=reason,
    )
    return request


def _get_request(db: Session, request_id: str) -> CorrectionRequest:
    request = db.get(CorrectionRequest, request_id)
    if request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="找不到更正申請"
        )
    return request


def list_events_for_period(
    db: Session, *, period_start: date, period_end: date
) -> list[dict]:
    """查詢特定期間內的所有出勤與巡診事件。"""
    from datetime import datetime, time, timezone
    from app.modules.identity.models import Staff
    
    start_dt = datetime.combine(period_start, time.min).replace(tzinfo=timezone.utc)
    end_dt = datetime.combine(period_end, time.max).replace(tzinfo=timezone.utc)

    stmt = (
        select(AttendanceEvent, Staff.name, Staff.employee_no)
        .join(Staff, AttendanceEvent.staff_id == Staff.id)
        .where(
            AttendanceEvent.occurred_at >= start_dt,
            AttendanceEvent.occurred_at <= end_dt,
        )
        .order_by(AttendanceEvent.occurred_at.asc())
    )
    results = db.execute(stmt).all()

    items = []
    for ev, staff_name, emp_no in results:
        items.append({
            "id": ev.id,
            "staff_id": ev.staff_id,
            "employee_no": emp_no,
            "name": staff_name,
            "event_type": ev.event_type.value if hasattr(ev.event_type, "value") else str(ev.event_type),
            "occurred_at": ev.occurred_at,
            "station_id": ev.station_id,
            "ward_code": ev.ward_code,
            "source": ev.source.value if hasattr(ev.source, "value") else str(ev.source),
            "override_reason": getattr(ev, "override_reason", None),
        })
    return items

