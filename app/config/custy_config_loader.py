# app/config/custy_config_loader.py

import tomllib
from functools import lru_cache
from pathlib import Path

from app.constants.path import CUSTY_SETTINGS


@lru_cache
def load_custy_config(path: str = CUSTY_SETTINGS) -> dict:
    """
    Load and parse the .custy.toml config file.
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
