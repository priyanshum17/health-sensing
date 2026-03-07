import json
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def load_test_config() -> dict:
    """Load centralized test configuration from JSON."""
    config_path = Path(__file__).resolve().parent.parent / "config" / "test_config.json"
    with config_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)
