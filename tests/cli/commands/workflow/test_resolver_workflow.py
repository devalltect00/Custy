# tests/cli/commands/workflow/test_resolver_workflow.py


"""
tests/cli/commands/workflow/test_resolver.py

Unit tests for resolve_workflow_args().
"""

from app.cli.commands.workflow import resolver
from app.cli.commands.workflow.models import BranchWorkflowArgs
from app.cli.constants import LogLevelChoices


class DummyConfig:
    def resolve(self, value, key, default):
        return default if value is None else value


class DummyCliArgs:
    def __init__(self, **kwargs):
        self.enforce = kwargs.get("enforce")
        self.check_transition = kwargs.get("check_transition")
        self.from_branch = kwargs.get("from_branch")
        self.to_branch = kwargs.get("to_branch")
        self.from_tag = kwargs.get("from_tag")
        self.to_tag = kwargs.get("to_tag")
        self.sync_backup = kwargs.get("sync_backup")
        self.dry_run = kwargs.get("dry_run")
        self.debug = kwargs.get("debug")
        self.log_level = kwargs.get("log_level")


class TestWorkflowResolver:

    def test_returns_branch_workflow_args(self):
        args = resolver.resolve_workflow_args(
            DummyConfig(),
            DummyCliArgs(),
        )
        assert isinstance(args, BranchWorkflowArgs)

    def test_defaults_are_used(self):
        args = resolver.resolve_workflow_args(
            DummyConfig(),
            DummyCliArgs(),
        )

        assert args.enforce is False
        assert args.check_transition is False
        assert args.sync_backup is False
        assert args.dry_run is False
        assert args.no_debug is False
        assert args.log_level == LogLevelChoices.INFO

    def test_explicit_values_are_preserved(self):
        args = resolver.resolve_workflow_args(
            DummyConfig(),
            DummyCliArgs(
                enforce=True,
                check_transition=True,
                from_branch="develop",
                to_branch="main",
                from_tag="v1.0.0",
                to_tag="v1.1.0",
                sync_backup=True,
                dry_run=True,
                debug=False,
                log_level=LogLevelChoices.DEBUG,
            ),
        )

        assert args.enforce is True
        assert args.check_transition is True
        assert args.from_branch == "develop"
        assert args.to_branch == "main"
        assert args.from_tag == "v1.0.0"
        assert args.to_tag == "v1.1.0"
        assert args.sync_backup is True
        assert args.dry_run is True
        assert args.no_debug is True
        assert args.log_level == LogLevelChoices.DEBUG

    def test_debug_true_disables_no_debug(self):
        args = resolver.resolve_workflow_args(
            DummyConfig(),
            DummyCliArgs(debug=True),
        )
        assert args.no_debug is False
