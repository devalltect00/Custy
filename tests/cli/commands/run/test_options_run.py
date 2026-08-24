# tests/cli/commands/run/test_options_run.py


"""
tests/cli/commands/run/test_options.py

Tests for CLI option declarations of the run command.
"""

from app.cli.commands.run import options


class TestRunOptions:
    """Validate Typer option definitions used by the run command."""

    def test_steps_argument_exists(self):
        assert options.StepsArgument is not None

    def test_commit_options_exist(self):
        for name in (
            "CheckCzOption",
            "AutoStageOption",
            "StageModeOption",
            "CommitMessageFileOption",
            "ForceCommitOption",
            "CommitMessageBackupDirOption",
        ):
            assert hasattr(options, name)

    def test_tag_options_exist(self):
        for name in (
            "TagMessageFileOption",
            "VersionFileOption",
            "StrategyOption",
            "BumpOption",
            "TagOption",
            "TagMessageOption",
            "PreReleaseOption",
            "PostReleaseOption",
            "DevReleaseOption",
            "MetaOption",
            "EpochOption",
            "ForceTagOption",
            "SkipChecksOption",
            "TagMessageBackupDirOption",
        ):
            assert hasattr(options, name)

    def test_push_options_exist(self):
        for name in (
            "AllRemoteOption",
            "RemoteOption",
            "SkipTagOption",
            "SyncBackupOption",
        ):
            assert hasattr(options, name)

    def test_metadata_is_available(self):
        for name in (
            "StepsArgument",
            "CheckCzOption",
            "AutoStageOption",
            "StageModeOption",
            "CommitMessageFileOption",
            "ForceCommitOption",
            "CommitMessageBackupDirOption",
            "TagMessageFileOption",
            "VersionFileOption",
            "StrategyOption",
            "BumpOption",
            "TagOption",
            "TagMessageOption",
            "PreReleaseOption",
            "PostReleaseOption",
            "DevReleaseOption",
            "MetaOption",
            "EpochOption",
            "ForceTagOption",
            "SkipChecksOption",
            "TagMessageBackupDirOption",
            "AllRemoteOption",
            "RemoteOption",
            "SkipTagOption",
            "SyncBackupOption",
        ):
            obj = getattr(options, name)
            assert getattr(obj, "__metadata__", None) is not None
