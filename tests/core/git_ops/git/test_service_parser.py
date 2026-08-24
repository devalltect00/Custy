# tests/core/git_ops/git/test_service_parser.py

"""
Tests for GitService commit message parser.

Covers:
- parse_commit()
"""

from unittest.mock import MagicMock

import pytest

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


class TestParseCommit:
    """
    Tests GitService.parse_commit().
    """

    def test_empty_message(self, service):
        """
        Empty commit message returns empty dictionary.
        """
        assert service.parse_commit("") == {}

    def test_whitespace_message(self, service):
        """
        Whitespace-only commit message returns empty dictionary.
        """
        assert service.parse_commit("   \n\n   ") == {}

    def test_merge_commit(self, service):
        """
        Merge commits should be skipped.
        """
        result = service.parse_commit(
            "Merge branch 'develop' into main"
        )

        assert result == {
            "type": "merge",
            "skip": True,
        }

    def test_conventional_commit(self, service):
        """
        Conventional commit without scope.
        """
        result = service.parse_commit(
            "feat: add login"
        )

        assert result["type"] == "feat"
        assert result["scope"] == "general"
        assert result["subject"] == "add login"
        assert result["body"] == ""
        assert result["raw_body_lines"] == []

    def test_conventional_commit_with_scope(self, service):
        """
        Conventional commit with scope.
        """
        result = service.parse_commit(
            "fix(auth): validate token"
        )

        assert result["type"] == "fix"
        assert result["scope"] == "auth"
        assert result["subject"] == "validate token"

    def test_non_conventional_commit(self, service):
        """
        Non-conventional commits fall back to 'other'.
        """
        result = service.parse_commit(
            "Updated README"
        )

        assert result["type"] == "other"
        assert result["scope"] == "general"
        assert result["subject"] == "Updated README"

    def test_body(self, service):
        """
        Body should be preserved.
        """
        msg = (
            "feat(api): add endpoint\n"
            "\n"
            "This adds a new endpoint.\n"
            "Supports pagination."
        )

        result = service.parse_commit(msg)

        assert result["type"] == "feat"
        assert result["scope"] == "api"
        assert result["subject"] == "add endpoint"

        assert result["body"] == (
            "This adds a new endpoint.\n"
            "Supports pagination."
        )

        assert result["raw_body_lines"] == [
            "",
            "This adds a new endpoint.",
            "Supports pagination.",
        ]

    def test_multiline_body(self, service):
        """
        Multiple body lines are preserved.
        """
        msg = (
            "docs: update docs\n"
            "line1\n"
            "line2\n"
            "line3"
        )

        result = service.parse_commit(msg)

        assert result["body"] == (
            "line1\n"
            "line2\n"
            "line3"
        )

        assert len(result["raw_body_lines"]) == 3
