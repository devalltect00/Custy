# app/core/workflow/workflow_builder.py

"""
WorkflowEngine Builder

Provides a clean and explicit way to construct WorkflowEngine instances.

Design Goals:
- Avoid constructor explosion
- Replace flag-based builders (anti-pattern)
- Keep CLI → Engine mapping clean
- Support both direct config and fluent builder usage

Usage:

    builder = WorkflowEngineBuilder()
    engine = (
        builder
        .with_commit_file("commit-msg.txt")
        .with_tag("v1.2.3")
        .with_strategy("semver")
        .with_dry_run(True)
        .build()
    )

Or from CLI args:

    engine = WorkflowEngineBuilder().from_cli_args(args).build()
"""

from pathlib import Path
from typing import Optional, List

from app.core.workflow.workflow_config import WorkflowConfig
from app.core.workflow.workflow_engine import WorkflowEngine
from app.cli.constants.enums import (
    StrategyChoices,
    BumpChoices,
    StageModeChoices,
    LogLevelChoices,
    CleanupTypeChoices,
)


class WorkflowEngineBuilder:
    """
    Builder for WorkflowEngine.

    This class helps construct WorkflowConfig step-by-step
    and then instantiate WorkflowEngine.

    It supports:
    - Fluent API (chainable methods)
    - CLI argument mapping
    - Validation before build
    """

    def __init__(self):
        self.config = WorkflowConfig()

    # =========================================================
    # Private
    # =========================================================

    @staticmethod
    def _get(args, name: str, default=None):
        return getattr(args, name, default)

    # =========================================================
    # 🔧 Fluent API (Manual Construction)
    # =========================================================

    def with_commit_message(self, message: str):
        self.config.commit_message_input = message
        return self

    def with_commit_file(self, path: str):
        self.config.commit_message_file = Path(path)
        return self

    def with_tag(self, tag: str):
        self.config.tag_input = tag
        return self

    def with_tag_message(self, message: str):
        self.config.tag_message_input = message
        return self

    def with_tag_file(self, path: str):
        self.config.tag_message_file = Path(path)
        return self

    def with_strategy(self, strategy: StrategyChoices):
        self.config.strategy = strategy
        return self

    def with_bump(self, value: BumpChoices):
        self.config.bump_level = value
        return self

    def with_pre_release(self, value: str):
        self.config.pre_release = value
        return self

    def with_post_release(self, value: bool = True):
        self.config.post_release = value
        return self

    def with_dev_release(self, value: bool = True):
        self.config.dev_release = value
        return self

    def with_meta(self, meta: str):
        self.config.meta = meta
        return self

    def with_epoch(self, epoch: int):
        self.config.epoch = epoch
        return self

    def with_version_file(self, path: str):
        self.config.version_file = Path(path)
        return self

    def with_auto_stage(self, mode: StageModeChoices):
        self.config.auto_stage = True
        self.config.stage_mode = mode
        return self

    def with_stage_mode(self, mode: StageModeChoices):
        self.config.stage_mode = mode
        return self

    def with_force_commit(self, value: bool = True):
        self.config.force_commit = value
        return self

    def with_force_tag(self, value: bool = True):
        self.config.force_tag = value
        return self

    def with_force_changelog(self, value: bool = True):
        self.config.force_changelog = value
        return self

    def with_sync_backup(self, value: bool = True):
        self.config.sync_backup = value
        return self

    def with_main_remotes(self, remotes: List[str]):
        self.config.main_remotes = remotes
        return self

    def with_backup_remotes(self, remotes: List[str]):
        self.config.backup_remotes = remotes
        return self

    def with_cleanup_types(self, types: CleanupTypeChoices):
        self.config.cleanup_backup_type = types
        return self

    def with_backup_retention(self, count: Optional[int]):
        self.config.backup_retention_count = count
        return self

    def with_commit_backup_dir(self, path: str):
        self.config.commit_message_backup_dir = Path(path)
        return self

    def with_tag_backup_dir(self, path: str):
        self.config.tag_message_backup_dir = Path(path)
        return self

    def with_dry_run(self, value: bool = True):
        self.config.dry_run = value
        return self

    def with_debug(self, value: bool = True):
        self.config.no_debug = not value
        return self

    def with_skip_checks(self, value: bool = True):
        self.config.skip_checks = value
        return self

    def with_log_level(self, choice: LogLevelChoices):
        self.config.log_level = choice
        return self

    # =========================================================
    # 🧠 CLI Mapping (IMPORTANT)
    # =========================================================

    def from_cli_args(self, args):
        """
        Populate config from CLI arguments.

        This keeps CLI logic OUT of WorkflowEngine.
        """

        # print("args", args)

        if getattr(args, "commit_message", None):
            self.with_commit_message(args.commit_message)

        if getattr(args, "commit_message_file", None):
            self.with_commit_file(args.commit_message_file)

        if getattr(args, "tag", None):
            self.with_tag(args.tag)

        if getattr(args, "tag_message", None):
            self.with_tag_message(args.tag_message)

        if getattr(args, "tag_message_file", None):
            self.with_tag_file(args.tag_message_file)

        # if hasattr(args, "strategy"):
        #     value = self._get(args, "strategy")
        #     if value not in (None):
        #         self.with_strategy(value)

        # if hasattr(args, "bump_level"):
        #     value = self._get(args, "bump_level")
        #     if value not in (None):
        #         self.with_bump(args.bump_level)

        if getattr(args, "strategy", None):
            self.with_strategy(args.strategy)

        if getattr(args, "bump_level", None):
            self.with_bump(args.bump_level)

        if getattr(args, "pre_release", None):
            self.with_pre_release(args.pre_release)

        if getattr(args, "post_release", False):
            self.with_post_release(True)

        if getattr(args, "dev_release", False):
            self.with_dev_release(True)

        if getattr(args, "meta", None):
            self.with_meta(args.meta)

        if getattr(args, "epoch", None):
            self.with_epoch(args.epoch)

        if getattr(args, "version_file", None):
            self.with_version_file(args.version_file)

        if getattr(args, "auto_stage", False):
            self.with_auto_stage(getattr(args, "stage_mode", StageModeChoices.ALL))

        if getattr(args, "force_commit", False):
            self.with_force_commit(True)

        if getattr(args, "force_tag", False):
            self.with_force_tag(True)

        if getattr(args, "force_changelog", False):
            self.with_force_changelog(True)

        if getattr(args, "sync_backup", False):
            self.with_sync_backup(True)

        if hasattr(args, "cleanup_backup_type"):
            value = self._get(args, "cleanup_backup_type")
            if value not in (None, CleanupTypeChoices.ALL):
                self.with_cleanup_types(args.cleanup_backup_type)

        if getattr(args, "backup_retention_count", None):
            self.with_backup_retention(args.backup_retention_count)

        if getattr(args, "commit_message_backup_dir", None):
            self.with_commit_backup_dir(args.commit_message_backup_dir)

        if getattr(args, "tag_message_backup_dir", None):
            self.with_tag_backup_dir(args.tag_message_backup_dir)

        if getattr(args, "dry_run", False):
            self.with_dry_run(True)

        if getattr(args, "debug", False):
            self.with_debug(True)

        if hasattr(args, "no_debug"):
            value = self._get(args, "no_debug")
            self.with_debug(not args.no_debug)

        if getattr(args, "skip_checks", False):
            self.with_skip_checks(True)

        if hasattr(args, "log_level"):
            value = self._get(args, "log_level")
            if value not in (None, LogLevelChoices.INFO):
                self.with_log_level(args.log_level)

        return self

    # =========================================================
    # ✅ Validation
    # =========================================================

    def _validate(self):
        """
        Validate configuration before building engine.

        Add rules here as your system grows.
        """

        if self.config.auto_stage and not self.config.stage_mode:
            raise ValueError("stage_mode must be set when auto_stage is enabled")

    # =========================================================
    # 🚀 Build
    # =========================================================

    def build(self) -> WorkflowEngine:
        """
        Finalize and create WorkflowEngine.
        """

        self._validate()
        return WorkflowEngine(self.config)
