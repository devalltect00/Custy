# tests/core/git_ops/git/test_executor_log.py

"""
Tests for app.core.git_ops.git.executor.

Part 3:
Log / history helper methods.
"""

from unittest.mock import MagicMock

import pytest

from app.core.git_ops.git.executor import GitCommandExecutor


@pytest.fixture
def executor():
    executor = GitCommandExecutor()
    executor._run = MagicMock(return_value="OK")
    return executor


class TestLogCommands:
    """
    Tests log/history wrapper methods.
    """

    def test_log_between_default(self, executor):
        assert executor.log_between("v1.0.0..v1.1.0") == "OK"

        executor._run.assert_called_once_with(
            [
                "log",
                "v1.0.0..v1.1.0",
                "--pretty=format:%H",
            ],
            check=True,
            read_only=True,
        )

    def test_log_between_custom_format(self, executor):
        executor.log_between(
            "HEAD~5..HEAD",
            pretty_format="%B",
        )

        executor._run.assert_called_once_with(
            [
                "log",
                "HEAD~5..HEAD",
                "--pretty=format:%B",
            ],
            check=True,
            read_only=True,
        )

    def test_log_between_reverse(self, executor):
        executor.log_between(
            "v1..v2",
            reverse=True,
        )

        executor._run.assert_called_once_with(
            [
                "log",
                "--reverse",
                "v1..v2",
                "--pretty=format:%H",
            ],
            check=True,
            read_only=True,
        )

    def test_show_commit_default(self, executor):
        executor.show_commit("abc123")

        executor._run.assert_called_once_with(
            [
                "show",
                "-s",
                "--format=%B",
                "abc123",
            ],
            check=True,
            read_only=True,
        )

    def test_show_commit_custom_format(self, executor):
        executor.show_commit(
            "abc123",
            pretty_format="%H",
        )

        executor._run.assert_called_once_with(
            [
                "show",
                "-s",
                "--format=%H",
                "abc123",
            ],
            check=True,
            read_only=True,
        )

    def test_get_commit_count(self, executor):
        executor.get_commit_count()

        executor._run.assert_called_once_with(
            [
                "rev-list",
                "--count",
                "HEAD",
            ],
            check=True,
            read_only=True,
        )

    def test_get_commits_between_tags(self, executor):
        executor.log_between = MagicMock(return_value="OK")

        result = executor.get_commits_between_tags(
            "v1.0.0",
            "v1.1.0",
        )

        executor.log_between.assert_called_once_with(
            ref_range="v1.0.0..v1.1.0",
            pretty_format="%H%n%s%n%an%n%ad%n%B%n---END---",
            reverse=True,
        )

        assert result == "OK"

    def test_get_commits_between_tags_without_from_tag(self, executor):
        executor.log_between = MagicMock(return_value="OK")

        executor.get_commits_between_tags(
            "",
            "v2.0.0",
        )

        executor.log_between.assert_called_once_with(
            ref_range="v2.0.0",
            pretty_format="%H%n%s%n%an%n%ad%n%B%n---END---",
            reverse=True,
        )

    def test_get_tag_date(self, executor):
        executor.get_tag_date("v1.0.0")

        executor._run.assert_called_once_with(
            [
                "log",
                "-1",
                "--format=%ad",
                "--date=short",
                "v1.0.0",
            ],
            check=True,
            read_only=True,
        )

    def test_get_all_tags(self, executor):
        executor.get_all_tags()

        executor._run.assert_called_once_with(
            [
                "tag",
                "--sort=creatordate",
            ],
            check=True,
            read_only=True,
        )

    def test_get_tags(self, executor):
        executor.get_tags()

        executor._run.assert_called_once_with(
            [
                "tag",
            ],
            check=True,
            read_only=True,
        )

    def test_diff_name_only(self, executor):
        executor.diff_name_only()

        executor._run.assert_called_once_with(
            [
                "diff",
                "--name-only",
            ],
            check=False,
            read_only=True,
        )

    def test_describe_latest_tag(self, executor):
        executor.describe_latest_tag()

        executor._run.assert_called_once_with(
            [
                "describe",
                "--tags",
                "--abbrev=0",
            ],
            check=False,
            read_only=True,
        )
