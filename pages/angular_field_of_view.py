import streamlit as st

from utils.experiment_layout import (
    render_instructions,
    render_page_header,
    render_saved_result,
    save_result,
)

st.set_page_config(
    page_title="Angular Field of View Test",
    layout="wide",
)

render_page_header(
    "Angular Field of View Test",
    "Measure left, right, up, and down limits while keeping head position fixed.",
    "fov",
)

render_instructions(
    "How To Run This Test",
    (
        "Use a high-contrast visual marker and move it toward the edge of your "
        "visible field without tilting or rotating your head."
    ),
    [
        "Record disappearance angles in four directions: left, right, up, down.",
        "Eye movement is allowed, but keep your head stable.",
        "Compute horizontal FOV as left + right and vertical FOV as up + down.",
    ],
)

with st.container(border=True):
    st.subheader("Enter Directional Limits (Degrees)")
    col_1, col_2, col_3, col_4 = st.columns(4)
    left_deg = col_1.number_input("Left", min_value=0.0, max_value=180.0, value=70.0, step=0.5)
    right_deg = col_2.number_input("Right", min_value=0.0, max_value=180.0, value=70.0, step=0.5)
    up_deg = col_3.number_input("Up", min_value=0.0, max_value=180.0, value=45.0, step=0.5)
    down_deg = col_4.number_input("Down", min_value=0.0, max_value=180.0, value=55.0, step=0.5)

    horizontal_fov = left_deg + right_deg
    vertical_fov = up_deg + down_deg

    metric_col_1, metric_col_2 = st.columns(2)
    metric_col_1.metric("Horizontal FOV (deg)", f"{horizontal_fov:.1f}")
    metric_col_2.metric("Vertical FOV (deg)", f"{vertical_fov:.1f}")

with st.container(border=True):
    st.subheader("Save Result")
    notes = st.text_area(
        "Notes",
        placeholder="Posture details, marker type, distance to display, etc.",
    )
    if st.button("Save Result", type="primary", use_container_width=True):
        save_result(
            "fov",
            {
                "Left (deg)": f"{left_deg:.1f}",
                "Right (deg)": f"{right_deg:.1f}",
                "Up (deg)": f"{up_deg:.1f}",
                "Down (deg)": f"{down_deg:.1f}",
                "Horizontal FOV (deg)": f"{horizontal_fov:.1f}",
                "Vertical FOV (deg)": f"{vertical_fov:.1f}",
                "Notes": notes.strip() or "None",
            },
        )
        st.success("Field-of-view result saved.")

render_saved_result("fov")
