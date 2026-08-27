# tests/core/initialize/models/test_init_builder.py

"""
tests/core/initialize/test_init_builder.py

Unit tests for the initialization specification builder.

These tests verify that InitBuilder correctly transforms initialization
configuration into executable initialization specifications for every
supported initialization mode, while also supporting custom overrides
and validation rules.
"""

from unittest.mock import MagicMock

import pytest

from app.cli.constants.enums import InitMode
from app.core.initialize.builder.init_builder import InitBuilder
from app.core.initialize.models.init_config import InitConfig
from app.core.initialize.models.init_spec import InitSpec


class TestInitBuilderFluentApi:
    """Tests for the InitBuilder fluent API."""

    def test_with_name_returns_builder(self):
        """Stores a custom initialization name."""

        builder = InitBuilder()

        assert builder.with_name("custom") is builder
        assert builder._name == "custom"

    def test_with_templates_returns_builder(self):
        """Stores custom template definitions."""

        templates = [MagicMock()]

        builder = InitBuilder()

        assert builder.with_templates(templates) is builder
        assert builder._templates == templates

    def test_with_dirs_returns_builder(self):
        """Stores custom directory definitions."""

        directories = ["dir"]

        builder = InitBuilder()

        assert builder.with_dirs(directories) is builder
        assert builder._dirs == directories

    def test_with_template_dirs_returns_builder(self):
        """Stores custom template directory definitions."""

        template_dirs = [MagicMock()]

        builder = InitBuilder()

        assert builder.with_template_dirs(template_dirs) is builder
        assert builder._template_dirs == template_dirs

    def test_with_messages_returns_builder(self):
        """Stores custom success messages."""

        messages = ["done"]

        builder = InitBuilder()

        assert builder.with_messages(messages) is builder
        assert builder._messages == messages


class TestInitBuilderValidation:
    """Tests for builder validation."""

    def test_requires_mode_or_templates(self):
        """Raises an exception when neither mode nor templates are supplied."""

        builder = InitBuilder(
            InitConfig(
                mode=None,
            )
        )

        with pytest.raises(
            ValueError,
            match="Either mode or templates must be provided",
        ):
            builder.build()


class TestInitBuilderBuildFromMode:
    """Tests for mode-based initialization plans."""

    @pytest.mark.parametrize(
        (
            "mode",
            "expected_name",
            "template_count",
            "dir_count",
            "template_dir_count",
            "message_count",
        ),
        [
            (
                InitMode.CONFIG,
                "configuration",
                1,
                1,
                0,
                1,
            ),
            (
                InitMode.TEMPLATES,
                "templates",
                3,
                5,
                0,
                1,
            ),
            (
                InitMode.EXAMPLES,
                "examples",
                0,
                3,
                1,
                1,
            ),
            (
                InitMode.ALL_NO_EXAMPLES,
                "all (no examples)",
                4,
                6,
                0,
                2,
            ),
            (
                InitMode.ALL,
                "all",
                4,
                9,
                1,
                3,
            ),
        ],
    )
    def test_builds_expected_plan(
        self,
        mode,
        expected_name,
        template_count,
        dir_count,
        template_dir_count,
        message_count,
    ):
        """Builds the expected execution plan for each initialization mode."""

        builder = InitBuilder(
            InitConfig(
                mode=mode,
            )
        )

        spec = builder.build()

        assert isinstance(spec, InitSpec)
        assert spec.name == expected_name

        assert len(spec.templates or []) == template_count
        assert len(spec.dirs or []) == dir_count
        assert len(spec.template_dirs or []) == template_dir_count
        assert len(spec.messages or []) == message_count

    def test_unsupported_mode_raises_value_error(self):
        """Rejects unsupported initialization modes."""

        builder = InitBuilder(
            InitConfig(
                mode=MagicMock(),
            )
        )

        with pytest.raises(
            ValueError,
            match="Unsupported init mode",
        ):
            builder.build()


class TestInitBuilderCustomBuild:
    """Tests for custom initialization plans."""

    def test_builds_custom_specification(self):
        """Builds a custom initialization specification."""

        templates = [MagicMock()]
        directories = ["dir"]
        template_dirs = [MagicMock()]
        messages = ["done"]

        spec = (
            InitBuilder()
            .with_name("custom")
            .with_templates(templates)
            .with_dirs(directories)
            .with_template_dirs(template_dirs)
            .with_messages(messages)
            .build()
        )

        assert spec.name == "custom"
        assert spec.templates == templates
        assert spec.dirs == directories
        assert spec.template_dirs == template_dirs
        assert spec.messages == messages

    def test_override_mode_generated_values(self):
        """Explicit overrides replace values generated from the selected mode."""

        templates = [MagicMock()]
        directories = ["override"]
        messages = ["custom"]

        spec = (
            InitBuilder(
                InitConfig(
                    mode=InitMode.CONFIG,
                )
            )
            .with_name("override")
            .with_templates(templates)
            .with_dirs(directories)
            .with_messages(messages)
            .build()
        )

        assert spec.name == "override"
        assert spec.templates == templates
        assert spec.dirs == directories
        assert spec.messages == messages
