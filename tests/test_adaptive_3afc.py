"""Tests for adaptive 3AFC staircase utilities."""

from __future__ import annotations

import types

import pytest

import utils.adaptive_3afc as adaptive


@pytest.fixture()
def fake_streamlit(monkeypatch: pytest.MonkeyPatch) -> types.SimpleNamespace:
    """Provide a fake Streamlit module with isolated session state."""
    fake_st = types.SimpleNamespace(session_state={})
    monkeypatch.setattr(adaptive, "st", fake_st)
    return fake_st


def test_init_adaptive_state_sets_defaults(fake_streamlit: types.SimpleNamespace) -> None:
    """`init_adaptive_state` should initialize expected keys and values."""
    state = adaptive.init_adaptive_state(
        "gap",
        start_level=20.0,
        min_level=0.5,
        max_level=120.0,
        initial_step=6.0,
        min_step=0.25,
        max_reversals=6,
        down=2,
    )

    assert state["current_level"] == 20.0
    assert state["step"] == 6.0
    assert state["reversals"] == []
    assert state["history"] == []
    assert not state["finished"]


def test_register_response_two_corrects_step_down(fake_streamlit: types.SimpleNamespace) -> None:
    """Two consecutive correct responses should decrease level in 2-down/1-up."""
    state = adaptive.init_adaptive_state(
        "amp",
        start_level=3.0,
        min_level=0.2,
        max_level=20.0,
        initial_step=1.0,
        min_step=0.1,
        max_reversals=6,
        down=2,
    )

    adaptive.register_response(
        state,
        level_used=3.0,
        is_correct=True,
        chosen_index=0,
        target_index=0,
    )
    assert state["current_level"] == 3.0

    adaptive.register_response(
        state,
        level_used=3.0,
        is_correct=True,
        chosen_index=0,
        target_index=0,
    )
    assert state["current_level"] == 2.0


def test_register_response_reversal_finishes_when_limit_reached(
    fake_streamlit: types.SimpleNamespace,
) -> None:
    """State should mark finished when reversal count reaches configured max."""
    state = adaptive.init_adaptive_state(
        "pitch",
        start_level=40.0,
        min_level=1.0,
        max_level=1000.0,
        initial_step=20.0,
        min_step=1.0,
        max_reversals=1,
        down=1,
    )

    adaptive.register_response(
        state,
        level_used=40.0,
        is_correct=False,
        chosen_index=0,
        target_index=1,
    )
    adaptive.register_response(
        state,
        level_used=60.0,
        is_correct=True,
        chosen_index=1,
        target_index=1,
    )

    assert len(state["reversals"]) == 1
    assert state["finished"] is True


def test_estimate_threshold_uses_recent_reversals(fake_streamlit: types.SimpleNamespace) -> None:
    """Threshold estimate should be mean of trailing reversal values when available."""
    state = adaptive.init_adaptive_state(
        "gap2",
        start_level=20.0,
        min_level=0.5,
        max_level=120.0,
        initial_step=6.0,
        min_step=0.25,
        max_reversals=6,
        down=2,
    )
    state["reversals"] = [10.0, 8.0, 6.0, 4.0, 2.0]

    estimate = adaptive.estimate_threshold(state, tail_count=4)
    assert estimate == pytest.approx(5.0)
