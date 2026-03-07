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
