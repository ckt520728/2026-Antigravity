"""事件配對：把原始出勤事件串成可計算的工作區段。

參考 `reference/employer-checkin/` 的 SQL 彙總邏輯，產出四項指標：
首次上班時間、最後下班時間、外出次數、總工時。

本檔為**純函式**，不碰資料庫，方便單元測試。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta

from app.core.enums import AttendanceEventType


@dataclass(frozen=True)
class RawEvent:
    """配對用的最小事件表示。"""

    event_id: str
    event_type: AttendanceEventType
    occurred_at: datetime


@dataclass
class WorkSession:
    """一段配對完成的工作區段。"""

    start_at: datetime
    end_at: datetime | None = None
    break_minutes: int = 0
    out_count: int = 0
    start_event_id: str | None = None
    end_event_id: str | None = None

    @property
    def is_closed(self) -> bool:
        return self.end_at is not None

    @property
    def worked_minutes(self) -> int:
        """區段淨工時（扣除外出時間）。未結束的區段回 0。"""
        if self.end_at is None:
            return 0
        gross = int((self.end_at - self.start_at) / timedelta(minutes=1))
        return max(0, gross - self.break_minutes)


@dataclass
class PairingResult:
    sessions: list[WorkSession] = field(default_factory=list)
    unmatched_event_ids: list[str] = field(default_factory=list)

    @property
    def first_check_in_at(self) -> datetime | None:
        return min((s.start_at for s in self.sessions), default=None)

    @property
    def last_check_out_at(self) -> datetime | None:
        return max(
            (s.end_at for s in self.sessions if s.end_at is not None), default=None
        )

    @property
    def total_out_count(self) -> int:
        return sum(s.out_count for s in self.sessions)

    @property
    def total_work_minutes(self) -> int:
        return sum(s.worked_minutes for s in self.sessions)

    @property
    def unmatched_count(self) -> int:
        return len(self.unmatched_event_ids)


#: 開啟區段的事件型別。ON_DUTY_* 與 CHECK_* 共用同一套配對邏輯，
#: 但在 overtime 模組會分別歸入不同時數桶（夜間／假日值班）。
_OPEN_TYPES = {
    AttendanceEventType.CHECK_IN,
    AttendanceEventType.ON_DUTY_SIGN_IN,
}
_CLOSE_TYPES = {
    AttendanceEventType.CHECK_OUT,
    AttendanceEventType.ON_DUTY_SIGN_OUT,
}


def pair_events(events: list[RawEvent]) -> PairingResult:
    """把事件串成工作區段。

    刻意採用保守策略：配不起來的事件**不猜測**，一律列入
    `unmatched_event_ids`，交由更正流程處理 (CLAUDE.md §10)。
    系統寧可回報「資料不完整」，也不自行補一個下班時間。

    CLINICAL_ROUND_SIGN_IN 不參與工時配對——它是在場證據，
    不代表工作區段的起訖 (CLAUDE.md §6)。
    """
    result = PairingResult()
    ordered = sorted(events, key=lambda e: e.occurred_at)

    current: WorkSession | None = None
    pending_break_start: datetime | None = None

    for event in ordered:
        etype = event.event_type

        if etype is AttendanceEventType.CLINICAL_ROUND_SIGN_IN:
            # 需求 d：僅為在場證據，不影響工時計算。
            continue

        if etype in _OPEN_TYPES:
            if current is not None:
                # 連續兩次上班而沒有下班：前一段無法計算，標記未配對。
                if current.start_event_id:
                    result.unmatched_event_ids.append(current.start_event_id)
            current = WorkSession(
                start_at=event.occurred_at, start_event_id=event.event_id
            )
            pending_break_start = None

        elif etype in _CLOSE_TYPES:
            if current is None:
                # 沒有對應上班的下班事件。
                result.unmatched_event_ids.append(event.event_id)
                continue
            if pending_break_start is not None:
                # 外出未返回就直接下班：外出時段不計入工時。
                current.break_minutes += int(
                    (event.occurred_at - pending_break_start) / timedelta(minutes=1)
                )
                pending_break_start = None
            current.end_at = event.occurred_at
            current.end_event_id = event.event_id
            result.sessions.append(current)
            current = None

        elif etype is AttendanceEventType.BREAK_OUT:
            if current is None:
                result.unmatched_event_ids.append(event.event_id)
                continue
            current.out_count += 1
            pending_break_start = event.occurred_at

        elif etype is AttendanceEventType.BREAK_IN:
            if current is None or pending_break_start is None:
                result.unmatched_event_ids.append(event.event_id)
                continue
            current.break_minutes += int(
                (event.occurred_at - pending_break_start) / timedelta(minutes=1)
            )
            pending_break_start = None

    if current is not None:
        # 期末仍未關閉的區段：只有上班沒有下班。
        result.sessions.append(current)
        if current.start_event_id:
            result.unmatched_event_ids.append(current.start_event_id)

    return result
