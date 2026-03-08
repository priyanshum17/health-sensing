# Student Function Implementation Guide

This guide explains each assignment function in plain language.
Use it with in-file docstrings in `pages/*.py`.

## Read This First

For each function:

1. read inputs and expected output type
2. implement smallest correct version first
3. add safety checks (bounds, empty input, invalid values)
4. test immediately in app

## Vision: Contrast Sensitivity (`pages/greyscale_resolution.py`)

## `student_build_preview_triplets(letters_pool, rows, seed)`

Purpose:
- deterministic 3-letter preview rows

Must do:
- use local seeded RNG (`random.Random(seed)`)
- return exactly `rows` strings
- each string length is 3

Safety checks:
- `rows <= 0` should return empty list
- handle empty `letters_pool` safely

## `student_compute_contrast_levels(rows, step_log10)`

Purpose:
- log-spaced contrast levels in percent

Must do:
- formula: `100 * 10 ** (-(i * step_log10))`
- list length equals `rows`

Safety checks:
- handle `rows <= 0`

## `student_advance_contrast_state(trial_index, response_yes, total_levels)`

Purpose:
- decide next trial index and finish status

Must do:
- response `No` ends run immediately
- response `Yes` advances index
- finish at end of schedule

Safety checks:
- clamp or guard invalid `trial_index` and `total_levels`

## `student_compute_log_contrast_sensitivity(threshold_percent)`

Purpose:
- convert threshold percent to logCS metric

Must do:
- `log10(1 / (threshold_percent / 100))`

Safety checks:
- protect against zero/negative threshold

## Vision: Tumbling E (`pages/smallest_noticeable_size.py`)

## `student_next_size_index(current_index, is_correct, max_index)`

Purpose:
- adaptive difficulty step

Must do:
- correct => harder (`+1` index)
- incorrect => easier (`-1` index)
- clamp to valid range

## `student_build_trial_log_row(...)`

Purpose:
- standardized per-trial log record

Must do:
- include expected columns
- include correctness field
- round MAR for readability

## `student_validate_screen_geometry(distance_cm, screen_width_mm, screen_width_px)`

Purpose:
- reject invalid setup values

Must do:
- return `False` for non-positive values
- return `True` only for usable geometry

## `student_compute_mar_arcmin(size_px, mm_per_px, distance_cm)`

Purpose:
- convert pixel size to visual angle metric

Must do:
- compute MAR in arcminutes

Safety checks:
- guard zero/negative geometry values

## `student_format_trial_log_row(...)`

Purpose:
- maintain consistent log formatting schema

Must do:
- match table schema used by page

## Hearing: Pitch Range (`pages/pitch_frequency_range.py`)

## `student_tone_preset(level, default_frequency_hz)`

Purpose:
- map difficulty level to `(frequency_hz, amplitude)`

Must do:
- handle `easy`, `medium`, `hard`
- fallback safely for unknown input
- keep values in valid range

## `student_estimate_audible_bounds(probe_history_hz, heard_flags)`

Purpose:
- estimate lowest/highest heard frequencies

Must do:
- align two input lists by index
- use heard-only subset
- return safe fallback for empty/no-heard case

## `student_validate_audio_params(frequency_hz, amplitude)`

Purpose:
- reject invalid audio values before synthesis

Must do:
- frequency in `[20, 20000]`
- amplitude in `(0, 1]`

## Shared 3AFC Core (`pages/_shared_3afc_student.py`)

Implement these once and all 3AFC pages will use them.

## `shared_student_apply_reversal_update(...)`

Purpose:
- one 2-down/1-up update step

Must do:
- maintain correct streak logic
- update level only when rule triggers
- clamp level to `[min_level, max_level]`

## `shared_student_update_staircase_state(...)`

Purpose:
- reusable staircase update helper

Must do:
- remain consistent with reversal update behavior

## `shared_student_build_three_interval_targets(target_index)`

Purpose:
- create length-3 mask with one target

Must do:
- exactly one `True`
- all other entries `False`

## `shared_student_estimate_threshold_from_reversals(reversals, fallback_level, tail_count=4)`

Purpose:
- final threshold estimate

Must do:
- average trailing reversals when available
- fallback to default level otherwise

## `shared_student_compute_recent_accuracy(history, window=12)`

Purpose:
- trailing percent-correct metric

Must do:
- compute using last `window` trials
- return percentage in `[0, 100]`

## `shared_student_validate_audio_params(amplitude, stimulus_value)`

Purpose:
- shared validation guard for 3AFC pages

Must do:
- validate amplitude and numeric stimulus value
- return strict `True`/`False`

## `shared_student_plot_staircase(history, threshold, y_label, title)`
## `shared_student_plot_staircase_with_threshold(...)`

Purpose:
- readable staircase visualization for reports

Must do:
- plot trial levels over time
- distinguish correct/incorrect responses
- include threshold line
- include labels/title

Safety checks:
- handle short or empty history gracefully

## 3AFC Page-Specific Builders

You still implement one page-local builder in each file:

- `student_build_gap_intervals_audio` in `pages/sound_gap_detection.py`
- `student_build_amplitude_intervals_audio` in `pages/amplitude_threshold.py`
- `student_build_pitch_intervals_audio` in `pages/pitch_threshold.py`

## Final Submission Checklist

- no assignment TODO raises `NotImplementedError`
- all pages load and run
- shared 3AFC helpers work for all 3AFC pages
- lint and tests pass
