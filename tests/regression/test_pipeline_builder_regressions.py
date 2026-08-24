# tests/regression/test_pipeline_builder_regressions.py

"""
tests/regression/test_pipeline_builder_regressions.py

Regression tests for PipelineBuilder.

These tests protect pipeline construction against future
refactoring.
"""

from app.core.pipeline.builder import PipelineBuilder
from app.core.pipeline.pipeline import Pipeline


class TestPipelineBuilderRegressions:
    """
    Regression tests for PipelineBuilder.
    """

    def test_build_returns_pipeline(self):
        """
        Regression:
        build() should always return a Pipeline instance.
        """
        builder = PipelineBuilder(
            isVisible=False,
        )

        pipeline = builder.build([])

        assert isinstance(pipeline, Pipeline)

    def test_empty_pipeline(self):
        """
        Regression:
        Building an empty pipeline should succeed.
        """
        builder = PipelineBuilder(
            isVisible=False,
        )

        pipeline = builder.build([])

        assert isinstance(pipeline, Pipeline)
        assert pipeline.steps == []

    def test_pipeline_contains_requested_steps(self):
        """
        Regression:
        Every resolved step should appear in the pipeline.
        """
        builder = PipelineBuilder(
            isVisible=False,
        )

        pipeline = builder.build(
            [
                {
                    "name": "ensure_git_repo_step",
                },
                {
                    "name": "prepare_version_step",
                },
                {
                    "name": "commit_step",
                },
            ]
        )

        names = [
            step.__class__.__name__
            for step in pipeline.steps
        ]

        assert names == [
            "EnsureGitRepoStep",
            "PrepareVersionStep",
            "CommitStep",
        ]

    def test_pipeline_preserves_step_order(self):
        """
        Regression:
        Step order must never change.
        """
        builder = PipelineBuilder(
            isVisible=False,
        )

        pipeline = builder.build(
            [
                {"name": "stage_step"},
                {"name": "commit_step"},
                {"name": "push_step"},
            ]
        )

        names = [
            step.__class__.__name__
            for step in pipeline.steps
        ]

        assert names == [
            "StageStep",
            "CommitStep",
            "PushStep",
        ]

    def test_build_creates_new_pipeline_each_time(self):
        """
        Regression:
        build() should never reuse Pipeline instances.
        """
        builder = PipelineBuilder(
            isVisible=False,
        )

        first = builder.build([])
        second = builder.build([])

        assert first is not second

    def test_build_creates_new_step_instances(self):
        """
        Regression:
        Every build should create fresh step instances.
        """
        builder = PipelineBuilder(
            isVisible=False,
        )

        first = builder.build(
            [
                {
                    "name": "commit_step",
                },
            ]
        )

        second = builder.build(
            [
                {
                    "name": "commit_step",
                },
            ]
        )

        assert first.steps[0] is not second.steps[0]
