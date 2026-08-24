# tests/core/git_ops/git/test_service_log.py

"""
Tests for GitService commit history and log operations.

This module covers:

- get_commit_message()
- get_commit_hashes()
- get_raw_log()
- get_commit_count()
"""

from unittest.mock import MagicMock

import pytest

from app.core.git_ops.git.result import CommandResult
from app.core.git_ops.git.service import GitService


@pytest.fixture
def service():
    """
    Create a GitService backed by mocked executor/config.
    """
    executor = MagicMock()
    config = MagicMock()

    return GitService(
        executor=executor,
        config=config,
    )


class TestGetCommitMessage:
    """
    Tests GitService.get_commit_message().
    """

    def test_success(self, service):
        service.executor.show_commit.return_value = CommandResult(
            returncode=0,
            stdout="feat: add login\n\nbody\n",
        )

        assert (
            service.get_commit_message("abc123")
            == "feat: add login\n\nbody"
        )

        service.executor.show_commit.assert_called_once_with("abc123")

    def test_empty_output(self, service):
        service.executor.show_commit.return_value = CommandResult(
            returncode=0,
            stdout="",
        )

        assert service.get_commit_message("abc123") == ""


class TestGetCommitHashes:
    """
    Tests GitService.get_commit_hashes().
    """

    def test_multiple_hashes(self, service):
        service.executor.log_between.return_value = CommandResult(
            returncode=0,
            stdout=(
                "aaa111\n"
                "bbb222\n"
                "ccc333\n"
            ),
        )

        assert service.get_commit_hashes("v1.0.0..HEAD") == [
            "aaa111",
            "bbb222",
            "ccc333",
        ]

        service.executor.log_between.assert_called_once_with(
            "v1.0.0..HEAD",
            "%H",
        )

    def test_empty(self, service):
        service.executor.log_between.return_value = CommandResult(
            returncode=0,
            stdout="",
        )

        assert service.get_commit_hashes("HEAD") == []


class TestGetRawLog:
    """
    Tests GitService.get_raw_log().
    """

    def test_default_format(self, service):
        service.executor.log_between.return_value = CommandResult(
            returncode=0,
            stdout="abc\nxyz\n",
        )

        assert service.get_raw_log("HEAD") == [
            "abc",
            "xyz",
        ]

        service.executor.log_between.assert_called_once_with(
            "HEAD",
            "%H",
            False,
        )

    def test_custom_format(self, service):
        service.executor.log_between.return_value = CommandResult(
            returncode=0,
            stdout="feat\nfix\n",
        )

        result = service.get_raw_log(
            ref_range="HEAD~5..HEAD",
            pretty_format="%s",
            reverse=True,
        )

        assert result == [
            "feat",
            "fix",
        ]

        service.executor.log_between.assert_called_once_with(
            "HEAD~5..HEAD",
            "%s",
            True,
        )

    def test_empty(self, service):
        service.executor.log_between.return_value = CommandResult(
            returncode=0,
            stdout="",
        )

        assert service.get_raw_log("HEAD") == []


class TestGetCommitCount:
    """
    Tests GitService.get_commit_count().
    """

    def test_success(self, service):
        service.executor.get_commit_count.return_value = CommandResult(
            returncode=0,
            stdout="123\n",
        )

        assert service.get_commit_count() == 123

    def test_executor_failure(self, service):
        service.executor.get_commit_count.return_value = CommandResult(
            returncode=1,
            stderr="fatal",
        )

        with pytest.raises(RuntimeError):
            service.get_commit_count()

    def test_invalid_integer(self, service):
        service.executor.get_commit_count.return_value = CommandResult(
            returncode=0,
            stdout="not-a-number",
        )

        with pytest.raises(RuntimeError):
            service.get_commit_count()
