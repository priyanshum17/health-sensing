import random
import statistics
from typing import Any

import streamlit as st


def init_adaptive_state(
    state_key: str,
    *,
    start_level: float,
    min_level: float,
    max_level: float,
    initial_step: float,
    min_step: float,
    max_reversals: int = 8,
    down: int = 2,
) -> dict[str, Any]:
    """Create or fetch an adaptive 3AFC staircase state.

    Args:
        state_key: Namespace prefix for Streamlit session-state keys.
        start_level: Initial stimulus level.
        min_level: Lower bound for stimulus level.
        max_level: Upper bound for stimulus level.
        initial_step: Initial step size for level updates.
        min_step: Minimum step size after reversal shrinkage.
        max_reversals: Number of reversals required to finish.
        down: Number of consecutive correct responses required to step down.

    Returns:
        Mutable adaptive staircase state dictionary.
    """
    key = f"{state_key}_adaptive"
    if key not in st.session_state:
        st.session_state[key] = {
            "current_level": float(start_level),
            "min_level": float(min_level),
            "max_level": float(max_level),
            "step": float(initial_step),
            "min_step": float(min_step),
            "max_reversals": int(max_reversals),
            "down": int(down),
            "correct_streak": 0,
            "last_direction": None,
            "reversals": [],
            "history": [],
            "finished": False,
        }
    return st.session_state[key]


def get_or_create_trial(state_key: str) -> dict[str, int]:
    """Return a trial descriptor for 3AFC.

    Args:
        state_key: Namespace prefix for session-state keys.

    Returns:
        Trial descriptor containing target interval index and random seed.
    """
    key = f"{state_key}_trial"
    trial = st.session_state.get(key)
    if trial is None:
        trial = {
            "target_index": random.randint(0, 2),
            "seed": random.randint(1, 10_000_000),
        }
        st.session_state[key] = trial
    return trial


def advance_trial(state_key: str) -> None:
    """Generate and persist the next randomized trial descriptor.

    Args:
        state_key: Namespace prefix for session-state keys.
    """
    key = f"{state_key}_trial"
    previous = st.session_state.get(key, {})
    previous_target = previous.get("target_index")
    next_target = random.randint(0, 2)
    if previous_target in (0, 1, 2):
        while next_target == previous_target:
            next_target = random.randint(0, 2)
    st.session_state[key] = {
        "target_index": next_target,
        "seed": random.randint(1, 10_000_000),
    }


def reset_adaptive_state(state_key: str) -> None:
    """Reset adaptive and trial state for one test namespace.

    Args:
        state_key: Namespace prefix for session-state keys.
    """
    st.session_state.pop(f"{state_key}_adaptive", None)
    st.session_state.pop(f"{state_key}_trial", None)


def register_response(
    state: dict[str, Any],
    *,
    level_used: float,
    is_correct: bool,
    chosen_index: int,
    target_index: int,
) -> None:
    """Apply one 2-down/1-up update for a 3AFC response.

    Args:
        state: Adaptive staircase state dictionary.
        level_used: Stimulus level used in the current trial.
        is_correct: Whether the selected interval was correct.
        chosen_index: Selected interval index (0-based).
        target_index: Correct interval index (0-based).
    """
    if state["finished"]:
        return

    direction = None
    state["history"].append(
        {
            "level": float(level_used),
            "correct": bool(is_correct),
            "choice": int(chosen_index),
            "target": int(target_index),
        }
    )

    if is_correct:
        state["correct_streak"] += 1
        if state["correct_streak"] >= state["down"]:
            direction = "down"
            state["correct_streak"] = 0
    else:
        state["correct_streak"] = 0
        direction = "up"

    if direction is None:
        return

    if state["last_direction"] is not None and direction != state["last_direction"]:
        state["reversals"].append(float(level_used))
        state["step"] = max(state["min_step"], state["step"] * 0.7)

    state["last_direction"] = direction
    signed_step = -state["step"] if direction == "down" else state["step"]
    next_level = level_used + signed_step
    state["current_level"] = max(state["min_level"], min(state["max_level"], next_level))

    if len(state["reversals"]) >= state["max_reversals"]:
        state["finished"] = True


def estimate_threshold(state: dict[str, Any], tail_count: int = 4) -> float:
    """Estimate threshold from recent reversal points.

    Args:
        state: Adaptive staircase state dictionary.
        tail_count: Number of trailing reversals to average.

    Returns:
        Estimated threshold level.
    """
    reversals = state.get("reversals", [])
    if len(reversals) >= tail_count:
        return float(statistics.mean(reversals[-tail_count:]))
    return float(state["current_level"])
