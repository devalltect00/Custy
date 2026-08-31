# tests/core/git_ops/git/test_executor_runner.py

"""
Tests for app.core.git_ops.git.executor.

Part 1:
- constructor
- runner delegation
- _run()
"""

import subprocess
from unittest.mock import MagicMock, patch

import pytest

from app.core.git_ops.git.executor import GitCommandExecutor
from app.core.git_ops.git.result import CommandResult


class TestInitialization:
    """
    Constructor tests.
    """

    def test_constructor_defaults(self):
        executor = GitCommandExecutor()

        assert executor is not None

    def test_constructor_custom_flags(self):
        executor = GitCommandExecutor(
            dry_run=True,
            is_silent=True,
        )

        assert executor is not None


class TestRunnerDelegation:
    """
    Getter / setter delegation.
    """

    @pytest.fixture
    def executor(self):
        executor = GitCommandExecutor()

        executor.runner = MagicMock()

        return executor

    def test_get_silent(self, executor):
        executor.runner.get_silent.return_value = True

        assert executor.get_silent() is True

        executor.runner.get_silent.assert_called_once_with()

    def test_set_silent(self, executor):
        executor.set_silent(True)

        executor.runner.set_silent.assert_called_once_with(True)

    def test_get_is_dry_run(self, executor):
        executor.runner.get_is_dry_run.return_value = True

        assert executor.get_is_dry_run() is True

        executor.runner.get_is_dry_run.assert_called_once_with()

    def test_set_is_dry_run(self, executor):
        executor.set_is_dry_run(True)

        executor.runner.set_is_dry_run.assert_called_once_with(True)


class TestRun:
    """
    Tests for _run().
    """

    @pytest.fixture
    def executor(self):
        executor = GitCommandExecutor()
        executor.runner = MagicMock()
        return executor

    @patch("app.core.git_ops.git.executor.CommandResult.from_completed")
    def test_run_returns_command_result(
        self,
        from_completed,
        executor,
    ):
        completed = MagicMock()

        executor.runner.run.return_value = completed

        expected = MagicMock()

        from_completed.return_value = expected

        result = executor._run(["status"])

        executor.runner.run.assert_called_once_with(
            ["git", "status"],
            check=False,
            read_only=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )

        from_completed.assert_called_once_with(completed)

        assert result is expected

    @patch("app.core.git_ops.git.executor.CommandResult.from_completed")
    def test_terminal_passthrough_inherits_process_streams(
        self,
        from_completed,
        executor,
    ):
        """Interactive Git owns the terminal instead of captured pipes."""

        completed = MagicMock()
        executor.runner.run.return_value = completed
        expected = MagicMock()
        from_completed.return_value = expected

        result = executor._run(["push", "origin", "HEAD"], terminal_passthrough=True)

        executor.runner.run.assert_called_once_with(
            ["git", "push", "origin", "HEAD"],
            check=False,
            read_only=False,
            text=True,
            encoding="utf-8",
        )
        from_completed.assert_called_once_with(completed)
        assert result is expected

    @patch("app.core.git_ops.git.executor.CommandResult.dry_run")
    def test_run_returns_dry_run_result(
        self,
        dry_run,
        executor,
    ):
        expected = MagicMock()

        executor.runner.run.return_value = None
        executor.runner.get_is_dry_run.return_value = True

        dry_run.return_value = expected

        result = executor._run(["status"])

        dry_run.assert_called_once_with()

        assert result is expected

    def test_failed_read_only_command_is_not_reported_as_dry_run(
        self,
        executor,
    ):
        """Discovery failures remain failures while dry-run is enabled."""

        executor.runner.run.return_value = None
        executor.runner.get_is_dry_run.return_value = True

        result = executor._run(["status"], read_only=True)

        assert result.success is False
        assert result.skipped is False

    def test_run_with_check_true(self, executor):
        completed = MagicMock()

        executor.runner.run.return_value = completed

        with patch.object(
            CommandResult,
            "from_completed",
            return_value=MagicMock(),
        ):
            executor._run(
                ["status"],
                check=True,
            )

        assert executor.runner.run.call_args.kwargs["check"] is True

    def test_read_only_flag_is_forwarded(self, executor):
        """Executor discovery explicitly bypasses dry-run simulation."""

        executor.runner.run.return_value = MagicMock()

        with patch.object(
            CommandResult,
            "from_completed",
            return_value=MagicMock(),
        ):
            executor._run(["status"], read_only=True)

        assert executor.runner.run.call_args.kwargs["read_only"] is True

    def test_git_queries_are_read_only(self, executor):
        """Tag discovery is marked safe to execute during dry-run."""

        executor.runner.run.return_value = MagicMock()

        with patch.object(
            CommandResult,
            "from_completed",
            return_value=MagicMock(),
        ):
            executor.get_tags()

        assert executor.runner.run.call_args.kwargs["read_only"] is True

    def test_git_mutations_remain_simulated(self, executor):
        """Staging operations retain the mutating default."""

        executor.runner.run.return_value = MagicMock()

        with patch.object(
            CommandResult,
            "from_completed",
            return_value=MagicMock(),
        ):
            executor.add_all()

        assert executor.runner.run.call_args.kwargs["read_only"] is False
