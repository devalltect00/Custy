# tests/core/git_ops/tag_strategy/test_commitizen_strategy.py

"""
tests/core/git_ops/tag_strategy/test_commitizen_strategy.py

Unit tests for the Commitizen-based tag generation strategy.

These tests verify that CommitizenStrategy detects version bumps using
Commitizen, determines the correct semantic version increment, delegates
tag generation to SemverStrategy, and properly reports execution
failures.
"""

import subprocess
from unittest.mock import MagicMock

import pytest

from app.core.git_ops.tag_strategy import commitizen_strategy
from app.core.git_ops.tag_strategy.commitizen_strategy import (
    CommitizenStrategy,
)


class TestCommitizenStrategy:
    """Tests for CommitizenStrategy."""

    # ==========================================================
    # Construction
    # ==========================================================

    def test_construct_with_default_values(self):
        """Constructs the strategy using default configuration."""

        strategy = CommitizenStrategy()

        assert strategy.pre is None
        assert strategy.dry_run is False
        assert strategy.no_debug is False

    def test_construct_with_explicit_values(self):
        """Constructs the strategy using explicit configuration."""

        strategy = CommitizenStrategy(
            pre="beta",
            dry_run=True,
            no_debug=True,
        )

        assert strategy.pre == "beta"
        assert strategy.dry_run is True
        assert strategy.no_debug is True

    # ==========================================================
    # _get_bump_type()
    # ==========================================================

    @pytest.mark.parametrize(
        ("current", "next_version", "expected"),
        [
            ("1.0.0", "2.0.0", "major"),
            ("1.0.0", "1.1.0", "minor"),
            ("1.0.0", "1.0.1", "patch"),
            ("5.9.9", "6.0.0", "major"),
            ("5.9.9", "5.10.0", "minor"),
            ("5.9.9", "5.9.10", "patch"),
        ],
    )
    def test_detects_correct_bump_type(
        self,
        current,
        next_version,
        expected,
    ):
        """Infers the correct semantic version bump."""

        strategy = CommitizenStrategy()

        assert (
            strategy._get_bump_type(
                current,
                next_version,
            )
            == expected
        )

    # ==========================================================
    # get_next_tag()
    # ==========================================================

    @pytest.mark.parametrize(
        ("current", "next_version", "expected_bump"),
        [
            ("1.0.0", "1.0.1", "patch"),
            ("1.0.0", "1.1.0", "minor"),
            ("1.0.0", "2.0.0", "major"),
        ],
    )
    def test_get_next_tag_delegates_to_semver_strategy(
        self,
        monkeypatch,
        current,
        next_version,
        expected_bump,
    ):
        """Delegates tag generation to SemverStrategy."""

        output = f"bump: version {current} → {next_version}\n"

        monkeypatch.setattr(
            commitizen_strategy.subprocess,
            "check_output",
            lambda *_, **__: output,
        )

        semver = MagicMock()

        semver.return_value.get_next_tag.return_value = "v9.9.9"

        monkeypatch.setattr(
            commitizen_strategy,
            "SemverStrategy",
            semver,
        )

        strategy = CommitizenStrategy(
            pre="rc",
            dry_run=True,
            no_debug=True,
        )

        result = strategy.get_next_tag()

        semver.assert_called_once_with(
            bump=expected_bump,
            pre="rc",
            dry_run=True,
            no_debug=True,
        )

        semver.return_value.get_next_tag.assert_called_once_with()

        assert result == "v9.9.9"

    def test_get_next_tag_raises_runtime_error_when_commitizen_fails(
        self,
        monkeypatch,
    ):
        """Raises RuntimeError when Commitizen execution fails."""

        error = subprocess.CalledProcessError(
            returncode=1,
            cmd=["cz"],
            output="failure",
        )

        def raise_error(*_, **__):
            raise error

        monkeypatch.setattr(
            commitizen_strategy.subprocess,
            "check_output",
            raise_error,
        )

        strategy = CommitizenStrategy()

        with pytest.raises(
            RuntimeError,
            match="Failed to run commitizen",
        ):
            strategy.get_next_tag()

    def test_get_next_tag_raises_runtime_error_when_output_cannot_be_parsed(
        self,
        monkeypatch,
    ):
        """Raises RuntimeError when no bump information is found."""

        monkeypatch.setattr(
            commitizen_strategy.subprocess,
            "check_output",
            lambda *_, **__: "nothing useful",
        )

        strategy = CommitizenStrategy()

        with pytest.raises(
            RuntimeError,
            match="No eligible commits found to bump",
        ):
            strategy.get_next_tag()

    def test_invokes_commitizen_with_expected_command(
        self,
        monkeypatch,
    ):
        """Invokes Commitizen using the expected command line."""

        captured = {}

        def fake_check_output(
            command,
            **kwargs,
        ):
            captured["command"] = command
            captured["kwargs"] = kwargs

            return "bump: version 1.0.0 → 1.0.1"

        monkeypatch.setattr(
            commitizen_strategy.subprocess,
            "check_output",
            fake_check_output,
        )

        semver = MagicMock()

        semver.return_value.get_next_tag.return_value = "v1.0.1"

        monkeypatch.setattr(
            commitizen_strategy,
            "SemverStrategy",
            semver,
        )

        CommitizenStrategy().get_next_tag()

        assert captured["command"] == [
            "cz",
            "bump",
            "--dry-run",
            "--changelog",
        ]

        assert captured["kwargs"]["text"] is True

        assert captured["kwargs"]["stderr"] == subprocess.STDOUT
