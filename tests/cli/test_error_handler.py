# tests/cli/test_error_handler.py

"""Tests for the protected Custy CLI error boundary."""

import sys

import pytest

from app.cli import error_handler
from app.core.exceptions.validation_error import ValidationError
from app.core.shared import ConfigurationError


class TestHandleCliErrors:
    """Verifies normal and debug exception presentation."""

    def test_renders_structured_validation_error(self, monkeypatch):
        """Uses the structured Rich renderer and preserves the exit code."""

        rendered = []
        monkeypatch.setattr(
            error_handler,
            "show_structured_error",
            rendered.append,
        )
        failure = ValidationError(
            message="Version target is missing.",
            hint="Set version_file to auto.",
            code="VERSION_FILE_NOT_FOUND",
            exit_code=3,
        )

        with pytest.raises(SystemExit) as exc_info:
            error_handler.handle_cli_errors(lambda: (_ for _ in ()).throw(failure))

        assert exc_info.value.code == 3
        assert rendered == [failure]

    def test_renders_known_custy_error_without_traceback(self, monkeypatch):
        """Displays configuration errors through the shared error panel."""

        messages = []
        monkeypatch.setattr(error_handler, "show_error", messages.append)

        with pytest.raises(SystemExit) as exc_info:
            error_handler.handle_cli_errors(
                lambda: (_ for _ in ()).throw(ConfigurationError("Bad config"))
            )

        assert exc_info.value.code == 1
        assert messages == ["Bad config"]

    def test_summarizes_unexpected_error_in_normal_mode(self, monkeypatch):
        """Adds a debug hint instead of exposing a normal-mode traceback."""

        messages = []
        monkeypatch.setattr(error_handler, "show_error", messages.append)
        monkeypatch.setattr(sys, "argv", ["custy", "validate"])

        with pytest.raises(SystemExit):
            error_handler.handle_cli_errors(
                lambda: (_ for _ in ()).throw(RuntimeError("boom"))
            )

        assert "boom" in messages[0]
        assert "--debug" in messages[0]

    def test_reraises_unexpected_error_in_debug_mode(self, monkeypatch):
        """Preserves the original exception when debug was requested."""

        monkeypatch.setattr(sys, "argv", ["custy", "--debug", "validate"])

        with pytest.raises(RuntimeError, match="boom"):
            error_handler.handle_cli_errors(
                lambda: (_ for _ in ()).throw(RuntimeError("boom"))
            )
