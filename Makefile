.PHONY: setup run lint test clean ensure-uv ensure-python

PYTHON_VERSION=3.11
VENV=.venv
APP=app.py
UV_CACHE_DIR=.uv-cache

ensure-uv:
	@if ! command -v uv >/dev/null 2>&1; then \
		echo "Installing uv..."; \
		curl -Ls https://astral.sh/uv/install.sh | sh; \
		export PATH="$$HOME/.local/bin:$$HOME/.cargo/bin:$$PATH"; \
	fi

ensure-python: ensure-uv
	@export PATH="$$HOME/.local/bin:$$HOME/.cargo/bin:$$PATH"; \
	export UV_CACHE_DIR=$(UV_CACHE_DIR); \
	uv python install $(PYTHON_VERSION)

setup: ensure-python
	@export PATH="$$HOME/.local/bin:$$HOME/.cargo/bin:$$PATH"; \
	export UV_CACHE_DIR=$(UV_CACHE_DIR); \
	echo "Creating environment and installing dependencies..."; \
	uv sync

run: setup
	@export PATH="$$HOME/.local/bin:$$HOME/.cargo/bin:$$PATH"; \
	export UV_CACHE_DIR=$(UV_CACHE_DIR); \
	uv run streamlit run $(APP)

lint: setup
	@export PATH="$$HOME/.local/bin:$$HOME/.cargo/bin:$$PATH"; \
	export UV_CACHE_DIR=$(UV_CACHE_DIR); \
	uv run ruff check .

test: setup
	@export PATH="$$HOME/.local/bin:$$HOME/.cargo/bin:$$PATH"; \
	export UV_CACHE_DIR=$(UV_CACHE_DIR); \
	uv run pytest

clean:
	rm -rf .venv
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf coverage
