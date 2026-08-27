# tests/core/pipeline/steps/test_generate_artifacts_step.py

"""
tests/pipeline/steps/generation/test_generate_artifacts_step.py

Unit tests for GenerateArtifactsStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.generate_artifacts_step import (
    GenerateArtifactsStep,
)


class TestGenerateArtifactsStep:
    """
    Tests for GenerateArtifactsStep.
    """

    def test_execute_calls_engine(self):
        """
        execute() should delegate to
        WorkflowEngine.generate_release_artifacts().
        """
        ctx = MagicMock()

        step = GenerateArtifactsStep()

        step.execute(ctx)

        ctx.engine.generate_release_artifacts.assert_called_once_with()
