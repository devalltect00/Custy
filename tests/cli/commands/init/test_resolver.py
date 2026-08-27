# tests/cli/commands/init/test_resolver.py

"""
tests/cli/commands/init/test_resolver.py

Unit tests for the init command resolver.
"""

import pytest

from app.cli.commands.init.models import InitArgs
from app.cli.commands.init.resolver import resolve_init_args
from app.cli.constants.enums import InitMode


class DummyConfig:
    """Simple configuration stub."""

    def resolve(self, value, key, default):
        return default if value is None else value


class DummyCliArgs:
    """CLI argument stub."""

    def __init__(self, mode=None, force_init=None, ask=None):
        self.mode = mode
        self.force_init = force_init
        self.ask = ask


class TestResolveInitArgs:
    """Tests for resolve_init_args()."""

    def test_returns_init_args_instance(self):
        args = resolve_init_args(
            DummyConfig(),
            DummyCliArgs(),
        )
        assert isinstance(args, InitArgs)

    def test_defaults_mode_to_all(self):
        args = resolve_init_args(
            DummyConfig(),
            DummyCliArgs(mode=None),
        )
        assert args.mode == InitMode.ALL

    @pytest.mark.parametrize(
        ("mode",),
        [
            (InitMode.ALL,),
            (InitMode.CONFIG,),
            (InitMode.TEMPLATES,),
            (InitMode.EXAMPLES,),
        ],
    )
    def test_preserves_explicit_mode(self, mode):
        args = resolve_init_args(
            DummyConfig(),
            DummyCliArgs(mode=mode),
        )
        assert args.mode == mode

    @pytest.mark.parametrize("value", [True, False])
    def test_force_init_resolution(self, value):
        args = resolve_init_args(
            DummyConfig(),
            DummyCliArgs(force_init=value),
        )
        assert args.force_init is value

    @pytest.mark.parametrize("value", [True, False])
    def test_ask_resolution(self, value):
        args = resolve_init_args(
            DummyConfig(),
            DummyCliArgs(ask=value),
        )
        assert args.ask is value

    def test_configuration_defaults_are_used_when_none(self):
        cfg = DummyConfig()

        args = resolve_init_args(
            cfg,
            DummyCliArgs(
                force_init=None,
                ask=None,
            ),
        )

        assert args.force_init is False
        assert args.ask is False
