# Health Sensing

Health Sensing is a Streamlit application for running vision and hearing
psychophysics exercises in a structured lab flow.

## What This Repo Contains

Implemented experiment pages:

- Contrast sensitivity (Pelli-style progression)
- Visual resolution (Tumbling E)
- Pitch frequency range screening
- Sound gap detection (3AFC adaptive)
- Amplitude discrimination (3AFC adaptive)
- Pitch discrimination threshold (3AFC adaptive)

## How The App Works

- `app.py` is the multipage home screen and experiment launcher.
- Each file in `pages/` is one experiment workflow.
- Test parameters are centralized in `config/test_config.json`.
- Shared logic modules in `utils/`: `ui.py`, `adaptive_3afc.py`,
  `three_afc.py`, `audio_tools.py`, and `test_config.py`.

For a deeper walkthrough of runtime flow and module responsibilities, see
[docs/app_logic.md](docs/app_logic.md).

## Requirements

- Python 3.11+
- `uv` package manager

## Assignment Setup

Use this section if you are new to Git or `uv`.

### Step 1: Get The Project Files

Choose one option.

Option A: Use Git

```sh
git clone https://github.com/priyanshum17/healthsensing
cd healthsensing
```

If you already cloned before and want the latest changes:

```sh
cd healthsensing
git pull
```

Option B: Download ZIP from GitHub (no Git required)

1. Open the repository page on GitHub.
2. Click `Code`.
3. Click `Download ZIP`.
4. Extract the ZIP to a folder you can access.
5. Open a terminal in the extracted `healthsensing` folder.

## Open In VS Code

From terminal in the project folder:

```sh
code .
```

Or open VS Code manually and choose `File` -> `Open Folder...` -> `healthsensing`.

### Step 2: Install `uv`

Install `uv` from the official guide:

- https://docs.astral.sh/uv/getting-started/installation/

After installing, close and reopen your terminal.

### Step 3: Run The App

Use the command block for your platform/terminal.

macOS/Linux:

```sh
uv python install 3.11
UV_CACHE_DIR=.uv-cache uv sync
UV_CACHE_DIR=.uv-cache uv run streamlit run app.py
```

Windows PowerShell:

```powershell
uv python install 3.11
$env:UV_CACHE_DIR = ".uv-cache"
uv sync
uv run streamlit run app.py
```

Windows Git Bash:

```bash
uv python install 3.11
UV_CACHE_DIR=.uv-cache uv sync
UV_CACHE_DIR=.uv-cache uv run streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

## Developer Commands

- install/sync dependencies:
```sh
uv python install 3.11
UV_CACHE_DIR=.uv-cache uv sync
```
- run app:
```sh
UV_CACHE_DIR=.uv-cache uv run streamlit run app.py
```
- lint:
```sh
UV_CACHE_DIR=.uv-cache uv run ruff check .
```
- tests:
```sh
UV_CACHE_DIR=.uv-cache uv run pytest
```
- clean local artifacts:
```sh
rm -rf .venv __pycache__ .pytest_cache coverage
```

Windows PowerShell clean command:

```powershell
Remove-Item -Recurse -Force .venv, __pycache__, .pytest_cache, coverage -ErrorAction SilentlyContinue
```

## Repository Structure

```text
healthsensing/
  app.py
  pages/
    amplitude_threshold.py
    greyscale_resolution.py
    pitch_frequency_range.py
    pitch_threshold.py
    smallest_noticeable_size.py
    sound_gap_detection.py
  utils/
    adaptive_3afc.py
    audio_tools.py
    test_config.py
    three_afc.py
    ui.py
  config/
    test_config.json
  docs/
    app_logic.md
    assignment.md
    install.md
  tests/
```

## Troubleshooting

Start with [docs/install.md](docs/install.md). It includes:

- OS-specific install flows
- failure-mode troubleshooting by error symptom
- command-level recovery steps

## Notes

- The app is intended for local use.
- Runtime state is session-based (stored in Streamlit session state).
