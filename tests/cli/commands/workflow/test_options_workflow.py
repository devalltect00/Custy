# tests/cli/commands/workflow/test_options_workflow.py


"""
tests/cli/commands/workflow/test_options.py

Tests for CLI option declarations of the workflow command.
"""

from app.cli.commands.workflow import options


class TestWorkflowOptions:
    """Validate Typer option definitions."""

    def test_transition_options_exist(self):
        for name in (
            "EnforceOption",
            "CheckTransitionOption",
            "FromBranchOption",
            "ToBranchOption",
            "FromTagOption",
            "ToTagOption",
        ):
            assert hasattr(options, name)

    def test_sync_option_exists(self):
        assert options.SyncBackupOption is not None

    def test_execution_options_exist(self):
        assert options.DryRunOption is not None
        assert options.DebugOption is not None
        assert options.LogLevelOption is not None

    def test_expected_symbols_are_exported(self):
        expected = (
            "EnforceOption",
            "CheckTransitionOption",
            "FromBranchOption",
            "ToBranchOption",
            "FromTagOption",
            "ToTagOption",
            "SyncBackupOption",
            "DryRunOption",
            "DebugOption",
            "LogLevelOption",
        )
        for symbol in expected:
            assert hasattr(options, symbol)

    def test_options_have_metadata(self):
        for name in (
            "EnforceOption",
            "CheckTransitionOption",
            "FromBranchOption",
            "ToBranchOption",
            "FromTagOption",
            "ToTagOption",
            "SyncBackupOption",
            "DryRunOption",
            "DebugOption",
            "LogLevelOption",
        ):
            option = getattr(options, name)
            assert getattr(option, "__metadata__", None) is not None
