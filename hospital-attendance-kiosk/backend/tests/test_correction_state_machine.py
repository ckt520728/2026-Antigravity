"""更正流程狀態機測試 (CLAUDE.md §10)。

驗證的是「哪些轉換合法」與「終態不可再轉換」，不碰資料庫。
"""

from __future__ import annotations

import pytest
from fastapi import HTTPException

from app.core.enums import CorrectionState as S
from app.modules.attendance.service import _ALLOWED_TRANSITIONS, _assert_transition


def test_happy_path_transitions_are_allowed():
    path = [
        (S.DRAFT, S.SUBMITTED),
        (S.SUBMITTED, S.SUPERVISOR_APPROVED),
        (S.SUPERVISOR_APPROVED, S.HR_CONFIRMED),
        (S.HR_CONFIRMED, S.APPLIED),
    ]
    for current, target in path:
        _assert_transition(current, target)  # 不應拋出


@pytest.mark.parametrize(
    "current",
    [S.SUBMITTED, S.SUPERVISOR_APPROVED, S.HR_CONFIRMED],
)
def test_every_approval_stage_can_reject(current):
    _assert_transition(current, S.REJECTED)


def test_cannot_skip_supervisor_approval():
    """不得跳過主管核准直接由人事確認。"""
    with pytest.raises(HTTPException) as exc:
        _assert_transition(S.SUBMITTED, S.HR_CONFIRMED)
    assert exc.value.status_code == 409


def test_cannot_apply_before_hr_confirmation():
    with pytest.raises(HTTPException):
        _assert_transition(S.SUPERVISOR_APPROVED, S.APPLIED)


def test_draft_cannot_jump_to_applied():
    with pytest.raises(HTTPException):
        _assert_transition(S.DRAFT, S.APPLIED)


@pytest.mark.parametrize("terminal", [S.APPLIED, S.REJECTED])
def test_terminal_states_have_no_outgoing_transitions(terminal):
    assert _ALLOWED_TRANSITIONS[terminal] == set()
    for target in S:
        with pytest.raises(HTTPException):
            _assert_transition(terminal, target)


def test_rejected_cannot_be_reopened():
    with pytest.raises(HTTPException):
        _assert_transition(S.REJECTED, S.SUBMITTED)
