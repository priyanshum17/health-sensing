.PHONY: setup run lint test clean ensure-uv ensure-python

PYTHON_VERSION=3.11
VENV=.venv
APP=app.py

ensure-uv:
	@if ! command -v uv >/dev/null 2>&1; then \
		echo "Installing uv..."; \
		curl -Ls https://astral.sh/uv/install.sh | sh; \
		export PATH="$$HOME/.local/bin:$$HOME/.cargo/bin:$$PATH"; \
	fi

ensure-python: ensure-uv
	@export PATH="$$HOME/.local/bin:$$HOME/.cargo/bin:$$PATH"; \
	uv python install $(PYTHON_VERSION)

setup: ensure-python
	@export PATH="$$HOME/.local/bin:$$HOME/.cargo/bin:$$PATH"; \
	echo "Creating environment and installing dependencies..."; \
	uv sync

run: setup
	@export PATH="$$HOME/.local/bin:$$HOME/.cargo/bin:$$PATH"; \
	uv run streamlit run $(APP)

clean:
	rm -rf .venv
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf coverage