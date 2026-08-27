# tests/cli/commands/backup/test_command_backup.py

"""
tests/cli/commands/backup/test_command.py

Tests for backup command execution flow.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

from app.cli.commands.backup import command


class DummyAppContext:
    def __init__(self):
        self.dry_run = True
        self.debug = False
        self.log_level = "info"


class TestBackupCommand:
    def test_run_backup_pipeline_executes(self, monkeypatch):
        register = MagicMock()
        resolver_inst = MagicMock()
        resolver_inst.resolve.return_value = ["backup_all"]
        resolver_cls = MagicMock(return_value=resolver_inst)

        builder = MagicMock()
        pipeline = MagicMock()
        builder.build.return_value = pipeline
        builder_cls = MagicMock(return_value=builder)

        engine_builder = MagicMock()
        engine_builder.from_cli_args.return_value = engine_builder
        engine_builder.build.return_value = MagicMock()
        engine_cls = MagicMock(return_value=engine_builder)

        monkeypatch.setattr(command, "register_all_steps", register)
        monkeypatch.setattr(command, "CommandResolver", resolver_cls)
        monkeypatch.setattr(command, "WorkflowEngineBuilder", engine_cls)
        monkeypatch.setattr(command, "PipelineBuilder", builder_cls)

        command._run_backup_pipeline(SimpleNamespace(), ["backup_all"])

        register.assert_called_once()
        resolver_inst.resolve.assert_called_once_with(["backup_all"])
        engine_builder.from_cli_args.assert_called_once()
        builder.build.assert_called_once_with(["backup_all"])
        pipeline.run.assert_called_once()

    def test_commit_command_calls_pipeline(self, monkeypatch):
        app_ctx = DummyAppContext()

        monkeypatch.setattr(command, "get_config", MagicMock(return_value=MagicMock()))
        monkeypatch.setattr(command, "get_context", MagicMock(return_value=app_ctx))
        monkeypatch.setattr(
            command,
            "resolve_backup_commit_args",
            MagicMock(return_value=SimpleNamespace()),
        )
        run = MagicMock()
        monkeypatch.setattr(command, "_run_backup_pipeline", run)

        command.commit_message(
            ctx=MagicMock(),
            commit_message_file=None,
            commit_message_backup_dir=None,
        )

        run.assert_called_once()

    def test_tag_command_calls_pipeline(self, monkeypatch):
        app_ctx = DummyAppContext()

        monkeypatch.setattr(command, "get_config", MagicMock(return_value=MagicMock()))
        monkeypatch.setattr(command, "get_context", MagicMock(return_value=app_ctx))
        monkeypatch.setattr(
            command,
            "resolve_backup_tag_args",
            MagicMock(return_value=SimpleNamespace()),
        )
        run = MagicMock()
        monkeypatch.setattr(command, "_run_backup_pipeline", run)

        command.tag_message(
            ctx=MagicMock(),
            tag_message_file=None,
            tag_message_backup_dir=None,
        )

        run.assert_called_once()

    def test_all_command_calls_pipeline(self, monkeypatch):
        app_ctx = DummyAppContext()

        monkeypatch.setattr(command, "get_config", MagicMock(return_value=MagicMock()))
        monkeypatch.setattr(command, "get_context", MagicMock(return_value=app_ctx))
        monkeypatch.setattr(
            command,
            "resolve_backup_all_args",
            MagicMock(return_value=SimpleNamespace()),
        )
        run = MagicMock()
        monkeypatch.setattr(command, "_run_backup_pipeline", run)

        command.all_backup(ctx=MagicMock())

        run.assert_called_once()
