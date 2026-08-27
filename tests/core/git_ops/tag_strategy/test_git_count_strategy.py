# tests/core/git_ops/tag_strategy/test_git_count_strategy.py

"""
tests/core/git_ops/tag_strategy/test_git_count_strategy.py

Unit tests for the Git commit count tag generation strategy.

These tests verify that GitCountStrategy generates version tags based on
the total number of commits in the current repository and properly
propagates failures from the underlying Git service.
"""

from unittest.mock import MagicMock

import pytest

from app.core.git_ops.tag_strategy import git_count_strategy
from app.core.git_ops.tag_strategy.git_count_strategy import (
    GitCountStrategy,
)


class TestGitCountStrategy:
    """Tests for GitCountStrategy."""

    # ==========================================================
    # Construction
    # ==========================================================

    def test_construct_with_default_values(
        self,
        monkeypatch,
    ):
        """Constructs the strategy using the default configuration."""

        git = MagicMock()

        factory = MagicMock(
            return_value=git,
        )

        monkeypatch.setattr(
            git_count_strategy,
            "create_git_service",
            factory,
        )

        strategy = GitCountStrategy()

        factory.assert_called_once_with(
            dry_run=False,
            no_debug=False,
        )

        assert strategy.git is git

    def test_construct_with_explicit_values(
        self,
        monkeypatch,
    ):
        """Constructs the strategy using explicit configuration."""

        git = MagicMock()

        factory = MagicMock(
            return_value=git,
        )

        monkeypatch.setattr(
            git_count_strategy,
            "create_git_service",
            factory,
        )

        strategy = GitCountStrategy(
            dry_run=True,
            no_debug=True,
        )

        factory.assert_called_once_with(
            dry_run=True,
            no_debug=True,
        )

        assert strategy.git is git

    # ==========================================================
    # get_next_tag()
    # ==========================================================

    @pytest.mark.parametrize(
        "commit_count",
        [
            1,
            15,
            999,
        ],
    )
    def test_get_next_tag_returns_git_commit_count(
        self,
        monkeypatch,
        commit_count,
    ):
        """Generates a version tag using the Git commit count."""

        git = MagicMock()

        git.get_commit_count.return_value = commit_count

        monkeypatch.setattr(
            git_count_strategy,
            "create_git_service",
            lambda **_: git,
        )

        strategy = GitCountStrategy()

        result = strategy.get_next_tag()

        git.get_commit_count.assert_called_once_with()

        assert result == f"v{commit_count}"

    def test_get_next_tag_reraises_git_errors(
        self,
        monkeypatch,
    ):
        """Re-raises exceptions produced by the Git service."""

        git = MagicMock()

        git.get_commit_count.side_effect = RuntimeError(
            "Git failure",
        )

        monkeypatch.setattr(
            git_count_strategy,
            "create_git_service",
            lambda **_: git,
        )

        strategy = GitCountStrategy()

        with pytest.raises(
            RuntimeError,
            match="Git failure",
        ):
            strategy.get_next_tag()

        git.get_commit_count.assert_called_once_with()
