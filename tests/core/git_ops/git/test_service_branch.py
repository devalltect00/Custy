# tests/core/git_ops/git/test_service_branch.py

"""
Tests for branch-related GitService methods.
"""

from datetime import datetime
from unittest.mock import MagicMock

import pytest

from app.core.git_ops.git.result import CommandResult
from app.core.git_ops.git.service import GitService


@pytest.fixture
def service():
    executor = MagicMock()
    config = MagicMock()

    return GitService(
        executor=executor,
        config=config,
    )


class TestBranchExists:
    """
    Tests branch_exists().
    """

    def test_exists(self, service):
        result = MagicMock()
        result.success = True

        service.executor.branch_exists.return_value = result

        assert service.branch_exists("develop") is True

        service.executor.branch_exists.assert_called_once_with("develop")

    def test_missing(self, service):
        result = MagicMock()
        result.success = False

        service.executor.branch_exists.return_value = result

        assert service.branch_exists("develop") is False


class TestGetCurrentBranch:
    """
    Tests get_current_branch().
    """

    def test_with_commits(self, service):
        service.has_commit = MagicMock(return_value=True)

        result = MagicMock()
        result.stdout = "develop\n"

        service.executor.current_branch.return_value = result

        assert service.get_current_branch() == "develop"

    def test_with_commits_empty(self, service):
        service.has_commit = MagicMock(return_value=True)

        result = MagicMock()
        result.stdout = ""

        service.executor.current_branch.return_value = result

        assert service.get_current_branch() == "unknown"

    def test_without_commits(self, service):
        service.has_commit = MagicMock(return_value=False)

        result = MagicMock()
        result.stdout = "main\n"

        service.executor.symbolic_head.return_value = result

        assert service.get_current_branch() == "main"

    def test_without_commits_empty(self, service):
        service.has_commit = MagicMock(return_value=False)

        result = MagicMock()
        result.stdout = ""

        service.executor.symbolic_head.return_value = result

        assert service.get_current_branch() == "main"

    def test_detached_head(self, service):
        service.has_commit = MagicMock(return_value=True)

        result = MagicMock()
        result.stdout = "HEAD\n"

        service.executor.current_branch.return_value = result

        assert service.get_current_branch() == "HEAD"


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


class TestListBranches:
    """Tests branch metadata aggregation."""

    def test_combines_metadata_merge_and_remote_state(self, service):
        """Structured branches include all cleanup metadata."""

        service.executor.list_branch_metadata.return_value = CommandResult(
            returncode=0,
            stdout="feature/one|1700000000\nfeature/two|1700001000\n",
        )
        service.executor.list_merged_branches.return_value = CommandResult(
            returncode=0,
            stdout="feature/one\n",
        )
        service.remote_branch_exists = MagicMock(side_effect=[True, False])

        branches = service.list_branches()

        assert [branch.name for branch in branches] == [
            "feature/one",
            "feature/two",
        ]
        assert branches[0].merged is True
        assert branches[1].merged is False
        assert branches[0].remote_exists is True
        assert branches[1].remote_exists is False
        assert branches[0].last_commit == datetime.fromtimestamp(1700000000)
        assert [
            entry.args[0] for entry in service.remote_branch_exists.call_args_list
        ] == ["feature/one", "feature/two"]

    def test_ignores_empty_metadata_lines(self, service):
        """Blank Git output does not create invalid branch objects."""

        service.executor.list_branch_metadata.return_value = CommandResult(
            returncode=0,
            stdout="\n  \n",
        )
        service.executor.list_merged_branches.return_value = CommandResult(
            returncode=0,
            stdout="",
        )

        assert service.list_branches() == []


class TestRemoteBranchExists:
    """Tests remote branch discovery."""

    @pytest.mark.parametrize(
        ("stdout", "expected"),
        [
            ("abc refs/heads/feature/test\n", True),
            ("", False),
        ],
    )
    def test_returns_output_presence(self, service, stdout, expected):
        """Any ls-remote output indicates that the branch exists."""

        service.resolve_default_remote = MagicMock(return_value="origin")
        service.executor.remote_branch_exists.return_value = CommandResult(
            returncode=0,
            stdout=stdout,
        )

        assert service.remote_branch_exists("feature/test") is expected
        service.executor.remote_branch_exists.assert_called_once_with(
            "origin",
            "feature/test",
        )


class TestDeleteBranch:
    """Tests local and remote branch-deletion delegation."""

    def test_delete_local_branch(self, service):
        """Successful local deletion delegates force behavior."""

        service.executor.delete_local_branch.return_value = CommandResult(returncode=0)

        service.delete_local_branch("feature/test", force=True)

        service.executor.delete_local_branch.assert_called_once_with(
            "feature/test",
            force=True,
        )

    def test_delete_local_branch_failure_raises(self, service):
        """A failed local deletion becomes a service-level error."""

        service.executor.delete_local_branch.return_value = CommandResult(returncode=1)

        with pytest.raises(RuntimeError, match="feature/test"):
            service.delete_local_branch("feature/test")

    def test_delete_remote_branch(self, service):
        """Successful remote deletion resolves and delegates the remote."""

        service.resolve_default_remote = MagicMock(return_value="backup")
        service.executor.delete_remote_branch.return_value = CommandResult(returncode=0)

        service.delete_remote_branch("feature/test")

        service.executor.delete_remote_branch.assert_called_once_with(
            "backup",
            "feature/test",
        )

    def test_delete_remote_branch_failure_raises(self, service):
        """A failed remote deletion becomes a service-level error."""

        service.resolve_default_remote = MagicMock(return_value="origin")
        service.executor.delete_remote_branch.return_value = CommandResult(returncode=1)

        with pytest.raises(RuntimeError, match="origin"):
            service.delete_remote_branch("feature/test")
