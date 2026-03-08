import streamlit as st

from utils.adaptive_3afc import (
    estimate_threshold,
    get_or_create_trial,
    init_adaptive_state,
    reset_adaptive_state,
)
from utils.audio_tools import noise_burst_with_gap_wav
from utils.test_config import load_test_config
from utils.three_afc import (
    render_completion_summary,
    render_feedback,
    render_staircase_plot,
    submit_3afc_response,
)
from utils.ui import (
    render_instructions,
    render_page_header,
)

st.set_page_config(
    page_title="Sound Gap Detection Test",
    layout="wide",
)

render_page_header(
    "Sound Gap Detection Test",
    "3AFC adaptive test: select which interval contains a silent gap.",
    "gap",
)

render_instructions(
    "How To Run This Test",
    (
        "You will hear three short noise bursts. Exactly one burst contains a "
        "centered silence gap. Pick the correct interval every trial."
    ),
    [
        "Use all three play buttons to compare candidates before answering.",
        "Select the interval with the gap, then submit your response.",
        "The adaptive staircase will shrink or expand the gap based on performance.",
        "After finishing, recreate the staircase plot from the trial history as a lab exercise.",
    ],
)

config = load_test_config()
cfg = config["gap_detection"]


def student_build_gap_intervals_audio(
    *,
    gap_ms: float,
    amplitude: float,
    target_index: int,
    seed: int,
) -> list[bytes]:
    """TODO (student): Build one 3AFC trial audio set for gap detection.

    Why this function exists:
        The listener must compare three intervals where only one contains the silent
        gap. Centralizing generation here makes stimuli reproducible and easy to test.

    Inputs:
        gap_ms: Gap duration for the target interval.
        amplitude: Playback amplitude for all intervals.
        target_index: Index (0, 1, 2) containing the gap.
        seed: Seed used so generated noise bursts are deterministic.

    Output:
        A list of exactly three WAV byte payloads.

    Required behavior:
        - Target interval gets `gap_ms`.
        - Other intervals get zero gap.
        - Keep amplitude consistent across all three clips.
        - Use deterministic seeds so repeated runs are reproducible.
    """
    raise NotImplementedError("Student TODO: implement 3-interval gap audio builder.")


def student_apply_reversal_update(
    *,
    current_level: float,
    step: float,
    is_correct: bool,
    correct_streak: int,
    down_n: int,
    min_level: float,
    max_level: float,
) -> tuple[float, int]:
    """TODO (student): Apply one 2-down/1-up update to gap level and streak.

    Why this function exists:
        Adaptive logic controls difficulty and converges toward threshold. Students
        implement the update rule directly to understand staircase mechanics.

    Inputs/outputs:
        Same semantics as the other 3AFC pages:
        return `(next_level, next_correct_streak)` with proper clamping.
    """
    raise NotImplementedError("Student TODO: implement reversal step update.")


def student_plot_staircase(history: list[dict], threshold: float, y_label: str, title: str) -> None:
    """TODO (student): Plot staircase history with matplotlib.

    Why this function exists:
        A visual staircase plot is required for analysis and makes reversal behavior
        obvious. It also helps verify your update logic is behaving correctly.

    Plot requirements:
        - X-axis: trial number.
        - Y-axis: tested gap level (ms).
        - Mark correct vs incorrect responses using different colors/markers.
        - Draw threshold as a horizontal dashed reference line.
    """
    raise NotImplementedError("Student TODO: implement staircase plotting.")


def student_build_three_interval_targets(*, target_index: int) -> list[bool]:
    """TODO (student): Return 3-element boolean target mask for interval selection.

    Example:
        `target_index=1` -> `[False, True, False]`.
    """
    raise NotImplementedError("Student TODO: implement 3AFC target mask builder.")


def student_update_staircase_state(
    *,
    current_level: float,
    step: float,
    is_correct: bool,
    correct_streak: int,
    down_n: int,
    min_level: float,
    max_level: float,
) -> tuple[float, int]:
    """TODO (student): Update staircase level and streak in a reusable helper.

    Tip:
        Keep this logic consistent with `student_apply_reversal_update` so both
        helpers produce identical behavior.
    """
    raise NotImplementedError("Student TODO: implement staircase state update.")


def student_estimate_threshold_from_reversals(
    *, reversals: list[float], fallback_level: float, tail_count: int = 4
) -> float:
    """TODO (student): Estimate threshold from final reversal values.

    Expected approach:
        - If enough reversals exist, average the last `tail_count`.
        - Otherwise return `fallback_level`.
    """
    raise NotImplementedError("Student TODO: implement reversal-threshold estimate.")


def student_compute_recent_accuracy(history: list[dict], window: int = 12) -> float:
    """TODO (student): Compute rolling percent-correct from recent trials.

    Expected output:
        Percentage in `[0, 100]` computed from up to `window` most recent trials.
    """
    raise NotImplementedError("Student TODO: implement recent accuracy metric.")


def student_validate_audio_params(*, amplitude: float, gap_ms: float) -> bool:
    """TODO (student): Validate parameters before generating gap stimuli.

    Minimum checks:
        - `amplitude` in (0, 1].
        - `gap_ms` non-negative and within realistic configured limits.
    """
    raise NotImplementedError("Student TODO: implement audio validation.")


def student_plot_staircase_with_threshold(
    *, history: list[dict], threshold: float, y_label: str, title: str
) -> None:
    """TODO (student): Wrapper that renders staircase with threshold annotation.

    Purpose:
        Keep plotting interface consistent across all 3AFC assignment pages.
    """
    raise NotImplementedError("Student TODO: implement staircase plotting helper.")


with st.expander("Assignment TODOs (Edit This Page)"):
    st.markdown(
        "- Implement `student_build_gap_intervals_audio`.\n"
        "- Implement `student_apply_reversal_update`.\n"
        "- Implement `student_plot_staircase`.\n"
        "- Implement `student_build_three_interval_targets`.\n"
        "- Implement `student_update_staircase_state`.\n"
        "- Implement `student_estimate_threshold_from_reversals`.\n"
        "- Implement `student_compute_recent_accuracy`.\n"
        "- Implement `student_validate_audio_params`.\n"
        "- Implement `student_plot_staircase_with_threshold`."
    )

st.caption(
    "How these functions connect: generate three noise intervals (one with gap) -> "
    "update adaptive staircase from responses -> estimate threshold from reversals -> plot."
)

adaptive = init_adaptive_state(
    "gap",
    start_level=float(cfg["adaptive"]["start_level"]),
    min_level=float(cfg["adaptive"]["min_level"]),
    max_level=float(cfg["adaptive"]["max_level"]),
    initial_step=float(cfg["adaptive"]["initial_step"]),
    min_step=float(cfg["adaptive"]["min_step"]),
    max_reversals=int(cfg["adaptive"]["max_reversals"]),
    down=int(cfg["adaptive"]["down"]),
)
trial = get_or_create_trial("gap")
current_gap_ms = float(adaptive["current_level"])
feedback_key = "gap_last_feedback"

with st.container(border=True):
    st.subheader("3AFC Trial")
    amplitude = st.slider(
        "Playback amplitude",
        min_value=float(cfg["playback"]["amplitude"]["min"]),
        max_value=float(cfg["playback"]["amplitude"]["max"]),
        value=float(cfg["playback"]["amplitude"]["default"]),
        step=float(cfg["playback"]["amplitude"]["step"]),
        key="gap_amplitude",
    )
    st.caption(
        f"Current adaptive gap level: {current_gap_ms:.2f} ms | "
        f"Reversals: {len(adaptive['reversals'])}/{adaptive['max_reversals']}"
    )
    play_cols = st.columns(3)
    for idx in range(3):
        gap_ms = current_gap_ms if idx == trial["target_index"] else 0.0
        wav_bytes = noise_burst_with_gap_wav(
            duration_s=float(cfg["playback"]["burst_duration_s"]),
            gap_ms=gap_ms,
            amplitude=amplitude,
            seed=trial["seed"] + idx,
        )
        play_cols[idx].audio(wav_bytes, format="audio/wav")
        play_cols[idx].caption(f"Interval {idx + 1}")

with st.container(border=True):
    st.subheader("Respond")
    render_feedback(feedback_key)
    choice = st.radio("Which interval had the gap?", [1, 2, 3], horizontal=True)
    submitted = st.button(
        "Submit Response",
        type="primary",
        width="stretch",
        disabled=adaptive["finished"],
    )
    if submitted and not adaptive["finished"]:
        submit_3afc_response(
            state_key="gap",
            adaptive=adaptive,
            trial=trial,
            level_used=current_gap_ms,
            selected_interval=int(choice),
            feedback_key=feedback_key,
        )

    estimated_gap = estimate_threshold(adaptive)
    st.metric("Estimated Gap Threshold (ms)", f"{estimated_gap:.2f}")

if adaptive["finished"]:
    with st.container(border=True):
        st.subheader("Adaptive Test Complete")
        st.success("Staircase finished. Final estimate and statistics are shown below.")
        history = adaptive["history"]
        render_completion_summary(adaptive, estimated_value=estimated_gap, value_label="ms")
        render_staircase_plot(
            history=history,
            estimated_value=estimated_gap,
            threshold_label="Estimated Threshold",
            y_label="Gap (ms)",
            title="Gap Detection Adaptive Staircase",
        )

with st.container(border=True):
    st.subheader("Test Controls")
    if st.button("Restart Adaptive Test", width="stretch"):
        reset_adaptive_state("gap")
        st.session_state.pop(feedback_key, None)
        st.rerun()
