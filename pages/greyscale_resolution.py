import math
import random

import streamlit as st

from utils.experiment_layout import (
    render_instructions,
    render_page_header,
)
from utils.test_config import load_test_config

st.set_page_config(
    page_title="Contrast Sensitivity Test",
    layout="wide",
)

render_page_header(
    "Contrast Sensitivity Test (Pelli-Style)",
    "Single-letter Pelli-style progression with fixed log contrast steps.",
    "greyscale",
)

render_instructions(
    "How To Run This Test",
    (
        "This version follows a strict Pelli-style progression (no 3AFC). "
        "One letter is shown at a time while contrast decreases by a fixed log step."
    ),
    [
        "Keep viewing distance and screen brightness fixed.",
        "At each level, report whether you can still identify the letter.",
        "Threshold is estimated from the last contrast level you could identify.",
    ],
)

config = load_test_config()
cfg = config["greyscale"]
letters = cfg["letters"]
row_count = int(cfg["preview"]["rows"])
log_step = float(cfg["preview"]["log_contrast_step"])
contrast_levels_pct = [100.0 * (10 ** (-(idx * log_step))) for idx in range(row_count)]


def draw_letter_card(letter: str, contrast_pct: float) -> str:
    bg = int(cfg["background_rgb"])
    contrast = max(0.0, min(1.0, contrast_pct / 100.0))
    fg = int(max(0, min(255, bg * (1.0 - contrast))))
    return (
        "<div style='background:rgb(255,255,255); border:1px solid #d3d3d3; border-radius:10px; "
        "padding:1rem 0.5rem; text-align:center;'>"
        f"<div style='font-size:3rem; font-weight:700; color:rgb({fg},{fg},{fg}); "
        "font-family:serif;'>"
        f"{letter}</div></div>"
    )


if "greyscale_pelli_index" not in st.session_state:
    st.session_state["greyscale_pelli_index"] = 0
if "greyscale_pelli_letter" not in st.session_state:
    st.session_state["greyscale_pelli_letter"] = random.choice(letters)
if "greyscale_pelli_history" not in st.session_state:
    st.session_state["greyscale_pelli_history"] = []
if "greyscale_pelli_finished" not in st.session_state:
    st.session_state["greyscale_pelli_finished"] = False
if "greyscale_pelli_threshold_pct" not in st.session_state:
    st.session_state["greyscale_pelli_threshold_pct"] = contrast_levels_pct[0]

with st.container(border=True):
    st.subheader("Pelli-Style Contrast Chart Preview")
    st.caption("Letter groups are shown from high contrast (top) to low contrast (bottom).")
    bg = int(cfg["background_rgb"])
    html_rows = []
    rng = random.Random(int(cfg["preview"]["seed"]))
    for row_idx in range(row_count):
        contrast = 10 ** (-(row_idx * log_step))
        fg = int(max(0, min(255, bg * (1.0 - contrast))))
        triplet = "".join(rng.choice(letters) for _ in range(3))
        html_rows.append(
            (
                f"<div style='letter-spacing:0.45rem; font-size:1.9rem; font-weight:700; "
                f"color:rgb({fg},{fg},{fg}); margin:0.2rem 0;'>{triplet}</div>"
            )
        )
    st.markdown(
        (
            "<div style='background:rgb(255,255,255); border:1px solid #d3d3d3; "
            "border-radius:10px; padding:1rem; text-align:center; font-family:serif;'>"
            + "".join(html_rows)
            + "</div>"
        ),
        unsafe_allow_html=True,
    )

trial_index = int(st.session_state["greyscale_pelli_index"])
finished = bool(st.session_state["greyscale_pelli_finished"])
current_contrast_pct = contrast_levels_pct[min(trial_index, len(contrast_levels_pct) - 1)]
current_letter = st.session_state["greyscale_pelli_letter"]

with st.container(border=True):
    st.subheader("Single-Letter Trial")
    st.caption(f"Current level: {trial_index + 1}/{len(contrast_levels_pct)}")
    st.caption(f"Current contrast: {current_contrast_pct:.2f}%")
    st.markdown(draw_letter_card(current_letter, current_contrast_pct), unsafe_allow_html=True)

with st.container(border=True):
    st.subheader("Respond")
    response = st.radio(
        "Can you identify this letter?",
        ["Yes", "No"],
        horizontal=True,
        key="greyscale_pelli_response",
    )
    submitted = st.button(
        "Submit Response",
        type="primary",
        width="stretch",
        disabled=finished,
    )
    if submitted and not finished:
        # LAB NOTE: This block drives the Pelli-style staircase progression.
        # Students can extend it with stricter scoring rules (for example typed-letter checks).
        can_identify = response == "Yes"
        st.session_state["greyscale_pelli_history"].append(
            {
                "Level": trial_index + 1,
                "Letter": current_letter,
                "Contrast (%)": round(current_contrast_pct, 2),
                "Identified": "Yes" if can_identify else "No",
            }
        )

        if can_identify:
            st.session_state["greyscale_pelli_threshold_pct"] = current_contrast_pct
            next_index = trial_index + 1
            if next_index >= len(contrast_levels_pct):
                st.session_state["greyscale_pelli_finished"] = True
            else:
                st.session_state["greyscale_pelli_index"] = next_index
                st.session_state["greyscale_pelli_letter"] = random.choice(letters)
        else:
            if trial_index > 0:
                st.session_state["greyscale_pelli_threshold_pct"] = contrast_levels_pct[trial_index - 1]
            st.session_state["greyscale_pelli_finished"] = True
        st.rerun()

threshold_pct = float(st.session_state["greyscale_pelli_threshold_pct"])
log_cs = math.log10(1.0 / max(1e-6, threshold_pct / 100.0))

with st.container(border=True):
    col_1, col_2 = st.columns(2)
    col_1.metric("Estimated Contrast Threshold (%)", f"{threshold_pct:.2f}")
    col_2.metric("Estimated log Contrast Sensitivity", f"{log_cs:.2f}")
    if finished:
        st.success("Pelli-style run complete.")

with st.container(border=True):
    st.subheader("Trial Log")
    history = st.session_state["greyscale_pelli_history"]
    if history:
        st.dataframe(history, width="stretch", hide_index=True)
    else:
        st.caption("No responses yet.")

with st.container(border=True):
    st.subheader("Test Controls")

    if st.button("Restart Test", width="stretch"):
        for key in [
            "greyscale_pelli_index",
            "greyscale_pelli_letter",
            "greyscale_pelli_history",
            "greyscale_pelli_finished",
            "greyscale_pelli_threshold_pct",
            "greyscale_pelli_response",
        ]:
            st.session_state.pop(key, None)
        st.rerun()
