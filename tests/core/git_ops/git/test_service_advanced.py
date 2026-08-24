# tests/core/git_ops/git/test_service_advanced.py

"""
Tests for advanced GitService commit retrieval operations.

Covers:
- get_commits_between()
- get_commits_between_tags()
"""

from unittest.mock import MagicMock

import pytest

from app.core.git_ops.git.result import CommandResult
from app.core.git_ops.git.service import GitService


@pytest.fixture
def service():
    """
    Create GitService backed by mocked executor.
    """
    executor = MagicMock()
    config = MagicMock()

    return GitService(
        executor=executor,
        config=config,
    )


# ============================================================
# get_commits_between()
# ============================================================


class TestGetCommitsBetween:
    """
    Tests GitService.get_commits_between().
    """

    def test_returns_commit_messages(self, service):
        service.executor.log_between.return_value = CommandResult(
            returncode=0,
            stdout="aaa111\nbbb222\n",
        )

        service.executor.show_commit.side_effect = [
            CommandResult(
                returncode=0,
                stdout="feat: first commit",
            ),
            CommandResult(
                returncode=0,
                stdout="fix: second commit",
            ),
        ]

        assert service.get_commits_between(
            "v1.0.0",
            "v1.1.0",
        ) == [
            "feat: first commit",
            "fix: second commit",
        ]

        service.executor.log_between.assert_called_once_with(
            "v1.0.0..v1.1.0",
        )

    def test_empty_start_tag(self, service):
        service.executor.log_between.return_value = CommandResult(
            returncode=0,
            stdout="abc123\n",
        )

        service.executor.show_commit.return_value = CommandResult(
            returncode=0,
            stdout="feat: initial",
        )

        assert service.get_commits_between(
            "",
            "HEAD",
        ) == [
            "feat: initial",
        ]

        service.executor.log_between.assert_called_once_with(
            "HEAD",
        )

    def test_no_commits(self, service):
        service.executor.log_between.return_value = CommandResult(
            returncode=0,
            stdout="",
        )

        assert service.get_commits_between(
            "v1",
            "v2",
        ) == []

    def test_skip_empty_commit_output(self, service):
        service.executor.log_between.return_value = CommandResult(
            returncode=0,
            stdout="aaa\nbbb\n",
        )

        service.executor.show_commit.side_effect = [
            CommandResult(
                returncode=0,
                stdout="",
            ),
            CommandResult(
                returncode=0,
                stdout="feat: valid",
            ),
        ]

        assert service.get_commits_between(
            "v1",
            "v2",
        ) == [
            "feat: valid",
        ]


# ============================================================
# get_commits_between_tags()
# ============================================================


class TestGetCommitsBetweenTags:
    """
    Tests GitService.get_commits_between_tags().
    """

    def test_single_commit(self, service):
        service.executor.get_commits_between_tags.return_value = CommandResult(
            returncode=0,
            stdout=(
                "abc123\n"
                "feat: login\n"
                "Alice\n"
                "2026-06-27\n"
                "Body line\n"
                "---END---"
            ),
        )

        result = service.get_commits_between_tags(
            "v1.0.0",
            "v1.1.0",
        )

        assert result == [
            {
                "sha": "abc123",
                "header": "feat: login",
                "author": "Alice",
                "date": "2026-06-27",
                "body": "Body line",
            }
        ]

    def test_multiple_commits(self, service):
        service.executor.get_commits_between_tags.return_value = CommandResult(
            returncode=0,
            stdout=(
                "111\n"
                "feat: one\n"
                "Alice\n"
                "2026-01-01\n"
                "Body1\n"
                "---END---"
                "222\n"
                "fix: two\n"
                "Bob\n"
                "2026-01-02\n"
                "Body2\n"
                "---END---"
            ),
        )

        result = service.get_commits_between_tags(
            "v1",
            "v2",
        )

        assert len(result) == 2
        assert result[0]["sha"] == "111"
        assert result[1]["sha"] == "222"

    def test_empty_stdout(self, service):
        service.executor.get_commits_between_tags.return_value = CommandResult(
            returncode=0,
            stdout="",
        )

        assert service.get_commits_between_tags(
            "v1",
            "v2",
        ) == []

    def test_skip_invalid_chunk(self, service):
        service.executor.get_commits_between_tags.return_value = CommandResult(
            returncode=0,
            stdout=(
                "invalid\n"
                "---END---"
                "abc\n"
                "feat: login\n"
                "Alice\n"
                "2026-06-27\n"
                "Body\n"
                "---END---"
            ),
        )

        result = service.get_commits_between_tags(
            "v1",
            "v2",
        )

        assert len(result) == 1
        assert result[0]["sha"] == "abc"

    def test_multiline_body(self, service):
        service.executor.get_commits_between_tags.return_value = CommandResult(
            returncode=0,
            stdout=(
                "abc\n"
                "feat: login\n"
                "Alice\n"
                "2026-06-27\n"
                "line1\n"
                "line2\n"
                "line3\n"
                "---END---"
            ),
        )

        result = service.get_commits_between_tags(
            "v1",
            "v2",
        )

        assert result[0]["body"] == "line1\nline2\nline3"
