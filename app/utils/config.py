from functools import lru_cache
from pathlib import Path

import tomllib


@lru_cache
def load_custor_config(path: str = ".custor.toml") -> dict:
    """
    Load and parse the .custor.toml config file.
    Returns a dict with 'release' section, or empty dict if not found.

    Memoized for reuse across modules.
    """
    config_path = Path(path)
    if config_path.exists():
        try:
            with config_path.open("rb") as f:
                data = tomllib.load(f)
            return data.get("release", {})
        except Exception as e:
            print(f"⚠️ Failed to parse {path}: {e}")
    return {}
