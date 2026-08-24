# tests/core/git_ops/git/test_executor_core.py

"""
Tests for app.core.git_ops.git.executor.

Part 2:
Core Git command wrappers.
"""

from unittest.mock import MagicMock

import pytest

from app.core.git_ops.git.executor import GitCommandExecutor


@pytest.fixture
def executor():
    executor = GitCommandExecutor()
    executor._run = MagicMock(return_value="OK")
    return executor


class TestCoreCommands:
    """
    Tests core Git command wrappers.
    """

    def test_diff_cached_quiet(self, executor):
        assert executor.diff_cached_quiet() == "OK"

        executor._run.assert_called_once_with(
            ["diff", "--cached", "--quiet"],
            check=False,
            read_only=True,
        )

    def test_add_all(self, executor):
        assert executor.add_all() == "OK"

        executor._run.assert_called_once_with(
            ["add", "."],
            check=True,
        )

    def test_add_update(self, executor):
        assert executor.add_update() == "OK"

        executor._run.assert_called_once_with(
            ["add", "--update"],
            check=True,
        )

    def test_add_files(self, executor):
        files = ["a.py", "b.py"]

        assert executor.add_files(files) == "OK"

        executor._run.assert_called_once_with(
            ["add", "a.py", "b.py"],
            check=True,
        )

    def test_list_staged_files(self, executor):
        assert executor.list_staged_files() == "OK"

        executor._run.assert_called_once_with(
            ["diff", "--cached", "--name-only"],
            check=True,
            read_only=True,
        )

    def test_rev_parse_inside_work_tree(self, executor):
        assert executor.rev_parse_inside_work_tree() == "OK"

        executor._run.assert_called_once_with(
            ["rev-parse", "--is-inside-work-tree"],
            check=False,
            read_only=True,
        )

    def test_rev_parse_head(self, executor):
        assert executor.rev_parse_head() == "OK"

        executor._run.assert_called_once_with(
            ["rev-parse", "--verify", "HEAD"],
            check=False,
            read_only=True,
        )

    def test_current_branch(self, executor):
        assert executor.current_branch() == "OK"

        executor._run.assert_called_once_with(
            ["rev-parse", "--abbrev-ref", "HEAD"],
            check=False,
            read_only=True,
        )

    def test_symbolic_head(self, executor):
        assert executor.symbolic_head() == "OK"

        executor._run.assert_called_once_with(
            ["symbolic-ref", "--short", "HEAD"],
            check=False,
            read_only=True,
        )

    def test_branch_exists(self, executor):
        assert executor.branch_exists("develop") == "OK"

        executor._run.assert_called_once_with(
            ["rev-parse", "--verify", "--quiet", "develop"],
            check=False,
            read_only=True,
        )

    def test_list_local_branches(self, executor):
        """Local branch discovery remains read-only."""

        assert executor.list_local_branches() == "OK"

        executor._run.assert_called_once_with(
            [
                "for-each-ref",
                "refs/heads",
                "--format=%(refname:short)",
            ],
            check=True,
            read_only=True,
        )

    def test_list_merged_branches(self, executor):
        """Merged branch discovery remains read-only."""

        assert executor.list_merged_branches() == "OK"

        executor._run.assert_called_once_with(
            [
                "for-each-ref",
                "refs/heads",
                "--merged",
                "--format=%(refname:short)",
            ],
            check=True,
            read_only=True,
        )

    def test_list_branch_metadata(self, executor):
        """Branch timestamp discovery remains read-only."""

        assert executor.list_branch_metadata() == "OK"

        executor._run.assert_called_once_with(
            [
                "for-each-ref",
                "refs/heads",
                "--format=%(refname:short)|%(committerdate:unix)",
            ],
            check=True,
            read_only=True,
        )

    def test_remote_branch_exists(self, executor):
        """Remote branch discovery remains read-only."""

        assert executor.remote_branch_exists("origin", "feature/test") == "OK"

        executor._run.assert_called_once_with(
            [
                "ls-remote",
                "--heads",
                "origin",
                "feature/test",
            ],
            check=False,
            read_only=True,
        )

    @pytest.mark.parametrize(
        ("force", "flag"),
        [
            (False, "-d"),
            (True, "-D"),
        ],
    )
    def test_delete_local_branch_is_mutating(self, executor, force, flag):
        """Local deletion retains the simulated-mutation default."""

        assert executor.delete_local_branch("feature/test", force=force) == "OK"

        executor._run.assert_called_once_with(
            ["branch", flag, "feature/test"],
            check=True,
        )

    def test_delete_remote_branch_is_mutating(self, executor):
        """Remote deletion retains the simulated-mutation default."""

        assert executor.delete_remote_branch("origin", "feature/test") == "OK"

        executor._run.assert_called_once_with(
            ["push", "origin", "--delete", "feature/test"],
            check=True,
        )

    def test_remote_get_url(self, executor):
        assert executor.remote_get_url("origin") == "OK"

        executor._run.assert_called_once_with(
            ["remote", "get-url", "origin"],
            check=True,
            read_only=True,
        )

    def test_remote_get_url_default(self, executor):
        executor.remote_get_url()

        executor._run.assert_called_once_with(
            ["remote", "get-url", "origin"],
            check=True,
            read_only=True,
        )
