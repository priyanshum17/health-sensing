"""Shared helpers for 3AFC experiment pages."""

from __future__ import annotations

import statistics
from typing import Any

import streamlit as st

from utils.adaptive_3afc import advance_trial, register_response


def render_feedback(feedback_key: str) -> None:
    """Render correctness feedback from the previous trial.

    Args:
        feedback_key: Session-state key used to store previous feedback value.
    """
    last_feedback = st.session_state.get(feedback_key)
    if last_feedback == "correct":
        st.success("Previous response: Correct.")
    elif last_feedback == "incorrect":
        st.error("Previous response: Incorrect.")


def submit_3afc_response(
    *,
    state_key: str,
    adaptive: dict[str, Any],
    trial: dict[str, int],
    level_used: float,
    selected_interval: int,
    feedback_key: str,
) -> None:
    """Apply one 3AFC response and advance to the next randomized trial.

    Args:
        state_key: Adaptive state namespace key.
        adaptive: Mutable adaptive staircase state.
        trial: Current trial descriptor containing target interval index.
        level_used: Stimulus level used in the current trial.
        selected_interval: User-selected interval in 1-based indexing.
        feedback_key: Session-state key for last-response feedback.
    """
    chosen_idx = int(selected_interval) - 1
    is_correct = chosen_idx == int(trial["target_index"])
    register_response(
        adaptive,
        level_used=level_used,
        is_correct=is_correct,
        chosen_index=chosen_idx,
        target_index=int(trial["target_index"]),
    )
    advance_trial(state_key)
    st.session_state[feedback_key] = "correct" if is_correct else "incorrect"
    st.rerun()


def render_recent_accuracy_metric(history: list[dict[str, Any]], trailing_n: int = 12) -> None:
    """Render recent accuracy over the trailing trials.

    Args:
        history: Adaptive response history.
        trailing_n: Number of recent responses to include.
    """
    recent_accuracy = 0.0
    if history:
        recent = history[-trailing_n:]
        recent_accuracy = 100.0 * statistics.mean(
            1.0 if item["correct"] else 0.0 for item in recent
        )
    st.metric(f"Recent Accuracy (last {trailing_n})", f"{recent_accuracy:.1f}%")


def render_completion_summary(
    adaptive: dict[str, Any],
    *,
    estimated_value: float,
    value_label: str,
) -> None:
    """Render common completion summary metrics for adaptive 3AFC tests.

    Args:
        adaptive: Adaptive staircase state.
        estimated_value: Final threshold estimate.
        value_label: Threshold unit label, for example ``"ms"``.
    """
    history = adaptive["history"]
    total_trials = len(history)
    accuracy = 100.0 * statistics.mean(1.0 if item["correct"] else 0.0 for item in history)
    col_1, col_2, col_3, col_4 = st.columns(4)
    col_1.metric("Total Trials", f"{total_trials}")
    col_2.metric("Overall Accuracy", f"{accuracy:.1f}%")
    col_3.metric("Reversals", f"{len(adaptive['reversals'])}")
    col_4.metric("Threshold", f"{estimated_value:.2f} {value_label}")


def render_staircase_plot(
    *,
    history: list[dict[str, Any]],
    estimated_value: float,
    threshold_label: str,
    y_label: str,
    title: str,
) -> None:
    """Render a staircase plot for one adaptive run.

    Args:
        history: Trial history from adaptive state.
        estimated_value: Estimated threshold value.
        threshold_label: Threshold label shown in the legend.
        y_label: Y-axis label.
        title: Plot title.
    """
    try:
        import matplotlib.pyplot as plt
    except Exception:
        st.info("Matplotlib plot unavailable in this environment.")
        return

    trials = list(range(1, len(history) + 1))
    levels = [float(item["level"]) for item in history]
    correct = [bool(item["correct"]) for item in history]
    colors = ["#2E7D32" if item else "#C62828" for item in correct]

    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.plot(trials, levels, color="#1565C0", linewidth=1.6, label="Level")
    ax.scatter(trials, levels, c=colors, s=25, alpha=0.9, label="Trial Response")
    ax.axhline(
        estimated_value,
        color="#6A1B9A",
        linestyle="--",
        linewidth=1.3,
        label=f"{threshold_label} {estimated_value:.2f}",
    )
    ax.set_xlabel("Trial Number")
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.grid(alpha=0.25)
    ax.legend(loc="best")
    st.pyplot(fig)
    plt.close(fig)
