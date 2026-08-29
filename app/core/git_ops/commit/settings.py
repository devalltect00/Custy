# app/core/git_ops/commit/settings.py

"""Typed settings for commit-message validation providers.

Custy's built-in validation is always available. External Commitizen
validation is resolved separately so projects that do not use Commitizen do
not need to install or configure it.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from app.core.shared import ConfigurationError


class CommitValidationProvider(StrEnum):
    """Commit-message validation providers accepted by project configuration."""

    AUTO = "auto"
    CUSTY = "custy"
    COMMITIZEN = "commitizen"
    GIT = "git"


@dataclass(frozen=True, slots=True)
class CommitValidationSettings:
    """Configure commit-message validation provider selection.

    Args:
        provider: Provider requested by ``tool.custy.commit.validation``.
        require_tool: Whether an unavailable or invalid optional external
            provider must stop the workflow instead of falling back to Custy.
    """

    provider: CommitValidationProvider = CommitValidationProvider.AUTO
    require_tool: bool = False

    @classmethod
    def from_mapping(
        cls,
        raw: Mapping[str, Any] | None,
    ) -> CommitValidationSettings:
        """Create validated settings from project configuration.

        Args:
            raw: Parsed ``tool.custy.commit.validation`` table, or ``None``.

        Returns:
            Validated immutable settings.

        Raises:
            ConfigurationError: If a provider or strictness value is invalid.
        """

        if raw is None or not raw:
            return cls()
        if not isinstance(raw, Mapping):
            raise ConfigurationError(
                "tool.custy.commit.validation must be a TOML table."
            )

        provider_value = raw.get("provider", CommitValidationProvider.AUTO.value)
        if not isinstance(provider_value, str):
            raise ConfigurationError(
                "tool.custy.commit.validation.provider must be a string."
            )

        try:
            provider = CommitValidationProvider(provider_value.strip().lower())
        except ValueError as error:
            supported = ", ".join(item.value for item in CommitValidationProvider)
            raise ConfigurationError(
                "Unsupported commit validation provider "
                f"{provider_value!r}. Supported values: {supported}."
            ) from error

        require_tool = raw.get("require_tool", False)
        if not isinstance(require_tool, bool):
            raise ConfigurationError(
                "tool.custy.commit.validation.require_tool must be a boolean."
            )

        return cls(provider=provider, require_tool=require_tool)
