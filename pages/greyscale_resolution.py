import math

import streamlit as st

from utils.experiment_layout import (
    render_instructions,
    render_page_header,
    render_saved_result,
    save_result,
)

st.set_page_config(
    page_title="Greyscale Resolution Test",
    layout="wide",
)

render_page_header(
    "Greyscale Resolution Test",
    "Compare close shades of grey to estimate your brightness discrimination threshold.",
    "greyscale",
)

render_instructions(
    "How To Run This Test",
    (
        "Start from high contrast and reduce the contrast until the foreground text "
        "is barely distinguishable from the background."
    ),
    [
        "Set a background greyscale level.",
        "Adjust the difference percentage to the smallest noticeable value.",
        "Record the threshold percentage and estimate the bit resolution.",
    ],
)

with st.container(border=True):
    st.subheader("Interactive Comparison")
    base_percent = st.slider(
        "Background greyscale (%)",
        min_value=0,
        max_value=100,
        value=55,
        step=1,
    )
    delta_percent = st.slider(
        "Difference threshold (%)",
        min_value=0.1,
        max_value=20.0,
        value=2.0,
        step=0.1,
    )
    direction = st.radio(
        "Foreground relative to background",
        options=["Lighter", "Darker"],
        horizontal=True,
    )

    foreground_percent = (
        min(100.0, base_percent + delta_percent)
        if direction == "Lighter"
        else max(0.0, base_percent - delta_percent)
    )

    bg_value = int(round(base_percent * 255 / 100))
    fg_value = int(round(foreground_percent * 255 / 100))
    bg_hex = f"#{bg_value:02x}{bg_value:02x}{bg_value:02x}"
    fg_hex = f"#{fg_value:02x}{fg_value:02x}{fg_value:02x}"

    st.markdown(
        f"""
        <div style="padding: 1.2rem; border-radius: 10px; border: 1px solid #666;
        background: {bg_hex}; color: {fg_hex}; font-size: 1.05rem; font-weight: 700;">
        The quick brown fox jumps over the lazy dog.
        </div>
        """,
        unsafe_allow_html=True,
    )

    discrete_levels = max(1, int(round(100 / delta_percent)))
    estimated_bits = max(1, math.ceil(math.log2(discrete_levels)))
    metric_col_1, metric_col_2 = st.columns(2)
    metric_col_1.metric("Threshold Difference (%)", f"{delta_percent:.1f}")
    metric_col_2.metric("Estimated Bit Resolution", f"{estimated_bits}-bit")

with st.container(border=True):
    st.subheader("Save Result")
    with st.form("greyscale_save_form", clear_on_submit=False):
        final_threshold = st.number_input(
            "Final threshold percentage (%)",
            min_value=0.1,
            max_value=100.0,
            value=float(delta_percent),
            step=0.1,
        )
        notes = st.text_area(
            "Notes",
            placeholder="Lighting conditions, screen brightness, distance, etc.",
        )
        submitted = st.form_submit_button("Save Result", type="primary", use_container_width=True)

    if submitted:
        final_levels = max(1, int(round(100 / final_threshold)))
        final_bits = max(1, math.ceil(math.log2(final_levels)))
        save_result(
            "greyscale",
            {
                "Threshold (%)": f"{final_threshold:.1f}",
                "Estimated Bits": f"{final_bits}-bit",
                "Notes": notes.strip() or "None",
            },
        )
        st.success("Greyscale result saved.")

render_saved_result("greyscale")
