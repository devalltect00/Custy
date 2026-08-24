# tests/core/cleanup/branch/test_display.py

"""Unit tests for branch-cleanup terminal presentation."""

from unittest.mock import MagicMock

import pytest

import app.core.cleanup.branch.display as display_module
from app.core.cleanup.branch.display import BranchCleanupDisplay
from app.core.cleanup.branch.models import BranchCleanupResult


@pytest.fixture
def presentation(monkeypatch):
    """Replace Rich presentation helpers with observable doubles."""

    printed = MagicMock()
    info = MagicMock(return_value="INFO")
    warning = MagicMock(return_value="WARNING")
    success = MagicMock(return_value="SUCCESS")
    table = MagicMock(return_value="TABLE")

    monkeypatch.setattr(display_module.console, "print", printed)
    monkeypatch.setattr(display_module, "info_panel", info)
    monkeypatch.setattr(display_module, "warning_panel", warning)
    monkeypatch.setattr(display_module, "success_panel", success)
    monkeypatch.setattr(display_module, "branch_cleanup_table", table)

    return {
        "printed": printed,
        "info": info,
        "warning": warning,
        "success": success,
        "table": table,
    }


class TestBranchCleanupDisplay:
    """Tests every branch-cleanup presentation route."""

    def test_show_start_uses_information_panel(self, presentation):
        """The scan lifecycle begins with an information panel."""

        BranchCleanupDisplay().show_start()

        presentation["info"].assert_called_once_with("Scanning Git branches...")
        presentation["printed"].assert_called_once_with("INFO")

    def test_show_no_branches_uses_warning_panel(self, presentation):
        """An empty result is shown as an actionable warning."""

        BranchCleanupDisplay().show_no_branches()

        message = presentation["warning"].call_args.args[0]
        assert "No branches matched" in message
        presentation["printed"].assert_called_once_with("WARNING")

    def test_show_no_prefixes_explains_safety_skip(self, presentation):
        """Missing prefixes explain why deletion was not attempted."""

        BranchCleanupDisplay().show_no_prefixes()

        message = presentation["warning"].call_args.args[0]
        assert "cleanup was skipped" in message
        assert "--prefix" in message
        presentation["printed"].assert_called_once_with("WARNING")

    def test_show_summary_renders_applied_result(self, presentation):
        """Normal cleanup reports applied local and remote counts."""

        result = BranchCleanupResult(
            scanned=3,
            deleted_local=["feature/one"],
            deleted_remote=["feature/one"],
            skipped=["main"],
        )

        BranchCleanupDisplay().show_summary(result)

        presentation["table"].assert_called_once_with(result)
        message = presentation["success"].call_args.args[0]
        assert "Deleted" in message
        assert "Scanned      : 3" in message
        assert "Dry-run mode enabled" not in message
        assert [
            entry.args[0]
            for entry in presentation["printed"].call_args_list
        ] == ["TABLE", "SUCCESS"]

    def test_show_summary_labels_dry_run_candidates(self, presentation):
        """Preview summaries never imply that branches were deleted."""

        result = BranchCleanupResult(
            scanned=1,
            deleted_local=["feature/preview"],
            deleted_remote=["feature/preview"],
            dry_run=True,
        )

        BranchCleanupDisplay().show_summary(result)

        message = presentation["success"].call_args.args[0]
        assert "Would delete" in message
        assert "No local or remote branches were deleted" in message
