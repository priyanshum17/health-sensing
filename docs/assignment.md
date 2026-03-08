# Assignment: Human Sensing Lab

This assignment is designed to be easy-to-medium difficulty.
You will complete student functions in the `pages/` directory.

## What You Are Building

You will implement logic for:

- Vision contrast progression and sensitivity calculation
- Vision size-adaptation and trial logging (Tumbling E)
- Hearing pitch presets and audible bound estimation
- 3AFC audio generation, staircase updates, and plotting

## Editing Scope

Edit only `pages/*.py`.

- Keep the existing function names and parameters.
- Keep instruction sections and page layout intact.
- Focus on `student_...` functions.

## How To Work Through The Assignment

1. Open the repo in VS Code.
2. Start app:
```sh
uv run streamlit run app.py
```
3. Open each page and read the `Assignment TODOs` box.
4. Implement functions one by one.
5. Re-run page and verify behavior.

## Vision Experiments

## 1) Contrast Sensitivity

File: `pages/greyscale_resolution.py`

What this test measures:
- The smallest contrast difference you can still detect.

Implement these functions:
- `student_build_preview_triplets`
- `student_compute_contrast_levels`
- `student_advance_contrast_state`
- `student_compute_log_contrast_sensitivity`

What good output looks like:
- Preview rows are deterministic for the same seed.
- Contrast starts high and decreases each level.
- Test state advances correctly and finishes correctly.
- Log contrast sensitivity is computed from threshold percent.

Useful references:
- Python random with seed:
  https://docs.python.org/3/library/random.html#random.Random
- Python log10:
  https://docs.python.org/3/library/math.html#math.log10

## 2) Visual Resolution (Tumbling E)

File: `pages/smallest_noticeable_size.py`

What this test measures:
- The smallest optotype size you can reliably identify.

Implement these functions:
- `student_next_size_index`
- `student_build_trial_log_row`
- `student_validate_screen_geometry`
- `student_compute_mar_arcmin`
- `student_format_trial_log_row`

What good output looks like:
- Correct response makes E smaller, incorrect makes it larger.
- Size index stays within valid bounds.
- MAR values are stable and realistic.
- Trial log row format is consistent.

Useful references:
- Visual angle basics:
  https://en.wikipedia.org/wiki/Visual_angle
- Python dict basics:
  https://docs.python.org/3/tutorial/datastructures.html#dictionaries

## Hearing (Non-3AFC)

## 3) Pitch Frequency Range

File: `pages/pitch_frequency_range.py`

What this test measures:
- Approximate lower and upper audible frequency bounds.

Implement these functions:
- `student_tone_preset`
- `student_estimate_audible_bounds`
- `student_validate_audio_params`

What good output looks like:
- Easy/medium/hard presets map to usable tone settings.
- Bound estimation handles empty and normal probe histories.
- Audio validation rejects invalid settings.

Useful references:
- Human hearing range overview:
  https://en.wikipedia.org/wiki/Hearing_range

## 3AFC Experiments

3AFC means 3-alternative forced choice:
- One of three intervals contains the target cue.
- User must pick 1, 2, or 3 each trial.

You will implement shared patterns in three files.

Core categories:
1. Build three-interval target layout
2. Build interval audio clips
3. Update staircase state (2-down/1-up style)
4. Estimate threshold from reversals
5. Compute recent accuracy
6. Validate audio params
7. Plot staircase with threshold

## 4) Sound Gap Detection 3AFC

File: `pages/sound_gap_detection.py`

Implement:
- `student_build_gap_intervals_audio`
- `student_apply_reversal_update`
- `student_plot_staircase`
- `student_build_three_interval_targets`
- `student_update_staircase_state`
- `student_estimate_threshold_from_reversals`
- `student_compute_recent_accuracy`
- `student_validate_audio_params`
- `student_plot_staircase_with_threshold`

## 5) Amplitude Discrimination 3AFC

File: `pages/amplitude_threshold.py`

Implement:
- `student_build_amplitude_intervals_audio`
- `student_apply_reversal_update`
- `student_plot_staircase`
- `student_build_three_interval_targets`
- `student_update_staircase_state`
- `student_estimate_threshold_from_reversals`
- `student_compute_recent_accuracy`
- `student_validate_audio_params`
- `student_plot_staircase_with_threshold`

## 6) Pitch Discrimination 3AFC

File: `pages/pitch_threshold.py`

Implement:
- `student_build_pitch_intervals_audio`
- `student_apply_reversal_update`
- `student_plot_staircase`
- `student_build_three_interval_targets`
- `student_update_staircase_state`
- `student_estimate_threshold_from_reversals`
- `student_compute_recent_accuracy`
- `student_validate_audio_params`
- `student_plot_staircase_with_threshold`

Useful references for 3AFC pages:
- Matplotlib plotting:
  https://matplotlib.org/stable/tutorials/index.html
- Forced-choice method overview:
  https://en.wikipedia.org/wiki/Forced-choice_test

## Validation Checklist

- All `student_...` functions are implemented.
- App pages run without `NotImplementedError`.
- Visual pages update state and logs correctly.
- 3AFC pages produce changing levels and plot output.

## Suggested Commands

Run app:
```sh
uv run streamlit run app.py
```

Run tests:
```sh
uv run pytest
```

Lint:
```sh
uv run ruff check .
```
