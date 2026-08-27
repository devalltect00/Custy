# tests/cli/commands/main/test_resolver.py

"""Tests for app.cli.commands.main.resolver."""

from app.cli.commands.main.resolver import resolve_main_args
from app.cli.constants import LogLevelChoices


class DummyConfig:
    def resolve(self, value, path, default):
        return default if value is None else value


class DummyCli:
    no_banner = False
    help = False
    version = None
    dry_run = True
    debug = True
    log_level = LogLevelChoices.DEBUG


def test_resolve_main_args_debug_conversion():
    args = resolve_main_args(DummyConfig(), DummyCli())
    assert args.no_debug is False
    assert args.dry_run is True
