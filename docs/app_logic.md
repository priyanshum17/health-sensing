# Application Logic Guide

## Purpose

This document explains the runtime logic and code organization of the
Health Sensing app so contributors can modify behavior safely.

## Runtime Flow

1. Streamlit starts with `app.py`.
2. Home page renders experiment tiles and routes users to `pages/*.py`.
3. Each experiment page loads its own config block from `test_config.json`.
4. User actions update `st.session_state` and trigger reruns.
5. Adaptive tests continue until stopping criteria are reached.

## Core Modules

### `utils/ui.py`

Shared presentation components:

- home/test navigation buttons
- experiment tiles
- page headers
- instruction cards

Use this module whenever you need shared page layout behavior.

### `utils/test_config.py`

Loads `config/test_config.json` and caches it with `lru_cache`.

- source of truth for test defaults/ranges/staircase parameters
- avoids hardcoding repeated constants across page files

### `utils/adaptive_3afc.py`

Implements adaptive staircase mechanics:

- adaptive state initialization
- randomized target interval generation
- response registration (`2-down/1-up`)
- reversal tracking and threshold estimation

This file is pure test logic; it should remain UI-agnostic except for
session-state storage.

### `utils/three_afc.py`

Provides reusable page-level 3AFC helpers:

- response feedback UI
- response submit-and-advance action
- recent/overall metric rendering
- staircase plot rendering

This module reduces duplication in 3AFC page files.

### `utils/audio_tools.py`

Audio synthesis utilities:

- sine tone generation
- white noise generation
- silent gaps
- WAV serialization

All hearing tests rely on this module for consistent output format.

## Page Responsibilities

### `pages/greyscale_resolution.py`

- Fixed Pelli-style progression.
- Contrast levels derived from config (`rows`, `log_contrast_step`).
- Session-state fields track current level, history, and completion.

### `pages/smallest_noticeable_size.py`

- Tumbling E orientation task.
- Correct response makes target smaller; incorrect makes it larger.
- MAR computed from screen geometry + viewing distance.

### `pages/pitch_frequency_range.py`

- Direct tone playback by frequency and amplitude controls.
- Intended as manual screening rather than adaptive staircase.

### 3AFC Pages

- `pages/sound_gap_detection.py`
- `pages/amplitude_threshold.py`
- `pages/pitch_threshold.py`

Shared structure:

1. Initialize adaptive state and trial descriptor.
2. Render three interval stimuli (one target + two references).
3. Collect forced-choice response.
4. Update staircase and rerun.
5. Show threshold metrics and completion plot.

## Configuration Conventions

- Keep all experiment constants in `config/test_config.json`.
- Add new keys under a dedicated test namespace.
- Prefer descriptive names such as `adaptive.start_level`,
  `adaptive.min_level`, and `adaptive.max_reversals`.

## Testing Conventions

- Add unit tests for reusable logic in `utils/`.
- Avoid UI-heavy tests unless behavior cannot be validated otherwise.
- Keep tests deterministic where possible (`seed` usage).

Current tests cover:

- adaptive staircase updates
- audio output shape/headers
- config loader behavior
