# tests/utils/test_logging_setup.py

"""
tests/utils/test_logging_setup.py

Unit tests for application logging configuration.

These tests verify that setup_logging() correctly resolves logging
configuration, constructs logging handlers, and configures the Python
logging subsystem.
"""

import logging
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from app.cli.constants.enums import LogLevelChoices
from app.utils import logging as logging_utils


class DummyConfig:
    """Simple configuration object used for testing."""

    def __init__(self):
        self.logging = {
            "level": "INFO",
            "console_format": "%(message)s",
            "markup": True,
            "rich_tracebacks": True,
            "show_time": False,
            "show_level": False,
        }

        self.file = {
            "level": "DEBUG",
            "log_dir": "logs",
            "log_file": "custy.log",
            "max_bytes": "10MB",
            "backup_count": 3,
            "file_format": "%(message)s",
        }

    def get_section(self, *keys):
        """Return configuration sections."""

        if keys == ("logging",):
            return self.logging

        if keys == ("logging", "file"):
            return self.file

        return {}


class TestSetupLogging:
    """Tests for setup_logging()."""

    # ==========================================================
    # Helpers
    # ==========================================================

    def _prepare(
        self,
        monkeypatch,
    ):
        """Prepare all mocked collaborators."""

        config = DummyConfig()

        monkeypatch.setattr(
            logging_utils,
            "get_config",
            lambda: config,
        )

        parse_size = MagicMock(return_value=10485760)

        monkeypatch.setattr(
            logging_utils,
            "parse_size",
            parse_size,
        )

        rich_handler = MagicMock(name="RichHandler")

        rich_handler_cls = MagicMock(
            return_value=rich_handler,
        )

        monkeypatch.setattr(
            logging_utils,
            "RichHandler",
            rich_handler_cls,
        )

        rotating_handler = MagicMock(name="RotatingFileHandler")

        rotating_cls = MagicMock(
            return_value=rotating_handler,
        )

        monkeypatch.setattr(
            logging_utils,
            "RotatingFileHandler",
            rotating_cls,
        )

        basic_config = MagicMock()

        monkeypatch.setattr(
            logging,
            "basicConfig",
            basic_config,
        )

        mkdir = MagicMock()

        monkeypatch.setattr(
            Path,
            "mkdir",
            mkdir,
        )

        return {
            "config": config,
            "parse_size": parse_size,
            "rich_cls": rich_handler_cls,
            "rich": rich_handler,
            "rotating_cls": rotating_cls,
            "rotating": rotating_handler,
            "basic_config": basic_config,
            "mkdir": mkdir,
        }

    # ==========================================================
    # Logging level
    # ==========================================================

    def test_debug_mode_forces_debug_level(
        self,
        monkeypatch,
    ):
        """Debug mode overrides the configured log level."""

        env = self._prepare(monkeypatch)

        logging_utils.setup_logging(debug=True)

        env["basic_config"].assert_called_once()

        _, kwargs = env["basic_config"].call_args

        assert kwargs["level"] == logging.DEBUG

        assert env["config"].logging["show_level"] is True

    @pytest.mark.parametrize(
        "level",
        [
            "WARNING",
            LogLevelChoices.ERROR,
            LogLevelChoices.INFO,
        ],
    )
    def test_explicit_level_overrides_configuration(
        self,
        monkeypatch,
        level,
    ):
        """Uses the explicitly supplied logging level."""

        env = self._prepare(monkeypatch)

        logging_utils.setup_logging(level=level)

        _, kwargs = env["basic_config"].call_args

        expected = getattr(
            logging,
            str(level).split(".")[-1].upper(),
        )

        assert kwargs["level"] == expected

    def test_uses_configuration_level_by_default(
        self,
        monkeypatch,
    ):
        """Uses the configured logging level when no override is supplied."""

        env = self._prepare(monkeypatch)

        env["config"].logging["level"] = "ERROR"

        logging_utils.setup_logging()

        _, kwargs = env["basic_config"].call_args

        assert kwargs["level"] == logging.ERROR

    # ==========================================================
    # File handler
    # ==========================================================

    def test_creates_rotating_file_handler(
        self,
        monkeypatch,
    ):
        """Creates the rotating file handler."""

        env = self._prepare(monkeypatch)

        logging_utils.setup_logging()

        env["parse_size"].assert_called_once_with("10MB")

        env["rotating_cls"].assert_called_once()

        _, kwargs = env["rotating_cls"].call_args

        assert kwargs["backupCount"] == 3
        assert kwargs["encoding"] == "utf-8"

    def test_creates_log_directory(
        self,
        monkeypatch,
    ):
        """Creates the configured log directory."""

        env = self._prepare(monkeypatch)

        logging_utils.setup_logging()

        env["mkdir"].assert_called_once_with(
            parents=True,
            exist_ok=True,
        )

    def test_sets_file_handler_level(
        self,
        monkeypatch,
    ):
        """Sets the configured file logging level."""

        env = self._prepare(monkeypatch)

        logging_utils.setup_logging()

        env["rotating"].setLevel.assert_called_once_with(
            logging.DEBUG,
        )

    def test_sets_separator_formatter(
        self,
        monkeypatch,
    ):
        """Installs the custom separator formatter."""

        env = self._prepare(monkeypatch)

        env["rotating"].setFormatter = MagicMock()

        logging_utils.setup_logging()

        formatter = env["rotating"].setFormatter.call_args.args[0]

        assert isinstance(
            formatter,
            logging_utils.SeparatorFormatter,
        )

    # ==========================================================
    # Rich handler
    # ==========================================================

    def test_creates_rich_handler(
        self,
        monkeypatch,
    ):
        """Creates the Rich console handler."""

        env = self._prepare(monkeypatch)

        logging_utils.setup_logging()

        env["rich_cls"].assert_called_once()

        _, kwargs = env["rich_cls"].call_args

        assert kwargs["console"] is logging_utils.console
        assert kwargs["highlighter"] is None

    # ==========================================================
    # basicConfig
    # ==========================================================

    def test_basic_config_receives_handlers(
        self,
        monkeypatch,
    ):
        """Registers both console and file handlers."""

        env = self._prepare(monkeypatch)

        logging_utils.setup_logging()

        _, kwargs = env["basic_config"].call_args

        handlers = kwargs["handlers"]

        assert len(handlers) == 2

        assert env["rich"] in handlers
        assert env["rotating"] in handlers

    def test_uses_console_format(
        self,
        monkeypatch,
    ):
        """Uses the configured console format."""

        env = self._prepare(monkeypatch)

        env["config"].logging["console_format"] = "%(levelname)s %(message)s"

        logging_utils.setup_logging()

        _, kwargs = env["basic_config"].call_args

        assert kwargs["format"] == "%(levelname)s %(message)s"
