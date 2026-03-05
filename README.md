# Health Sensing

A Streamlit application for running six interactive human sensory experiments across sight and hearing.

## Overview

This project helps users measure and record sensing limits using guided, page-by-page workflows.

Implemented experiment pages:

- Greyscale resolution
- Angular field of view
- Smallest noticeable size
- Pitch frequency range
- Sound gap detection
- Amplitude threshold

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

## Project Structure

```text
healthsensing/
  app.py                     # Homepage with experiment tiles and objective summary
  pages/                     # Individual experiment pages
    greyscale_resolution.py
    angular_field_of_view.py
    smallest_noticeable_size.py
    pitch_frequency_range.py
    sound_gap_detection.py
    amplitude_threshold.py
  utils/                     # Shared helpers
    navigation.py            # Navigation and CTA buttons
    home.py                  # Homepage tile rendering
    experiment_layout.py     # Shared page header/instructions/save-result blocks
    audio_tools.py           # WAV audio generation for hearing experiments
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
