# tests/cli/commands/main/test_options.py

"""Smoke tests for CLI option metadata."""

from app.cli.commands.main import options


def test_options_exist():
    assert options.NoBannerOption is not None
    assert options.DebugOption is not None
    assert options.LogLevelOption is not None
