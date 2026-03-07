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
    page_title="Pitch Discrimination Threshold Test",
    layout="wide",
)

render_page_header(
    "Pitch Discrimination Threshold Test",
    "3AFC adaptive test: identify the interval with higher pitch.",
    "pitch_threshold",
)

render_instructions(
    "How To Run This Test",
    (
        "You will hear three tones at the same level. One tone has a slightly higher "
        "frequency than the reference. Select that interval each trial."
    ),
    [
        "Keep volume fixed and use headphones if possible.",
        "Answer every trial even when unsure (forced choice).",
        "The adaptive staircase estimates your minimum detectable frequency increment.",
        "After finishing, recreate the staircase plot from trial history as a lab task.",
    ],
)

config = load_test_config()
cfg = config["pitch_discrimination"]

adaptive = init_adaptive_state(
    "pitch_threshold",
    start_level=float(cfg["adaptive"]["start_level"]),
    min_level=float(cfg["adaptive"]["min_level"]),
    max_level=float(cfg["adaptive"]["max_level"]),
    initial_step=float(cfg["adaptive"]["initial_step"]),
    min_step=float(cfg["adaptive"]["min_step"]),
    max_reversals=int(cfg["adaptive"]["max_reversals"]),
    down=int(cfg["adaptive"]["down"]),
)
trial = get_or_create_trial("pitch_threshold")
current_delta_hz = float(adaptive["current_level"])
feedback_key = "pitch_threshold_last_feedback"

with st.container(border=True):
    st.subheader("3AFC Trial")
    reference_hz = st.number_input(
        "Reference frequency (Hz)",
        min_value=int(cfg["reference_frequency_hz"]["min"]),
        max_value=int(cfg["reference_frequency_hz"]["max"]),
        value=int(cfg["reference_frequency_hz"]["default"]),
        step=int(cfg["reference_frequency_hz"]["step"]),
    )
    amplitude = st.slider(
        "Playback amplitude",
        min_value=float(cfg["playback_amplitude"]["min"]),
        max_value=float(cfg["playback_amplitude"]["max"]),
        value=float(cfg["playback_amplitude"]["default"]),
        step=float(cfg["playback_amplitude"]["step"]),
    )
    target_hz = min(20000.0, float(reference_hz) + current_delta_hz)
    st.caption(
        f"Current adaptive pitch delta: {current_delta_hz:.1f} Hz | "
        f"Target frequency: {target_hz:.1f} Hz"
    )
    st.caption(f"Reversals: {len(adaptive['reversals'])}/{adaptive['max_reversals']}")

    play_cols = st.columns(3)
    for idx in range(3):
        test_hz = target_hz if idx == trial["target_index"] else float(reference_hz)
        play_cols[idx].audio(
            single_tone_wav(
                frequency_hz=test_hz,
                duration_s=float(cfg["tone_duration_s"]),
                amplitude=amplitude,
            ),
            format="audio/wav",
        )
        play_cols[idx].caption(f"Interval {idx + 1}")

with st.container(border=True):
    st.subheader("Respond")
    render_feedback(feedback_key)
    choice = st.radio("Which interval had the higher pitch?", [1, 2, 3], horizontal=True)
    submitted = st.button(
        "Submit Response",
        type="primary",
        width="stretch",
        disabled=adaptive["finished"],
    )
    if submitted and not adaptive["finished"]:
        submit_3afc_response(
            state_key="pitch_threshold",
            adaptive=adaptive,
            trial=trial,
            level_used=current_delta_hz,
            selected_interval=int(choice),
            feedback_key=feedback_key,
        )

    estimated_hz = estimate_threshold(adaptive)
    history = adaptive["history"]
    col_1, col_2 = st.columns(2)
    col_1.metric("Estimated Delta Threshold (Hz)", f"{estimated_hz:.1f}")
    with col_2:
        render_recent_accuracy_metric(history)

if adaptive["finished"]:
    with st.container(border=True):
        st.subheader("Adaptive Test Complete")
        st.success("Staircase finished. Final estimate and statistics are shown below.")
        history = adaptive["history"]
        render_completion_summary(adaptive, estimated_value=estimated_hz, value_label="Hz")
        render_staircase_plot(
            history=history,
            estimated_value=estimated_hz,
            threshold_label="Estimated Threshold",
            y_label="Pitch Delta (Hz)",
            title="Pitch Discrimination Adaptive Staircase",
        )

with st.container(border=True):
    st.subheader("Test Controls")
    if st.button("Restart Adaptive Test", width="stretch"):
        reset_adaptive_state("pitch_threshold")
        st.session_state.pop(feedback_key, None)
        st.rerun()
