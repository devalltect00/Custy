# app/cli/commands/cleanup/models.py

from dataclasses import dataclass, field
from datetime import timedelta, datetime
from pathlib import Path
from typing import Optional

from app.cli.constants import (
  CleanupTypeChoices,
  MergeStatusChoices,
)

@dataclass(slots=True)
class CleanupBackupArgs:
  """
  Resolved arguments for backup cleanup.
  """

  type: CleanupTypeChoices
  keep: int | None
  commit_message_backup_dir: Path | None
  tag_message_backup_dir: Path | None

@dataclass(slots=True)
class CleanupBranchesArgs:
    """
    Resolved arguments for branch cleanup.

    Every field in this model has already been resolved from CLI
    arguments and configuration values.
    """

    include_prefixes: list[str] = field(default_factory=list)
    merge_status: MergeStatusChoices = MergeStatusChoices.MERGED
    max_age: timedelta | None = None
    before: datetime | None = None

@dataclass(slots=True)
class CleanupAllArgs:
    """
    Resolved arguments for the complete cleanup workflow.
    """

    type: CleanupTypeChoices
    keep: int | None
    include_prefixes: list[str] = field(default_factory=list)
    merge_status: MergeStatusChoices = MergeStatusChoices.MERGED
    max_age: timedelta | None = None
    before: datetime | None = None
    commit_message_backup_dir: Path | None = None
    tag_message_backup_dir: Path | None = None
