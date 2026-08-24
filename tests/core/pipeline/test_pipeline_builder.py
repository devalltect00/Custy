# tests/core/pipeline/test_pipeline_builder.py

"""
tests/workflow/test_pipeline_builder.py

Unit tests for PipelineBuilder and SimplePipelineBuilder.
"""

from unittest.mock import MagicMock

import pytest

from app.core.pipeline.builder import (
    PipelineBuilder,
    SimplePipelineBuilder,
)
from app.core.pipeline.pipeline import (
    Pipeline,
    SimplePipeline,
)
from app.core.pipeline.registry import StepRegistry


class TestPipelineBuilder:

    def test_default_visibility(self):
        builder = PipelineBuilder()

        assert builder.isVisible is True

    def test_custom_visibility(self):
        builder = PipelineBuilder(False)

        assert builder.isVisible is False

    def test_build_pipeline(self, monkeypatch):
        step = MagicMock()

        monkeypatch.setattr(
            StepRegistry,
            "create",
            lambda name, **kwargs: step,
        )

        pipeline = PipelineBuilder().build([
            {"name": "validate"},
            {"name": "commit"},
        ])

        assert isinstance(pipeline, Pipeline)
        assert len(pipeline.steps) == 2
        assert pipeline.steps[0] is step
        assert pipeline.steps[1] is step

    def test_passes_constructor_args(self, monkeypatch):
        received = {}

        def fake_create(name, **kwargs):
            received["name"] = name
            received["kwargs"] = kwargs
            return MagicMock()

        monkeypatch.setattr(
            StepRegistry,
            "create",
            fake_create,
        )

        PipelineBuilder().build([
            {
                "name": "cleanup",
                "args": {
                    "cleanup_backups": True,
                },
            }
        ])

        assert received["name"] == "cleanup"
        assert received["kwargs"] == {
            "cleanup_backups": True,
        }


class TestSimplePipelineBuilder:

    def test_default_completed_message(self):
        builder = SimplePipelineBuilder()

        assert builder.useCompletedMessage is True

    def test_custom_completed_message(self):
        builder = SimplePipelineBuilder(False)

        assert builder.useCompletedMessage is False

    def test_build_simple_pipeline(self, monkeypatch):
        monkeypatch.setattr(
            StepRegistry,
            "create",
            lambda *args, **kwargs: MagicMock(),
        )

        pipeline = SimplePipelineBuilder().build([
            {"name": "validate"},
            {"name": "commit"},
        ])

        assert isinstance(pipeline, SimplePipeline)
        assert len(pipeline.steps) == 2
