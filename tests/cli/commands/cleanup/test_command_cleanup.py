# tests/cli/commands/cleanup/test_command_cleanup.py

"""
tests/cli/commands/cleanup/test_command.py

Tests for cleanup command execution flow.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

from app.cli.commands.cleanup import command
from app.cli.commands.cleanup.models import (
    CleanupAllArgs,
    CleanupBackupArgs,
    CleanupBranchesArgs,
)
from app.cli.constants import CleanupTypeChoices


class DummyAppContext:
    def __init__(self):
        self.dry_run = True
        self.debug = False
        self.log_level = "info"


class TestCleanupCommand:
    def test_run_cleanup_backup_pipeline(self, monkeypatch):
        register = MagicMock()

        resolver = MagicMock()
        resolver.resolve.return_value = ["cleanup_backups"]

        builder = MagicMock()
        pipeline = MagicMock()
        builder.build.return_value = pipeline

        engine = MagicMock()
        engine.from_cli_args.return_value = engine
        engine.build.return_value = MagicMock()

        monkeypatch.setattr(command, "register_all_steps", register)
        monkeypatch.setattr(
            command, "CommandResolver", MagicMock(return_value=resolver)
        )
        monkeypatch.setattr(
            command, "WorkflowEngineBuilder", MagicMock(return_value=engine)
        )
        monkeypatch.setattr(command, "PipelineBuilder", MagicMock(return_value=builder))

        command._run_cleanup_backup_pipeline(SimpleNamespace(), ["cleanup_backups"])

        register.assert_called_once()
        resolver.resolve.assert_called_once_with(["cleanup_backups"])
        builder.build.assert_called_once_with(["cleanup_backups"])
        pipeline.run.assert_called_once()

    def test_backups_command_calls_pipeline(self, monkeypatch):
        monkeypatch.setattr(command, "get_config", MagicMock(return_value=MagicMock()))
        monkeypatch.setattr(
            command, "get_context", MagicMock(return_value=DummyAppContext())
        )
        resolved_args = CleanupBackupArgs(
            type=CleanupTypeChoices.ALL,
            keep=10,
            commit_message_backup_dir=None,
            tag_message_backup_dir=None,
        )
        monkeypatch.setattr(
            command,
            "resolve_cleanup_backup_args",
            MagicMock(return_value=resolved_args),
        )

        run = MagicMock()
        monkeypatch.setattr(command, "_run_cleanup_backup_pipeline", run)

        command.backups(ctx=MagicMock())

        run.assert_called_once()

    def test_branches_command_calls_pipeline(self, monkeypatch):
        monkeypatch.setattr(command, "get_config", MagicMock(return_value=MagicMock()))
        monkeypatch.setattr(
            command, "get_context", MagicMock(return_value=DummyAppContext())
        )
        monkeypatch.setattr(
            command,
            "resolve_cleanup_branches_args",
            MagicMock(return_value=CleanupBranchesArgs()),
        )

        run = MagicMock()
        monkeypatch.setattr(command, "_run_cleanup_branch_pipeline", run)

        command.branches(ctx=MagicMock())

        run.assert_called_once()

    def test_all_command_calls_both_pipelines(self, monkeypatch):
        monkeypatch.setattr(command, "get_config", MagicMock(return_value=MagicMock()))
        monkeypatch.setattr(
            command, "get_context", MagicMock(return_value=DummyAppContext())
        )
        resolved_args = CleanupAllArgs(
            type=CleanupTypeChoices.ALL,
            keep=10,
        )
        monkeypatch.setattr(
            command,
            "resolve_cleanup_all_args",
            MagicMock(return_value=resolved_args),
        )

        backup = MagicMock()
        branch = MagicMock()

        monkeypatch.setattr(command, "_run_cleanup_backup_pipeline", backup)
        monkeypatch.setattr(command, "_run_cleanup_branch_pipeline", branch)

        command.all(ctx=MagicMock())

        backup.assert_called_once()
        branch.assert_called_once()
