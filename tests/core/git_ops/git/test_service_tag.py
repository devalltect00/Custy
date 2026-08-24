# tests/core/git_ops/git/test_service_tag.py

"""
Tests for tag-related GitService methods.
"""

from unittest.mock import MagicMock

import pytest

from app.core.git_ops.git.service import GitService
from app.core.git_ops.git.result import CommandResult

@pytest.fixture
def service():
    executor = MagicMock()
    config = MagicMock()

    return GitService(
        executor=executor,
        config=config,
    )


class TestTag:
    """
    Tests tag().
    """

    def test_inline_message(self, service):
        result = MagicMock()
        result.success = True

        service.executor.tag.return_value = result

        service.tag(
            tag="v1.2.3",
            message="Release v1.2.3",
        )

        service.executor.tag.assert_called_once_with(
            "v1.2.3",
            "Release v1.2.3",
            None,
        )

    def test_message_file(self, service, tmp_path):
        result = MagicMock()
        result.success = True

        service.executor.tag.return_value = result

        msg = tmp_path / "tag.txt"
        msg.write_text("release")

        service.tag(
            tag="v1.2.3",
            message_file=str(msg),
        )

        service.executor.tag.assert_called_once_with(
            "v1.2.3",
            None,
            str(msg),
        )

    def test_message_and_file(self, service, tmp_path):
        result = MagicMock()
        result.success = True

        service.executor.tag.return_value = result

        msg = tmp_path / "tag.txt"
        msg.write_text("release")

        service.tag(
            tag="v1.2.3",
            message="Release",
            message_file=str(msg),
        )

        service.executor.tag.assert_called_once_with(
            "v1.2.3",
            "Release",
            str(msg),
        )

    def test_failure(self, service):
        result = MagicMock()
        result.success = False

        service.executor.tag.return_value = result

        with pytest.raises(RuntimeError):
            service.tag(
                tag="v1.2.3",
                message="Release",
            )


class TestGetLatestTag:
    """
    Tests get_latest_tag().
    """

    def test_latest_tag(self, service):
        result = MagicMock()
        result.stdout = "v2.0.0\n"

        service.executor.describe_latest_tag.return_value = result

        assert service.get_latest_tag() == "v2.0.0"

    def test_no_tag(self, service):
        result = MagicMock()
        result.stdout = ""

        service.executor.describe_latest_tag.return_value = result

        assert service.get_latest_tag() == "v0.0.0"


# ============================================================
# Additional tag retrieval tests
# ============================================================


class TestGetTags:
    """
    Tests GitService.get_tags().
    """

    def test_returns_sorted_tags(self, service):
        service.executor.get_tags.return_value = CommandResult(
            returncode=0,
            stdout="v1.0.0\nv2.0.0\nv1.5.0\n",
        )

        assert service.get_tags() == [
            "v2.0.0",
            "v1.5.0",
            "v1.0.0",
        ]

        service.executor.get_tags.assert_called_once_with()

    def test_empty(self, service):
        service.executor.get_tags.return_value = CommandResult(
            returncode=0,
            stdout="",
        )

        assert service.get_tags() == []


class TestGetAllTags:
    """
    Tests GitService.get_all_tags().
    """

    def test_returns_tags(self, service):
        service.executor.get_all_tags.return_value = CommandResult(
            returncode=0,
            stdout="v0.9.0\nv1.0.0\nv2.0.0\n",
        )

        assert service.get_all_tags() == [
            "v0.9.0",
            "v1.0.0",
            "v2.0.0",
        ]

        service.executor.get_all_tags.assert_called_once_with()

    def test_empty(self, service):
        service.executor.get_all_tags.return_value = CommandResult(
            returncode=0,
            stdout="",
        )

        assert service.get_all_tags() == []


class TestGetTagDate:
    """
    Tests GitService.get_tag_date().
    """

    def test_success(self, service):
        service.executor.get_tag_date.return_value = CommandResult(
            returncode=0,
            stdout="2026-06-27\n",
        )

        assert service.get_tag_date("v1.2.3") == "2026-06-27"

        service.executor.get_tag_date.assert_called_once_with(
            "v1.2.3",
        )

    def test_unknown_when_empty(self, service):
        service.executor.get_tag_date.return_value = CommandResult(
            returncode=0,
            stdout="",
        )

        assert service.get_tag_date("v1.2.3") == "unknown"
