# Installation and Troubleshooting

This guide focuses on reliable setup and fast recovery when something fails.

## Prerequisites

- Python 3.11 or newer
- Internet connection for dependency resolution
- Terminal access (`Terminal` on macOS, `PowerShell` on Windows)

## Standard Setup

From the project root:

```sh
make run
```

This command installs prerequisites (via `uv`) and starts Streamlit at
`http://localhost:8501`.

## Windows: If `make` Does Not Work

Use this fallback flow directly in PowerShell:

```powershell
uv python install 3.11
$env:UV_CACHE_DIR = ".uv-cache"
uv sync
uv run streamlit run app.py
```

If port `8501` is occupied:

```powershell
uv run streamlit run app.py --server.port 8502
```

## Manual Setup (Any OS)

Use this when you do not want to use Make:

```sh
uv python install 3.11
UV_CACHE_DIR=.uv-cache uv sync
UV_CACHE_DIR=.uv-cache uv run streamlit run app.py
```

## Platform-Specific Notes

### macOS

If command line tools are missing:

```sh
xcode-select --install
```

If `uv` is not in PATH, add this to `~/.zshrc`:

```sh
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
```

Then reload:

```sh
source ~/.zshrc
```

### Windows

If execution policy blocks scripts:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

If you want to install `make`, use one of these:

- Chocolatey: `choco install make`
- Scoop: `scoop install main/make`
- Git Bash (if already installed)

## Symptom-Based Troubleshooting

### `make` command not found

Cause: no GNU Make in current shell.  
Fix: use the Windows fallback block above, or install `make`.

### `uv` command not found

Cause: `uv` not installed or not on PATH.  
Fix:

- Install `uv`: https://docs.astral.sh/uv/getting-started/installation/
- Restart terminal
- Re-run commands

### Permission error on uv cache path

Cause: default cache directory blocked by environment policy.  
Fix: force local cache directory:

```sh
UV_CACHE_DIR=.uv-cache uv sync
UV_CACHE_DIR=.uv-cache uv run streamlit run app.py
```

PowerShell variant:

```powershell
$env:UV_CACHE_DIR = ".uv-cache"
uv sync
uv run streamlit run app.py
```

### Python version mismatch

Check:

```sh
python --version
```

Install required version:

```sh
uv python install 3.11
```

### Streamlit starts but app page is blank

Fix sequence:

1. Check terminal for import/runtime errors.
2. Hard refresh browser (`Ctrl+Shift+R` or `Cmd+Shift+R`).
3. Restart Streamlit process.

### Audio does not play

Fix sequence:

1. Verify OS output device.
2. Verify browser tab is not muted.
3. Try a different browser.

### Dependency installation fails

Fix sequence:

1. Confirm network access.
2. Remove environment and reinstall:

```sh
make clean
make run
```

If Make is unavailable:

```sh
rm -rf .venv
UV_CACHE_DIR=.uv-cache uv sync
```

## Reporting Issues

When opening an issue, include:

- OS and version
- Python version
- full command run
- full terminal output
