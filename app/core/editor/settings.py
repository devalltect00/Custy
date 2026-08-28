# app/core/editor/settings.py

"""Typed configuration for Custy's interactive editor selection.

The settings model accepts only known editor identifiers from project
configuration. Environment variables remain available for advanced custom
commands, while TOML configuration stays predictable and safe to validate.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from app.core.shared import ConfigurationError


class EditorIdentifier(StrEnum):
    """Stable editor names accepted by ``tool.custy.editor.candidates``."""

    VSCODE = "vscode"
    NOTEPAD = "notepad"
    MICRO = "micro"
    NANO = "nano"
    VIM = "vim"
    VI = "vi"
    NEOVIM = "neovim"


_EDITOR_ALIASES: dict[str, EditorIdentifier] = {
    "code": EditorIdentifier.VSCODE,
    "nvim": EditorIdentifier.NEOVIM,
}


@dataclass(frozen=True, slots=True)
class EditorSettings:
    """Control editor precedence for local and container workflows.

    Args:
        prefer_environment: Whether ``VISUAL`` and ``EDITOR`` precede
            configured editor identifiers.
        allow_fallback: Whether built-in platform candidates are appended after
            configured candidates.
        windows: Preferred editor identifiers on Windows.
        linux: Preferred editor identifiers on Linux outside containers.
        macos: Preferred editor identifiers on macOS.
        container: Preferred terminal editors inside a container.
    """

    prefer_environment: bool = True
    allow_fallback: bool = True
    windows: tuple[EditorIdentifier, ...] = (
        EditorIdentifier.VSCODE,
        EditorIdentifier.NOTEPAD,
    )
    linux: tuple[EditorIdentifier, ...] = (
        EditorIdentifier.MICRO,
        EditorIdentifier.NANO,
        EditorIdentifier.VIM,
        EditorIdentifier.VI,
    )
    macos: tuple[EditorIdentifier, ...] = (
        EditorIdentifier.VSCODE,
        EditorIdentifier.MICRO,
        EditorIdentifier.NANO,
        EditorIdentifier.VIM,
        EditorIdentifier.VI,
    )
    container: tuple[EditorIdentifier, ...] = (
        EditorIdentifier.MICRO,
        EditorIdentifier.NANO,
        EditorIdentifier.VIM,
        EditorIdentifier.VI,
    )

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any] | None) -> EditorSettings:
        """Create validated settings from ``tool.custy.editor``.

        Args:
            raw: Parsed editor configuration, or ``None`` for defaults.

        Returns:
            Validated editor settings with immutable candidate sequences.

        Raises:
            ConfigurationError: If booleans, candidate tables, or editor names
                use unsupported shapes or values.
        """

        if raw is None or not raw:
            return cls()
        if not isinstance(raw, Mapping):
            raise ConfigurationError("tool.custy.editor must be a TOML table.")

        defaults = cls()
        candidates = raw.get("candidates", {})
        if not isinstance(candidates, Mapping):
            raise ConfigurationError(
                "tool.custy.editor.candidates must be a TOML table."
            )

        return cls(
            prefer_environment=cls._read_bool(
                raw,
                "prefer_environment",
                defaults.prefer_environment,
            ),
            allow_fallback=cls._read_bool(
                raw,
                "allow_fallback",
                defaults.allow_fallback,
            ),
            windows=cls._read_candidates(candidates, "windows", defaults.windows),
            linux=cls._read_candidates(candidates, "linux", defaults.linux),
            macos=cls._read_candidates(candidates, "macos", defaults.macos),
            container=cls._read_candidates(
                candidates,
                "container",
                defaults.container,
            ),
        )

    @staticmethod
    def _read_bool(
        raw: Mapping[str, Any],
        key: str,
        default: bool,
    ) -> bool:
        """Read a strict boolean editor setting."""

        value = raw.get(key, default)
        if not isinstance(value, bool):
            raise ConfigurationError(f"tool.custy.editor.{key} must be a boolean.")
        return value

    @classmethod
    def _read_candidates(
        cls,
        raw: Mapping[str, Any],
        key: str,
        default: tuple[EditorIdentifier, ...],
    ) -> tuple[EditorIdentifier, ...]:
        """Read and normalize one platform candidate list."""

        value = raw.get(key, default)
        if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
            raise ConfigurationError(
                f"tool.custy.editor.candidates.{key} must be an array of editor names."
            )

        resolved: list[EditorIdentifier] = []
        for item in value:
            if not isinstance(item, str):
                raise ConfigurationError(
                    f"tool.custy.editor.candidates.{key} must contain only strings."
                )
            resolved.append(cls._resolve_identifier(item, key))

        return tuple(dict.fromkeys(resolved))

    @staticmethod
    def _resolve_identifier(value: str, platform_key: str) -> EditorIdentifier:
        """Normalize one supported editor identifier or alias."""

        normalized = value.strip().lower()
        normalized_identifier = _EDITOR_ALIASES.get(normalized, normalized)

        try:
            return EditorIdentifier(normalized_identifier)
        except ValueError as error:
            supported = ", ".join(editor.value for editor in EditorIdentifier)
            raise ConfigurationError(
                "Unsupported editor "
                f"{value!r} in tool.custy.editor.candidates.{platform_key}. "
                f"Supported values: {supported}."
            ) from error
