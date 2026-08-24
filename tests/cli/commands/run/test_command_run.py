# tests/cli/commands/run/test_command_run.py


"""
tests/cli/commands/run/test_command.py

Tests for the run command execution flow.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

from app.cli.commands.run import command


class DummyAppContext:
    def __init__(self):
        self.dry_run = True
        self.debug = False
        self.log_level = "info"


class TestRunCommand:

    def test_run_executes_pipeline(self, monkeypatch):
        monkeypatch.setattr(command, "get_config", MagicMock(return_value=MagicMock()))
        monkeypatch.setattr(command, "get_context", MagicMock(return_value=DummyAppContext()))
        monkeypatch.setattr(
            command,
            "resolve_run_args",
            MagicMock(return_value=SimpleNamespace(steps=["release"])),
        )

        monkeypatch.setattr(command, "register_all_steps", MagicMock())

        resolver = MagicMock()
        resolver.resolve.return_value = ["commit", "tag", "push"]
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

        git_context = MagicMock()
        monkeypatch.setattr(command, "GitContext", MagicMock(return_value=git_context))

        pipeline = MagicMock()
        builder = MagicMock()
        builder.build.return_value = pipeline
        monkeypatch.setattr(
            command,
            "PipelineBuilder",
            MagicMock(return_value=builder),
        )

        command.run(ctx=MagicMock(), steps=["release"])

        resolver.resolve.assert_called_once_with(["release"])
        engine.from_cli_args.assert_called_once()
        builder.build.assert_called_once_with(["commit", "tag", "push"])
        pipeline.run.assert_called_once_with(git_context)

    def test_global_flags_are_forwarded(self, monkeypatch):
        app_ctx = DummyAppContext()

        monkeypatch.setattr(command, "get_context", MagicMock(return_value=app_ctx))
        monkeypatch.setattr(command, "get_config", MagicMock(return_value=MagicMock()))
        monkeypatch.setattr(
            command,
            "resolve_run_args",
            MagicMock(return_value=SimpleNamespace(steps=[])),
        )
        monkeypatch.setattr(command, "register_all_steps", MagicMock())

        resolver = MagicMock()
        resolver.resolve.return_value = []
        monkeypatch.setattr(command, "CommandResolver", MagicMock(return_value=resolver))

        engine = MagicMock()
        engine.from_cli_args.return_value = engine
        engine.build.return_value = MagicMock()
        monkeypatch.setattr(
            command,
            "WorkflowEngineBuilder",
            MagicMock(return_value=engine),
        )

        monkeypatch.setattr(command, "GitContext", MagicMock())

        pipeline = MagicMock(run=MagicMock())
        builder = MagicMock()
        builder.build.return_value = pipeline
        monkeypatch.setattr(
            command,
            "PipelineBuilder",
            MagicMock(return_value=builder),
        )

        command.run(ctx=MagicMock(), steps=[])

        merged = engine.from_cli_args.call_args.args[0]
        assert merged.dry_run is True
        assert merged.debug is False
        assert merged.log_level == "info"
