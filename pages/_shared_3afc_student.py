"""Shared TODOs for all 3AFC assignment pages.

Why this file exists:
- All 3AFC pages use the same staircase, accuracy, and plotting patterns.
- Shared logic is implemented here once and reused by all 3AFC pages.

Used by:
- pages/sound_gap_detection.py
- pages/amplitude_threshold.py
- pages/pitch_threshold.py

Implementation expectations:
- Keep return types exactly as annotated.
- Prefer small, pure functions with no Streamlit state mutations.
- Validate/clamp values to avoid invalid outputs.
"""


def shared_student_apply_reversal_update(
    *,
    current_level: float,
    step: float,
    is_correct: bool,
    correct_streak: int,
    down_n: int,
    min_level: float,
    max_level: float,
) -> tuple[float, int]:
    """Apply one 2-down/1-up staircase update.

    Inputs:
        current_level: current adaptive stimulus level.
        step: step size for level change.
        is_correct: whether the response is correct.
        correct_streak: consecutive correct count before this trial.
        down_n: number of correct responses needed to step down.
        min_level: minimum allowed level.
        max_level: maximum allowed level.

    Returns:
        Tuple `(next_level, next_correct_streak)` after one update.

    Safety requirements:
        - Clamp level to `[min_level, max_level]`.
        - Treat `down_n < 1` as 1 to avoid zero-step loops.
    """
    raise NotImplementedError("Not implemented yet; follow the docstring guidance.")


def shared_student_plot_staircase(
    history: list[dict], threshold: float, y_label: str, title: str
) -> None:
    """Plot the staircase trace for the given history.

    Expected plot content:
        - X-axis: trial number.
        - Y-axis: level value per trial.
        - Visual distinction for correct vs incorrect trials.
        - Threshold drawn as a horizontal dashed line.

    Safety requirements:
        - Do not crash for empty or very short history lists.
    """
    raise NotImplementedError("Not implemented yet; follow the docstring guidance.")


def shared_student_build_three_interval_targets(*, target_index: int) -> list[bool]:
    """Build a length-3 target mask with exactly one `True` entry.

    Example:
        target_index=1 -> [False, True, False]
    """
    raise NotImplementedError("Not implemented yet; follow the docstring guidance.")


def shared_student_update_staircase_state(
    *,
    current_level: float,
    step: float,
    is_correct: bool,
    correct_streak: int,
    down_n: int,
    min_level: float,
    max_level: float,
) -> tuple[float, int]:
    """Reusable helper that keeps staircase behavior consistent.

    This can wrap or share logic with `shared_student_apply_reversal_update`.
    """
    raise NotImplementedError("Not implemented yet; follow the docstring guidance.")


def shared_student_estimate_threshold_from_reversals(
    *, reversals: list[float], fallback_level: float, tail_count: int = 4
) -> float:
    """Estimate threshold using the trailing reversal points.

    Recommended behavior:
        - When there are enough reversals, average the last `tail_count` values.
        - Otherwise return `fallback_level`.
    """
    raise NotImplementedError("Not implemented yet; follow the docstring guidance.")


def shared_student_compute_recent_accuracy(history: list[dict], window: int = 12) -> float:
    """Compute a trailing percent-correct accuracy metric.

    Output should be a percentage in the `[0, 100]` range.
    """
    raise NotImplementedError("Not implemented yet; follow the docstring guidance.")


def shared_student_validate_audio_params(*, amplitude: float, stimulus_value: float) -> bool:
    """Validate amplitude and stimulus-specific numeric values.

    Returns:
        `True` when inputs are in safe ranges, otherwise `False`.
    """
    raise NotImplementedError("Not implemented yet; follow the docstring guidance.")


def shared_student_plot_staircase_with_threshold(
    *, history: list[dict], threshold: float, y_label: str, title: str
) -> None:
    """Wrapper that draws the staircase and highlights the threshold.

    Hint:
        Call `shared_student_plot_staircase(...)` internally to avoid duplicate code.
    """
    raise NotImplementedError("Not implemented yet; follow the docstring guidance.")
