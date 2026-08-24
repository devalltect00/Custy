# app/cli/commands/version/models.py

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from app.cli.constants import (
  StrategyChoices,
  BumpChoices,
)

@dataclass
class VersionArgs:
  version_file: Optional[Path]
  tag: Optional[str]
  strategy: Optional[StrategyChoices]
  bump: Optional[BumpChoices]
