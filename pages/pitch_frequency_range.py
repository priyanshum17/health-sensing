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
    """TODO (student): Map a difficulty label to a safe tone preset.

    Why this function exists:
        The page lets users start from easy/medium/hard settings instead of manual
        tuning every time. This function is the single source of truth for those
        presets, so all users begin with predictable frequency and loudness values.

    Inputs:
        level: Difficulty string in {"easy", "medium", "hard"}.
        default_frequency_hz: Fallback value from config.

    Output:
        `(frequency_hz, amplitude)` where:
        - `frequency_hz` is an integer in the app range [20, 20000].
        - `amplitude` is a float in (0.0, 1.0].

    Suggested strategy:
        - Define one preset per level with progressively harder frequencies.
        - Use `default_frequency_hz` as fallback for unknown or missing level.
        - Clamp outputs to legal bounds before returning.
    """
    raise NotImplementedError("Student TODO: implement difficulty preset.")


def student_estimate_audible_bounds(
    *,
    probe_history_hz: list[int],
    heard_flags: list[bool],
) -> tuple[int, int]:
    """TODO (student): Estimate audible low/high bounds from probe history.

    Why this function exists:
        A raw list of heard/not-heard responses is hard to interpret quickly. This
        helper summarizes probe data into a clean range students can report in lab
        writeups and compare across participants.

    Inputs:
        probe_history_hz: Tested frequencies in Hz.
        heard_flags: Boolean responses aligned by index (`True` if heard).

    Output:
        `(lowest_heard_hz, highest_heard_hz)` as integer bounds.

    Required behavior:
        - Treat the two lists as aligned trial history.
        - Extract frequencies where `heard_flags[i]` is `True`.
        - Return min/max of heard frequencies.
        - For empty input or no heard tones, return safe fallback bounds.
    """
    raise NotImplementedError("Student TODO: implement audible-bound estimation.")


def student_validate_audio_params(*, frequency_hz: int, amplitude: float) -> bool:
    """TODO (student): Validate frequency/amplitude before waveform generation.

    Why this function exists:
        Audio synthesis should fail early for illegal values. This keeps the UI
        stable and teaches students to guard data before expensive operations.

    Inputs:
        frequency_hz: Tone frequency candidate.
        amplitude: Loudness scalar.

    Output:
        `True` if parameters are inside legal ranges; otherwise `False`.

    Minimum validation:
        - Frequency in [20, 20000].
        - Amplitude strictly greater than 0 and at most 1.
    """
    raise NotImplementedError("Student TODO: implement audio parameter validation.")


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
