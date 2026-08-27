# tests/core/git_ops/git/test_executor_commit.py

"""
Tests for app.core.git_ops.git.executor.

Part 4:
Commit / tag / push methods.
"""

from unittest.mock import MagicMock

import pytest

from app.core.git_ops.git.executor import GitCommandExecutor


@pytest.fixture
def executor():
    executor = GitCommandExecutor()
    executor._run = MagicMock(return_value="OK")
    return executor


class TestCommit:
    """
    Tests commit().
    """

    def test_commit_with_message(self, executor):
        result = executor.commit(message="feat: hello")

        executor._run.assert_called_once_with(
            [
                "commit",
                "-m",
                "feat: hello",
            ],
            check=True,
        )

        assert result == "OK"

    def test_commit_with_message_file(self, executor):
        result = executor.commit(message_file="commit.txt")

        executor._run.assert_called_once_with(
            [
                "commit",
                "-F",
                "commit.txt",
            ],
            check=True,
        )

        assert result == "OK"

    def test_commit_prefers_message_file(self, executor):
        executor.commit(
            message="ignored",
            message_file="commit.txt",
        )

        executor._run.assert_called_once_with(
            [
                "commit",
                "-F",
                "commit.txt",
            ],
            check=True,
        )

    def test_commit_requires_input(self, executor):
        with pytest.raises(
            ValueError,
            match="Either message or message_file must be provided",
        ):
            executor.commit()


class TestTag:
    """
    Tests tag().
    """

    def test_tag_default(self, executor):
        executor.tag(
            tag="v1.0.0",
            message="Release",
        )

        executor._run.assert_called_once_with(
            [
                "tag",
                "-a",
                "v1.0.0",
                "-m",
                "Release",
            ],
            check=True,
        )

    def test_tag_message_file(self, executor):
        executor.tag(
            tag="v1.0.0",
            message_file="tag.txt",
        )

        executor._run.assert_called_once_with(
            [
                "tag",
                "-a",
                "v1.0.0",
                "-F",
                "tag.txt",
            ],
            check=True,
        )

    def test_tag_prefers_message_file(self, executor):
        executor.tag(
            tag="v1.0.0",
            message="ignored",
            message_file="tag.txt",
        )

        executor._run.assert_called_once_with(
            [
                "tag",
                "-a",
                "v1.0.0",
                "-F",
                "tag.txt",
            ],
            check=True,
        )

    def test_tag_not_annotated(self, executor):
        executor.tag(
            tag="v1.0.0",
            annotated=False,
        )

        executor._run.assert_called_once_with(
            [
                "tag",
                "v1.0.0",
            ],
            check=True,
        )

    def test_tag_without_message(self, executor):
        executor.tag(
            tag="v1.0.0",
        )

        executor._run.assert_called_once_with(
            [
                "tag",
                "-a",
                "v1.0.0",
            ],
            check=True,
        )


class TestPush:
    """
    Tests push().
    """

    def test_push_default(self, executor):
        executor.push()

        executor._run.assert_called_once_with(
            [
                "push",
                "origin",
                "HEAD",
            ],
            check=True,
        )

    def test_push_custom(self, executor):
        executor.push(
            remote="backup",
            ref="develop",
        )

        executor._run.assert_called_once_with(
            [
                "push",
                "backup",
                "develop",
            ],
            check=True,
        )

    def test_push_set_upstream(self, executor):
        executor.push(
            remote="origin",
            ref="develop",
            set_upstream=True,
        )

        executor._run.assert_called_once_with(
            [
                "push",
                "--set-upstream",
                "origin",
                "develop",
            ],
            check=True,
        )

    def test_push_tag(self, executor):
        executor.push_tag(
            remote="origin",
            tag="v1.2.3",
        )

        executor._run.assert_called_once_with(
            [
                "push",
                "origin",
                "v1.2.3",
            ],
            check=True,
        )
