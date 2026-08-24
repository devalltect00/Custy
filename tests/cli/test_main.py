# tests/cli/test_main.py

"""Tests for CLI application registration."""
from app.cli.main import app

def test_app_exists():
    assert app is not None
