# app/core/workflow/workflow_config.py

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from app.cli.constants.enums import (
    BumpChoices,
    CleanupTypeChoices,
    LogLevelChoices,
    StageModeChoices,
    StrategyChoices,
)
from app.core.editor import EditorSettings


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

    # ===== Editor =====
    editor_settings: EditorSettings = field(default_factory=EditorSettings)

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
    skip_tag: bool = False

    # ===== Remotes =====
    remote: Optional[str] = None
    default_remote: str = "origin"
    all_remote: bool = False
    push_to: str = "main"
    main_remotes: Optional[list[str]] = None
    backup_remotes: Optional[list[str]] = None

    # ===== Backups =====
    commit_message_backup_dir: Optional[Path] = None
    tag_message_backup_dir: Optional[Path] = None
    cleanup_backup_type: CleanupTypeChoices = CleanupTypeChoices.ALL
    backup_retention_count: Optional[int] = 10
