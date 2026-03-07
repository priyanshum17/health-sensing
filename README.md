# Health Sensing

A Streamlit application for running six standardized human sensory experiments across vision and hearing.

## Overview

This project helps users measure and record sensing limits using guided, page-by-page workflows.

Implemented experiment pages:

- Contrast sensitivity (Pelli-style)
- Visual resolution (Tumbling E)
- Pitch frequency range
- Sound gap detection (3AFC adaptive)
- Amplitude discrimination (3AFC adaptive)
- Pitch discrimination threshold (3AFC adaptive)

Each experiment page includes:

- Step-by-step instructions
- Interactive controls for running the test
- Calculated metrics where applicable
- A structured result-saving section

## Requirements

- Python 3.11+
- `uv` package manager (recommended; auto-installed via `make`)

## Installation

### Quick start

```sh
# Clone and enter project
git clone https://github.com/priyanshum17/healthsensing
cd healthsensing

# Install dependencies and run app
make run
```

Then open: `http://localhost:8501`

### Manual setup (without Makefile)

```sh
uv python install 3.11
uv sync
uv run streamlit run app.py
```

For OS-specific setup and troubleshooting, see [docs/install.md](docs/install.md).

### Windows note about `make`

`make` commands are commonly available on Unix-like systems but may be missing in
standard Windows CMD/PowerShell environments.

If `make run` fails on Windows, either:

- use the manual `uv` commands above, or
- install GNU `make` via Chocolatey/Scoop, or
- run from Git Bash if `make` is available there.

Detailed steps are in [docs/install.md](docs/install.md).

## Project Structure

```text
healthsensing/
  app.py                     # Homepage with experiment tiles and objective summary
  pages/                     # Individual experiment pages
    greyscale_resolution.py
    smallest_noticeable_size.py
    pitch_frequency_range.py
    sound_gap_detection.py
    amplitude_threshold.py
    pitch_threshold.py
  utils/                     # Shared helpers
    navigation.py            # Navigation and CTA buttons
    home.py                  # Homepage tile rendering
    experiment_layout.py     # Shared page header/instructions/save-result blocks
    audio_tools.py           # WAV audio generation for hearing experiments
    adaptive_3afc.py         # Shared 3AFC adaptive staircase logic
  .streamlit/config.toml     # Streamlit theme/runtime config
  pyproject.toml             # Python and dependency metadata
  Makefile                   # Setup/run/clean shortcuts
  docs/
    install.md               # Detailed installation and troubleshooting
    assignment.md            # Assignment requirements/specification
```

## Running the App

```sh
make run
```

This command:

1. Ensures `uv` is installed
2. Ensures Python 3.11 is available
3. Syncs dependencies into `.venv`
4. Starts Streamlit using `app.py`

## Available Make Targets

- `make setup` - install Python and dependencies
- `make run` - start the Streamlit app
- `make clean` - remove local environment/artifacts

## Notes

- Saved experiment results are currently stored in Streamlit session state (per running session).
- The app is optimized for local execution.

## Documentation

- Installation and troubleshooting: [docs/install.md](docs/install.md)
- Assignment details: [docs/assignment.md](docs/assignment.md)
