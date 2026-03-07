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
- Shared logic modules in `utils/`:
- `ui.py`: shared page layout and navigation components
- `adaptive_3afc.py`: generic adaptive staircase state/update logic
- `three_afc.py`: reusable 3AFC page interaction/feedback/plot helpers
- `audio_tools.py`: WAV generation for tones and noise bursts
- `test_config.py`: cached loader for JSON config

For a deeper walkthrough of runtime flow and module responsibilities, see
[docs/app_logic.md](docs/app_logic.md).

## Requirements

- Python 3.11+
- `uv` package manager

## Quick Start

```sh
git clone https://github.com/priyanshum17/healthsensing
cd healthsensing
make run
```

Open `http://localhost:8501`.

## Windows Fallback (No `make`)

If `make` is not available or fails in PowerShell/CMD, run:

```powershell
uv python install 3.11
$env:UV_CACHE_DIR = ".uv-cache"
uv sync
uv run streamlit run app.py
```

This is the supported fallback path for Windows users who cannot run Make
commands.

## Developer Commands

- `make setup`: install Python and dependencies
- `make run`: launch Streamlit app
- `make lint`: run Ruff checks
- `make test`: run pytest suite
- `make clean`: remove local environment artifacts

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
