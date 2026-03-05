import streamlit as st
from utils.home import render_experiment_tile

st.set_page_config(
    page_title="Human Sensory Limits",
    layout="wide"
)

st.title("Vision and Hearing Experiment Suite")
st.caption(
    "Objective: Test and record the sensing limits of a person to understand human sensory capabilities and limitations."
)

with st.container(border=True):
    st.subheader("Objective")
    st.write(
        "This assignment focuses on sight and hearing. For sight, you will measure "
        "greyscale resolution, angular field of view, and smallest noticeable size. "
        "For hearing, you will measure pitch frequency range, sound gap detection, "
        "and amplitude resolution."
    )

with st.container(border=True):
    st.subheader("Experiment Summary")
    metric_total, metric_vision, metric_hearing = st.columns(3)
    metric_total.metric("Total Experiments", 6)
    metric_vision.metric("Vision", 3)
    metric_hearing.metric("Hearing", 3)

with st.container(border=True):
    st.subheader("Sight Experiments")
    render_experiment_tile(
        title="Greyscale Resolution",
        description="Measure the smallest visible brightness difference and estimate bit resolution.",
        page_path="pages/greyscale_resolution.py",
        key="open_greyscale",
    )
    render_experiment_tile(
        title="Angular Field of View",
        description="Measure left, right, up, and down angle limits and compute horizontal/vertical FOV.",
        page_path="pages/angular_field_of_view.py",
        key="open_fov",
    )
    render_experiment_tile(
        title="Smallest Noticeable Size",
        description="Find line-size visibility threshold and compute angular resolution in arc minutes.",
        page_path="pages/smallest_noticeable_size.py",
        key="open_size",
    )

with st.container(border=True):
    st.subheader("Hearing Experiments")
    render_experiment_tile(
        title="Pitch Frequency Range",
        description="Use tone playback to find the highest frequency still audible to you.",
        page_path="pages/pitch_frequency_range.py",
        key="open_pitch",
    )
    render_experiment_tile(
        title="Sound Gap Detection",
        description="Use tone-gap-tone playback to find the shortest noticeable silence gap.",
        page_path="pages/sound_gap_detection.py",
        key="open_gap",
    )
    render_experiment_tile(
        title="Amplitude Threshold",
        description="Compare two tones and find the smallest detectable amplitude change in dB.",
        page_path="pages/amplitude_threshold.py",
        key="open_amplitude",
    )
