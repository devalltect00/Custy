# app/cli/commands/run/models.py

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List

from app.cli.constants import(
  StrategyChoices,
  BumpChoices,
  StageModeChoices,
)

@dataclass
class RunArgs:
  steps: Optional[List[str]]
  
  # Commit
  ## Commit • Validation
  check_cz: bool
  ## Commit • Staging
  auto_stage: bool
  stage_mode: StageModeChoices
  ## Commit • Files
  commit_message_file: Optional[Path]
  ## Commit • Behavior
  force_commit: bool
  ## Commit • Backup
  commit_message_backup_dir: Optional[Path]

  # Tag
  ## Tag • Files
  tag_message_file: Optional[Path]
  version_file: Optional[Path]
  ## Tag • Versioning
  strategy: Optional[StrategyChoices]
  bump: Optional[BumpChoices]
  tag: Optional[str]
  tag_message: Optional[str]
  pre_release: Optional[str]
  post_release: bool
  dev_release: bool
  meta: Optional[str]
  epoch: Optional[int]
  ## Tag • Behavior
  force_tag: bool
  skip_check: bool
  ## Tag • Backup
  tag_message_backup_dir: Optional[Path]

  # Push
  ## Push • Execution
  all_remote: bool
  remote: Optional[str]
  ## Push • Behavior
  skip_tag: bool
  sync_backup: bool
