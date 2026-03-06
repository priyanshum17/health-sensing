import io
import math
import random
import struct
import wave


def _sine_samples(
    frequency_hz: float,
    duration_s: float,
    amplitude: float,
    sample_rate: int,
) -> bytes:
    """Create 16-bit PCM sine wave samples."""
    sample_count = max(1, int(duration_s * sample_rate))
    clipped_amplitude = max(0.0, min(amplitude, 1.0))
    pcm = bytearray()
    for index in range(sample_count):
        t = index / sample_rate
        sample = clipped_amplitude * math.sin(2 * math.pi * frequency_hz * t)
        pcm.extend(struct.pack("<h", int(sample * 32767)))
    return bytes(pcm)


def _silence_samples(duration_s: float, sample_rate: int) -> bytes:
    """Create 16-bit PCM silence samples."""
    sample_count = max(1, int(duration_s * sample_rate))
    return b"\x00\x00" * sample_count


def _to_wav(pcm_frames: bytes, sample_rate: int) -> bytes:
    """Wrap PCM frames into a WAV byte stream."""
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(pcm_frames)
    return buffer.getvalue()


def _noise_samples(
    duration_s: float,
    amplitude: float,
    sample_rate: int,
    seed: int | None = None,
) -> bytes:
    """Create 16-bit PCM white noise samples."""
    sample_count = max(1, int(duration_s * sample_rate))
    clipped_amplitude = max(0.0, min(amplitude, 1.0))
    rng = random.Random(seed)
    pcm = bytearray()
    for _ in range(sample_count):
        sample = clipped_amplitude * (2.0 * rng.random() - 1.0)
        pcm.extend(struct.pack("<h", int(sample * 32767)))
    return bytes(pcm)


def single_tone_wav(
    frequency_hz: float,
    duration_s: float = 1.2,
    amplitude: float = 0.4,
    sample_rate: int = 44100,
) -> bytes:
    """Generate a single-tone WAV clip."""
    frames = _sine_samples(frequency_hz, duration_s, amplitude, sample_rate)
    return _to_wav(frames, sample_rate)


def two_tone_gap_wav(
    frequency_hz: float,
    gap_ms: float,
    amplitude_1: float,
    amplitude_2: float,
    tone_duration_s: float = 0.6,
    sample_rate: int = 44100,
) -> bytes:
    """Generate two tones separated by a silence gap."""
    gap_s = max(0.0, gap_ms / 1000.0)
    frames = b"".join(
        [
            _sine_samples(frequency_hz, tone_duration_s, amplitude_1, sample_rate),
            _silence_samples(gap_s, sample_rate),
            _sine_samples(frequency_hz, tone_duration_s, amplitude_2, sample_rate),
        ]
    )
    return _to_wav(frames, sample_rate)


def noise_burst_with_gap_wav(
    *,
    duration_s: float,
    gap_ms: float,
    amplitude: float = 0.35,
    sample_rate: int = 44100,
    seed: int | None = None,
) -> bytes:
    """Generate one noise burst with a centered silence gap."""
    gap_s = max(0.0, gap_ms / 1000.0)
    if gap_s <= 0.0:
        return _to_wav(_noise_samples(duration_s, amplitude, sample_rate, seed), sample_rate)

    left_duration = max(0.0, (duration_s - gap_s) / 2.0)
    right_duration = max(0.0, duration_s - left_duration - gap_s)
    frames = b"".join(
        [
            _noise_samples(left_duration, amplitude, sample_rate, seed),
            _silence_samples(gap_s, sample_rate),
            _noise_samples(right_duration, amplitude, sample_rate, None if seed is None else seed + 1),
        ]
    )
    return _to_wav(frames, sample_rate)
