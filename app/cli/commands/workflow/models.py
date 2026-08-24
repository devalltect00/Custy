# app/cli/commands/workflow/models.py

from dataclasses import dataclass
from typing import Optional

from app.cli.constants import LogLevelChoices

@dataclass
class BranchWorkflowArgs:
  enforce: bool
  check_transition: bool
  from_branch: Optional[str]
  to_branch: Optional[str]
  from_tag: Optional[str]
  to_tag: Optional[str]
  sync_backup: bool
  dry_run: bool
  no_debug: bool
  log_level: LogLevelChoices
