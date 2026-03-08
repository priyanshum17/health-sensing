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


def student_tone_preset(
    *,
    level: str,
    default_frequency_hz: int,
) -> tuple[int, float]:
    """TODO: convert a difficulty label to `(frequency_hz, amplitude)` values.

    If the label is missing or unknown, return `(default_frequency_hz, default_amplitude)`
    (from config). Make sure the returned values lie within the configured bounds.
    """
    raise NotImplementedError("Not implemented yet; follow the docstring guidance.")


def student_estimate_audible_bounds(
    *,
    probe_history_hz: list[int],
    heard_flags: list[bool],
) -> tuple[int, int]:
    """TODO: convert probe history into lower and upper heard bounds.

    Identify frequencies marked `True` in `heard_flags` and return their min and
    max. If no tones were heard, return safe fallback values (for example the
    default frequency).
    """
    raise NotImplementedError("Not implemented yet; follow the docstring guidance.")


def student_validate_audio_params(*, frequency_hz: int, amplitude: float) -> bool:
    """TODO: validate frequency and amplitude before synthesis.

    Return `True` when `frequency_hz` and `amplitude` fall within the config limits,
    otherwise `False`.
    """
    raise NotImplementedError("Not implemented yet; follow the docstring guidance.")


with st.expander("Assignment TODOs (Edit This Page)"):
    st.markdown(
        "- Implement `student_tone_preset` to create easy/medium/hard probe tones.\n"
        "- Implement `student_estimate_audible_bounds` using probe results.\n"
        "- Implement `student_validate_audio_params`."
    )

st.caption(
    "How these functions connect: choose preset start values -> validate playback params "
    "-> summarize heard/not-heard probes into final audible bounds."
)

try:
    preset_hz, preset_amp = student_tone_preset(
        level="easy",
        default_frequency_hz=int(cfg["frequency_hz"]["default"]),
    )
    estimated_low, estimated_high = student_estimate_audible_bounds(
        probe_history_hz=[125, 250, 500, 1000],
        heard_flags=[True, True, True, False],
    )
except NotImplementedError as error:
    st.error(str(error))
    st.info("This page is locked until the student TODO functions are implemented.")
    st.stop()

if not (int(cfg["frequency_hz"]["min"]) <= int(preset_hz) <= int(cfg["frequency_hz"]["max"])):
    st.error("`student_tone_preset` returned out-of-range frequency.")
    st.stop()
if not (0.0 < float(preset_amp) <= 1.0):
    st.error("`student_tone_preset` returned invalid amplitude.")
    st.stop()
if int(estimated_low) > int(estimated_high):
    st.error("`student_estimate_audible_bounds` returned invalid bounds.")
    st.stop()
if not student_validate_audio_params(frequency_hz=int(preset_hz), amplitude=float(preset_amp)):
    st.error("`student_validate_audio_params` returned invalid result.")
    st.stop()

with st.container(border=True):
    st.subheader("Preset And Bounds Check")
    level = st.selectbox("Difficulty preset", ["easy", "medium", "hard"])
    preset_hz, preset_amp = student_tone_preset(
        level=level,
        default_frequency_hz=int(cfg["frequency_hz"]["default"]),
    )
    col_1, col_2 = st.columns(2)
    col_1.metric("Preset Frequency", f"{int(preset_hz)} Hz")
    col_2.metric("Preset Amplitude", f"{float(preset_amp):.2f}")
    st.caption(
        f"Example estimated bounds from sample probes: {int(estimated_low)} Hz to "
        f"{int(estimated_high)} Hz"
    )

with st.container(border=True):
    st.subheader("Tone Playback")
    frequency_hz = st.number_input(
        "Exact test frequency (Hz)",
        min_value=int(cfg["frequency_hz"]["min"]),
        max_value=int(cfg["frequency_hz"]["max"]),
        value=int(preset_hz),
        step=int(cfg["frequency_hz"]["step"]),
        key="pitch_playback_input",
    )
    amplitude = st.slider(
        "Playback amplitude",
        min_value=float(cfg["playback_amplitude"]["min"]),
        max_value=float(cfg["playback_amplitude"]["max"]),
        value=float(preset_amp),
        step=float(cfg["playback_amplitude"]["step"]),
    )
    st.audio(single_tone_wav(frequency_hz=frequency_hz, amplitude=amplitude), format="audio/wav")
    st.caption(f"Current test tone: {format_frequency_hz(int(frequency_hz))}")
