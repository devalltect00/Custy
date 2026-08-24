# tests/cli/commands/changelog/test_command_changelog.py


"""
tests/cli/commands/changelog/test_command.py

Tests for the changelog command execution flow.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

from app.cli.commands.changelog import command


class DummyAppContext:
    def __init__(self):
        self.dry_run = True
        self.debug = False
        self.log_level = "info"


class TestChangelogCommand:

    def test_generate_executes_pipeline(self, monkeypatch):
        monkeypatch.setattr(command, "get_config", MagicMock(return_value=MagicMock()))
        monkeypatch.setattr(command, "get_context", MagicMock(return_value=DummyAppContext()))
        monkeypatch.setattr(
            command,
            "resolve_changelog_args",
            MagicMock(return_value=SimpleNamespace()),
        )

        register = MagicMock()
        monkeypatch.setattr(command, "register_all_steps", register)

        resolver = MagicMock()
        resolver.resolve.return_value = ["changelog"]
        monkeypatch.setattr(command, "CommandResolver", MagicMock(return_value=resolver))

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
            "SimplePipelineBuilder",
            MagicMock(return_value=builder),
        )

        command.generate(
            ctx=MagicMock(),
            commit_message_file=None,
            force_changelog=None,
        )

        register.assert_called_once()
        resolver.resolve.assert_called_once_with(["changelog"])
        engine.from_cli_args.assert_called_once()
        builder.build.assert_called_once_with(["changelog"])
        pipeline.run.assert_called_once()

    def test_global_flags_are_forwarded(self, monkeypatch):
        app_ctx = DummyAppContext()

        monkeypatch.setattr(command, "get_context", MagicMock(return_value=app_ctx))
        monkeypatch.setattr(command, "get_config", MagicMock(return_value=MagicMock()))
        monkeypatch.setattr(
            command,
            "resolve_changelog_args",
            MagicMock(return_value=SimpleNamespace()),
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

        pipeline = MagicMock(run=MagicMock())
        builder = MagicMock()
        builder.build.return_value = pipeline
        monkeypatch.setattr(
            command,
            "SimplePipelineBuilder",
            MagicMock(return_value=builder),
        )

        command.generate(ctx=MagicMock())

        merged = engine.from_cli_args.call_args.args[0]
        assert merged.dry_run is True
        assert merged.debug is False
        assert merged.log_level == "info"
