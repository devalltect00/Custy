# tests/core/files/test_cross_project_version_updates.py

"""Tests for cross-project version metadata updates."""

import json

import pytest

from app.core.files.update_files import (
    update_json_version,
    update_python_version_module,
    update_toml_project_version,
    update_version_universal,
)
from app.core.shared import ConfigurationError


class TestCrossProjectVersionUpdates:
    """Verifies Python, Node.js, mixed, and generic update behavior."""

    def test_updates_python_module_without_discarding_content(self, tmp_path):
        """Replaces only __version__ and preserves the surrounding module."""

        path = tmp_path / "__version__.py"
        path.write_text(
            '"""Version metadata."""\n\nNAME = "demo"\n__version__ = "1.0.0"\n',
            encoding="utf-8",
        )

        assert update_python_version_module(path, "v2.0.0") is True

        content = path.read_text(encoding="utf-8")
        assert 'NAME = "demo"' in content
        assert '__version__ = "2.0.0"' in content
        assert content.endswith("\n")

    def test_adds_final_newline_when_replacing_version_at_eof(self, tmp_path):
        """Normalizes a version module that previously lacked its final LF."""

        path = tmp_path / "__version__.py"
        path.write_text('__version__ = "1.0.0"', encoding="utf-8")

        assert update_python_version_module(path, "v2.0.0") is True

        assert path.read_text(encoding="utf-8") == '__version__ = "2.0.0"\n'

    def test_updates_static_pyproject_version(self, tmp_path):
        """Writes normalized metadata while preserving TOML structure."""

        path = tmp_path / "pyproject.toml"
        path.write_text(
            '[project]\nname = "demo"\nversion = "1.0.0"\n',
            encoding="utf-8",
        )

        assert update_toml_project_version("v2.0.0", path) is True
        assert 'version = "2.0.0"' in path.read_text(encoding="utf-8")

    def test_updates_node_and_package_lock_versions(self, tmp_path):
        """Updates package metadata including the npm root lock entry."""

        package = tmp_path / "package.json"
        package.write_text(
            json.dumps({"name": "docs", "version": "0.0.0"}),
            encoding="utf-8",
        )
        lock = tmp_path / "package-lock.json"
        lock.write_text(
            json.dumps(
                {
                    "name": "docs",
                    "version": "0.0.0",
                    "packages": {"": {"name": "docs", "version": "0.0.0"}},
                }
            ),
            encoding="utf-8",
        )

        assert update_version_universal(tmp_path, "v0.1.0-alpha.1", "node") is True

        assert json.loads(package.read_text())["version"] == "0.1.0-alpha.1"
        lock_data = json.loads(lock.read_text())
        assert lock_data["version"] == "0.1.0-alpha.1"
        assert lock_data["packages"][""]["version"] == "0.1.0-alpha.1"

    def test_updates_mixed_project_metadata(self, tmp_path):
        """Updates both Python and Node metadata in automatic mode."""

        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "mixed"\nversion = "1.0.0"\n',
            encoding="utf-8",
        )
        (tmp_path / "package.json").write_text(
            json.dumps({"name": "mixed", "version": "1.0.0"}),
            encoding="utf-8",
        )

        assert update_version_universal(tmp_path, "v2.0.0") is True
        assert 'version = "2.0.0"' in (tmp_path / "pyproject.toml").read_text(
            encoding="utf-8"
        )
        assert (
            json.loads((tmp_path / "package.json").read_text(encoding="utf-8"))[
                "version"
            ]
            == "2.0.0"
        )

    def test_generic_project_is_a_valid_noop(self, tmp_path):
        """Leaves a repository without supported metadata unchanged."""

        assert update_version_universal(tmp_path, "v1.0.0") is False

    def test_invalid_json_raises_configuration_error(self, tmp_path):
        """Surfaces malformed package metadata instead of silently skipping it."""

        package = tmp_path / "package.json"
        package.write_text("{invalid", encoding="utf-8")

        with pytest.raises(ConfigurationError, match="Unable to parse JSON"):
            update_json_version(package, "1.0.0")
