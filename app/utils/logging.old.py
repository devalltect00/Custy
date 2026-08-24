# app/utils/logging.old.py

import logging
from rich.logging import RichHandler
from rich.console import Console
from typing import Optional
from app.config.config_loader import get_config
from app.theme import theme

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

    if debug:
        # log_cfg["level"] = "DEBUG"
        level_str = "DEBUG"
        log_cfg["show_level"] = True
    elif level is not None:
        level_str = level.value if hasattr(level, "value") else level
    else:
        level_str = log_cfg.get("level", "INFO")
        
    logging_level = getattr(logging, level_str.upper(), logging.INFO)

    logging.basicConfig(
        level=logging_level,
        format="%(message)s",
        handlers=[
            RichHandler(
                console=console,
                markup=log_cfg.get("markup", True),
                rich_tracebacks=log_cfg.get("rich_tracebacks", True),
                show_time=log_cfg.get("show_time", False),
                show_level=log_cfg.get("show_level", False),
                highlighter=None,  # prevents weird color (green) strings
            )
        ],
    )
