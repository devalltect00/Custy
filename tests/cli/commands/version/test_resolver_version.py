# tests/cli/commands/version/test_resolver_version.py

"""
tests/cli/commands/version/test_resolver.py

Unit tests for resolve_version_args().
"""

import pytest

from app.cli.commands.version.models import VersionArgs
from app.cli.commands.version import resolver
from app.cli.constants import StrategyChoices, BumpChoices


class DummyConfig:
    def resolve(self, value, key, default):
        return default if value is None else value


class DummyCliArgs:
    def __init__(
        self,
        version_file=None,
        tag=None,
        strategy=None,
        bump=None,
    ):
        self.version_file = version_file
        self.tag = tag
        self.strategy = strategy
        self.bump = bump


class TestResolveVersionArgs:

    def test_returns_version_args(self, monkeypatch):
        monkeypatch.setattr(
            resolver,
            "detect_project_strategy",
            lambda no_debug=True: StrategyChoices.SEMVER,
        )

        args = resolver.resolve_version_args(
            DummyConfig(),
            DummyCliArgs(),
        )

        assert isinstance(args, VersionArgs)

    def test_defaults_are_used(self, monkeypatch):
        monkeypatch.setattr(
            resolver,
            "detect_project_strategy",
            lambda no_debug=True: StrategyChoices.SEMVER,
        )

        args = resolver.resolve_version_args(
            DummyConfig(),
            DummyCliArgs(),
        )

        assert args.version_file == "app/__version__.py"
        assert args.strategy == StrategyChoices.SEMVER
        assert args.bump is None

    def test_explicit_values_are_preserved(self):
        args = resolver.resolve_version_args(
            DummyConfig(),
            DummyCliArgs(
                version_file="src/__version__.py",
                tag="v2.0.0",
                strategy=StrategyChoices.PEP440,
                bump=BumpChoices.MINOR,
            ),
        )

        assert args.version_file == "src/__version__.py"
        assert args.tag == "v2.0.0"
        assert args.strategy == StrategyChoices.PEP440
        assert args.bump == BumpChoices.MINOR

    def test_fallback_to_semver_when_detection_returns_none(self, monkeypatch):
        monkeypatch.setattr(
            resolver,
            "detect_project_strategy",
            lambda no_debug=True: None,
        )

        args = resolver.resolve_version_args(
            DummyConfig(),
            DummyCliArgs(),
        )

        assert args.strategy == StrategyChoices.SEMVER
