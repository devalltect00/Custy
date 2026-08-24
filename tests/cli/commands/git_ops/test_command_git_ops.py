# tests/cli/commands/git_ops/test_command_git_ops.py


"""
tests/cli/commands/git_ops/test_command.py

Tests for git operations command execution flow.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

from app.cli.commands.git_ops import command


class DummyAppContext:
    def __init__(self):
        self.dry_run = True
        self.debug = False
        self.log_level = "info"


class TestGitOpsCommand:

    def test_run_pipeline_executes(self, monkeypatch):
        monkeypatch.setattr(command, "register_all_steps", MagicMock())

        resolver = MagicMock()
        resolver.resolve.return_value = ["commit"]
        monkeypatch.setattr(
            command,
            "CommandResolver",
            MagicMock(return_value=resolver),
        )

        engine = MagicMock()
        engine.from_cli_args.return_value = engine
        engine.build.return_value = MagicMock()
        monkeypatch.setattr(
            command,
            "WorkflowEngineBuilder",
            MagicMock(return_value=engine),
        )

        pipeline = MagicMock()
        builder = MagicMock()
        builder.build.return_value = pipeline
        monkeypatch.setattr(
            command,
            "PipelineBuilder",
            MagicMock(return_value=builder),
        )

        command._run_pipeline(SimpleNamespace(), ["commit"])

        resolver.resolve.assert_called_once_with(["commit"])
        engine.from_cli_args.assert_called_once()
        builder.build.assert_called_once_with(["commit"])
        pipeline.run.assert_called_once()

    def test_commit_calls_pipeline(self, monkeypatch):
        monkeypatch.setattr(command, "get_config", MagicMock(return_value=MagicMock()))
        monkeypatch.setattr(command, "get_context", MagicMock(return_value=DummyAppContext()))
        monkeypatch.setattr(command, "resolve_commit_args", MagicMock(return_value=SimpleNamespace()))

        run = MagicMock()
        monkeypatch.setattr(command, "_run_pipeline", run)

        command.commit(ctx=MagicMock())

        run.assert_called_once()

    def test_tag_calls_pipeline(self, monkeypatch):
        monkeypatch.setattr(command, "get_config", MagicMock(return_value=MagicMock()))
        monkeypatch.setattr(command, "get_context", MagicMock(return_value=DummyAppContext()))
        monkeypatch.setattr(command, "resolve_tag_args", MagicMock(return_value=SimpleNamespace()))

        run = MagicMock()
        monkeypatch.setattr(command, "_run_pipeline", run)

        command.tag(ctx=MagicMock())

        run.assert_called_once()

    def test_push_calls_pipeline(self, monkeypatch):
        monkeypatch.setattr(command, "get_config", MagicMock(return_value=MagicMock()))
        monkeypatch.setattr(command, "get_context", MagicMock(return_value=DummyAppContext()))
        monkeypatch.setattr(command, "resolve_push_args", MagicMock(return_value=SimpleNamespace()))

        run = MagicMock()
        monkeypatch.setattr(command, "_run_pipeline", run)

        command.push(ctx=MagicMock())

        run.assert_called_once()
