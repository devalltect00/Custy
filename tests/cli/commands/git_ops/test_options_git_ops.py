# tests/cli/commands/git_ops/test_options_git_ops.py


"""
tests/cli/commands/git_ops/test_options.py

Tests for CLI option declarations of the git operations command.
"""

from app.cli.commands.git_ops import options


class TestGitOpsOptions:
    """Validate Typer option definitions."""

    def test_commit_options_exist(self):
        assert options.CommitMessageFileOption is not None
        assert options.AutoStageOption is not None
        assert options.StageModeOption is not None
        assert options.ForceCommitOption is not None
        assert options.CheckCzOption is not None

    def test_tag_options_exist(self):
        assert options.TagMessageFileOption is not None
        assert options.VersionFileOption is not None
        assert options.StrategyOption is not None
        assert options.BumpOption is not None
        assert options.TagOption is not None
        assert options.ForceTagOption is not None

    def test_push_options_exist(self):
        assert options.RemoteOption is not None
        assert options.AllRemoteOption is not None
        assert options.SkipTagOption is not None
        assert options.SyncBackupOption is not None

    def test_expected_symbols_are_exported(self):
        expected = (
            "CommitMessageFileOption",
            "AutoStageOption",
            "StageModeOption",
            "ForceCommitOption",
            "CheckCzOption",
            "TagMessageFileOption",
            "VersionFileOption",
            "StrategyOption",
            "BumpOption",
            "TagOption",
            "ForceTagOption",
            "RemoteOption",
            "AllRemoteOption",
            "SkipTagOption",
            "SyncBackupOption",
        )
        for symbol in expected:
            assert hasattr(options, symbol)

    def test_options_expose_metadata(self):
        for name in (
            "CommitMessageFileOption",
            "AutoStageOption",
            "StageModeOption",
            "ForceCommitOption",
            "CheckCzOption",
            "TagMessageFileOption",
            "VersionFileOption",
            "StrategyOption",
            "BumpOption",
            "TagOption",
            "ForceTagOption",
            "RemoteOption",
            "AllRemoteOption",
            "SkipTagOption",
            "SyncBackupOption",
        ):
            option = getattr(options, name)
            assert getattr(option, "__metadata__", None) is not None
