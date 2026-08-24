# app/cli/commands/changelog/models.py

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from app.cli.constants import LogLevelChoices

@dataclass
class ChangelogArgs:
  commit_message_file: Optional[Path]
  force_changelog: bool
