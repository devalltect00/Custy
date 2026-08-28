# tests/config/test_config_loader.py

"""
tests/config/test_config_loader.py

Unit tests for ConfigLoader.
"""

from pathlib import Path

import pytest

from app.config.config_loader import ConfigLoader, get_config
from app.core.editor import EditorIdentifier, EditorSettings
from app.core.shared import ConfigurationError

VALID_TOML = """
[tool.custy.git]
auto_push = true

[tool.custy.logging]
level = "debug"

[tool.custy.cli.execution]
dry_run = true

[tool.custy.editor]
prefer_environment = false

[tool.custy.editor.candidates]
windows = ["vscode", "notepad"]
"""

INVALID_TOML = """
[tool.custy
broken = true
"""


class TestConfigLoader:
    def test_load_valid_toml(self, tmp_path):
        path = tmp_path / "config.toml"
        path.write_text(VALID_TOML)

        loader = ConfigLoader(path)

        assert loader.get("git", "auto_push") is True

    def test_missing_file(self, tmp_path):
        loader = ConfigLoader(tmp_path / "missing.toml")
        assert loader.config == {}

    def test_invalid_toml(self, tmp_path):
        path = tmp_path / "config.toml"
        path.write_text(INVALID_TOML)

        with pytest.raises(ConfigurationError):
            ConfigLoader(path)

    def test_get_default(self, tmp_path):
        path = tmp_path / "config.toml"
        path.write_text(VALID_TOML)

        loader = ConfigLoader(path)

        assert loader.get("missing", default=123) == 123

    def test_require(self, tmp_path):
        path = tmp_path / "config.toml"
        path.write_text(VALID_TOML)

        loader = ConfigLoader(path)

        assert loader.require("git", "auto_push") is True

        with pytest.raises(ConfigurationError):
            loader.require("missing")

    def test_get_section(self, tmp_path):
        path = tmp_path / "config.toml"
        path.write_text(VALID_TOML)

        loader = ConfigLoader(path)

        assert loader.get_section("git")["auto_push"] is True
        assert loader.get_section("editor")["prefer_environment"] is False
        assert loader.get_section("editor")["candidates"]["windows"] == [
            "vscode",
            "notepad",
        ]
        assert loader.get_section("unknown") == {}

    def test_resolve_priority(self, tmp_path):
        path = tmp_path / "config.toml"
        path.write_text(VALID_TOML)

        loader = ConfigLoader(path)

        assert loader.resolve(False, ["git", "auto_push"], True) is False
        assert loader.resolve(None, ["git", "auto_push"], False) is True
        assert loader.resolve(None, ["missing"], "fallback") == "fallback"

    def test_required_resolve(self, tmp_path):
        path = tmp_path / "config.toml"
        path.write_text(VALID_TOML)

        loader = ConfigLoader(path)

        with pytest.raises(ConfigurationError):
            loader.resolve(None, ["missing"], required=True)

    def test_false_as_none(self, tmp_path):
        path = tmp_path / "config.toml"
        path.write_text(VALID_TOML)

        loader = ConfigLoader(path)

        assert (
            loader.resolve(
                False,
                ["git", "auto_push"],
                treat_false_as_none=True,
            )
            is True
        )

    def test_singleton(self):
        assert get_config() is get_config()

    def test_packaged_template_has_valid_editor_defaults(self):
        loader = ConfigLoader(Path("app/templates/config.toml"))

        settings = EditorSettings.from_mapping(loader.get_section("editor"))

        assert settings.windows == (
            EditorIdentifier.VSCODE,
            EditorIdentifier.NOTEPAD,
        )
        assert settings.container[0] is EditorIdentifier.MICRO
