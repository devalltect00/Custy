# tests/core/project/test_detector.py

"""Tests for cross-project layout and version-target detection."""

import json

import pytest

from app.core.project import (
    ProjectEcosystem,
    detect_project_layout,
    detect_project_name,
)
from app.core.shared import ConfigurationError


class TestProjectLayoutDetection:
    """Covers Python, Node.js, mixed, and generic repositories."""

    def test_detects_python_app_layout(self, tmp_path):
        """Selects app and an existing Python version module."""

        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "demo"\ndynamic = ["version"]\n',
            encoding="utf-8",
        )
        app_dir = tmp_path / "app"
        app_dir.mkdir()
        version_file = app_dir / "__version__.py"
        version_file.write_text('__version__ = "1.0.0"\n', encoding="utf-8")

        layout = detect_project_layout(root=tmp_path)

        assert layout.source_dir == app_dir.resolve()
        assert layout.version_target == version_file.resolve()
        assert layout.is_python is True
        assert layout.is_node is False

    def test_detects_static_pyproject_version(self, tmp_path):
        """Uses pyproject.toml when no Python version module exists."""

        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            '[project]\nname = "demo"\nversion = "1.0.0"\n',
            encoding="utf-8",
        )
        (tmp_path / "src").mkdir()

        layout = detect_project_layout(root=tmp_path)

        assert layout.source_dir == (tmp_path / "src").resolve()
        assert layout.version_target == pyproject.resolve()

    def test_detects_node_docusaurus_layout(self, tmp_path):
        """Selects src and package.json for a Node.js documentation project."""

        package_json = tmp_path / "package.json"
        package_json.write_text(
            json.dumps({"name": "docs", "version": "0.1.0"}),
            encoding="utf-8",
        )
        source = tmp_path / "src"
        source.mkdir()

        layout = detect_project_layout(root=tmp_path)

        assert layout.source_dir == source.resolve()
        assert layout.version_target == package_json.resolve()
        assert layout.is_node is True
        assert layout.is_python is False

    def test_detects_mixed_project(self, tmp_path):
        """Retains both ecosystems when Python and Node markers coexist."""

        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "mixed"\ndynamic = ["version"]\n',
            encoding="utf-8",
        )
        (tmp_path / "package.json").write_text(
            json.dumps({"name": "mixed", "version": "1.0.0"}),
            encoding="utf-8",
        )

        layout = detect_project_layout(root=tmp_path)

        assert ProjectEcosystem.PYTHON in layout.ecosystems
        assert ProjectEcosystem.NODE in layout.ecosystems
        assert layout.version_target == (tmp_path / "package.json").resolve()

    def test_generic_project_falls_back_to_root(self, tmp_path):
        """Allows repositories without language-specific marker files."""

        layout = detect_project_layout(root=tmp_path)

        assert layout.source_dir == tmp_path.resolve()
        assert layout.version_target is None
        assert layout.is_generic is True

    def test_honors_explicit_paths(self, tmp_path):
        """Uses existing explicitly configured source and version paths."""

        source = tmp_path / "website"
        source.mkdir()
        version = tmp_path / "VERSION.json"
        version.write_text('{"version": "1.0.0"}', encoding="utf-8")

        layout = detect_project_layout(
            root=tmp_path,
            project_source="website",
            version_file="VERSION.json",
        )

        assert layout.source_dir == source.resolve()
        assert layout.version_target == version.resolve()
        assert layout.source_is_explicit is True
        assert layout.version_is_explicit is True

    def test_rejects_missing_explicit_source(self, tmp_path):
        """Provides an actionable error for a configured missing source."""

        with pytest.raises(ConfigurationError, match="project_source"):
            detect_project_layout(root=tmp_path, project_source="missing")

    def test_rejects_missing_explicit_version_target(self, tmp_path):
        """Provides an actionable error for a configured missing target."""

        with pytest.raises(ConfigurationError, match="version_file"):
            detect_project_layout(root=tmp_path, version_file="missing.json")


class TestProjectNameDetection:
    """Cover Python, Node.js, and generic release-message project names."""

    def test_prefers_pyproject_name(self, tmp_path) -> None:
        """Python project metadata has deterministic priority."""

        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "path-header-scanner"\n',
            encoding="utf-8",
        )

        assert detect_project_name(root=tmp_path) == "path-header-scanner"

    def test_uses_package_name_when_python_metadata_is_absent(self, tmp_path) -> None:
        """Node.js and Docusaurus projects use package.json metadata."""

        (tmp_path / "package.json").write_text(
            json.dumps({"name": "devalltect-docs"}),
            encoding="utf-8",
        )

        assert detect_project_name(root=tmp_path) == "devalltect-docs"

    def test_generic_project_uses_directory_name(self, tmp_path) -> None:
        """Repositories without supported metadata still receive a name."""

        assert detect_project_name(root=tmp_path) == tmp_path.name
