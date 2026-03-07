import streamlit as st

from utils.audio_tools import single_tone_wav
from utils.test_config import load_test_config
from utils.ui import (
    render_instructions,
    render_page_header,
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

config = load_test_config()
cfg = config["pitch_range"]


def format_frequency_hz(frequency_hz: int) -> str:
    """Format frequency as Hz under 1 kHz and kHz above 1 kHz."""
    if frequency_hz < 1000:
        return f"{frequency_hz} Hz"
    return f"{frequency_hz / 1000:.2f} kHz"

with st.container(border=True):
    st.subheader("Tone Playback")
    frequency_hz = st.number_input(
        "Exact test frequency (Hz)",
        min_value=int(cfg["frequency_hz"]["min"]),
        max_value=int(cfg["frequency_hz"]["max"]),
        value=int(cfg["frequency_hz"]["default"]),
        step=int(cfg["frequency_hz"]["step"]),
        key="pitch_playback_input",
    )
    amplitude = st.slider(
        "Playback amplitude",
        min_value=float(cfg["playback_amplitude"]["min"]),
        max_value=float(cfg["playback_amplitude"]["max"]),
        value=float(cfg["playback_amplitude"]["default"]),
        step=float(cfg["playback_amplitude"]["step"]),
    )
    st.audio(single_tone_wav(frequency_hz=frequency_hz, amplitude=amplitude), format="audio/wav")
    st.caption(f"Current test tone: {format_frequency_hz(int(frequency_hz))}")
