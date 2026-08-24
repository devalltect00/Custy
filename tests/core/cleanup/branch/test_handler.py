# tests/core/cleanup/branch/test_handler.py

"""Unit tests for branch-cleanup handler orchestration."""

from unittest.mock import MagicMock

import pytest

from app.core.cleanup.branch.handler import BranchCleanupHandler
from app.core.cleanup.branch.models import BranchCleanupRequest, BranchCleanupResult


@pytest.fixture
def collaborators(monkeypatch):
    """Replace handler collaborators with observable doubles."""

    git_service = MagicMock()
    git_service.get_is_dry_run.return_value = True
    cleanup_service = MagicMock()
    display = MagicMock()

    create_git = MagicMock(return_value=git_service)
    cleanup_cls = MagicMock(return_value=cleanup_service)
    display_cls = MagicMock(return_value=display)

    monkeypatch.setattr(
        "app.core.cleanup.branch.handler.create_git_service",
        create_git,
    )
    monkeypatch.setattr(
        "app.core.cleanup.branch.handler.BranchCleanupService",
        cleanup_cls,
    )
    monkeypatch.setattr(
        "app.core.cleanup.branch.handler.BranchCleanupDisplay",
        display_cls,
    )

    return {
        "git": git_service,
        "cleanup": cleanup_service,
        "display": display,
        "create_git": create_git,
        "cleanup_cls": cleanup_cls,
        "display_cls": display_cls,
    }


class TestInitialization:
    """Tests collaborator construction."""

    def test_builds_collaborators_with_execution_flags(self, collaborators):
        """Dry-run and silent state reach the Git layer."""

        request = BranchCleanupRequest(include_prefixes=["feature/"])

        BranchCleanupHandler(
            request,
            dry_run=True,
            silent=True,
        )

        collaborators["create_git"].assert_called_once_with(
            dry_run=True,
            no_debug=True,
        )
        collaborators["cleanup_cls"].assert_called_once_with(
            collaborators["git"]
        )
        collaborators["display_cls"].assert_called_once_with()


class TestClean:
    """Tests cleanup orchestration and display routing."""

    def test_no_prefixes_stops_before_discovery(self, collaborators):
        """Missing prefixes produce a safe, dry-run-aware result."""

        handler = BranchCleanupHandler(
            BranchCleanupRequest(),
            dry_run=True,
        )

        result = handler.clean()

        collaborators["display"].show_start.assert_called_once_with()
        collaborators["display"].show_no_prefixes.assert_called_once_with()
        collaborators["cleanup"].cleanup.assert_not_called()
        assert result.dry_run is True

    def test_empty_scan_shows_no_branch_message(self, collaborators):
        """An empty scan does not render a normal summary."""

        request = BranchCleanupRequest(include_prefixes=["feature/"])
        expected = BranchCleanupResult(scanned=0)
        collaborators["cleanup"].cleanup.return_value = expected
        handler = BranchCleanupHandler(request)

        result = handler.clean()

        collaborators["cleanup"].cleanup.assert_called_once_with(request)
        collaborators["display"].show_no_branches.assert_called_once_with()
        collaborators["display"].show_summary.assert_not_called()
        assert result is expected

    def test_nonempty_scan_shows_summary(self, collaborators):
        """A completed scan is forwarded to the summary display."""

        request = BranchCleanupRequest(include_prefixes=["feature/"])
        expected = BranchCleanupResult(
            scanned=2,
            deleted_local=["feature/old"],
            skipped=["feature/recent"],
        )
        collaborators["cleanup"].cleanup.return_value = expected
        handler = BranchCleanupHandler(request)

        result = handler.clean()

        collaborators["display"].show_summary.assert_called_once_with(expected)
        collaborators["display"].show_no_branches.assert_not_called()
        assert result is expected
