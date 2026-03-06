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
    ],
)

adaptive = init_adaptive_state(
    "amplitude",
    start_level=3.0,
    min_level=0.2,
    max_level=20.0,
    initial_step=1.0,
    min_step=0.1,
    max_reversals=8,
)
trial = get_or_create_trial("amplitude")
current_delta_db = float(adaptive["current_level"])
feedback_key = "amplitude_last_feedback"

with st.container(border=True):
    st.subheader("3AFC Trial")
    baseline_amplitude = st.slider(
        "Reference amplitude",
        min_value=0.08,
        max_value=0.6,
        value=0.30,
        step=0.01,
        key="amp_reference",
    )
    reference_hz = st.number_input(
        "Reference tone frequency (Hz)",
        min_value=200,
        max_value=4000,
        value=1000,
        step=10,
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
                duration_s=0.65,
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
    choice = st.radio("Which interval was louder?", [1, 2, 3], horizontal=True, key="amp_choice")
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
            level_used=current_delta_db,
            is_correct=is_correct,
            chosen_index=chosen_idx,
            target_index=int(trial["target_index"]),
        )
        advance_trial("amplitude")
        st.session_state[feedback_key] = "correct" if is_correct else "incorrect"
        st.rerun()

    estimated_db = estimate_threshold(adaptive)
    history = adaptive["history"]
    recent_accuracy = 0.0
    if history:
        recent = history[-12:]
        recent_accuracy = 100.0 * statistics.mean([1.0 if item["correct"] else 0.0 for item in recent])
    col_1, col_2 = st.columns(2)
    col_1.metric("Estimated Threshold (dB)", f"{estimated_db:.2f}")
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

            trials = list(range(1, total_trials + 1))
            levels = [float(item["level"]) for item in history]
            correct = [bool(item["correct"]) for item in history]
            colors = ["#2E7D32" if item else "#C62828" for item in correct]

            fig, ax = plt.subplots(figsize=(8, 3.5))
            ax.plot(trials, levels, color="#1565C0", linewidth=1.6, label="Delta Level")
            ax.scatter(trials, levels, c=colors, s=25, alpha=0.9, label="Trial Response")
            ax.axhline(
                estimated_db,
                color="#6A1B9A",
                linestyle="--",
                linewidth=1.3,
                label=f"Estimated Threshold {estimated_db:.2f} dB",
            )
            ax.set_xlabel("Trial Number")
            ax.set_ylabel("Amplitude Delta (dB)")
            ax.set_title("Amplitude Discrimination Adaptive Staircase")
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
        placeholder="Environment noise, confidence, retries, discomfort limits, etc.",
    )
    if st.button("Save Result", type="primary", use_container_width=True):
        save_result(
            "amplitude",
            {
                "Adaptive Method": "3AFC 2-down/1-up",
                "Estimated Threshold (dB)": f"{estimated_db:.2f}",
                "Reference Frequency (Hz)": f"{reference_hz}",
                "Reference Amplitude": f"{baseline_amplitude:.2f}",
                "Total Trials": f"{len(adaptive['history'])}",
                "Notes": notes.strip() or "None",
            },
        )
        st.success("Amplitude threshold result saved.")
    if st.button("Restart Adaptive Test", use_container_width=True):
        reset_adaptive_state("amplitude")
        st.session_state.pop(feedback_key, None)
        st.rerun()

render_saved_result("amplitude")
