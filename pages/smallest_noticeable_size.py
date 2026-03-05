import math

import streamlit as st

from utils.experiment_layout import (
    render_instructions,
    render_page_header,
    render_saved_result,
    save_result,
)

st.set_page_config(
    page_title="Smallest Noticeable Size Test",
    layout="wide",
)

render_page_header(
    "Smallest Noticeable Size Test",
    "Measure threshold distance and compute angular resolution in arc minutes.",
    "size",
)

render_instructions(
    "How To Run This Test",
    (
        "Display multiple equal-thickness lines and increase viewing distance until "
        "you can no longer distinguish the exact line count."
    ),
    [
        "Use fixed line thickness t and spacing d where t = d.",
        "Find the threshold viewing distance from your eyes to the screen.",
        "Compute angular resolution from thickness and threshold distance.",
    ],
)

with st.container(border=True):
    st.subheader("Input Measurements")
    col_1, col_2 = st.columns(2)
    thickness_mm = col_1.number_input(
        "Line thickness t (mm)",
        min_value=0.01,
        max_value=20.0,
        value=1.00,
        step=0.01,
    )
    distance_cm = col_2.number_input(
        "Threshold distance (cm)",
        min_value=1.0,
        max_value=500.0,
        value=80.0,
        step=1.0,
    )

    distance_mm = distance_cm * 10.0
    angle_deg = math.degrees(math.atan(thickness_mm / distance_mm))
    angle_arcmin = angle_deg * 60.0

    metric_col_1, metric_col_2 = st.columns(2)
    metric_col_1.metric("Angular Resolution (deg)", f"{angle_deg:.4f}")
    metric_col_2.metric("Angular Resolution (arcmin)", f"{angle_arcmin:.2f}")

with st.container(border=True):
    st.subheader("Save Result")
    notes = st.text_area(
        "Notes",
        placeholder="Screen details, line rendering method, ambient light, etc.",
    )
    if st.button("Save Result", type="primary", use_container_width=True):
        save_result(
            "size",
            {
                "Line Thickness (mm)": f"{thickness_mm:.2f}",
                "Threshold Distance (cm)": f"{distance_cm:.1f}",
                "Angular Resolution (arcmin)": f"{angle_arcmin:.2f}",
                "Notes": notes.strip() or "None",
            },
        )
        st.success("Smallest-size result saved.")

render_saved_result("size")
