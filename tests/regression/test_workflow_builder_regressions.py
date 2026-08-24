# tests/regression/test_workflow_builder_regressions.py

"""
Regression tests for WorkflowEngineBuilder.

These tests protect the fluent builder API against
future regressions.
"""

from pathlib import Path

from app.core.workflow.workflow_builder import WorkflowEngineBuilder
from app.core.workflow.workflow_engine import WorkflowEngine


class TestWorkflowBuilderRegressions:
    """
    Regression tests for WorkflowEngineBuilder.
    """

    def test_builder_can_be_created(self):
        builder = WorkflowEngineBuilder()

        assert builder is not None

    def test_builder_starts_with_config(self):
        builder = WorkflowEngineBuilder()

        assert builder.config is not None

    def test_build_returns_workflow_engine(self):
        builder = WorkflowEngineBuilder()

        engine = builder.build()

        assert isinstance(engine, WorkflowEngine)

    def test_builder_methods_are_chainable(self):
        builder = WorkflowEngineBuilder()

        result = (
            builder
            .with_tag("v1.0.0")
            .with_version_file(Path("version.py"))
            .with_commit_file(Path("commit.txt"))
            .with_tag_file(Path("tag.txt"))
            .with_dry_run(True)
        )

        assert result is builder

    def test_tag_is_stored_in_config(self):
        builder = (
            WorkflowEngineBuilder()
            .with_tag("v9.9.9")
        )

        assert builder.config.tag_input == "v9.9.9"

    def test_version_file_is_stored_in_config(self):
        version_file = Path("version.py")

        builder = (
            WorkflowEngineBuilder()
            .with_version_file(version_file)
        )

        assert builder.config.version_file == version_file

    def test_commit_message_file_is_stored_in_config(self):
        commit_file = Path("commit-message.txt")

        builder = (
            WorkflowEngineBuilder()
            .with_commit_file(str(commit_file))
        )

        assert builder.config.commit_message_file == commit_file

    def test_tag_message_file_is_stored_in_config(self):
        tag_file = Path("tag-message.txt")

        builder = (
            WorkflowEngineBuilder()
            .with_tag_file(str(tag_file))
        )

        assert builder.config.tag_message_file == tag_file

    def test_build_creates_new_engine_instances(self):
        builder = WorkflowEngineBuilder()

        first = builder.build()
        second = builder.build()

        assert first is not second

    def test_build_preserves_configuration(self):
        builder = (
            WorkflowEngineBuilder()
            .with_tag("v3.1.4")
        )

        engine = builder.build()

        assert engine.config.tag_input == "v3.1.4"
