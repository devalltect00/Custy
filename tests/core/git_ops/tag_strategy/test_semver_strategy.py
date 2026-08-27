# tests/core/git_ops/tag_strategy/test_semver_strategy.py

"""
tests/core/git_ops/tag_strategy/test_semver_strategy.py

Unit tests for the Semantic Version tag generation strategy.

These tests verify that SemverStrategy retrieves the latest Git tag,
delegates version calculation to SemverVersionHelper, and returns the
generated semantic version.
"""

from unittest.mock import MagicMock

import pytest

from app.core.git_ops.tag_strategy import semver_strategy
from app.core.git_ops.tag_strategy.semver_strategy import (
    SemverStrategy,
)


class TestSemverStrategy:
    """Tests for SemverStrategy."""

    # ==========================================================
    # Construction
    # ==========================================================

    def test_construct_with_default_values(
        self,
        monkeypatch,
    ):
        """Constructs the strategy using default configuration."""

        git = MagicMock()

        factory = MagicMock(
            return_value=git,
        )

        monkeypatch.setattr(
            semver_strategy,
            "create_git_service",
            factory,
        )

        strategy = SemverStrategy(
            bump="patch",
        )

        factory.assert_called_once_with(
            dry_run=False,
            no_debug=False,
        )

        assert strategy.bump == "patch"
        assert strategy.pre_release is None
        assert strategy.build_meta is None
        assert strategy.dev is False
        assert strategy.post is False
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
            semver_strategy,
            "create_git_service",
            factory,
        )

        strategy = SemverStrategy(
            bump="minor",
            pre_release="beta",
            build_meta="build42",
            dev=True,
            post=True,
            dry_run=True,
            no_debug=True,
        )

        factory.assert_called_once_with(
            dry_run=True,
            no_debug=True,
        )

        assert strategy.bump == "minor"
        assert strategy.pre_release == "beta"
        assert strategy.build_meta == "build42"
        assert strategy.dev is True
        assert strategy.post is True
        assert strategy.git is git

    # ==========================================================
    # get_next_tag()
    # ==========================================================

    @pytest.mark.parametrize(
        (
            "bump",
            "pre_release",
            "build_meta",
            "dev",
            "post",
        ),
        [
            (
                "patch",
                None,
                None,
                False,
                False,
            ),
            (
                "minor",
                "alpha",
                "build1",
                True,
                False,
            ),
            (
                "major",
                "rc",
                "ci001",
                False,
                True,
            ),
        ],
    )
    def test_get_next_tag_uses_semver_helper(
        self,
        monkeypatch,
        bump,
        pre_release,
        build_meta,
        dev,
        post,
    ):
        """Delegates version calculation to SemverVersionHelper."""

        git = MagicMock()
        git.get_latest_tag.return_value = "v1.2.3"

        helper_instance = MagicMock()
        helper_instance.get_bump_version.return_value = "v2.0.0"

        helper = MagicMock(
            return_value=helper_instance,
        )

        monkeypatch.setattr(
            semver_strategy,
            "create_git_service",
            lambda **_: git,
        )

        monkeypatch.setattr(
            semver_strategy,
            "SemverVersionHelper",
            helper,
        )

        strategy = SemverStrategy(
            bump=bump,
            pre_release=pre_release,
            build_meta=build_meta,
            dev=dev,
            post=post,
        )

        result = strategy.get_next_tag()

        git.get_latest_tag.assert_called_once_with()

        helper.assert_called_once_with(
            "v1.2.3",
        )

        helper_instance.get_bump_version.assert_called_once_with(
            level=bump,
            target_pre=pre_release,
            build=build_meta,
            prefix_v=True,
            dev=dev,
            post=post,
        )

        assert result == "v2.0.0"

    def test_get_next_tag_propagates_helper_errors(
        self,
        monkeypatch,
    ):
        """Propagates helper exceptions."""

        git = MagicMock()
        git.get_latest_tag.return_value = "v1.2.3"

        helper_instance = MagicMock()

        helper_instance.get_bump_version.side_effect = RuntimeError(
            "Invalid version",
        )

        monkeypatch.setattr(
            semver_strategy,
            "create_git_service",
            lambda **_: git,
        )

        monkeypatch.setattr(
            semver_strategy,
            "SemverVersionHelper",
            lambda *_: helper_instance,
        )

        strategy = SemverStrategy(
            bump="patch",
        )

        with pytest.raises(
            RuntimeError,
            match="Invalid version",
        ):
            strategy.get_next_tag()

        git.get_latest_tag.assert_called_once_with()

        helper_instance.get_bump_version.assert_called_once_with(
            level="patch",
            target_pre=None,
            build=None,
            prefix_v=True,
            dev=False,
            post=False,
        )
