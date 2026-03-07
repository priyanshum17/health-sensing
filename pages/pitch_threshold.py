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
from utils.audio_tools import single_tone_wav
from utils.experiment_layout import (
    render_instructions,
    render_page_header,
    render_saved_result,
    save_result,
)
from utils.test_config import load_test_config

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
    last_feedback = st.session_state.get(feedback_key)
    if last_feedback == "correct":
        st.success("Previous response: Correct.")
    elif last_feedback == "incorrect":
        st.error("Previous response: Incorrect.")
    choice = st.radio("Which interval had the higher pitch?", [1, 2, 3], horizontal=True)
    submitted = st.button(
        "Submit Response",
        type="primary",
        use_container_width=True,
        disabled=adaptive["finished"],
    )
    if submitted and not adaptive["finished"]:
        chosen_idx = int(choice) - 1
        is_correct = chosen_idx == int(trial["target_index"])
        register_response(
            adaptive,
            level_used=current_delta_hz,
            is_correct=is_correct,
            chosen_index=chosen_idx,
            target_index=int(trial["target_index"]),
        )
        advance_trial("pitch_threshold")
        st.session_state[feedback_key] = "correct" if is_correct else "incorrect"
        st.rerun()

    estimated_hz = estimate_threshold(adaptive)
    history = adaptive["history"]
    recent_accuracy = 0.0
    if history:
        recent = history[-12:]
        recent_accuracy = 100.0 * statistics.mean([1.0 if item["correct"] else 0.0 for item in recent])
    col_1, col_2 = st.columns(2)
    col_1.metric("Estimated Delta Threshold (Hz)", f"{estimated_hz:.1f}")
    col_2.metric("Recent Accuracy (last 12)", f"{recent_accuracy:.1f}%")

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

            # LAB NOTE: Students should be able to reproduce this figure from history data.
            trials = list(range(1, total_trials + 1))
            levels = [float(item["level"]) for item in history]
            correct = [bool(item["correct"]) for item in history]
            colors = ["#2E7D32" if item else "#C62828" for item in correct]

            fig, ax = plt.subplots(figsize=(8, 3.5))
            ax.plot(trials, levels, color="#1565C0", linewidth=1.6, label="Delta Level")
            ax.scatter(trials, levels, c=colors, s=25, alpha=0.9, label="Trial Response")
            ax.axhline(
                estimated_hz,
                color="#6A1B9A",
                linestyle="--",
                linewidth=1.3,
                label=f"Estimated Threshold {estimated_hz:.1f} Hz",
            )
            ax.set_xlabel("Trial Number")
            ax.set_ylabel("Pitch Delta (Hz)")
            ax.set_title("Pitch Discrimination Adaptive Staircase")
            ax.grid(alpha=0.25)
            ax.legend(loc="best")
            st.pyplot(fig)
            plt.close(fig)
        except Exception:
            st.info("Matplotlib plot unavailable in this environment.")

with st.container(border=True):
    st.subheader("Save Result")
    notes = st.text_area(
        "Notes",
        placeholder="Headphones, fatigue effects, retries, room noise, etc.",
    )
    if st.button("Save Result", type="primary", use_container_width=True):
        save_result(
            "pitch_threshold",
            {
                "Adaptive Method": "3AFC 2-down/1-up",
                "Reference Frequency (Hz)": f"{reference_hz}",
                "Estimated Delta Threshold (Hz)": f"{estimated_hz:.1f}",
                "Total Trials": f"{len(adaptive['history'])}",
                "Reversals": f"{len(adaptive['reversals'])}",
                "Notes": notes.strip() or "None",
            },
        )
        st.success("Pitch discrimination result saved.")
    if st.button("Restart Adaptive Test", use_container_width=True):
        reset_adaptive_state("pitch_threshold")
        st.session_state.pop(feedback_key, None)
        st.rerun()

render_saved_result("pitch_threshold")
