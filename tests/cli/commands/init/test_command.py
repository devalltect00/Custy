# tests/cli/commands/init/test_command.py

"""
tests/cli/commands/init/test_command.py

Tests for the init command execution flow.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.cli.commands.init import command


class DummyContext:
    """Minimal Typer context."""

    def __init__(self):
        self.obj = None


class DummyAppContext:
    """Minimal application context."""

    dry_run = False
    debug = False
    log_level = "INFO"


class TestInitCommand:
    """Tests for the init command."""

    def test_run_init_pipeline_registers_steps(self, monkeypatch):
        register = MagicMock()
        resolver = MagicMock()
        builder = MagicMock()
        pipeline = MagicMock()

        # builder.build.return_value = pipeline
        builder.return_value.build.return_value = pipeline
        # resolver.resolve.return_value = ["init"]
        resolver.return_value.resolve.return_value = ["init"]

        monkeypatch.setattr(command, "register_all_steps", register)
        monkeypatch.setattr(command, "CommandResolver", resolver)
        monkeypatch.setattr(command, "SimplePipelineBuilder", builder)

        args = MagicMock()
        commands = ["init"]

        command._run_init_pipeline(args, commands)

        register.assert_called_once()
        # resolver.resolve.assert_called_once_with(commands)
        resolver.return_value.resolve.assert_called_once_with(commands)
        # builder.build.assert_called_once()
        builder.return_value.build.assert_called_once()
        pipeline.run.assert_called_once()

    def test_init_uses_context_and_resolver(self, monkeypatch):
        ctx = DummyContext()

        cfg = MagicMock()
        resolved = SimpleNamespace(
            mode="all",
            force_init=False,
            ask=False,
        )

        get_config = MagicMock(return_value=cfg)
        get_context = MagicMock(return_value=DummyAppContext())
        resolve = MagicMock(return_value=resolved)
        run_pipeline = MagicMock()

        monkeypatch.setattr(command, "get_config", get_config)
        monkeypatch.setattr(command, "get_context", get_context)
        monkeypatch.setattr(command, "resolve_init_args", resolve)
        monkeypatch.setattr(command, "_run_init_pipeline", run_pipeline)

        command.init(
            ctx=ctx,
            mode=None,
            force_init=None,
            ask=None,
        )

        get_config.assert_called_once()
        get_context.assert_called_once_with(ctx)
        resolve.assert_called_once()

        run_pipeline.assert_called_once()
        args, commands = run_pipeline.call_args.args

        assert commands == ["init"]
        assert args.mode == resolved.mode
        assert args.force_init == resolved.force_init
        assert args.ask == resolved.ask
        assert args.dry_run is False
        assert args.debug is False
        assert args.log_level == "INFO"

    @pytest.mark.parametrize("mode", [None])
    def test_init_accepts_default_arguments(self, monkeypatch, mode):
        monkeypatch.setattr(command, "get_config", MagicMock(return_value=MagicMock()))
        monkeypatch.setattr(
            command,
            "get_context",
            MagicMock(return_value=DummyAppContext()),
        )
        monkeypatch.setattr(
            command,
            "resolve_init_args",
            MagicMock(
                return_value=SimpleNamespace(
                    mode="all",
                    force_init=False,
                    ask=False,
                )
            ),
        )
        monkeypatch.setattr(command, "_run_init_pipeline", MagicMock())

        command.init(
            ctx=DummyContext(),
            mode=mode,
            force_init=None,
            ask=None,
        )
