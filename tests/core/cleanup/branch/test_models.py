# tests/core/cleanup/branch/test_models.py

"""Unit tests for branch-cleanup domain models."""

from datetime import datetime, timedelta

from app.core.cleanup.branch.models import (
    DEFAULT_PROTECTED_BRANCHES,
    BranchCleanupRequest,
    BranchCleanupResult,
    BranchInfo,
)


class TestBranchInfo:
    """Tests branch metadata helpers."""

    def test_age_reports_elapsed_time(self):
        """Age is calculated from the latest branch commit."""

        branch = BranchInfo(
            name="feature/coverage",
            last_commit=datetime.now() - timedelta(days=5),
            merged=True,
        )

        assert timedelta(days=4) < branch.age < timedelta(days=6)


class TestBranchCleanupRequest:
    """Tests cleanup-request defaults."""

    def test_safe_defaults(self):
        """Default request protects primary branches and requires prefixes."""

        request = BranchCleanupRequest()

        assert request.include_prefixes == []
        assert request.delete_local is True
        assert request.delete_remote is True
        assert request.remote == "origin"
        assert request.protected_branches == list(DEFAULT_PROTECTED_BRANCHES)

    def test_protected_branch_lists_are_independent(self):
        """Mutating one request does not affect another request."""

        first = BranchCleanupRequest()
        second = BranchCleanupRequest()

        first.protected_branches.append("release")

        assert "release" not in second.protected_branches


class TestBranchCleanupResult:
    """Tests cleanup-result counters and success state."""

    def test_counters_and_success(self):
        """Result properties summarize deletion outcomes."""

        result = BranchCleanupResult(
            deleted_local=["feature/one", "feature/two"],
            skipped=["main"],
        )

        assert result.deleted_count == 2
        assert result.skipped_count == 1
        assert result.failed_count == 0
        assert result.success is True

    def test_failure_marks_result_unsuccessful(self):
        """Any recorded failure makes the result unsuccessful."""

        result = BranchCleanupResult(
            failed={"feature/broken": "permission denied"},
        )

        assert result.failed_count == 1
        assert result.success is False
