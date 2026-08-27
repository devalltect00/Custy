# tests/cli/commands/validate/test_resolver_validate.py

"""
tests/cli/commands/validate/test_resolver.py

Unit tests for resolve_validate_args().
"""

from pathlib import Path

import pytest

from app.cli.commands.validate.models import ValidateArgs
from app.cli.commands.validate.resolver import resolve_validate_args
from app.cli.constants import StageModeChoices


class DummyConfig:
    def resolve(self, value, key, default):
        return default if value is None else value


class DummyCliArgs:
    def __init__(
        self,
        commit_message_file=None,
        tag_message_file=None,
        version_file=None,
        auto_stage=None,
        stage_mode=None,
        check_cz=None,
    ):
        self.commit_message_file = commit_message_file
        self.tag_message_file = tag_message_file
        self.version_file = version_file
        self.auto_stage = auto_stage
        self.stage_mode = stage_mode
        self.check_cz = check_cz


class TestResolveValidateArgs:
    def test_returns_validate_args(self):
        args = resolve_validate_args(DummyConfig(), DummyCliArgs())
        assert isinstance(args, ValidateArgs)

    def test_uses_defaults_when_values_are_none(self):
        args = resolve_validate_args(DummyConfig(), DummyCliArgs())

        assert args.version_file == Path("app/__version__.py").resolve()
        assert args.auto_stage is False
        assert args.stage_mode == StageModeChoices.ALL
        assert args.check_cz is False

    def test_preserves_explicit_paths(self, tmp_path):
        commit = Path("commit.txt")
        tag = Path("tag.txt")
        version = tmp_path / "__version__.py"
        version.write_text('__version__ = "1.0.0"\n', encoding="utf-8")

        args = resolve_validate_args(
            DummyConfig(),
            DummyCliArgs(
                commit_message_file=commit,
                tag_message_file=tag,
                version_file=version,
            ),
        )

        assert args.commit_message_file == commit
        assert args.tag_message_file == tag
        assert args.version_file == version.resolve()

    @pytest.mark.parametrize("value", [True, False])
    def test_auto_stage_resolution(self, value):
        args = resolve_validate_args(
            DummyConfig(),
            DummyCliArgs(auto_stage=value),
        )
        assert args.auto_stage is value

    @pytest.mark.parametrize("value", [True, False])
    def test_check_cz_resolution(self, value):
        args = resolve_validate_args(
            DummyConfig(),
            DummyCliArgs(check_cz=value),
        )
        assert args.check_cz is value

    @pytest.mark.parametrize(
        "mode",
        [
            StageModeChoices.ALL,
            StageModeChoices.UPDATE,
        ],
    )
    def test_stage_mode_resolution(self, mode):
        args = resolve_validate_args(
            DummyConfig(),
            DummyCliArgs(stage_mode=mode),
        )
        assert args.stage_mode == mode
