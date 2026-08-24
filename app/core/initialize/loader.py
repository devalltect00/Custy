# app/core/initialize/loader.py

from importlib.resources import files
from pathlib import Path

from app.constants.path import (
    THIS_PROJECT_SOURCE,
)


def load_template(name: str) -> str:
    # user override
    user_path = Path("templates") / name
    if user_path.exists():
        return user_path.read_text(encoding="utf-8")

    # fallback to package
    return (
        files(f"{THIS_PROJECT_SOURCE}.templates")
        .joinpath(name)
        .read_text(encoding="utf-8")
    )
