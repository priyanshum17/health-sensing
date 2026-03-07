# Installation Guide

This guide covers installation on macOS and Windows, including common fixes.

## Prerequisites

- Python 3.11 or newer
- Internet access for dependency installation
- Terminal access (`Terminal` on macOS, `PowerShell` on Windows)

## Standard Installation (Recommended)

From the project root:

```sh
make run
```

This performs setup and starts Streamlit at `http://localhost:8501`.

## Manual Installation with `uv`

If you do not want to use `make`:

```sh
uv python install 3.11
uv sync
uv run streamlit run app.py
```

## macOS Setup Notes

### 1. Xcode Command Line Tools missing

If build tools are missing:

```sh
xcode-select --install
```

### 2. `uv` command not found after install

Add common install paths to your shell profile (`~/.zshrc`):

```sh
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
```

Then reload your shell:

```sh
source ~/.zshrc
```

### 3. Python version mismatch

Check version:

```sh
python3 --version
```

If needed, explicitly install 3.11:

```sh
uv python install 3.11
```

## Windows Setup Notes

Use PowerShell in the project directory.

### 1. `make` may not be available in CMD/PowerShell

`make` is typically preinstalled on Unix-like systems, but not on standard Windows shells.
If `make run` fails, use one of the options below.

Option A: run the app without `make` (works everywhere on Windows):

```powershell
uv python install 3.11
uv sync
uv run streamlit run app.py
```

Option B: install GNU `make` with Chocolatey:

1. Install Chocolatey from: https://chocolatey.org/install
2. Open an elevated PowerShell or Command Prompt (Run as Administrator)
3. Install make:

```powershell
choco install make
```

4. Restart terminal and verify:

```powershell
make -v
```

Option C: install GNU `make` with Scoop:

1. Install Scoop from: https://scoop.sh
2. In PowerShell:

```powershell
scoop bucket add main
scoop install main/make
```

3. Restart terminal and verify:

```powershell
make -v
```

Option D: use Git Bash (includes GNU tooling in many setups):

1. Install Git for Windows: https://gitforwindows.org
2. Open **Git Bash** (instead of CMD/PowerShell)
3. Verify:

```bash
make -v
```

If `make` is still unavailable in Git Bash, use Option A manual commands.

### 2. `uv` is not recognized

Install `uv` from the official installer and reopen PowerShell:

- https://docs.astral.sh/uv/getting-started/installation/

### 3. Execution policy blocks scripts

If PowerShell blocks local scripts:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then restart PowerShell.

### 4. Port 8501 already in use

Run Streamlit on a different port:

```powershell
uv run streamlit run app.py --server.port 8502
```

## Common Troubleshooting

### Dependency install fails

- Confirm network access
- Delete and recreate environment:

```sh
make clean
make run
```

### Streamlit launches but page is blank

- Check terminal logs for Python errors
- Hard refresh browser (`Ctrl+Shift+R` / `Cmd+Shift+R`)
- Restart Streamlit process

### Audio does not play in hearing tests

- Confirm system output device is correct
- Disable browser tab mute
- Try another browser (Chrome/Edge/Safari)

## Getting Help

When reporting installation issues, include:

- OS and version
- Python version
- Exact command run
- Full terminal error output
