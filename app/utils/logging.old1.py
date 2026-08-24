# app/utils/logging.old1.py

import re
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from rich.logging import RichHandler
from rich.console import Console
from typing import Optional

from app.config.config_loader import get_config
from app.theme import theme
from app.utils.parsing import parse_size
from app.cli.constants.enums import (
    LogLevelChoices,
)
from app.constants.path import (
    LOG_DIRECTORY,
    LOG_FILENAME,
)

def setup_logging(level: Optional[str] = None, debug: bool = False) -> None:
    """
    Configure application-wide logging using Rich.

    Args:
        config (dict): configuration dict

    Returns:
        None
    """

    console = Console(theme=theme.to_rich_theme())

    config = get_config()
    # log_cfg = config.resolve(
    #     cli_value=None,
    #     config_keys=["cli", "logging", "level"],
    #     default="INFO",
    # )
    log_cfg = config.get_section("logging")

    # =========================
    # Resolve logging level
    # =========================
    if debug:
        # log_cfg["level"] = "DEBUG"
        level_str = "DEBUG"
        log_cfg["show_level"] = True
    elif level is not None:
        level_str = level.value if hasattr(level, "value") else level
    else:
        level_str = log_cfg.get("level", LogLevelChoices.INFO)

    logging_level = getattr(
        logging,
        level_str.upper(),
        logging.INFO
    )

    console_formatter = log_cfg.get(
        "console_format",
        "%(message)s"
    )

    ##### File logging setup (with rotation) #####
    log_file_cfg = config.get_section("logging", "file")
    # =========================
    # Log directory
    # =========================
    log_dir = Path(log_file_cfg.get("log_dir", LOG_DIRECTORY))
    log_dir.mkdir(parents=True, exist_ok=True)

    # =========================
    # Log file
    # =========================
    log_file = log_dir / log_file_cfg.get("log_file", LOG_FILENAME)

    # =========================
    # File handler
    # =========================
    log_file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=parse_size(
                log_file_cfg.get(
                "max_bytes",
                "10MB"
            ),
        ),
        backupCount=log_file_cfg.get(
            "backup_count",
            5
        ),
        encoding="utf-8",
    )

    log_file_handler.setLevel(logging_level)
    # log_file_handler.setLevel(logging.DEBUG)

    # =========================
    # File formatter
    # =========================
    # File log format (can be more detailed than console)
    # file_formatter = logging.Formatter(
    file_formatter = SeperatorFormatter(
        log_file_cfg.get(
            "file_format",
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
    )

    log_file_handler.setFormatter(file_formatter)

    # =========================
    # Rich console handler
    # =========================
    rich_handler = RichHandler(
        console=console,
        markup=log_cfg.get("markup", True),
        rich_tracebacks=log_cfg.get("rich_tracebacks", True),
        show_time=log_cfg.get("show_time", False),
        show_level=log_cfg.get("show_level", False),
        highlighter=None,  # prevents weird color (green) strings
    )

    ##### Console logging setup with RichHandler #####
    logging.basicConfig(
        level=logging_level,
        format=console_formatter,
        handlers=[
            # Rich console output handler
            rich_handler,

            # File output handler
            log_file_handler,
        ],
    )

class SeperatorFormatter(logging.Formatter):
    """
    Custom formatter for file logs.

    Features:
    - Converts empty messages into separators
    - Removes Rich markup tags
    - Keeps normal logs fully formatted
    - Improves readability for file logging

    Examples:
        logger.info("")
        -> --------------------------------------------------

        logger.info("[cyan]Hello[/cyan]")
        -> Hello
    """

    # Matches Rich tags:
    # [cyan]
    # [/cyan]
    # [bold]
    # [/bold]
    # [dim]
    # [/dim]
    RICH_TAG_PATTERN = re.compile(r"\[/?[^\]]+\]")

    TITLE_SEPARATOR = "=" * 50
    COMMON_SEPARATOR = "-" * 50

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log records.

        Args:
            record (logging.LogRecord):
                Log record instance.

        Returns:
            str:
                Formatted log message.
        """

        # Original formatted log
        original = super().format(record)

        # Original message only
        message = record.getMessage()

        # print(f"~{message}>{original}<")

        # =========================
        # Remove Rich markup
        # =========================
        # Remove Rich markup tags from the original formatted log
        cleaned_original = self.RICH_TAG_PATTERN.sub("", original)
        cleaned_message = self.RICH_TAG_PATTERN.sub("", message)

        # =========================
        # Empty line -> separator
        # =========================
        if cleaned_message.strip() == "":
            return self.COMMON_SEPARATOR

        # =========================
        # STEP START formatting
        # =========================
        if "CLI COMMAND" in cleaned_message:
            return (
                f"\n"
                f"{self.TITLE_SEPARATOR}\n"
                f"{cleaned_original}\n"
                f"{self.TITLE_SEPARATOR}\n"
            )

        return cleaned_original
