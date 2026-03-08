import streamlit as st

from utils.adaptive_3afc import (
    estimate_threshold,
    get_or_create_trial,
    init_adaptive_state,
    reset_adaptive_state,
)
from utils.audio_tools import single_tone_wav
from utils.test_config import load_test_config
from utils.three_afc import (
    render_completion_summary,
    render_feedback,
    render_recent_accuracy_metric,
    render_staircase_plot,
    submit_3afc_response,
)
from utils.ui import (
    render_instructions,
    render_page_header,
)

st.set_page_config(
    page_title="Amplitude Threshold Test",
    layout="wide",
    initial_sidebar_state="collapsed",
)

render_page_header(
    "Amplitude Threshold Test",
    "3AFC adaptive test: identify the interval with higher amplitude.",
    "amplitude",
)

render_instructions(
    "How To Run This Test",
    (
        "You will hear three tones. One tone is slightly louder than the other two. "
        "Select the louder interval in each trial."
    ),
    [
        "Keep system volume fixed and only use in-app playback controls.",
        "Answer every trial even when unsure (forced choice).",
        "Adaptive step sizes shrink after reversals to stabilize the threshold.",
        "After finishing, recreate the staircase plot from trial history as a lab task.",
    ],
)

config = load_test_config()
cfg = config["amplitude_discrimination"]


def student_build_amplitude_intervals_audio(
    *,
    baseline_amplitude: float,
    delta_db: float,
    reference_hz: int,
    target_index: int,
) -> list[bytes]:
    """TODO (student): Build one 3AFC trial audio set for amplitude discrimination.

    Why this function exists:
        Each trial needs exactly three candidate sounds with one target interval.
        This function packages trial generation so the page can remain focused on UI
        and adaptive logic, while students practice controlled stimulus design.

    Inputs:
        baseline_amplitude: Reference amplitude for non-target intervals.
        delta_db: Loudness increment in decibels for the target interval.
        reference_hz: Tone frequency used for all intervals.
        target_index: Index (0, 1, or 2) of the louder interval.

    Output:
        A list of exactly 3 WAV byte payloads in interval order.

    Required behavior:
        - Convert `delta_db` to an amplitude ratio.
        - Build 3 tones at `reference_hz`.
        - Use baseline amplitude for two intervals.
        - Use louder amplitude for `target_index`.
        - Return WAV bytes compatible with `st.audio`.
    """
    raise NotImplementedError("Student TODO: implement 3-interval amplitude audio builder.")


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
    """TODO (student): Apply one 2-down/1-up staircase update step.

    Why this function exists:
        Adaptive thresholding is the core psychophysics concept in this test. This
        function controls whether the next trial becomes harder or easier based on
        current correctness and streak state.

    Inputs:
        current_level: Current stimulus level (delta dB).
        step: Current step size.
        is_correct: Whether current response is correct.
        correct_streak: Number of consecutive correct responses before this trial.
        down_n: Correct responses required to step down (usually 2).
        min_level: Lower bound for difficulty level.
        max_level: Upper bound for difficulty level.

    Output:
        `(next_level, next_correct_streak)` after one response update.

    Required behavior:
        - Correct: increment streak and step down only when streak reaches `down_n`.
        - Incorrect: reset streak and step up immediately.
        - Clamp `next_level` to `[min_level, max_level]`.
    """
    raise NotImplementedError("Student TODO: implement reversal step update.")


def student_plot_staircase(history: list[dict], threshold: float, y_label: str, title: str) -> None:
    """TODO (student): Plot trial-by-trial staircase values with matplotlib.

    Why this function exists:
        Visualizing the staircase helps students debug response behavior and justify
        the final threshold estimate in reports.

    Plot requirements:
        - X-axis: trial index/order.
        - Y-axis: level value used each trial.
        - Encode correct/incorrect responses with distinct markers or colors.
        - Draw threshold as a horizontal dashed line.
        - Add axis labels, title, and readable legend.
    """
    raise NotImplementedError("Student TODO: implement staircase plotting.")


def student_build_three_interval_targets(*, target_index: int) -> list[bool]:
    """TODO (student): Build a boolean mask identifying the target interval.

    Why this function exists:
        A compact mask such as `[False, True, False]` is useful for checking trial
        correctness, generating clips, and testing without hard-coding interval logic.
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
    """TODO (student): State-update helper for staircase level and streak.

    Why this function exists:
        This is a modular alternative to `student_apply_reversal_update`. You can
        implement one in terms of the other to avoid duplicated logic.
    """
    raise NotImplementedError("Student TODO: implement staircase state update.")


def student_estimate_threshold_from_reversals(
    *, reversals: list[float], fallback_level: float, tail_count: int = 4
) -> float:
    """TODO (student): Estimate threshold from recent reversal points.

    Why this function exists:
        Reversals approximate where performance transitions occur. Averaging the
        trailing reversals gives a stable threshold estimate at test completion.
    """
    raise NotImplementedError("Student TODO: implement reversal-threshold estimate.")


def student_compute_recent_accuracy(history: list[dict], window: int = 12) -> float:
    """TODO (student): Compute recent rolling accuracy from trial history.

    Why this function exists:
        Recent accuracy is a quick quality-control metric. It indicates whether the
        staircase is hovering near threshold (instead of being too easy/hard).
    """
    raise NotImplementedError("Student TODO: implement recent accuracy metric.")


def student_validate_audio_params(*, amplitude: float, frequency_hz: int) -> bool:
    """TODO (student): Validate parameters before generating amplitude stimuli.

    Minimum checks:
        - `amplitude` in (0, 1].
        - `frequency_hz` in a sensible audible range (for example 20..20000).
    """
    raise NotImplementedError("Student TODO: implement audio validation.")


def student_plot_staircase_with_threshold(
    *, history: list[dict], threshold: float, y_label: str, title: str
) -> None:
    """TODO (student): Convenience wrapper that draws staircase plus threshold.

    Why this function exists:
        This keeps plotting calls consistent across 3AFC pages and can internally
        call `student_plot_staircase` to avoid repeated plotting boilerplate.
    """
    raise NotImplementedError("Student TODO: implement staircase plotting helper.")


with st.expander("Assignment TODOs (Edit This Page)"):
    st.markdown(
        "- Implement `student_build_amplitude_intervals_audio`.\n"
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
    "How these functions connect: generate 3-interval audio -> collect response -> "
    "update staircase/reversals -> estimate threshold -> compute accuracy -> plot results."
)

adaptive = init_adaptive_state(
    "amplitude",
    start_level=float(cfg["adaptive"]["start_level"]),
    min_level=float(cfg["adaptive"]["min_level"]),
    max_level=float(cfg["adaptive"]["max_level"]),
    initial_step=float(cfg["adaptive"]["initial_step"]),
    min_step=float(cfg["adaptive"]["min_step"]),
    max_reversals=int(cfg["adaptive"]["max_reversals"]),
    down=int(cfg["adaptive"]["down"]),
)
trial = get_or_create_trial("amplitude")
current_delta_db = float(adaptive["current_level"])
feedback_key = "amplitude_last_feedback"

with st.container(border=True):
    st.subheader("3AFC Trial")
    baseline_amplitude = st.slider(
        "Reference amplitude",
        min_value=float(cfg["reference_amplitude"]["min"]),
        max_value=float(cfg["reference_amplitude"]["max"]),
        value=float(cfg["reference_amplitude"]["default"]),
        step=float(cfg["reference_amplitude"]["step"]),
        key="amp_reference",
    )
    reference_hz = st.number_input(
        "Reference tone frequency (Hz)",
        min_value=int(cfg["reference_frequency_hz"]["min"]),
        max_value=int(cfg["reference_frequency_hz"]["max"]),
        value=int(cfg["reference_frequency_hz"]["default"]),
        step=int(cfg["reference_frequency_hz"]["step"]),
    )
    ratio = 10 ** (current_delta_db / 20.0)
    target_amplitude = max(0.01, min(0.95, baseline_amplitude * ratio))
    st.caption(
        f"Current adaptive delta: {current_delta_db:.2f} dB | "
        f"Reversals: {len(adaptive['reversals'])}/{adaptive['max_reversals']}"
    )

    play_cols = st.columns(3)
    for idx in range(3):
        amplitude = target_amplitude if idx == trial["target_index"] else baseline_amplitude
        play_cols[idx].audio(
            single_tone_wav(
                frequency_hz=float(reference_hz),
                duration_s=float(cfg["tone_duration_s"]),
                amplitude=amplitude,
            ),
            format="audio/wav",
        )
        play_cols[idx].caption(f"Interval {idx + 1}")

with st.container(border=True):
    st.subheader("Respond")
    render_feedback(feedback_key)
    choice = st.radio("Which interval was louder?", [1, 2, 3], horizontal=True, key="amp_choice")
    submitted = st.button(
        "Submit Response",
        type="primary",
        width="stretch",
        disabled=adaptive["finished"],
    )
    if submitted and not adaptive["finished"]:
        submit_3afc_response(
            state_key="amplitude",
            adaptive=adaptive,
            trial=trial,
            level_used=current_delta_db,
            selected_interval=int(choice),
            feedback_key=feedback_key,
        )

    estimated_db = estimate_threshold(adaptive)
    history = adaptive["history"]
    col_1, col_2 = st.columns(2)
    col_1.metric("Estimated Threshold (dB)", f"{estimated_db:.2f}")
    with col_2:
        render_recent_accuracy_metric(history)

if adaptive["finished"]:
    with st.container(border=True):
        st.subheader("Adaptive Test Complete")
        st.success("Staircase finished. Final estimate and statistics are shown below.")
        history = adaptive["history"]
        render_completion_summary(adaptive, estimated_value=estimated_db, value_label="dB")
        render_staircase_plot(
            history=history,
            estimated_value=estimated_db,
            threshold_label="Estimated Threshold",
            y_label="Amplitude Delta (dB)",
            title="Amplitude Discrimination Adaptive Staircase",
        )

with st.container(border=True):
    st.subheader("Test Controls")
    if st.button("Restart Adaptive Test", width="stretch"):
        reset_adaptive_state("amplitude")
        st.session_state.pop(feedback_key, None)
        st.rerun()
