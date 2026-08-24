# app/cli/commands/main/models.py

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from app.cli.constants import LogLevelChoices

@dataclass
class MainArgs:
  no_banner: bool
  help: bool
  version: bool | None
  dry_run: bool
  no_debug: bool
  log_level: LogLevelChoices
