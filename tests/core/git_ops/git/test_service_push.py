# tests/core/git_ops/git/test_service_push.py

"""
Tests for push-related GitService methods.
"""

from unittest.mock import MagicMock

import pytest

from app.core.git_ops.git.result import CommandResult
from app.core.git_ops.git.service import GitService
from app.core.shared import GitOperationError


@pytest.fixture
def service():
    executor = MagicMock()
    config = MagicMock()

    return GitService(
        executor=executor,
        config=config,
    )


class TestPush:
    """
    Tests push().
    """

    def test_push_head(self, service):
        result = MagicMock()
        result.success = True

        service.executor.push.return_value = result

        service.push(
            remote="origin",
            ref="HEAD",
        )

        # service.executor.push.assert_called_once_with(
        #     "origin",
        #     "HEAD",
        # )

        service.executor.push.assert_called_once_with(
            remote="origin",
            ref="HEAD",
        )

    def test_push_branch(self, service):
        result = MagicMock()
        result.success = True

        service.executor.push.return_value = result

        service.push(
            remote="backup",
            ref="develop",
        )

        # service.executor.push.assert_called_once_with(
        #     "backup",
        #     "develop",
        # )

        service.executor.push.assert_called_once_with(
            remote="backup",
            ref="develop",
        )

    def test_push_failure(self, service):
        service.executor.push.return_value = CommandResult(
            returncode=128,
            stderr="fatal: Authentication failed for origin",
        )

        with pytest.raises(GitOperationError) as exc_info:
            service.push(
                remote="origin",
                ref="HEAD",
            )

        assert exc_info.value.operation == "push"
        assert exc_info.value.returncode == 128
        assert exc_info.value.detail == "fatal: Authentication failed for origin"


class TestPushTag:
    """
    Tests push_tag().
    """

    def test_success(self, service):
        result = MagicMock()
        result.success = True

        service.executor.push_tag.return_value = result

        service.push_tag(
            remote="origin",
            tag="v1.2.3",
        )

        service.executor.push_tag.assert_called_once_with(
            "origin",
            "v1.2.3",
        )

    def test_failure(self, service):
        service.executor.push_tag.return_value = CommandResult(
            returncode=1,
            stderr="remote rejected the tag",
        )

        with pytest.raises(GitOperationError) as exc_info:
            service.push_tag(
                remote="origin",
                tag="v1.2.3",
            )

        assert exc_info.value.operation == "push-tag"
        assert exc_info.value.returncode == 1
        assert exc_info.value.detail == "remote rejected the tag"


# class TestPushAllTags:
#     """
#     Tests push_all_tags().
#     """

#     def test_success(self, service):
#         result = MagicMock()
#         result.success = True

#         service.executor.push_all_tags.return_value = result

#         service.push_all_tags(
#             remote="origin",
#         )

#         service.executor.push_all_tags.assert_called_once_with(
#             "origin",
#         )

#     def test_failure(self, service):
#         result = MagicMock()
#         result.success = False

#         service.executor.push_all_tags.return_value = result

#         with pytest.raises(RuntimeError):
#             service.push_all_tags(
#                 remote="origin",
#             )
