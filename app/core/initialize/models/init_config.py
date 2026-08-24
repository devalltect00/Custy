# app/core/initialize/models/init_config.py

from dataclasses import dataclass
from typing import Optional

from app.cli.constants.enums import InitMode, LogLevelChoices


@dataclass
class InitConfig:
    """
    Immutable configuration for initialization workflow.

    Represents CLI input + resolved config.
    """

    mode: Optional[InitMode] = None

    force_init: Optional[bool] = False
    ask: Optional[bool] = False

    dry_run: bool = False
    no_debug: bool = True
    log_level: LogLevelChoices = LogLevelChoices.INFO
