# app/core/workflow/workflow_config.py

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List

from app.cli.constants.enums import (
    StrategyChoices,
    BumpChoices,
    StageModeChoices,
    LogLevelChoices,
    CleanupTypeChoices,
)


@dataclass
class WorkflowConfig:
    """
    Immutable configuration for WorkflowEngine.

    This represents user input + CLI options.
    """

    # ===== Commit =====
    commit_message_input: Optional[str] = None
    commit_message_file: Optional[Path] = None

    # ===== Tag =====
    tag_input: Optional[str] = None
    tag_message_input: Optional[str] = None
    tag_message_file: Optional[Path] = None

    # ===== Versioning =====
    strategy: Optional[StrategyChoices] = None
    bump_level: Optional[BumpChoices] = None
    pre_release: Optional[str] = None
    post_release: bool = False
    dev_release: bool = False
    meta: Optional[str] = None
    epoch: Optional[int] = None

    # ===== Execution =====
    dry_run: bool = False
    no_debug: bool = True
    skip_checks: bool = False
    log_level: LogLevelChoices = LogLevelChoices.INFO

    # ===== Files =====
    version_file: Optional[Path] = None

    # ===== Staging =====
    auto_stage: bool = False
    stage_mode: StageModeChoices = StageModeChoices.ALL

    # ===== Flags =====
    force_tag: bool = False
    force_commit: bool = False
    force_changelog: bool = False
    sync_backup: bool = False

    # ===== Remotes =====
    main_remotes: Optional[List[str]] = None
    backup_remotes: Optional[List[str]] = None

    # ===== Backups =====
    commit_message_backup_dir: Optional[Path] = None
    tag_message_backup_dir: Optional[Path] = None
    cleanup_backup_type: CleanupTypeChoices = CleanupTypeChoices.ALL
    backup_retention_count: Optional[int] = 10
