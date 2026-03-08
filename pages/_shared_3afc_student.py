"""Shared student TODOs for all 3AFC assignment pages.

Why this file exists:
- All 3AFC pages use the same staircase, accuracy, and plotting patterns.
- Students implement shared logic once here, then reuse it everywhere.

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
    """TODO (student): Apply one 2-down/1-up staircase update.

    Inputs:
        current_level: current adaptive stimulus level.
        step: step size for level change.
        is_correct: whether current response is correct.
        correct_streak: consecutive correct count before this trial.
        down_n: number of consecutive correct responses needed to step down.
        min_level: minimum allowed level.
        max_level: maximum allowed level.

    Returns:
        Tuple `(next_level, next_correct_streak)` after one update.

    Safety requirements:
        - Clamp level to `[min_level, max_level]`.
        - Handle invalid `down_n` defensively (for example, treat values < 1 as 1).
    """
    raise NotImplementedError(
        "Student TODO: implement shared 3AFC reversal update in pages/_shared_3afc_student.py."
    )


def shared_student_plot_staircase(
    history: list[dict], threshold: float, y_label: str, title: str
) -> None:
    """TODO (student): Plot staircase trace for trial history.

    Expected plot content:
        - X-axis: trial number.
        - Y-axis: level value per trial.
        - Visual distinction for correct vs incorrect trials.
        - Threshold as a horizontal dashed line.

    Safety requirements:
        - Do not crash for empty/short history.
    """
    raise NotImplementedError(
        "Student TODO: implement shared 3AFC staircase plotting in pages/_shared_3afc_student.py."
    )


def shared_student_build_three_interval_targets(*, target_index: int) -> list[bool]:
    """TODO (student): Build a length-3 target mask with exactly one `True`.

    Example:
        target_index=1 -> [False, True, False]
    """
    raise NotImplementedError(
        "Student TODO: implement shared 3AFC target mask in pages/_shared_3afc_student.py."
    )


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
    """TODO (student): Reusable staircase state-update helper.

    Keep behavior consistent with `shared_student_apply_reversal_update`.
    """
    raise NotImplementedError(
        "Student TODO: implement shared 3AFC staircase state update in "
        "pages/_shared_3afc_student.py."
    )


def shared_student_estimate_threshold_from_reversals(
    *, reversals: list[float], fallback_level: float, tail_count: int = 4
) -> float:
    """TODO (student): Estimate threshold using trailing reversal values.

    Recommended behavior:
        - If enough reversals exist, average last `tail_count` values.
        - Otherwise return `fallback_level`.
    """
    raise NotImplementedError(
        "Student TODO: implement shared 3AFC reversal-threshold estimate in "
        "pages/_shared_3afc_student.py."
    )


def shared_student_compute_recent_accuracy(history: list[dict], window: int = 12) -> float:
    """TODO (student): Compute trailing percent-correct.

    Recommended output:
        Percent value in range `[0, 100]`.
    """
    raise NotImplementedError(
        "Student TODO: implement shared 3AFC recent accuracy in pages/_shared_3afc_student.py."
    )


def shared_student_validate_audio_params(*, amplitude: float, stimulus_value: float) -> bool:
    """TODO (student): Shared audio-parameter validation.

    Inputs:
        amplitude: normalized loudness scalar.
        stimulus_value: test-specific numeric value (for example gap, dB delta, Hz delta).

    Returns:
        `True` when values are safe/valid; otherwise `False`.
    """
    raise NotImplementedError(
        "Student TODO: implement shared 3AFC audio validation in pages/_shared_3afc_student.py."
    )


def shared_student_plot_staircase_with_threshold(
    *, history: list[dict], threshold: float, y_label: str, title: str
) -> None:
    """TODO (student): Wrapper for staircase plot with threshold annotation.

    Recommended approach:
        Call `shared_student_plot_staircase(...)` internally to avoid duplicated code.
    """
    raise NotImplementedError(
        "Student TODO: implement shared 3AFC staircase wrapper in pages/_shared_3afc_student.py."
    )
