# tests/cli/commands/changelog/test_models_changelog.py

"""
tests/cli/commands/changelog/test_models.py

Unit tests for ChangelogArgs.
"""

from pathlib import Path

from app.cli.commands.changelog.models import ChangelogArgs


class TestChangelogArgs:
    def test_construct(self):
        args = ChangelogArgs(
            commit_message_file=Path("commit.txt"),
            force_changelog=True,
        )
        assert args.commit_message_file == Path("commit.txt")
        assert args.force_changelog is True

    def test_equality(self):
        assert ChangelogArgs(None, False) == ChangelogArgs(None, False)

    def test_repr_contains_field(self):
        text = repr(ChangelogArgs(None, True))
        assert "force_changelog=True" in text
