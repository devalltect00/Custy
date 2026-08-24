# tests/cli/commands/workflow/test_models_workflow.py


"""
tests/cli/commands/workflow/test_models.py

Unit tests for BranchWorkflowArgs.
"""

from app.cli.commands.workflow.models import BranchWorkflowArgs
from app.cli.constants import LogLevelChoices


class TestBranchWorkflowArgs:

    def test_construct(self):
        args = BranchWorkflowArgs(
            enforce=True,
            check_transition=True,
            from_branch="develop",
            to_branch="main",
            from_tag="v1.0.0",
            to_tag="v1.1.0",
            sync_backup=True,
            dry_run=False,
            no_debug=True,
            log_level=LogLevelChoices.INFO,
        )

        assert args.enforce is True
        assert args.check_transition is True
        assert args.from_branch == "develop"
        assert args.to_branch == "main"
        assert args.from_tag == "v1.0.0"
        assert args.to_tag == "v1.1.0"
        assert args.sync_backup is True
        assert args.log_level == LogLevelChoices.INFO

    def test_dataclass_equality(self):
        left = BranchWorkflowArgs(
            False, False, None, None, None, None,
            False, False, False, LogLevelChoices.INFO
        )
        right = BranchWorkflowArgs(
            False, False, None, None, None, None,
            False, False, False, LogLevelChoices.INFO
        )

        assert left == right
