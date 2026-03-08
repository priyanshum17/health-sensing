# Health Sensing

Health Sensing is a Streamlit lab app used for beginner-friendly vision and hearing
psychophysics assignments.

This repository is intentionally scaffolded so students implement a focused set of
TODO functions instead of building the full app from scratch.

## First 10 Minutes

1. Install and run setup from [docs/install.md](docs/install.md).
2. Start the app: `uv run streamlit run app.py`.
3. Read [docs/assignment.md](docs/assignment.md) once before coding.
4. Keep [docs/student_functions.md](docs/student_functions.md) open while implementing TODOs.

## What You Edit

Students should edit only files in `pages/`:

- experiment-specific TODOs in page files
- shared 3AFC TODOs in `pages/_shared_3afc_student.py`

Do not rename function signatures unless an instructor explicitly asks.

## Assignment File Map

- `pages/greyscale_resolution.py`
- `pages/smallest_noticeable_size.py`
- `pages/pitch_frequency_range.py`
- `pages/sound_gap_detection.py`
- `pages/amplitude_threshold.py`
- `pages/pitch_threshold.py`
- `pages/_shared_3afc_student.py` (shared 3AFC logic)

## Quick Setup

### Option A: Git Clone

```sh
git clone https://github.com/priyanshum17/healthsensing
cd healthsensing
```

### Option B: ZIP Download

1. Open the repository on GitHub.
2. Click `Code` -> `Download ZIP`.
3. Extract ZIP.
4. Open extracted `healthsensing` folder in VS Code.
5. Open terminal in that folder.

## Run (All Platforms)

```sh
uv python install 3.11
uv sync
uv run streamlit run app.py
```

Open `http://localhost:8501`.

## Windows Options

### PowerShell

```powershell
uv python install 3.11
uv sync
uv run streamlit run app.py
```

### Git Bash

```bash
uv python install 3.11
uv sync
uv run streamlit run app.py
```

If `git` is missing on Windows, install Git for Windows:
https://gitforwindows.org

## Safety and Quality Checklist (Before Submission)

1. `uv run ruff check .`
2. `uv run pytest`
3. Confirm no assignment TODO still raises `NotImplementedError`
4. Confirm each page runs without crashing
5. Confirm adaptive values are clamped to configured limits

## Documentation Index

- [docs/install.md](docs/install.md): setup and troubleshooting
- [docs/assignment.md](docs/assignment.md): assignment scope and workflow
- [docs/student_functions.md](docs/student_functions.md): detailed per-function guidance
- [docs/app_logic.md](docs/app_logic.md): architecture and runtime flow

## Project Structure

```text
healthsensing/
  app.py
  config/
    test_config.json
  docs/
    app_logic.md
    assignment.md
    install.md
    student_functions.md
  pages/
    _shared_3afc_student.py
    amplitude_threshold.py
    greyscale_resolution.py
    pitch_frequency_range.py
    pitch_threshold.py
    smallest_noticeable_size.py
    sound_gap_detection.py
  utils/
  tests/
```

## If You Are Stuck

1. Check [docs/install.md](docs/install.md).
2. Check [docs/student_functions.md](docs/student_functions.md).
3. Ask for help with command output and traceback included.
