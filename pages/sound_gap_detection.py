import streamlit as st

from utils.audio_tools import two_tone_gap_wav
from utils.experiment_layout import (
    render_instructions,
    render_page_header,
    render_saved_result,
    save_result,
)

st.set_page_config(
    page_title="Sound Gap Detection Test",
    layout="wide",
)

render_page_header(
    "Sound Gap Detection Test",
    "Find the shortest silence gap in a tone sequence that you can still notice.",
    "gap",
)

render_instructions(
    "How To Run This Test",
    (
        "Use a continuous-sounding tone pattern with a controlled silent interval in "
        "the middle. Reduce the gap until it becomes difficult to detect."
    ),
    [
        "Play tone-gap-tone clips while adjusting gap duration in milliseconds.",
        "Use repeated listening near your threshold region.",
        "Record the smallest reliably noticeable gap duration.",
    ],
)

with st.container(border=True):
    st.subheader("Gap Playback")
    frequency_hz = st.slider(
        "Tone frequency (Hz)",
        min_value=200,
        max_value=4000,
        value=1000,
        step=100,
    )
    gap_ms = st.slider(
        "Silence gap (ms)",
        min_value=0,
        max_value=120,
        value=20,
        step=1,
    )
    amplitude = st.slider(
        "Playback amplitude",
        min_value=0.05,
        max_value=0.8,
        value=0.35,
        step=0.05,
    )
    st.audio(
        two_tone_gap_wav(
            frequency_hz=frequency_hz,
            gap_ms=gap_ms,
            amplitude_1=amplitude,
            amplitude_2=amplitude,
        ),
        format="audio/wav",
    )

with st.container(border=True):
    st.subheader("Save Result")
    threshold_ms = st.number_input(
        "Smallest noticeable gap (ms)",
        min_value=0.0,
        max_value=500.0,
        value=float(gap_ms),
        step=0.5,
    )
    notes = st.text_area(
        "Notes",
        placeholder="Listening conditions, repeated trials, confidence level, etc.",
    )
    if st.button("Save Result", type="primary", use_container_width=True):
        save_result(
            "gap",
            {
                "Threshold Gap (ms)": f"{threshold_ms:.1f}",
                "Test Frequency (Hz)": f"{frequency_hz}",
                "Notes": notes.strip() or "None",
            },
        )
        st.success("Gap detection result saved.")

render_saved_result("gap")
