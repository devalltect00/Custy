# tests/core/initialize/models/test_registry.py

"""
tests/core/initialize/test_registry.py

Unit tests for the initialization registry.

These tests verify that the registry exposes the expected directory and
template definitions used by the initialization workflow.
"""

from unittest.mock import MagicMock

import os
import pytest

from app.core.initialize.models.template_dir import TemplateDir
from app.core.initialize.models.template_file import TemplateFile
from app.core.initialize.registry import (
    DirRegistry,
    FileRegistry,
    detect_version_file,
)


class TestDetectVersionFile:
    """Tests for detect_version_file()."""

    def test_returns_target_project_version_file_when_project_source_exists(
        self,
        monkeypatch,
    ):
        """Returns the configured project version file when it exists."""

        # monkeypatch.setattr(
        #     "app.core.initialize.registry.os.path.exists",
        #     lambda _: True,
        # )

        monkeypatch.setattr(
            os.path,
            "exists",
            lambda _: True,
        )

        monkeypatch.setattr(
            "app.core.initialize.registry.TARGET_PROJECT_SOURCE",
            "app",
        )

        assert detect_version_file() == "app/__version__.py"

    def test_returns_default_version_file_when_project_source_does_not_exist(
        self,
        monkeypatch,
    ):
        """Falls back to the default version file."""

        # monkeypatch.setattr(
        #     "app.core.initialize.registry.os.path.exists",
        #     lambda _: False,
        # )

        monkeypatch.setattr(
            os.path,
            "exists",
            lambda _: False,
        )

        assert detect_version_file() == "src/__version__.py"


class TestDirRegistry:
    """Tests for DirRegistry."""

    def test_returns_configuration_directories(self):
        """Returns the configuration directory list."""

        assert DirRegistry.get_config_directories() == [
            ".config/custy",
        ]

    def test_returns_template_directories(self):
        """Returns all template directories."""

        directories = DirRegistry.get_templates_directories()

        assert ".config/custy/templates" in directories
        assert ".config/custy/templates/backups" in directories
        assert ".config/custy/templates/backups/commit" in directories
        assert ".config/custy/templates/backups/tag" in directories
        assert ".config/custy/templates/changelog" in directories

    def test_returns_example_directories(self):
        """Returns all example directories."""

        directories = DirRegistry.get_examples_directories()

        assert ".config/custy/templates/examples" in directories
        assert (
            ".config/custy/templates/examples/commit_message"
            in directories
        )
        assert (
            ".config/custy/templates/examples/tag_message"
            in directories
        )

    def test_returns_all_directories(self):
        """Combines every directory registry into a single list."""

        registry = DirRegistry()

        directories = registry.get_all_directories()

        assert directories == (
            DirRegistry.get_config_directories()
            + DirRegistry.get_templates_directories()
            + DirRegistry.get_examples_directories()
        )


class TestFileRegistry:
    """Tests for FileRegistry."""

    def test_constructs_registry(self):
        """Constructs all template definitions."""

        registry = FileRegistry()

        assert isinstance(registry.config, TemplateFile)
        assert isinstance(registry.version, TemplateFile)
        assert isinstance(registry.changelog, TemplateFile)
        assert isinstance(registry.commit_message, TemplateFile)
        assert isinstance(registry.tag_message, TemplateFile)

    @pytest.mark.parametrize(
        ("method", "expected_length"),
        [
            ("get_config", 1),
            ("get_templates", 3),
            ("get_version", 1),
            ("get_examples", 1),
        ],
    )
    def test_registry_methods_return_expected_number_of_items(
        self,
        method,
        expected_length,
    ):
        """Returns the expected number of registry entries."""

        result = getattr(FileRegistry, method)()

        assert len(result) == expected_length

    def test_get_config_returns_template_files(self):
        """Returns TemplateFile instances."""

        files = FileRegistry.get_config()

        assert all(
            isinstance(item, TemplateFile)
            for item in files
        )

    def test_get_templates_returns_template_files(self):
        """Returns template file definitions."""

        files = FileRegistry.get_templates()

        assert all(
            isinstance(item, TemplateFile)
            for item in files
        )

    def test_get_version_returns_template_files(self):
        """Returns version template definitions."""

        files = FileRegistry.get_version()

        assert all(
            isinstance(item, TemplateFile)
            for item in files
        )

    def test_get_examples_returns_template_directories(self):
        """Returns example template directories."""

        directories = FileRegistry.get_examples()

        assert all(
            isinstance(item, TemplateDir)
            for item in directories
        )

    def test_get_all_files_combines_every_registry(
        self,
        monkeypatch,
    ):
        """Combines every registry collection into a single list."""

        config = [MagicMock()]
        templates = [MagicMock(), MagicMock()]
        version = [MagicMock()]
        examples = [MagicMock()]

        monkeypatch.setattr(
            FileRegistry,
            "get_config",
            staticmethod(lambda: config),
        )

        monkeypatch.setattr(
            FileRegistry,
            "get_templates",
            staticmethod(lambda: templates),
        )

        monkeypatch.setattr(
            FileRegistry,
            "get_version",
            staticmethod(lambda: version),
        )

        monkeypatch.setattr(
            FileRegistry,
            "get_examples",
            staticmethod(lambda: examples),
        )

        registry = FileRegistry()

        result = registry.get_all_files()

        assert result == (
            config
            + templates
            + version
            + examples
        )
