# tests/cli/commands/version/test_command_version.py

"""
tests/cli/commands/version/test_command.py

Tests for the `custy version update` command execution flow.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

from app.cli.commands.version import command


class DummyAppContext:
    """Minimal application context used by the command."""

    def __init__(self):
        self.dry_run = True
        self.debug = False
        self.log_level = "info"


class TestVersionUpdateCommand:
    def test_update_executes_pipeline(self, monkeypatch):
        cfg = MagicMock()
        resolved_args = MagicMock()

        monkeypatch.setattr(command, "get_config", MagicMock(return_value=cfg))
        monkeypatch.setattr(
            command, "get_context", MagicMock(return_value=DummyAppContext())
        )
        monkeypatch.setattr(
            command, "resolve_version_args", MagicMock(return_value=resolved_args)
        )
        monkeypatch.setattr(command, "register_all_steps", MagicMock())

        resolver_instance = MagicMock()
        resolver_instance.resolve.return_value = ["apply_version"]
        monkeypatch.setattr(
            command,
            "CommandResolver",
            MagicMock(return_value=resolver_instance),
        )

        builder = MagicMock()
        builder.from_cli_args.return_value = builder
        builder.build.return_value = MagicMock()
        monkeypatch.setattr(
            command,
            "WorkflowEngineBuilder",
            MagicMock(return_value=builder),
        )

        pipeline = MagicMock()
        pipeline_builder = MagicMock()
        pipeline_builder.build.return_value = pipeline
        monkeypatch.setattr(
            command,
            "SimplePipelineBuilder",
            MagicMock(return_value=pipeline_builder),
        )

        command.update(
            ctx=MagicMock(),
            version_file=None,
            strategy=None,
            bump=None,
            tag=None,
        )

        resolver_instance.resolve.assert_called_once_with(["apply_version"])
        builder.from_cli_args.assert_called_once()
        pipeline_builder.build.assert_called_once_with(["apply_version"])
        pipeline.run.assert_called_once()

    def test_global_flags_are_forwarded(self, monkeypatch):
        app_ctx = DummyAppContext()

        monkeypatch.setattr(command, "get_context", MagicMock(return_value=app_ctx))
        monkeypatch.setattr(command, "get_config", MagicMock(return_value=MagicMock()))
        monkeypatch.setattr(
            command,
            "resolve_version_args",
            MagicMock(return_value=SimpleNamespace()),
        )
        monkeypatch.setattr(command, "register_all_steps", MagicMock())

        resolver = MagicMock()
        resolver.resolve.return_value = []
        monkeypatch.setattr(
            command, "CommandResolver", MagicMock(return_value=resolver)
        )

        wb = MagicMock()
        wb.from_cli_args.return_value = wb
        wb.build.return_value = MagicMock()
        monkeypatch.setattr(
            command, "WorkflowEngineBuilder", MagicMock(return_value=wb)
        )

        pb = MagicMock()
        pb.build.return_value = MagicMock(run=MagicMock())
        monkeypatch.setattr(
            command, "SimplePipelineBuilder", MagicMock(return_value=pb)
        )

        command.update(ctx=MagicMock())

        merged = wb.from_cli_args.call_args.args[0]
        assert merged.dry_run is True
        assert merged.debug is False
        assert merged.log_level == "info"
