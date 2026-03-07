"""Reusable Streamlit UI components.

This module centralizes shared UI building blocks used by the homepage and
experiment pages.
"""

import streamlit as st


def back_to_home_button(
    label: str = "Back to Home",
    icon: str = "",
    key: str | None = None,
    stretch: bool = True,
) -> None:
    """Render a button that navigates back to the homepage.

    Args:
        label: Visible button label.
        icon: Optional icon prefix.
        key: Optional Streamlit widget key.
        stretch: If True, stretch button width to its container.
    """
    button_label = f"{icon} {label}".strip()
    if st.button(
        button_label,
        key=key,
        width="stretch" if stretch else "content",
        type="primary",
    ):
        st.switch_page("app.py")


def open_test_button(
    page_path: str,
    label: str = "Open Test",
    key: str | None = None,
    stretch: bool = True,
) -> None:
    """Render a button that opens a specific experiment page.

    Args:
        page_path: Relative path to the target Streamlit page.
        label: Visible button label.
        key: Optional Streamlit widget key.
        stretch: If True, stretch button width to its container.
    """
    if st.button(
        label,
        key=key,
        width="stretch" if stretch else "content",
        type="primary",
    ):
        st.switch_page(page_path)


def render_experiment_tile(
    title: str,
    description: str,
    page_path: str,
    key: str,
) -> None:
    """Render one experiment tile with metadata and open action.

    Args:
        title: Experiment title.
        description: Short experiment summary.
        page_path: Relative path for `st.switch_page`.
        key: Streamlit key for the tile CTA.
    """
    with st.container(border=True):
        info_col, action_col = st.columns([5, 1], vertical_alignment="center")
        with info_col:
            st.markdown(f"**{title}**")
            st.caption(description)
        with action_col:
            open_test_button(page_path=page_path, key=key, stretch=True)


def render_page_header(title: str, subtitle: str, state_key: str) -> None:
    """Render a consistent experiment page header.

    Args:
        title: Page title.
        subtitle: Subtitle shown below the title.
        state_key: Unique page key used to namespace widget keys.
    """
    title_col, action_col = st.columns([6, 1], vertical_alignment="center")
    with title_col:
        st.title(title)
        st.caption(subtitle)
    with action_col:
        back_to_home_button(label="Home", icon="", key=f"{state_key}_home")


def render_instructions(section_title: str, overview: str, steps: list[str]) -> None:
    """Render a standard instruction block.

    Args:
        section_title: Instruction section title.
        overview: Introductory explanation for the section.
        steps: Ordered list of action steps.
    """
    with st.container(border=True):
        st.subheader(section_title)
        st.write(overview)
        for idx, step in enumerate(steps, start=1):
            st.write(f"{idx}. {step}")
