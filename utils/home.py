import streamlit as st

from utils.navigation import open_test_button


def render_experiment_tile(
    title: str,
    description: str,
    page_path: str,
    key: str,
) -> None:
    """Render one experiment tile with a CTA button."""
    with st.container(border=True):
        info_col, action_col = st.columns([5, 1], vertical_alignment="center")
        with info_col:
            st.markdown(f"**{title}**")
            st.caption(description)
        with action_col:
            open_test_button(page_path=page_path, key=key, use_container_width=True)

