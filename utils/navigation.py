import streamlit as st


def back_to_home_button(
    label: str = "Back to Home",
    icon: str = "",
    key: str | None = None,
    use_container_width: bool = True,
) -> None:
    """Render a reusable button that navigates back to the home page."""
    button_label = f"{icon} {label}".strip()
    if st.button(
        button_label,
        key=key,
        use_container_width=use_container_width,
    ):
        st.switch_page("app.py")


def open_test_button(
    page_path: str,
    label: str = "Open Test",
    key: str | None = None,
    use_container_width: bool = True,
) -> None:
    """Render a reusable CTA button that opens a specific experiment page."""
    if st.button(
        label,
        key=key,
        use_container_width=use_container_width,
        type="primary",
    ):
        st.switch_page(page_path)
