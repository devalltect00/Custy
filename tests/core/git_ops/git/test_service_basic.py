# tests/core/git_ops/git/test_service_basic.py

"""
Tests for basic GitService repository operations.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from app.core.git_ops.git.service import GitService


@pytest.fixture
def service():
    executor = MagicMock()
    config = MagicMock()

    return GitService(
        executor=executor,
        config=config,
    )


class TestInitialization:
    """
    Tests GitService construction.
    """

    def test_constructor(self):
        executor = MagicMock()
        config = MagicMock()

        service = GitService(
            executor=executor,
            config=config,
        )

        assert service.executor is executor
        assert service.config is config


class TestIsGitRepo:
    """
    Tests is_git_repo().
    """

    @patch.object(Path, "exists", return_value=True)
    def test_git_directory_exists(self, _, service):
        assert service.is_git_repo() is True

        service.executor.rev_parse_inside_work_tree.assert_not_called()

    @patch.object(Path, "exists", return_value=False)
    def test_rev_parse_success(self, _, service):
        result = MagicMock()
        result.success = True

        service.executor.rev_parse_inside_work_tree.return_value = result

        assert service.is_git_repo() is True

    @patch.object(Path, "exists", return_value=False)
    def test_rev_parse_failure(self, _, service):
        result = MagicMock()
        result.success = False

        service.executor.rev_parse_inside_work_tree.return_value = result

        assert service.is_git_repo() is False


class TestHasCommit:
    """
    Tests has_commit().
    """

    def test_true(self, service):
        result = MagicMock()
        result.success = True

        service.executor.rev_parse_head.return_value = result

        assert service.has_commit() is True

    def test_false(self, service):
        result = MagicMock()
        result.success = False

        service.executor.rev_parse_head.return_value = result

        assert service.has_commit() is False


class TestBranchExists:
    """
    Tests branch_exists().
    """

    def test_exists(self, service):
        result = MagicMock()
        result.success = True

        service.executor.branch_exists.return_value = result

        assert service.branch_exists("develop") is True

    def test_missing(self, service):
        result = MagicMock()
        result.success = False

        service.executor.branch_exists.return_value = result

        assert service.branch_exists("develop") is False


class TestGetCurrentBranch:
    """
    Tests get_current_branch().
    """

    def test_no_commit_defaults_symbolic(self, service):
        service.has_commit = MagicMock(return_value=False)

        result = MagicMock()
        result.stdout = "develop\n"

        service.executor.symbolic_head.return_value = result

        assert service.get_current_branch() == "develop"

    def test_no_commit_no_stdout(self, service):
        service.has_commit = MagicMock(return_value=False)

        result = MagicMock()
        result.stdout = ""

        service.executor.symbolic_head.return_value = result

        assert service.get_current_branch() == "main"

    def test_current_branch(self, service):
        service.has_commit = MagicMock(return_value=True)

        result = MagicMock()
        result.stdout = "feature/demo\n"

        service.executor.current_branch.return_value = result

        assert service.get_current_branch() == "feature/demo"

    def test_unknown_branch(self, service):
        service.has_commit = MagicMock(return_value=True)

        result = MagicMock()
        result.stdout = ""

        service.executor.current_branch.return_value = result

        assert service.get_current_branch() == "unknown"

    def test_detached_head(self, service):
        service.has_commit = MagicMock(return_value=True)

        result = MagicMock()
        result.stdout = "HEAD\n"

        service.executor.current_branch.return_value = result

        assert service.get_current_branch() == "HEAD"


class TestGetLatestTag:
    """
    Tests get_latest_tag().
    """

    def test_existing_tag(self, service):
        result = MagicMock()
        result.stdout = "v2.1.0\n"

        service.executor.describe_latest_tag.return_value = result

        assert service.get_latest_tag() == "v2.1.0"

    def test_no_tags(self, service):
        result = MagicMock()
        result.stdout = ""

        service.executor.describe_latest_tag.return_value = result

        assert service.get_latest_tag() == "v0.0.0"
