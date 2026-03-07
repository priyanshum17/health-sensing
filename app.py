import streamlit as st

from utils.ui import render_experiment_tile

st.set_page_config(
    page_title="Human Sensory Limits",
    layout="wide"
)

st.title("Vision and Hearing Experiment Suite")
st.caption(
    "Objective: Run standardized vision and hearing tasks to estimate sensory thresholds."
)

with st.container(border=True):
    st.subheader("Objective")
    st.write(
        "This assignment focuses on standardized psychophysics tasks. For vision, "
        "you will run a Pelli-style contrast task and a Tumbling-E resolution task. "
        "For hearing, you will run pitch range screening plus adaptive 3AFC tests for "
        "gap detection, amplitude discrimination, and pitch discrimination."
    )

with st.container(border=True):
    st.subheader("Experiment Summary")
    metric_total, metric_vision, metric_hearing = st.columns(3)
    metric_total.metric("Total Experiments", 6)
    metric_vision.metric("Vision", 2)
    metric_hearing.metric("Hearing", 4)

with st.container(border=True):
    st.subheader("Sight Experiments")
    render_experiment_tile(
        title="Contrast Sensitivity (Pelli-Style)",
        description=(
            "Estimate log contrast sensitivity using a standardized letter-contrast progression."
        ),
        page_path="pages/greyscale_resolution.py",
        key="open_greyscale",
    )
    render_experiment_tile(
        title="Visual Resolution (Tumbling E)",
        description="Use orientation judgments and compute MAR (minimum angle of resolution).",
        page_path="pages/smallest_noticeable_size.py",
        key="open_size",
    )

with st.container(border=True):
    st.subheader("Hearing Experiments")
    render_experiment_tile(
        title="Pitch Frequency Range",
        description="Screen audible low/high limits with fine frequency controls and direct input.",
        page_path="pages/pitch_frequency_range.py",
        key="open_pitch",
    )
    render_experiment_tile(
        title="Sound Gap Detection (3AFC Adaptive)",
        description=(
            "Find temporal gap threshold with a 3-alternative forced-choice adaptive staircase."
        ),
        page_path="pages/sound_gap_detection.py",
        key="open_gap",
    )
    render_experiment_tile(
        title="Amplitude Discrimination (3AFC Adaptive)",
        description="Estimate loudness discrimination threshold in dB with adaptive 3AFC trials.",
        page_path="pages/amplitude_threshold.py",
        key="open_amplitude",
    )
    render_experiment_tile(
        title="Pitch Discrimination (3AFC Adaptive)",
        description="Estimate the smallest detectable frequency increment above a reference tone.",
        page_path="pages/pitch_threshold.py",
        key="open_pitch_threshold",
    )
