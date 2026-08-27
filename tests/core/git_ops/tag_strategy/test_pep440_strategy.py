# tests/core/git_ops/tag_strategy/test_pep440_strategy.py

"""
tests/core/git_ops/tag_strategy/test_pep440_strategy.py

Unit tests for the PEP 440 tag generation strategy.

These tests verify that PEP440Strategy retrieves the latest Git tag,
delegates version calculation to PEP440VersionHelper, correctly handles
automatic bump detection, and returns the generated version.
"""

from unittest.mock import MagicMock

import pytest

from app.core.git_ops.tag_strategy import pep440_strategy
from app.core.git_ops.tag_strategy.pep440_strategy import (
    PEP440Strategy,
)


class TestPEP440Strategy:
    """Tests for PEP440Strategy."""

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
            pep440_strategy,
            "create_git_service",
            factory,
        )

        strategy = PEP440Strategy(
            bump="patch",
            epoch=None,
        )

        factory.assert_called_once_with(
            dry_run=False,
            no_debug=False,
        )

        assert strategy.bump == "patch"
        assert strategy.epoch is None
        assert strategy.pre_release is None
        assert strategy.post_release is None
        assert strategy.dev_release is None
        assert strategy.local is None
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
            pep440_strategy,
            "create_git_service",
            factory,
        )

        strategy = PEP440Strategy(
            bump="minor",
            epoch=2,
            pre_release="rc",
            post_release=True,
            dev_release=True,
            local="linux",
            dry_run=True,
            no_debug=True,
        )

        factory.assert_called_once_with(
            dry_run=True,
            no_debug=True,
        )

        assert strategy.bump == "minor"
        assert strategy.epoch == 2
        assert strategy.pre_release == "rc"
        assert strategy.post_release is True
        assert strategy.dev_release is True
        assert strategy.local == "linux"
        assert strategy.git is git

    # ==========================================================
    # get_next_tag()
    # ==========================================================

    @pytest.mark.parametrize(
        (
            "bump",
            "expected_level",
        ),
        [
            ("patch", "patch"),
            ("minor", "minor"),
            ("major", "major"),
            ("auto", None),
        ],
    )
    def test_get_next_tag_uses_pep440_helper(
        self,
        monkeypatch,
        bump,
        expected_level,
    ):
        """Delegates version calculation to PEP440VersionHelper."""

        git = MagicMock()

        git.get_latest_tag.return_value = "1.2.3"

        helper_instance = MagicMock()

        helper_instance.get_bump_version.return_value = "1.2.4"

        helper = MagicMock(
            return_value=helper_instance,
        )

        monkeypatch.setattr(
            pep440_strategy,
            "create_git_service",
            lambda **_: git,
        )

        monkeypatch.setattr(
            pep440_strategy,
            "PEP440VersionHelper",
            helper,
        )

        strategy = PEP440Strategy(
            bump=bump,
            epoch=1,
            pre_release="beta",
            post_release=True,
            dev_release=True,
            local="abc",
        )

        result = strategy.get_next_tag()

        git.get_latest_tag.assert_called_once_with()

        helper.assert_called_once_with(
            "1.2.3",
        )

        helper_instance.get_bump_version.assert_called_once_with(
            level=expected_level,
            target_pre="beta",
            post=True,
            dev=True,
            local="abc",
            epoch=1,
        )

        assert result == "1.2.4"

    def test_get_next_tag_propagates_helper_errors(
        self,
        monkeypatch,
    ):
        """Propagates helper exceptions."""

        git = MagicMock()

        git.get_latest_tag.return_value = "1.2.3"

        helper_instance = MagicMock()

        helper_instance.get_bump_version.side_effect = RuntimeError(
            "Invalid version",
        )

        monkeypatch.setattr(
            pep440_strategy,
            "create_git_service",
            lambda **_: git,
        )

        monkeypatch.setattr(
            pep440_strategy,
            "PEP440VersionHelper",
            lambda *_: helper_instance,
        )

        strategy = PEP440Strategy(
            bump="patch",
            epoch=None,
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
            post=None,
            dev=None,
            local=None,
            epoch=None,
        )
