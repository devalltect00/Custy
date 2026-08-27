# app/cli/commands/git_ops/models.py

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from app.cli.constants import (
    BumpChoices,
    StageModeChoices,
    StrategyChoices,
)


@dataclass
class CommitArgs:
    commit_message_file: Optional[Path]
    force_commit: bool
    auto_stage: bool
    stage_mode: StageModeChoices

    # Additional args for Generating release artifacts
    strategy: Optional[StrategyChoices]

    # Additional args for validation
    version_file: Optional[Path]
    check_cz: bool

    # Backup Dir Path
    commit_message_backup_dir: Optional[Path]


@dataclass
class TagArgs:
    tag_message_file: Optional[Path]
    version_file: Optional[Path]
    strategy: Optional[StrategyChoices]
    bump: Optional[BumpChoices]
    tag: Optional[str]
    tag_message: Optional[str]
    pre_release: Optional[str]
    post_release: bool
    dev_release: bool
    meta: Optional[str]
    epoch: Optional[int]
    skip_check: bool
    force_tag: bool

    # Backup Dir Path
    tag_message_backup_dir: Optional[Path]


@dataclass
class PushArgs:
    all_remote: bool
    remote: Optional[str]
    tag: Optional[str]
    skip_tag: bool
    sync_backup: bool
