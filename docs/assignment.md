# Assignment Guide: Human Sensing Lab

## Assignment Goal

Implement student TODO functions so each experiment page runs correctly and safely.
You are not expected to redesign the app UI or architecture.

## What You Must Edit

Edit only `pages/` files.

Required files:

- `pages/greyscale_resolution.py`
- `pages/smallest_noticeable_size.py`
- `pages/pitch_frequency_range.py`
- `pages/sound_gap_detection.py`
- `pages/amplitude_threshold.py`
- `pages/pitch_threshold.py`
- `pages/_shared_3afc_student.py`

## Rules

- Keep function names and signatures unchanged.
- Do not remove instruction sections.
- Keep outputs compatible with existing page code.
- Handle invalid values safely (bounds checks, non-empty checks, divide-by-zero guards).

## Recommended Order (Easy to Hard)

1. `greyscale_resolution.py`
2. `smallest_noticeable_size.py`
3. `pitch_frequency_range.py`
4. `pages/_shared_3afc_student.py`
5. `sound_gap_detection.py`
6. `amplitude_threshold.py`
7. `pitch_threshold.py`

## Experiments and Student Responsibilities

## 1) Contrast Sensitivity

File: `pages/greyscale_resolution.py`

Implement:
- deterministic preview generation
- log contrast level schedule
- progression stop/advance logic
- log contrast sensitivity calculation

## 2) Tumbling E Visual Resolution

File: `pages/smallest_noticeable_size.py`

Implement:
- adaptive size stepping
- screen geometry validation
- MAR conversion
- consistent trial log row formatting

## 3) Pitch Frequency Range Screening

File: `pages/pitch_frequency_range.py`

Implement:
- easy/medium/hard preset mapping
- heard-range estimation from probe history
- audio parameter validation

## 4) Shared 3AFC Core

File: `pages/_shared_3afc_student.py`

Implement shared helpers once:
- staircase updates
- target-mask generation
- threshold estimate from reversals
- recent accuracy metric
- validation helper
- staircase plotting helpers

## 5) 3AFC Stimulus Builders (Page-Specific)

Implement one page-specific audio builder per page:

- `pages/sound_gap_detection.py`: `student_build_gap_intervals_audio`
- `pages/amplitude_threshold.py`: `student_build_amplitude_intervals_audio`
- `pages/pitch_threshold.py`: `student_build_pitch_intervals_audio`

These pages call your shared 3AFC logic from `pages/_shared_3afc_student.py`.

## Completion Definition

You are done when:

- all required TODO functions are implemented
- no assignment `NotImplementedError` remains
- all pages run without crashing
- 3AFC pages stay locked until shared/page TODOs are implemented
- lint and tests pass

## Validation Steps

1. Run `uv run ruff check .`
2. Run `uv run pytest`
3. Run app and test each page manually

## If You Are New To Coding

Use this workflow:

1. Implement one function.
2. Run app and test immediately.
3. If it fails, read traceback from top to bottom.
4. Fix one error at a time.
5. Move to next function only after current one works.

## Help Order

1. [docs/student_functions.md](student_functions.md)
2. [docs/app_logic.md](app_logic.md)
3. [docs/install.md](install.md)
