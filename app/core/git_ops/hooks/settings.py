# app/core/git_ops/hooks/settings.py

"""Typed configuration for Git commit-hook execution.

Custy keeps native Git hook behavior as the normal path. The explicit
``pre_commit`` mode exists for projects that want Custy to invoke the
pre-commit framework directly, while ``auto`` can safely adapt a recognized
pre-commit wrapper that is incompatible with the current operating system.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from app.core.shared import ConfigurationError


class GitHookMode(StrEnum):
    """Supported Git hook execution policies."""

    AUTO = "auto"
    NATIVE = "native"
    PRE_COMMIT = "pre_commit"


@dataclass(frozen=True, slots=True)
class GitHookSettings:
    """Configure how commit hooks are executed.

    Args:
        mode: Hook policy selected by ``tool.custy.git.hooks.mode``.

    Notes:
        ``auto`` does not require or activate pre-commit for projects without
        an installed pre-commit-managed hook. Those projects continue through
        Git's normal native commit behavior.
    """

    mode: GitHookMode = GitHookMode.AUTO

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any] | None) -> GitHookSettings:
        """Create validated hook settings from a TOML mapping.

        Args:
            raw: Parsed ``tool.custy.git.hooks`` table, or ``None``.

        Returns:
            Validated immutable settings.

        Raises:
            ConfigurationError: If the table or mode value is invalid.
        """

        if raw is None or not raw:
            return cls()
        if not isinstance(raw, Mapping):
            raise ConfigurationError("tool.custy.git.hooks must be a TOML table.")

        mode_value = raw.get("mode", GitHookMode.AUTO.value)
        if not isinstance(mode_value, str):
            raise ConfigurationError("tool.custy.git.hooks.mode must be a string.")

        normalized = mode_value.strip().lower().replace("-", "_")
        try:
            mode = GitHookMode(normalized)
        except ValueError as error:
            supported = ", ".join(item.value for item in GitHookMode)
            raise ConfigurationError(
                f"Unsupported Git hook mode {mode_value!r}. "
                f"Supported values: {supported}."
            ) from error

        return cls(mode=mode)
