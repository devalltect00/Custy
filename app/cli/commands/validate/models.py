# app/cli/commands/validate/models.py

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from app.cli.constants import LogLevelChoices

@dataclass
class ValidateArgs:
  commit_message_file: Optional[Path]
  tag_message_file: Optional[Path]
  version_file: Optional[Path]
  auto_stage: bool
  stage_mode: Optional[str]
  check_cz: bool
