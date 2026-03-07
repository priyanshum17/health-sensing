"""Tests for centralized test configuration loading."""

from utils.test_config import load_test_config


def test_load_test_config_contains_expected_sections() -> None:
    """Config loader should provide required top-level sections."""
    load_test_config.cache_clear()
    config = load_test_config()
    assert "greyscale" in config
    assert "tumbling_e" in config
    assert "pitch_range" in config
    assert "gap_detection" in config
    assert "amplitude_discrimination" in config
    assert "pitch_discrimination" in config


def test_load_test_config_is_cached() -> None:
    """Repeated config loads should return the same cached object."""
    load_test_config.cache_clear()
    first = load_test_config()
    second = load_test_config()
    assert first is second
