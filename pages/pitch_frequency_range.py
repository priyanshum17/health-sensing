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
    "Use fine-grained controls to find your audible frequency range between 20 Hz and 20 kHz.",
    "pitch",
)

render_instructions(
    "How To Run This Test",
    (
        "Test tones from low to high frequencies with small frequency steps. Keep "
        "system volume fixed and use a quiet environment."
    ),
    [
        "Use the slider for quick sweeps and number input for exact frequencies.",
        "Increase frequency until you can no longer hear it reliably.",
        "Record the highest clearly audible frequency.",
    ],
)


def format_frequency_hz(frequency_hz: int) -> str:
    """Format frequency as Hz under 1 kHz and kHz above 1 kHz."""
    if frequency_hz < 1000:
        return f"{frequency_hz} Hz"
    return f"{frequency_hz / 1000:.2f} kHz"

with st.container(border=True):
    st.subheader("Tone Playback")
    frequency_hz = st.number_input(
        "Exact test frequency (Hz)",
        min_value=20,
        max_value=20000,
        value=4000,
        step=1,
        key="pitch_playback_input",
    )
    amplitude = st.slider(
        "Playback amplitude",
        min_value=0.05,
        max_value=0.8,
        value=0.35,
        step=0.05,
    )
    st.audio(single_tone_wav(frequency_hz=frequency_hz, amplitude=amplitude), format="audio/wav")
    st.caption(f"Current test tone: {format_frequency_hz(int(frequency_hz))}")

with st.container(border=True):
    st.subheader("Save Result")
    col_1, col_2 = st.columns(2)
    lowest_audible = col_1.number_input(
        "Lowest audible frequency (Hz)",
        min_value=20,
        max_value=20000,
        value=20,
        step=1,
    )
    highest_audible = col_2.number_input(
        "Highest audible frequency (Hz)",
        min_value=20,
        max_value=20000,
        value=int(frequency_hz),
        step=1,
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
                    "Lowest Audible": format_frequency_hz(int(lowest_audible)),
                    "Highest Audible": format_frequency_hz(int(highest_audible)),
                    "Range Width": format_frequency_hz(int(bandwidth)),
                    "Notes": notes.strip() or "None",
                },
            )
            st.success("Pitch range result saved.")

render_saved_result("pitch")
