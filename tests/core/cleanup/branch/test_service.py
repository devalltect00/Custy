# tests/core/cleanup/branch/test_service.py

"""Unit tests for branch-cleanup filtering and orchestration."""

from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest

from app.cli.constants.enums import MergeStatusChoices
from app.core.cleanup.branch.models import BranchCleanupRequest, BranchInfo
from app.core.cleanup.branch.service import BranchCleanupService


def make_branch(
    name: str,
    *,
    days_old: int = 60,
    merged: bool = True,
    remote_exists: bool = True,
) -> BranchInfo:
    """Build branch metadata with deterministic filtering inputs.

    Args:
        name:
            Branch name.

        days_old:
            Age of the latest commit in days.

        merged:
            Whether the branch is merged.

        remote_exists:
            Whether a matching remote branch exists.

    Returns:
        Branch metadata for cleanup tests.
    """

    return BranchInfo(
        name=name,
        last_commit=datetime.now() - timedelta(days=days_old),
        merged=merged,
        remote_exists=remote_exists,
    )


@pytest.fixture
def git_service():
    """Create a Git-service double with normal execution enabled."""

    service = MagicMock()
    service.executor.get_is_dry_run.return_value = False
    return service


@pytest.fixture
def cleanup_service(git_service):
    """Create a cleanup service using the Git-service double."""

    return BranchCleanupService(git_service)


class TestCleanup:
    """Tests complete branch-cleanup decisions."""

    def test_deletes_matching_local_and_remote_branch(
        self,
        cleanup_service,
        git_service,
    ):
        """A matching merged branch is deleted from both locations."""

        git_service.list_branches.return_value = [
            make_branch("feature/complete"),
        ]
        request = BranchCleanupRequest(include_prefixes=["feature/"])

        result = cleanup_service.cleanup(request)

        git_service.delete_local_branch.assert_called_once_with(
            "feature/complete"
        )
        git_service.delete_remote_branch.assert_called_once_with(
            "feature/complete",
            remote="origin",
        )
        assert result.scanned == 1
        assert result.deleted_local == ["feature/complete"]
        assert result.deleted_remote == ["feature/complete"]
        assert result.skipped == []

    def test_skips_protected_and_nonmatching_branches(
        self,
        cleanup_service,
        git_service,
    ):
        """Protected and prefix-mismatched branches remain untouched."""

        git_service.list_branches.return_value = [
            make_branch("main"),
            make_branch("docs/guide"),
        ]
        request = BranchCleanupRequest(include_prefixes=["feature/", "main"])

        result = cleanup_service.cleanup(request)

        git_service.delete_local_branch.assert_not_called()
        git_service.delete_remote_branch.assert_not_called()
        assert result.skipped == ["main", "docs/guide"]

    def test_remote_deletion_requires_remote_branch(
        self,
        cleanup_service,
        git_service,
    ):
        """Local cleanup proceeds when no remote branch exists."""

        git_service.list_branches.return_value = [
            make_branch("feature/local", remote_exists=False),
        ]
        request = BranchCleanupRequest(include_prefixes=["feature/"])

        result = cleanup_service.cleanup(request)

        git_service.delete_local_branch.assert_called_once_with("feature/local")
        git_service.delete_remote_branch.assert_not_called()
        assert result.deleted_local == ["feature/local"]
        assert result.deleted_remote == []

    def test_respects_disabled_deletion_targets(
        self,
        cleanup_service,
        git_service,
    ):
        """Request flags can disable both local and remote deletion."""

        git_service.list_branches.return_value = [
            make_branch("feature/report-only"),
        ]
        request = BranchCleanupRequest(
            include_prefixes=["feature/"],
            delete_local=False,
            delete_remote=False,
        )

        result = cleanup_service.cleanup(request)

        git_service.delete_local_branch.assert_not_called()
        git_service.delete_remote_branch.assert_not_called()
        assert result.deleted_local == []
        assert result.deleted_remote == []
        assert result.skipped == []

    def test_preserves_dry_run_state(self, cleanup_service, git_service):
        """Result metadata identifies planned deletion operations."""

        git_service.executor.get_is_dry_run.return_value = True
        git_service.list_branches.return_value = [
            make_branch("feature/preview"),
        ]

        result = cleanup_service.cleanup(
            BranchCleanupRequest(include_prefixes=["feature/"])
        )

        assert result.dry_run is True
        assert result.deleted_local == ["feature/preview"]
        assert result.deleted_remote == ["feature/preview"]


class TestFiltering:
    """Tests individual cleanup filters."""

    @pytest.mark.parametrize(
        ("branch", "cleanup_request", "expected"),
        [
            (
                make_branch("feature/merged", merged=True),
                BranchCleanupRequest(
                    include_prefixes=["feature/"],
                    merge_status=MergeStatusChoices.MERGED,
                ),
                True,
            ),
            (
                make_branch("feature/unmerged", merged=False),
                BranchCleanupRequest(
                    include_prefixes=["feature/"],
                    merge_status=MergeStatusChoices.MERGED,
                ),
                False,
            ),
            (
                make_branch("feature/unmerged", merged=False),
                BranchCleanupRequest(
                    include_prefixes=["feature/"],
                    merge_status=MergeStatusChoices.UNMERGED,
                ),
                True,
            ),
            (
                make_branch("feature/fresh", days_old=5),
                BranchCleanupRequest(
                    include_prefixes=["feature/"],
                    merge_status=MergeStatusChoices.ALL,
                    max_age=timedelta(days=30),
                ),
                False,
            ),
            (
                make_branch("feature/old", days_old=60),
                BranchCleanupRequest(
                    include_prefixes=["feature/"],
                    merge_status=MergeStatusChoices.ALL,
                    max_age=timedelta(days=30),
                ),
                True,
            ),
            (
                make_branch("feature/recent", days_old=5),
                BranchCleanupRequest(
                    include_prefixes=["feature/"],
                    merge_status=MergeStatusChoices.ALL,
                    before=datetime.now() - timedelta(days=30),
                ),
                False,
            ),
            (
                make_branch("feature/archive", days_old=60),
                BranchCleanupRequest(
                    include_prefixes=["feature/"],
                    merge_status=MergeStatusChoices.ALL,
                    before=datetime.now() - timedelta(days=30),
                ),
                True,
            ),
        ],
    )
    def test_should_delete(
        self,
        cleanup_service,
        branch,
        cleanup_request,
        expected,
    ):
        """Every configured filter participates in the decision."""

        assert (
            cleanup_service._should_delete(branch, cleanup_request)
            is expected
        )
