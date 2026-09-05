# tests/core/editor/test_settings.py

"""Unit tests for validated editor configuration."""

from __future__ import annotations

import pytest

from app.core.editor import EditorIdentifier, EditorSettings
from app.core.shared import ConfigurationError


class TestEditorSettings:
    """Tests for defaults, aliases, and invalid configuration."""

    def test_defaults_cover_local_and_container_platforms(self) -> None:
        """Default settings provide deterministic candidates everywhere."""

        settings = EditorSettings()

        assert settings.windows == (
            EditorIdentifier.VSCODE,
            EditorIdentifier.NOTEPAD,
        )
        assert settings.container[0] is EditorIdentifier.MICRO
        assert settings.prefer_environment is True
        assert settings.allow_fallback is True

    def test_mapping_normalizes_aliases_and_duplicates(self) -> None:
        """Friendly aliases normalize to stable identifiers and deduplicate."""

        settings = EditorSettings.from_mapping(
            {
                "prefer_environment": False,
                "allow_fallback": False,
                "candidates": {
                    "windows": ["code", "vscode", "notepad"],
                    "container": ["micro", "nvim"],
                },
            }
        )

        assert settings.windows == (
            EditorIdentifier.VSCODE,
            EditorIdentifier.NOTEPAD,
        )
        assert settings.container == (
            EditorIdentifier.MICRO,
            EditorIdentifier.NEOVIM,
        )
        assert settings.prefer_environment is False
        assert settings.allow_fallback is False

    @pytest.mark.parametrize(
        ("raw", "expected"),
        [
            ({"prefer_environment": "yes"}, "must be a boolean"),
            ({"candidates": []}, "must be a TOML table"),
            (
                {"candidates": {"windows": "vscode"}},
                "must be an array",
            ),
            (
                {"candidates": {"linux": ["unknown-editor"]}},
                "Unsupported editor",
            ),
        ],
    )
    def test_invalid_configuration_is_actionable(
        self,
        raw: dict[str, object],
        expected: str,
    ) -> None:
        """Invalid editor configuration fails with a focused explanation."""

        with pytest.raises(ConfigurationError, match=expected):
            EditorSettings.from_mapping(raw)
