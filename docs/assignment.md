# Assignment: Human Sensing Lab (Easy to Medium)

## Goal

You will complete missing functions across the experiment pages to build core
psychophysics behavior yourself.

The app already provides structure and UI. Your task is to implement algorithmic
parts in the `pages/` files.

## Editing Rule

Edit only files in `pages/`.

- Do not change function names/signatures for student TODO functions.
- Keep existing UI sections and labels unless a TODO explicitly asks to add one.

## How To Work

1. Open the project in VS Code.
2. Open each page listed below.
3. Search for `student_` function names and `Assignment TODOs`.
4. Implement functions and test directly in the Streamlit UI.

## Vision Tasks

## 1) Contrast Sensitivity (`pages/greyscale_resolution.py`)

Implement:

- `student_build_preview_triplets`
- `student_compute_contrast_levels`
- `student_advance_contrast_state`

What you should learn:

- deterministic preview generation using seeds
- log-step contrast schedule
- trial-state progression logic

Expected behavior:

- Preview rows are reproducible for the same seed.
- Contrast levels decrease per row using log spacing.
- State advances correctly and stops at the right point.

## 2) Tumbling E (`pages/smallest_noticeable_size.py`)

Implement:

- `student_next_size_index`
- `student_build_trial_log_row`

What you should learn:

- adaptive stepping (smaller on correct, larger on incorrect)
- bounded index updates
- structured trial logging for table display

Expected behavior:

- Size index always stays in valid range.
- Log rows have consistent schema and correctness flag.

## Hearing Task (Non-3AFC)

## 3) Pitch Range Screening (`pages/pitch_frequency_range.py`)

Implement:

- `student_tone_preset`
- `student_estimate_audible_bounds`

What you should learn:

- generating simple easy/medium/hard tone settings
- deriving lower and upper audible estimates from probe outcomes

Expected behavior:

- Presets always produce valid frequency/amplitude values.
- Audible bounds are computed robustly from probe history.

## 3AFC Tasks

For all 3AFC pages, implement three categories:

1. interval-audio builder
2. reversal/staircase update logic
3. matplotlib staircase plot

## 4) Sound Gap 3AFC (`pages/sound_gap_detection.py`)

Implement:

- `student_build_gap_intervals_audio`
- `student_apply_reversal_update`
- `student_plot_staircase`

## 5) Amplitude 3AFC (`pages/amplitude_threshold.py`)

Implement:

- `student_build_amplitude_intervals_audio`
- `student_apply_reversal_update`
- `student_plot_staircase`

## 6) Pitch 3AFC (`pages/pitch_threshold.py`)

Implement:

- `student_build_pitch_intervals_audio`
- `student_apply_reversal_update`
- `student_plot_staircase`

What you should learn from all 3AFC tasks:

- creating three-interval forced-choice audio stimuli
- adaptive reversal logic (2-down/1-up style)
- visualizing trial level history with threshold estimate

## Submission Checklist

- All `student_...` functions are implemented.
- App runs without `NotImplementedError`.
- Each page shows expected interaction behavior.
- 3AFC pages show a staircase plot after completion.

## Suggested Validation

- Run app:
```sh
uv run streamlit run app.py
```
- Run tests:
```sh
uv run pytest
```
- Optional lint:
```sh
uv run ruff check .
```
