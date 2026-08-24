# tests/core/initialize/models/test_models.py

"""
tests/core/initialize/models/test_models.py

Unit tests for the initialization model objects.

These tests verify the behavior of the lightweight data models used by
the initialization workflow, including configuration objects, execution
plans, execution summaries, and template definitions.
"""

from app.cli.constants.enums import InitMode, LogLevelChoices
from app.core.initialize.models.init_config import InitConfig
from app.core.initialize.models.init_spec import InitSpec
from app.core.initialize.models.initialization_result import (
    InitializationResult,
)
from app.core.initialize.models.template_dir import TemplateDir
from app.core.initialize.models.template_file import TemplateFile


class TestInitConfig:
    """Tests for InitConfig."""

    def test_construct_with_default_values(self):
        """Constructs InitConfig using default values."""

        config = InitConfig()

        assert config.mode is None
        assert config.force_init is False
        assert config.ask is False
        assert config.dry_run is False
        assert config.no_debug is True
        assert config.log_level == LogLevelChoices.INFO

    def test_construct_with_explicit_values(self):
        """Constructs InitConfig using explicit values."""

        config = InitConfig(
            mode=InitMode.ALL,
            force_init=True,
            ask=True,
            dry_run=True,
            no_debug=False,
            log_level=LogLevelChoices.DEBUG,
        )

        assert config.mode == InitMode.ALL
        assert config.force_init is True
        assert config.ask is True
        assert config.dry_run is True
        assert config.no_debug is False
        assert config.log_level == LogLevelChoices.DEBUG


class TestInitSpec:
    """Tests for InitSpec."""

    def test_construct_with_all_fields(self):
        """Constructs an execution specification with every field."""

        spec = InitSpec(
            name="example",
            templates=["template"],
            dirs=["directory"],
            template_dirs=["examples"],
            messages=["done"],
        )

        assert spec.name == "example"
        assert spec.templates == ["template"]
        assert spec.dirs == ["directory"]
        assert spec.template_dirs == ["examples"]
        assert spec.messages == ["done"]

    def test_optional_fields_default_to_none(self):
        """Optional fields default to None when omitted."""

        spec = InitSpec(
            name="example",
            templates=[],
            dirs=[],
        )

        assert spec.template_dirs is None
        assert spec.messages is None


class TestInitializationResult:
    """Tests for InitializationResult."""

    def test_construct_with_default_statistics(self):
        """Execution statistics default to zero."""

        result = InitializationResult(mode="config")

        assert result.mode == "config"
        assert result.created_files == 0
        assert result.copied_files == 0
        assert result.skipped_files == 0
        assert result.created_directories == 0
        assert result.dry_run is False

    def test_construct_with_explicit_statistics(self):
        """Stores explicitly supplied execution statistics."""

        result = InitializationResult(
            mode="all",
            created_files=1,
            copied_files=2,
            skipped_files=3,
            created_directories=4,
            dry_run=True,
        )

        assert result.mode == "all"
        assert result.created_files == 1
        assert result.copied_files == 2
        assert result.skipped_files == 3
        assert result.created_directories == 4
        assert result.dry_run is True


class TestTemplateDir:
    """Tests for TemplateDir."""

    def test_construct_with_target_and_source(self):
        """Stores the template source and destination."""

        template = TemplateDir(
            target="target",
            source="source",
        )

        assert template.target == "target"
        assert template.source == "source"


class TestTemplateFile:
    """Tests for TemplateFile."""

    def test_render_returns_static_content(self):
        """Returns static string content unchanged."""

        template = TemplateFile(
            target_path="example.txt",
            content="hello world",
        )

        assert template.render() == "hello world"

    def test_render_calls_content_callable(self):
        """Evaluates callable content before returning it."""

        template = TemplateFile(
            target_path="example.txt",
            content=lambda: "generated",
        )

        assert template.render() == "generated"

    def test_render_returns_empty_string_when_content_is_missing(self):
        """Returns an empty string when no content is provided."""

        template = TemplateFile(
            target_path="example.txt",
        )

        assert template.render() == ""

    def test_optional_flag_is_preserved(self):
        """Preserves the optional attribute."""

        template = TemplateFile(
            target_path="example.txt",
            optional=True,
        )

        assert template.optional is True
