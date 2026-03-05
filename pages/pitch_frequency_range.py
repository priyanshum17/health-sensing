import streamlit as st

from utils.audio_tools import single_tone_wav
from utils.experiment_layout import (
    render_instructions,
    render_page_header,
    render_saved_result,
    save_result,
)

st.set_page_config(
    page_title="Pitch Frequency Range Test",
    layout="wide",
)

render_page_header(
    "Pitch Frequency Range Test",
    "Use tone playback to find your highest audible frequency between 20 Hz and 20 kHz.",
    "pitch",
)

render_instructions(
    "How To Run This Test",
    (
        "Test tones from low to high frequencies. Keep system volume fixed and use "
        "a quiet environment."
    ),
    [
        "Select a frequency with 100 Hz step size and play the test tone.",
        "Increase frequency until you can no longer hear it reliably.",
        "Record the highest clearly audible frequency.",
    ],
)

with st.container(border=True):
    st.subheader("Tone Playback")
    frequency_hz = st.slider(
        "Test frequency (Hz)",
        min_value=20,
        max_value=20000,
        value=4000,
        step=100,
    )
    amplitude = st.slider(
        "Playback amplitude",
        min_value=0.05,
        max_value=0.8,
        value=0.35,
        step=0.05,
    )
    st.audio(single_tone_wav(frequency_hz=frequency_hz, amplitude=amplitude), format="audio/wav")

with st.container(border=True):
    st.subheader("Save Result")
    col_1, col_2 = st.columns(2)
    lowest_audible = col_1.number_input(
        "Lowest audible frequency (Hz)",
        min_value=20,
        max_value=20000,
        value=20,
        step=100,
    )
    highest_audible = col_2.number_input(
        "Highest audible frequency (Hz)",
        min_value=20,
        max_value=20000,
        value=frequency_hz,
        step=100,
    )
    notes = st.text_area(
        "Notes",
        placeholder="Headphone/speaker used, room noise, retries, etc.",
    )
    if st.button("Save Result", type="primary", use_container_width=True):
        if highest_audible < lowest_audible:
            st.error("Highest audible frequency must be greater than or equal to lowest.")
        else:
            bandwidth = highest_audible - lowest_audible
            save_result(
                "pitch",
                {
                    "Lowest Audible (Hz)": f"{lowest_audible}",
                    "Highest Audible (Hz)": f"{highest_audible}",
                    "Range Width (Hz)": f"{bandwidth}",
                    "Notes": notes.strip() or "None",
                },
            )
            st.success("Pitch range result saved.")

render_saved_result("pitch")
