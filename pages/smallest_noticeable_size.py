import math
import random
import statistics

import streamlit as st

from utils.experiment_layout import (
    render_instructions,
    render_page_header,
    render_saved_result,
    save_result,
)
from utils.test_config import load_test_config

st.set_page_config(
    page_title="Visual Resolution (Tumbling E Staircase)",
    layout="wide",
)

render_page_header(
    "Visual Resolution Test (Tumbling E Staircase)",
    "Single-optotype adaptive staircase with error logging and MAR tracking.",
    "size",
)

render_instructions(
    "How To Run This Test",
    (
        "You will see one Tumbling E at a time. Choose its orientation. "
        "Correct responses make the next E smaller; incorrect responses make it larger."
    ),
    [
        "Keep viewing distance fixed during the run.",
        "Answer every trial with one of: Up, Down, Left, Right.",
        "Test stops automatically after 8 reversals.",
    ],
)

config = load_test_config()
cfg = config["tumbling_e"]
SIZE_LEVELS_PX = [int(v) for v in cfg["size_levels_px"]]
ORIENTATIONS = ["Up", "Down", "Left", "Right"]


def init_tumbling_state() -> dict:
    key = "tumbling_e_state"
    if key not in st.session_state:
        st.session_state[key] = {
            "size_index": 0,
            "trial_orientation": random.choice(ORIENTATIONS),
            "last_direction": None,
            "reversals": [],
            "history": [],
            "max_reversals": int(cfg["max_reversals"]),
            "finished": False,
        }
    return st.session_state[key]


def next_orientation(previous: str) -> str:
    candidate = random.choice(ORIENTATIONS)
    while candidate == previous:
        candidate = random.choice(ORIENTATIONS)
    return candidate


def e_symbol(size_px: int, orientation: str) -> str:
    rotation = {"Right": 0, "Down": 90, "Left": 180, "Up": 270}[orientation]
    return (
        "<div style='display:flex; justify-content:center; align-items:center; "
        "background:#ffffff; border:1px solid #d0d0d0; border-radius:8px; padding:0.3rem;'>"
        # LAB NOTE: Keep this sans-serif so the optotype does not include serif end strokes.
        f"<div style='font-size:{size_px}px; font-family:\"Helvetica Neue\", Arial, sans-serif; font-weight:800; "
        f"color:#101010; line-height:1; transform:rotate({rotation}deg);'>E</div></div>"
    )


with st.container(border=True):
    st.subheader("Test Setup")
    col_1, col_2, col_3 = st.columns(3)
    distance_cm = col_1.number_input(
        "Viewing distance (cm)",
        min_value=float(cfg["setup"]["distance_cm"]["min"]),
        max_value=float(cfg["setup"]["distance_cm"]["max"]),
        value=float(cfg["setup"]["distance_cm"]["default"]),
        step=float(cfg["setup"]["distance_cm"]["step"]),
    )
    screen_width_mm = col_2.number_input(
        "Screen width (mm)",
        min_value=float(cfg["setup"]["screen_width_mm"]["min"]),
        max_value=float(cfg["setup"]["screen_width_mm"]["max"]),
        value=float(cfg["setup"]["screen_width_mm"]["default"]),
        step=float(cfg["setup"]["screen_width_mm"]["step"]),
    )
    screen_width_px = col_3.number_input(
        "Screen width (pixels)",
        min_value=int(cfg["setup"]["screen_width_px"]["min"]),
        max_value=int(cfg["setup"]["screen_width_px"]["max"]),
        value=int(cfg["setup"]["screen_width_px"]["default"]),
        step=int(cfg["setup"]["screen_width_px"]["step"]),
    )
    mm_per_px = float(screen_width_mm) / float(screen_width_px)
    st.caption(f"Pixel pitch: {mm_per_px:.4f} mm/px")


def mar_arcmin_for_size(size_px: int, mm_per_px: float, distance_cm: float) -> float:
    stroke_mm = (size_px * mm_per_px) / 5.0
    distance_mm = distance_cm * 10.0
    return math.degrees(math.atan(stroke_mm / distance_mm)) * 60.0


state = init_tumbling_state()
feedback_key = "tumbling_e_last_feedback"
current_index = int(state["size_index"])
current_size_px = SIZE_LEVELS_PX[current_index]
current_orientation = state["trial_orientation"]
current_mar = mar_arcmin_for_size(current_size_px, mm_per_px, distance_cm)

with st.container(border=True):
    st.subheader("Adaptive Tumbling E Trial")
    st.caption(
        f"Current size: {current_size_px}px | Current MAR: {current_mar:.2f} arcmin | "
        f"Reversals: {len(state['reversals'])}/{state['max_reversals']}"
    )
    st.markdown(e_symbol(current_size_px, current_orientation), unsafe_allow_html=True)

with st.container(border=True):
    st.subheader("Respond")
    last_feedback = st.session_state.get(feedback_key)
    if last_feedback == "correct":
        st.success("Previous response: Correct.")
    elif last_feedback == "incorrect":
        st.error("Previous response: Incorrect.")

    response = st.radio("Orientation", ORIENTATIONS, horizontal=True)
    submitted = st.button(
        "Submit Response",
        type="primary",
        use_container_width=True,
        disabled=state["finished"],
    )
    if submitted and not state["finished"]:
        is_correct = response == current_orientation
        if is_correct:
            next_index = min(current_index + 1, len(SIZE_LEVELS_PX) - 1)
            direction = "down" if next_index != current_index else None
        else:
            next_index = max(current_index - 1, 0)
            direction = "up" if next_index != current_index else None

        if direction and state["last_direction"] and direction != state["last_direction"]:
            state["reversals"].append(current_size_px)
        if direction:
            state["last_direction"] = direction

        state["history"].append(
            {
                "Trial": len(state["history"]) + 1,
                "Size (px)": current_size_px,
                "MAR (arcmin)": round(current_mar, 2),
                "Correct Orientation": current_orientation,
                "Your Response": response,
                "Correct": "Yes" if is_correct else "No",
            }
        )

        state["size_index"] = next_index
        state["trial_orientation"] = next_orientation(current_orientation)
        st.session_state[feedback_key] = "correct" if is_correct else "incorrect"
        if len(state["reversals"]) >= state["max_reversals"]:
            state["finished"] = True
        st.rerun()

if state["finished"]:
    with st.container(border=True):
        st.subheader("Staircase Complete")
        st.success("Test finished at 8 reversals.")
        reversal_mars = [mar_arcmin_for_size(px, mm_per_px, distance_cm) for px in state["reversals"]]
        estimated_mar = (
            statistics.mean(reversal_mars[-4:])
            if len(reversal_mars) >= 4
            else mar_arcmin_for_size(SIZE_LEVELS_PX[state["size_index"]], mm_per_px, distance_cm)
        )
        col_1, col_2, col_3 = st.columns(3)
        col_1.metric("Total Trials", f"{len(state['history'])}")
        col_2.metric("Reversals", f"{len(state['reversals'])}")
        col_3.metric("Estimated MAR", f"{estimated_mar:.2f} arcmin")

with st.container(border=True):
    st.subheader("Trial Log")
    history = state["history"]
    if history:
        st.dataframe(history, use_container_width=True, hide_index=True)
        wrong_only = [row for row in history if row["Correct"] == "No"]
        st.markdown("**Incorrect Responses**")
        if wrong_only:
            st.dataframe(wrong_only, use_container_width=True, hide_index=True)
        else:
            st.caption("No incorrect responses yet.")
    else:
        st.caption("No responses yet.")

with st.container(border=True):
    st.subheader("Save Result")
    estimated_mar = mar_arcmin_for_size(SIZE_LEVELS_PX[state["size_index"]], mm_per_px, distance_cm)
    if state["reversals"]:
        reversal_mars = [mar_arcmin_for_size(px, mm_per_px, distance_cm) for px in state["reversals"]]
        estimated_mar = statistics.mean(reversal_mars[-4:]) if len(reversal_mars) >= 4 else estimated_mar
    notes = st.text_area(
        "Notes",
        placeholder="Distance control, fatigue, monitor setup, retries, etc.",
    )
    if st.button("Save Result", type="primary", use_container_width=True):
        save_result(
            "size",
            {
                "Method": "Tumbling E Staircase",
                "Viewing Distance (cm)": f"{distance_cm:.1f}",
                "Pixel Pitch (mm/px)": f"{mm_per_px:.4f}",
                "Total Trials": f"{len(state['history'])}",
                "Reversals": f"{len(state['reversals'])}",
                "Estimated MAR (arcmin)": f"{estimated_mar:.2f}",
                "Notes": notes.strip() or "None",
            },
        )
        st.success("Visual resolution result saved.")
    if st.button("Restart Staircase", use_container_width=True):
        st.session_state.pop("tumbling_e_state", None)
        st.session_state.pop(feedback_key, None)
        st.rerun()

render_saved_result("size")
