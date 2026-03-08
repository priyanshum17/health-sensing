# Application Logic and Architecture

This document explains how the app works so students can edit TODO functions safely.

## Runtime Flow

1. `app.py` renders the home page.
2. User opens an experiment page from `pages/`.
3. Page loads configuration values from `config/test_config.json`.
4. User actions update `st.session_state`.
5. Streamlit reruns page code after each interaction.
6. Adaptive pages stop when their finish criteria are met.

## Directory Responsibilities

- `pages/`: assignment TODOs plus experiment-specific page flows
- `pages/_shared_3afc_student.py`: shared 3AFC student TODOs
- `utils/`: reusable infrastructure logic (audio/config/adaptive/ui)
- `config/`: parameter values and limits
- `tests/`: unit tests for reusable modules
- `docs/`: setup and assignment guides

## Why Shared 3AFC Logic Lives in `pages/`

This assignment keeps all student work in one directory (`pages/`) so beginners
have a single coding area.

Design split:

- page files contain stimulus-specific logic
- `_shared_3afc_student.py` contains shared adaptive/metrics/plot logic

This reduces repeated code and lowers assignment size while keeping structure clear.

## Utility Modules You Should Not Need To Edit

## `utils/test_config.py`

- loads and caches config JSON
- avoids repeated hardcoded constants

## `utils/audio_tools.py`

- waveform generation and WAV serialization
- used by hearing tests for consistent output format

## `utils/adaptive_3afc.py`

- adaptive state lifecycle
- target interval state and response bookkeeping
- reversal/threshold mechanics used by app runtime

## `utils/three_afc.py`

- shared 3AFC UI actions and summary rendering
- response handling wrappers used by page runtime

## Safety Expectations for Student Functions

- return correct output type
- clamp values to configured bounds
- validate inputs before numeric operations
- avoid division by zero and empty-list crashes
- keep behavior deterministic when seed is provided

## Common Mistakes

- returning wrong list length for 3AFC intervals
- forgetting to clamp adaptive level/index values
- mixing up percentage units vs fraction units
- using non-deterministic random behavior when deterministic output is required
- changing output key names in trial log dicts

## How To Debug Quickly

1. implement one function
2. run app page that uses it
3. read traceback from first error line
4. fix one issue at a time
5. run `uv run pytest` and `uv run ruff check .`
