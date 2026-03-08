# Installation and Troubleshooting

This guide focuses on reliable setup and fast recovery when something fails.

## Prerequisites

- Python 3.11 or newer
- Internet connection for dependency resolution
- Terminal access (`Terminal` on macOS/Linux, `PowerShell` or `Git Bash` on Windows)

## Before You Start (Beginner Checklist)

1. Confirm you can open a terminal.
2. Confirm you can access the project folder.
3. Install `uv` from: https://docs.astral.sh/uv/getting-started/installation/
4. Close and reopen your terminal after installing `uv`.

## Get The Project Code

Choose one approach.

### Option A: Clone with Git

```sh
git clone https://github.com/priyanshum17/healthsensing
cd healthsensing
```

If already cloned:

```sh
cd healthsensing
git pull
```

### Option B: Download ZIP from GitHub

1. Open the repository on GitHub.
2. Click `Code` -> `Download ZIP`.
3. Extract the archive.
4. Open terminal in the extracted `healthsensing` folder.

## Standard Setup Commands

### macOS/Linux

```sh
uv python install 3.11
uv sync
uv run streamlit run app.py
```

### Windows PowerShell

```powershell
uv python install 3.11
uv sync
uv run streamlit run app.py
```

### Windows Git Bash

```bash
uv python install 3.11
uv sync
uv run streamlit run app.py
```

When the app starts, open `http://localhost:8501`.

## Symptom-Based Troubleshooting

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
uv sync
uv run streamlit run app.py
```

PowerShell version:

```powershell
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

macOS/Linux or Git Bash:

```bash
rm -rf .venv
uv sync
uv run streamlit run app.py
```

PowerShell:

```powershell
Remove-Item -Recurse -Force .venv -ErrorAction SilentlyContinue
uv sync
uv run streamlit run app.py
```

### Git is not recognized (Windows)

Cause: Git not installed, or terminal needs restart.  
Fix:

1. Install Git for Windows: https://gitforwindows.org
2. Close all terminals.
3. Open a new PowerShell or Git Bash window.
4. Run `git --version` to verify.

### You downloaded ZIP and cannot run commands in the right folder

Cause: terminal is not in the project root folder.  
Fix:

1. In terminal, run `pwd` (or `Get-Location` in PowerShell).
2. Change directory to the folder containing `app.py`.
3. Re-run setup commands.

## Reporting Issues

When opening an issue, include:

- OS and version
- Python version
- full command run
- full terminal output
