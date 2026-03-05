import statistics

import streamlit as st

from utils.audio_tools import two_tone_gap_wav
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
    "Compare two same-frequency tones and find the smallest detectable loudness difference.",
    "amplitude",
)

render_instructions(
    "How To Run This Test",
    (
        "The first tone is baseline amplitude and the second tone is louder or "
        "quieter. Reduce amplitude difference until discrimination becomes unreliable."
    ),
    [
        "Keep device volume fixed for all trials.",
        "Repeat at three baseline levels: quiet, normal, and moderately loud.",
        "Record the smallest detectable difference in dB for each level.",
    ],
)

baseline_map = {
    "Quiet": 0.18,
    "Normal": 0.35,
    "Moderately Loud": 0.55,
}

with st.container(border=True):
    st.subheader("Tone Comparison Playback")
    baseline_label = st.radio("Baseline level", list(baseline_map.keys()), horizontal=True)
    baseline_amplitude = baseline_map[baseline_label]
    delta_db = st.slider(
        "Amplitude difference (dB)",
        min_value=0.0,
        max_value=20.0,
        value=3.0,
        step=0.1,
    )
    direction = st.radio("Second tone is", ["Louder", "Quieter"], horizontal=True)

    ratio = 10 ** (delta_db / 20.0)
    second_amplitude = baseline_amplitude * ratio if direction == "Louder" else baseline_amplitude / ratio
    second_amplitude = max(0.01, min(0.95, second_amplitude))

    st.audio(
        two_tone_gap_wav(
            frequency_hz=440.0,
            gap_ms=150,
            amplitude_1=baseline_amplitude,
            amplitude_2=second_amplitude,
        ),
        format="audio/wav",
    )

    metric_col_1, metric_col_2 = st.columns(2)
    metric_col_1.metric("Baseline Amplitude", f"{baseline_amplitude:.2f}")
    metric_col_2.metric("Second Tone Amplitude", f"{second_amplitude:.2f}")

with st.container(border=True):
    st.subheader("Record Thresholds")
    col_1, col_2, col_3 = st.columns(3)
    quiet_db = col_1.number_input("Quiet threshold (dB)", min_value=0.0, max_value=30.0, value=3.0, step=0.1)
    normal_db = col_2.number_input("Normal threshold (dB)", min_value=0.0, max_value=30.0, value=2.0, step=0.1)
    loud_db = col_3.number_input("Moderately loud threshold (dB)", min_value=0.0, max_value=30.0, value=1.5, step=0.1)

    avg_threshold = statistics.mean([quiet_db, normal_db, loud_db])
    st.metric("Average Threshold (dB)", f"{avg_threshold:.2f}")

    notes = st.text_area(
        "Notes",
        placeholder="Environment noise, confidence, retries, discomfort limits, etc.",
    )
    if st.button("Save Result", type="primary", use_container_width=True):
        save_result(
            "amplitude",
            {
                "Quiet Threshold (dB)": f"{quiet_db:.1f}",
                "Normal Threshold (dB)": f"{normal_db:.1f}",
                "Moderately Loud Threshold (dB)": f"{loud_db:.1f}",
                "Average Threshold (dB)": f"{avg_threshold:.2f}",
                "Notes": notes.strip() or "None",
            },
        )
        st.success("Amplitude threshold result saved.")

render_saved_result("amplitude")
