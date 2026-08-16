"""事件配對邏輯測試（純函式，不需資料庫）。

重點在**保守策略**：配不起來的事件不猜測，一律列為未配對，
交由更正流程處理 (CLAUDE.md §10)。
"""

from __future__ import annotations

from datetime import datetime, timedelta

from app.core.enums import AttendanceEventType as T
from app.modules.attendance.pairing import RawEvent, pair_events

BASE = datetime(2026, 8, 3, 8, 0)


def ev(offset_minutes: int, event_type: T, event_id: str | None = None) -> RawEvent:
    return RawEvent(
        event_id=event_id or f"e{offset_minutes}",
        event_type=event_type,
        occurred_at=BASE + timedelta(minutes=offset_minutes),
    )


def test_simple_shift_produces_one_closed_session():
    result = pair_events([ev(0, T.CHECK_IN), ev(480, T.CHECK_OUT)])

    assert len(result.sessions) == 1
    assert result.sessions[0].is_closed
    assert result.total_work_minutes == 480
    assert result.unmatched_count == 0
    assert result.first_check_in_at == BASE
    assert result.last_check_out_at == BASE + timedelta(minutes=480)


def test_breaks_are_deducted_and_counted():
    result = pair_events(
        [
            ev(0, T.CHECK_IN),
            ev(240, T.BREAK_OUT),
            ev(300, T.BREAK_IN),   # 外出 60 分鐘
            ev(540, T.CHECK_OUT),  # 毛工時 540
        ]
    )

    assert result.total_out_count == 1
    assert result.total_work_minutes == 480  # 540 - 60
    assert result.unmatched_count == 0


def test_missing_check_out_is_reported_not_guessed():
    """只有上班沒有下班時，系統不得自行補一個下班時間。"""
    result = pair_events([ev(0, T.CHECK_IN)])

    assert result.total_work_minutes == 0
    assert result.unmatched_count == 1
    assert result.last_check_out_at is None


def test_check_out_without_check_in_is_unmatched():
    result = pair_events([ev(60, T.CHECK_OUT)])

    assert result.sessions == []
    assert result.unmatched_count == 1


def test_double_check_in_marks_first_as_unmatched():
    result = pair_events(
        [ev(0, T.CHECK_IN, "first"), ev(30, T.CHECK_IN, "second"), ev(480, T.CHECK_OUT)]
    )

    assert "first" in result.unmatched_event_ids
    assert len(result.sessions) == 1


def test_clinical_round_signin_does_not_affect_work_hours():
    """需求 d：病房簽到是在場證據，不是工時起訖 (CLAUDE.md §6)。"""
    with_round = pair_events(
        [ev(0, T.CHECK_IN), ev(120, T.CLINICAL_ROUND_SIGN_IN), ev(480, T.CHECK_OUT)]
    )
    without_round = pair_events([ev(0, T.CHECK_IN), ev(480, T.CHECK_OUT)])

    assert with_round.total_work_minutes == without_round.total_work_minutes
    assert with_round.unmatched_count == 0


def test_on_duty_sign_in_out_pairs_like_a_shift():
    """需求 h / i：夜間與假日值班使用 ON_DUTY_* 事件。"""
    result = pair_events([ev(0, T.ON_DUTY_SIGN_IN), ev(720, T.ON_DUTY_SIGN_OUT)])

    assert len(result.sessions) == 1
    assert result.total_work_minutes == 720


def test_break_out_without_return_is_deducted_at_checkout():
    result = pair_events(
        [ev(0, T.CHECK_IN), ev(400, T.BREAK_OUT), ev(480, T.CHECK_OUT)]
    )

    assert result.total_out_count == 1
    assert result.total_work_minutes == 400  # 480 - 80 分鐘外出未返回


def test_events_are_sorted_before_pairing():
    """離線 kiosk 補送可能亂序抵達，配對前必須排序。"""
    result = pair_events([ev(480, T.CHECK_OUT), ev(0, T.CHECK_IN)])

    assert len(result.sessions) == 1
    assert result.total_work_minutes == 480
    assert result.unmatched_count == 0
