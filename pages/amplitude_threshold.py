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
    """TODO (student): Build 3 interval audio clips for amplitude discrimination.

    Requirements:
        - Return exactly 3 WAV clips.
        - Two intervals at baseline amplitude.
        - One interval at louder target amplitude derived from `delta_db`.
    """
    ratio = 10 ** (delta_db / 20.0)
    target_amplitude = max(0.01, min(0.95, baseline_amplitude * ratio))
    clips: list[bytes] = []
    for idx in range(3):
        amp = target_amplitude if idx == target_index else baseline_amplitude
        clips.append(
            single_tone_wav(
                frequency_hz=float(reference_hz),
                duration_s=float(cfg["tone_duration_s"]),
                amplitude=amp,
            )
        )
    return clips


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
    """TODO (student): Apply one staircase update for amplitude thresholding.

    Requirements:
        - Implement 2-down/1-up style update.
        - Return `(next_level, next_correct_streak)`.
        - Clamp level to bounds.
    """
    next_streak = correct_streak
    next_level = current_level
    if is_correct:
        next_streak += 1
        if next_streak >= down_n:
            next_level = current_level - step
            next_streak = 0
    else:
        next_streak = 0
        next_level = current_level + step
    next_level = max(min_level, min(max_level, next_level))
    return float(next_level), int(next_streak)


def student_plot_staircase(history: list[dict], threshold: float, y_label: str, title: str) -> None:
    """TODO (student): Plot staircase history with matplotlib."""
    import matplotlib.pyplot as plt

    trials = list(range(1, len(history) + 1))
    levels = [float(item["level"]) for item in history]
    correct = [bool(item["correct"]) for item in history]
    colors = ["#2E7D32" if item else "#C62828" for item in correct]

    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.plot(trials, levels, color="#1565C0", linewidth=1.6, label="Level")
    ax.scatter(trials, levels, c=colors, s=25, alpha=0.9, label="Trial Response")
    ax.axhline(threshold, color="#6A1B9A", linestyle="--", linewidth=1.3, label="Threshold")
    ax.set_xlabel("Trial Number")
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.grid(alpha=0.25)
    ax.legend(loc="best")
    st.pyplot(fig)
    plt.close(fig)


with st.expander("Assignment TODOs (Edit This Page)"):
    st.markdown(
        "- Implement `student_build_amplitude_intervals_audio`.\n"
        "- Implement `student_apply_reversal_update`.\n"
        "- Implement `student_plot_staircase`."
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
