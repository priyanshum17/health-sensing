import streamlit as st

from utils.navigation import back_to_home_button


def render_page_header(title: str, subtitle: str, state_key: str) -> None:
    """Render a consistent experiment page header with home navigation."""
    title_col, action_col = st.columns([6, 1], vertical_alignment="center")
    with title_col:
        st.title(title)
        st.caption(subtitle)
    with action_col:
        back_to_home_button(label="Home", icon="", key=f"{state_key}_home")


def render_instructions(section_title: str, overview: str, steps: list[str]) -> None:
    """Render a standard instructions card."""
    with st.container(border=True):
        st.subheader(section_title)
        st.write(overview)
        for idx, step in enumerate(steps, start=1):
            st.write(f"{idx}. {step}")


def save_result(state_key: str, payload: dict[str, str]) -> None:
    """Persist the latest saved payload in session state."""
    st.session_state[f"{state_key}_saved"] = payload


def render_saved_result(state_key: str, title: str = "Latest Saved Entry") -> None:
    """Render the latest saved payload from session state."""
    saved = st.session_state.get(f"{state_key}_saved")
    if not saved:
        return

    with st.container(border=True):
        st.subheader(title)
        for label, value in saved.items():
            st.write(f"**{label}:** {value}")

