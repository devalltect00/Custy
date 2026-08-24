# tests/core/git_ops/git/test_service_commit.py

"""
Tests for commit-related GitService methods.
"""

from pathlib import Path
from unittest.mock import MagicMock

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


class TestCommit:
    """
    Tests commit().
    """

    def test_inline_message(self, service):
        result = MagicMock()
        result.success = True

        service.executor.commit.return_value = result

        service.commit(
            message="feat: add feature",
        )

        # service.executor.commit.assert_called_once_with(
        #     message="feat: add feature",
        #     message_file=None,
        # )

        service.executor.commit.assert_called_once_with(
            "feat: add feature",
            None,
        )

    def test_message_file(self, service, tmp_path):
        result = MagicMock()
        result.success = True

        service.executor.commit.return_value = result

        message_file = tmp_path / "commit.txt"
        message_file.write_text("feat: test")

        service.commit(
            message_file=str(message_file),
        )

        # service.executor.commit.assert_called_once_with(
        #     message=None,
        #     message_file=str(message_file),
        # )

        service.executor.commit.assert_called_once_with(
            None,
            str(message_file),
        )

    def test_both_message_and_file(self, service, tmp_path):
        result = MagicMock()
        result.success = True

        service.executor.commit.return_value = result

        message_file = tmp_path / "commit.txt"
        message_file.write_text("ignored")

        service.commit(
            message="feat: priority",
            message_file=str(message_file),
        )

        # service.executor.commit.assert_called_once_with(
        #     message="feat: priority",
        #     message_file=str(message_file),
        # )

        service.executor.commit.assert_called_once_with(
            "feat: priority",
            str(message_file),
        )

    def test_failure(self, service):
        result = MagicMock()
        result.success = False

        service.executor.commit.return_value = result

        with pytest.raises(RuntimeError):
            service.commit(
                message="feat: fail",
            )


# class TestCommitAmend:
#     """
#     Tests commit_amend().
#     """

#     def test_success(self, service):
#         result = MagicMock()
#         result.success = True

#         service.executor.commit_amend.return_value = result

#         service.commit_amend()

#         service.executor.commit_amend.assert_called_once_with()

#     def test_failure(self, service):
#         result = MagicMock()
#         result.success = False

#         service.executor.commit_amend.return_value = result

#         with pytest.raises(RuntimeError):
#             service.commit_amend()


# class TestCommitExists:
#     """
#     Tests commit_exists().
#     """

#     def test_exists(self, service):
#         result = MagicMock()
#         result.success = True

#         service.executor.commit_exists.return_value = result

#         assert service.commit_exists("abc123") is True

#         service.executor.commit_exists.assert_called_once_with(
#             "abc123",
#         )

#     def test_missing(self, service):
#         result = MagicMock()
#         result.success = False

#         service.executor.commit_exists.return_value = result

#         assert service.commit_exists("abc123") is False
