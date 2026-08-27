# tests/cli/commands/changelog/test_resolver_changelog.py

"""
tests/cli/commands/changelog/test_resolver.py

Unit tests for resolve_changelog_args().
"""

from pathlib import Path

from app.cli.commands.changelog import resolver
from app.cli.commands.changelog.models import ChangelogArgs


class DummyConfig:
    def resolve(self, value, key, default):
        return default if value is None else value


class DummyCliArgs:
    def __init__(self, commit_message_file=None, force_changelog=None):
        self.commit_message_file = commit_message_file
        self.force_changelog = force_changelog


class TestChangelogResolver:
    def test_returns_changelog_args(self):
        args = resolver.resolve_changelog_args(
            DummyConfig(),
            DummyCliArgs(),
        )
        assert isinstance(args, ChangelogArgs)

    def test_default_values_are_used(self):
        args = resolver.resolve_changelog_args(
            DummyConfig(),
            DummyCliArgs(),
        )

        assert args.force_changelog is False

    def test_explicit_values_are_preserved(self):
        commit = Path("commit-message.txt")

        args = resolver.resolve_changelog_args(
            DummyConfig(),
            DummyCliArgs(
                commit_message_file=commit,
                force_changelog=True,
            ),
        )

        assert args.commit_message_file == commit
        assert args.force_changelog is True
