import math
import random

import streamlit as st

from utils.adaptive_3afc import (
    advance_trial,
    estimate_threshold,
    get_or_create_trial,
    init_adaptive_state,
    register_response,
    reset_adaptive_state,
)
from utils.experiment_layout import (
    render_instructions,
    render_page_header,
    render_saved_result,
    save_result,
)

st.set_page_config(
    page_title="Contrast Sensitivity Test",
    layout="wide",
)

render_page_header(
    "Contrast Sensitivity Test (Pelli-Style)",
    "Letter-contrast progression with a 3AFC adaptive threshold module.",
    "greyscale",
)

render_instructions(
    "How To Run This Test",
    (
        "This page uses a Pelli-inspired letter contrast workflow. The preview chart "
        "shows grouped letters with progressively lower contrast, and the adaptive "
        "task estimates threshold with forced-choice responses."
    ),
    [
        "Use the chart preview to familiarize yourself with contrast progression.",
        "In each adaptive trial, pick the interval containing the faintest letter.",
        "Continue until reversals stabilize, then save the estimated threshold.",
    ],
)

letters = "CDHKNORSVZ"

with st.container(border=True):
    st.subheader("Pelli-Style Contrast Chart Preview")
    st.caption("Letter groups are shown from high contrast (top) to low contrast (bottom).")
    bg = 255
    html_rows = []
    rng = random.Random(1988)
    for row_idx in range(12):
        # Pelli-style step: 0.15 log contrast per triplet
        log_contrast = row_idx * 0.15
        contrast = 10 ** (-log_contrast)
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

adaptive = init_adaptive_state(
    "greyscale",
    start_level=32.0,
    min_level=0.4,
    max_level=70.0,
    initial_step=4.0,
    min_step=0.2,
    max_reversals=8,
)
trial = get_or_create_trial("greyscale")
current_contrast_pct = float(adaptive["current_level"])
# Keep references near target, but provide clearer separation for easier interval judgment.
reference_offset = max(3.0, float(adaptive["step"]) * 1.35)
reference_contrast_pct = min(
    float(adaptive["max_level"]),
    current_contrast_pct + reference_offset,
)
feedback_key = "greyscale_last_feedback"


def draw_letter_card(letter: str, contrast_pct: float) -> str:
    bg = 255
    contrast = max(0.0, min(1.0, contrast_pct / 100.0))
    fg = int(max(0, min(255, bg * (1.0 - contrast))))
    return (
        "<div style='background:rgb(255,255,255); border:1px solid #d3d3d3; border-radius:10px; "
        "padding:1rem 0.5rem; text-align:center;'>"
        f"<div style='font-size:3rem; font-weight:700; color:rgb({fg},{fg},{fg}); "
        "font-family:serif;'>"
        f"{letter}</div></div>"
    )


with st.container(border=True):
    st.subheader("Adaptive 3AFC Trial")
    st.caption(
        f"Current adaptive contrast level: {current_contrast_pct:.2f}% | "
        f"Reversals: {len(adaptive['reversals'])}/{adaptive['max_reversals']}"
    )
    st.caption(
        f"Staircase rule: 2-down/1-up. Correct streak: {adaptive['correct_streak']}/2 "
        "(level decreases only after 2 consecutive correct responses)."
    )
    interval_cols = st.columns(3)
    trial_rng = random.Random(trial["seed"])
    for idx in range(3):
        letter = trial_rng.choice(letters)
        contrast = current_contrast_pct if idx == trial["target_index"] else reference_contrast_pct
        interval_cols[idx].markdown(draw_letter_card(letter, contrast), unsafe_allow_html=True)
        interval_cols[idx].caption(f"Interval {idx + 1}")

with st.container(border=True):
    st.subheader("Respond")
    last_feedback = st.session_state.get(feedback_key)
    if last_feedback == "correct":
        st.success("Previous response: Correct.")
    elif last_feedback == "incorrect":
        st.error("Previous response: Incorrect.")
    choice = st.radio("Which interval had the faintest letter?", [1, 2, 3], horizontal=True)
    submitted = st.button(
        "Submit Response",
        type="primary",
        use_container_width=True,
        disabled=adaptive["finished"],
    )
    if submitted and not adaptive["finished"]:
        chosen_idx = int(choice) - 1
        is_correct = chosen_idx == int(trial["target_index"])
        register_response(
            adaptive,
            level_used=current_contrast_pct,
            is_correct=is_correct,
            chosen_index=chosen_idx,
            target_index=int(trial["target_index"]),
        )
        advance_trial("greyscale")
        st.session_state[feedback_key] = "correct" if is_correct else "incorrect"
        st.rerun()

    estimated_contrast = estimate_threshold(adaptive)
    log_cs = math.log10(1.0 / max(1e-6, estimated_contrast / 100.0))
    col_1, col_2 = st.columns(2)
    col_1.metric("Estimated Contrast Threshold (%)", f"{estimated_contrast:.2f}")
    col_2.metric("Estimated log Contrast Sensitivity", f"{log_cs:.2f}")

with st.container(border=True):
    st.subheader("Save Result")
    notes = st.text_area(
        "Notes",
        placeholder="Screen brightness, viewing distance, ambient light, retries, etc.",
    )
    if st.button("Save Result", type="primary", use_container_width=True):
        save_result(
            "greyscale",
            {
                "Adaptive Method": "3AFC 2-down/1-up",
                "Estimated Contrast Threshold (%)": f"{estimated_contrast:.2f}",
                "Estimated log Contrast Sensitivity": f"{log_cs:.2f}",
                "Total Trials": f"{len(adaptive['history'])}",
                "Reversals": f"{len(adaptive['reversals'])}",
                "Notes": notes.strip() or "None",
            },
        )
        st.success("Contrast sensitivity result saved.")
    if st.button("Restart Adaptive Test", use_container_width=True):
        reset_adaptive_state("greyscale")
        st.session_state.pop(feedback_key, None)
        st.rerun()

render_saved_result("greyscale")
