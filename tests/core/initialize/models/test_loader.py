# tests/core/initialize/models/test_loader.py

"""
tests/core/initialize/test_loader.py

Unit tests for the initialization template loader.

These tests verify that template content is resolved from the user
template directory when available, and otherwise falls back to the
packaged templates bundled with Custy.
"""

from pathlib import Path
from unittest.mock import MagicMock

from app.core.initialize import loader


class TestLoadTemplate:
    """Tests for load_template()."""

    def test_loads_user_override_when_template_exists(
        self,
        monkeypatch,
        tmp_path,
    ):
        """Loads a template from the user's template directory."""

        template_dir = tmp_path / "templates"
        template_dir.mkdir()

        template_file = template_dir / "example.txt"
        template_file.write_text(
            "user template",
            encoding="utf-8",
        )

        monkeypatch.chdir(tmp_path)

        result = loader.load_template("example.txt")

        assert result == "user template"

    def test_loads_packaged_template_when_user_template_does_not_exist(
        self,
        monkeypatch,
    ):
        """Falls back to the packaged template when no user override exists."""

        packaged_template = MagicMock()
        packaged_template.read_text.return_value = "package template"

        packaged_root = MagicMock()
        packaged_root.joinpath.return_value = packaged_template

        monkeypatch.setattr(
            loader,
            "files",
            lambda _: packaged_root,
        )

        monkeypatch.setattr(
            Path,
            "exists",
            lambda self: False,
        )

        result = loader.load_template("example.txt")

        assert result == "package template"

        packaged_root.joinpath.assert_called_once_with("example.txt")

        packaged_template.read_text.assert_called_once_with(
            encoding="utf-8",
        )
