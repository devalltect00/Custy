# tests/core/git_ops/git/test_result.py

"""
Unit tests for app.core.git_ops.git.result.

These tests verify the lightweight result models used throughout the
Git execution layer.

Coverage target:
    - CommandResult: 100%
    - OperationResult: 100%
"""

from types import SimpleNamespace

from app.core.git_ops.git.result import (
    CommandResult,
    OperationResult,
)

# =========================================================
# CommandResult
# =========================================================


class TestCommandResult:
    """
    Tests for CommandResult.
    """

    def test_success_true(self) -> None:
        """
        success returns True when returncode == 0.
        """
        result = CommandResult(returncode=0)

        assert result.success is True

    def test_success_false(self) -> None:
        """
        success returns False when returncode != 0.
        """
        result = CommandResult(returncode=1)

        assert result.success is False

    def test_has_changes_true(self) -> None:
        """
        has_changes returns True when returncode != 0.
        """
        result = CommandResult(returncode=1)

        assert result.has_changes is True

    def test_has_changes_false(self) -> None:
        """
        has_changes returns False when returncode == 0.
        """
        result = CommandResult(returncode=0)

        assert result.has_changes is False

    def test_from_completed(self) -> None:
        """
        from_completed copies subprocess fields.
        """
        completed = SimpleNamespace(
            returncode=0,
            stdout="hello",
            stderr="",
        )

        result = CommandResult.from_completed(completed)

        assert result.returncode == 0
        assert result.stdout == "hello"
        assert result.stderr == ""
        assert result.skipped is False

    def test_from_completed_none_output(self) -> None:
        """
        None stdout/stderr become empty strings.
        """
        completed = SimpleNamespace(
            returncode=1,
            stdout=None,
            stderr=None,
        )

        result = CommandResult.from_completed(completed)

        assert result.returncode == 1
        assert result.stdout == ""
        assert result.stderr == ""

    def test_dry_run(self) -> None:
        """
        dry_run returns a skipped successful result.
        """
        result = CommandResult.dry_run()

        assert result.returncode == 0
        assert result.success is True
        assert result.skipped is True
        assert result.stdout == ""
        assert result.stderr == ""


# =========================================================
# OperationResult
# =========================================================


class TestOperationResult:
    """
    Tests for OperationResult.
    """

    def test_ok_defaults(self) -> None:
        """
        ok() creates a successful result.
        """
        result = OperationResult.ok()

        assert result.success is True
        assert result.message == ""
        assert result.data is None

    def test_ok_with_values(self) -> None:
        """
        ok() stores message and data.
        """
        payload = {"version": "1.2.3"}

        result = OperationResult.ok(
            message="done",
            data=payload,
        )

        assert result.success is True
        assert result.message == "done"
        assert result.data == payload

    def test_fail_defaults(self) -> None:
        """
        fail() creates an unsuccessful result.
        """
        result = OperationResult.fail()

        assert result.success is False
        assert result.message == ""
        assert result.data is None

    def test_fail_with_values(self) -> None:
        """
        fail() stores message and data.
        """
        payload = {"reason": "git"}

        result = OperationResult.fail(
            message="failed",
            data=payload,
        )

        assert result.success is False
        assert result.message == "failed"
        assert result.data == payload
