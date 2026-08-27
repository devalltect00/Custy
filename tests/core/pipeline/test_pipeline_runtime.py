# tests/core/pipeline/test_pipeline_runtime.py

"""
tests/workflow/test_pipeline_runtime.py

Unit tests for Pipeline and SimplePipeline runtime.
"""

from unittest.mock import MagicMock

import pytest

from app.core.pipeline.pipeline import Pipeline, SimplePipeline


class DummyStep:
    def __init__(self, name):
        self.name = name
        self.executed = False

    def execute(self, context):
        self.executed = True


class FailingStep:
    name = "failing"

    def execute(self, context):
        raise RuntimeError("boom")


class TestPipelineRuntime:
    def test_pipeline_runs_all_steps(self):
        steps = [DummyStep("one"), DummyStep("two")]
        ctx = MagicMock()

        Pipeline(steps, isVisible=False).run(ctx)

        assert all(step.executed for step in steps)

    def test_simple_pipeline_runs_all_steps(self):
        steps = [DummyStep("one"), DummyStep("two")]
        ctx = MagicMock()

        SimplePipeline(steps).run(ctx)

        assert all(step.executed for step in steps)

    def test_pipeline_stops_on_failure(self):
        steps = [
            DummyStep("first"),
            FailingStep(),
            DummyStep("last"),
        ]

        with pytest.raises(RuntimeError):
            Pipeline(steps, isVisible=False).run(MagicMock())

        assert steps[0].executed is True
        assert steps[2].executed is False

    def test_simple_pipeline_stops_on_failure(self):
        steps = [
            DummyStep("first"),
            FailingStep(),
            DummyStep("last"),
        ]

        with pytest.raises(RuntimeError):
            SimplePipeline(steps).run(MagicMock())

        assert steps[0].executed is True
        assert steps[2].executed is False

    def test_context_is_passed_to_every_step(self):
        calls = []

        class ContextStep:
            def __init__(self, name):
                self.name = name

            def execute(self, context):
                calls.append(context)

        ctx = object()

        Pipeline(
            [ContextStep("a"), ContextStep("b")],
            isVisible=False,
        ).run(ctx)

        assert calls == [ctx, ctx]
