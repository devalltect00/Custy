# tests/core/git_ops/commit/test_settings.py

"""Tests for typed commit-validation configuration."""

import pytest

from app.core.git_ops.commit.settings import (
    CommitValidationProvider,
    CommitValidationSettings,
)
from app.core.shared import ConfigurationError


class TestCommitValidationSettings:
    """Validate defaults, normalization, and rejected configuration."""

    def test_defaults_are_safe_and_optional(self) -> None:
        """Default configuration uses non-strict automatic discovery."""

        settings = CommitValidationSettings.from_mapping(None)

        assert settings.provider == CommitValidationProvider.AUTO
        assert settings.require_tool is False

    def test_normalizes_provider(self) -> None:
        """Provider names are case-insensitive and whitespace tolerant."""

        settings = CommitValidationSettings.from_mapping(
            {"provider": " Commitizen ", "require_tool": True}
        )

        assert settings.provider == CommitValidationProvider.COMMITIZEN
        assert settings.require_tool is True

    @pytest.mark.parametrize("provider", ["auto", "custy", "commitizen", "git"])
    def test_accepts_every_documented_provider(self, provider: str) -> None:
        """Every provider shown in the configuration matrix is supported."""

        assert (
            CommitValidationSettings.from_mapping({"provider": provider}).provider.value
            == provider
        )

    def test_rejects_unknown_provider(self) -> None:
        """Unsupported providers fail with the supported values listed."""

        with pytest.raises(ConfigurationError, match="Supported values"):
            CommitValidationSettings.from_mapping({"provider": "custom"})

    def test_rejects_non_boolean_strictness(self) -> None:
        """TOML strings cannot silently replace strict booleans."""

        with pytest.raises(ConfigurationError, match="must be a boolean"):
            CommitValidationSettings.from_mapping({"require_tool": "true"})
