"""Tests for waveform generation helpers."""

from __future__ import annotations

import io
import wave

from utils.audio_tools import noise_burst_with_gap_wav, single_tone_wav


def _wav_params(wav_bytes: bytes) -> tuple[int, int, int, int]:
    """Read core wave params from byte payload.

    Args:
        wav_bytes: Serialized wav bytes.

    Returns:
        Tuple of channels, sample width, sample rate, and frame count.
    """
    with wave.open(io.BytesIO(wav_bytes), "rb") as handle:
        return (
            handle.getnchannels(),
            handle.getsampwidth(),
            handle.getframerate(),
            handle.getnframes(),
        )


def test_single_tone_wav_has_valid_header_and_frames() -> None:
    """Single tone generator should return valid mono PCM WAV payload."""
    wav_bytes = single_tone_wav(frequency_hz=440, duration_s=1.0, amplitude=0.5, sample_rate=44100)
    channels, width, rate, frames = _wav_params(wav_bytes)
    assert channels == 1
    assert width == 2
    assert rate == 44100
    assert frames == 44100


def test_noise_gap_wav_frame_count_matches_duration() -> None:
    """Noise burst frame count should track duration regardless of gap value."""
    wav_no_gap = noise_burst_with_gap_wav(
        duration_s=0.8,
        gap_ms=0,
        amplitude=0.3,
        sample_rate=44100,
    )
    wav_with_gap = noise_burst_with_gap_wav(
        duration_s=0.8,
        gap_ms=20,
        amplitude=0.3,
        sample_rate=44100,
        seed=123,
    )
    _, _, _, frames_no_gap = _wav_params(wav_no_gap)
    _, _, _, frames_with_gap = _wav_params(wav_with_gap)
    assert frames_no_gap == frames_with_gap == 35280
