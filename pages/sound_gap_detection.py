import statistics

import streamlit as st

from utils.adaptive_3afc import (
    advance_trial,
    estimate_threshold,
    get_or_create_trial,
    init_adaptive_state,
    register_response,
    reset_adaptive_state,
)
from utils.audio_tools import noise_burst_with_gap_wav
from utils.experiment_layout import (
    render_instructions,
    render_page_header,
)
from utils.test_config import load_test_config

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
    last_feedback = st.session_state.get(feedback_key)
    if last_feedback == "correct":
        st.success("Previous response: Correct.")
    elif last_feedback == "incorrect":
        st.error("Previous response: Incorrect.")
    choice = st.radio("Which interval had the gap?", [1, 2, 3], horizontal=True)
    submitted = st.button(
        "Submit Response",
        type="primary",
        width="stretch",
        disabled=adaptive["finished"],
    )
    if submitted and not adaptive["finished"]:
        chosen_idx = int(choice) - 1
        is_correct = chosen_idx == int(trial["target_index"])
        register_response(
            adaptive,
            level_used=current_gap_ms,
            is_correct=is_correct,
            chosen_index=chosen_idx,
            target_index=int(trial["target_index"]),
        )
        advance_trial("gap")
        st.session_state[feedback_key] = "correct" if is_correct else "incorrect"
        st.rerun()

    estimated_gap = estimate_threshold(adaptive)
    st.metric("Estimated Gap Threshold (ms)", f"{estimated_gap:.2f}")

if adaptive["finished"]:
    with st.container(border=True):
        st.subheader("Adaptive Test Complete")
        st.success("Staircase finished. Final estimate and statistics are shown below.")
        history = adaptive["history"]
        total_trials = len(history)
        accuracy = 100.0 * statistics.mean([1.0 if item["correct"] else 0.0 for item in history])
        col_1, col_2, col_3 = st.columns(3)
        col_1.metric("Total Trials", f"{total_trials}")
        col_2.metric("Overall Accuracy", f"{accuracy:.1f}%")
        col_3.metric("Reversals", f"{len(adaptive['reversals'])}")

        try:
            import matplotlib.pyplot as plt

            # LAB NOTE: Students can rebuild this plot from adaptive["history"] manually.
            trials = list(range(1, total_trials + 1))
            levels = [float(item["level"]) for item in history]
            correct = [bool(item["correct"]) for item in history]
            colors = ["#2E7D32" if item else "#C62828" for item in correct]

            fig, ax = plt.subplots(figsize=(8, 3.5))
            ax.plot(trials, levels, color="#1565C0", linewidth=1.6, label="Gap Level")
            ax.scatter(trials, levels, c=colors, s=25, alpha=0.9, label="Trial Response")
            ax.axhline(
                estimated_gap,
                color="#6A1B9A",
                linestyle="--",
                linewidth=1.3,
                label=f"Estimated Threshold {estimated_gap:.2f} ms",
            )
            ax.set_xlabel("Trial Number")
            ax.set_ylabel("Gap (ms)")
            ax.set_title("Gap Detection Adaptive Staircase")
            ax.grid(alpha=0.25)
            ax.legend(loc="best")
            st.pyplot(fig)
            plt.close(fig)
        except Exception:
            st.info("Matplotlib plot unavailable in this environment.")

with st.container(border=True):
    st.subheader("Test Controls")
    if st.button("Restart Adaptive Test", width="stretch"):
        reset_adaptive_state("gap")
        st.session_state.pop(feedback_key, None)
        st.rerun()
