# tests/core/git_ops/git/test_service_changelog.py

"""
Tests for GitService changelog helper methods.

Covers:
- has_changelog_changed()
"""

from unittest.mock import MagicMock

import pytest

from app.core.git_ops.git.result import CommandResult
from app.core.git_ops.git.service import GitService


@pytest.fixture
def service():
    """
    Create a GitService backed by mocked executor.
    """
    executor = MagicMock()
    config = MagicMock()

    return GitService(
        executor=executor,
        config=config,
    )


class TestHasChangelogChanged:
    """
    Tests GitService.has_changelog_changed().
    """

    def test_changed(self, service):
        """
        Returns True when CHANGELOG.md appears in diff.
        """
        service.executor.diff_name_only.return_value = CommandResult(
            returncode=0,
            stdout=(
                "README.md\n"
                "CHANGELOG.md\n"
                "app/main.py\n"
            ),
        )

        assert service.has_changelog_changed() is True

        service.executor.diff_name_only.assert_called_once_with()

    def test_not_changed(self, service):
        """
        Returns False when CHANGELOG.md is absent.
        """
        service.executor.diff_name_only.return_value = CommandResult(
            returncode=0,
            stdout=(
                "README.md\n"
                "app/main.py\n"
            ),
        )

        assert service.has_changelog_changed() is False

    def test_empty_diff(self, service):
        """
        Returns False when there are no modified files.
        """
        service.executor.diff_name_only.return_value = CommandResult(
            returncode=0,
            stdout="",
        )

        assert service.has_changelog_changed() is False
