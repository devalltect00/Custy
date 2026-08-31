# tests/core/pipeline/test_pipeline_runtime.py

"""
tests/workflow/test_pipeline_runtime.py

Unit tests for Pipeline and SimplePipeline runtime.
"""

from contextlib import contextmanager
from unittest.mock import MagicMock

import pytest

from app.core.pipeline import pipeline as pipeline_module
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

    def test_pipeline_suspends_progress_for_exclusive_terminal_step(
        self,
        monkeypatch,
    ):
        """Releases live progress while an interactive step uses the terminal."""

        events = []

        class InteractiveStep:
            name = "interactive"
            requires_exclusive_terminal = True

            def execute(self, context):
                events.append("execute")

        @contextmanager
        def fake_suspend_progress(
            progress,
            task_id,
            *,
            restore_visible,
        ):
            events.append(("suspend", restore_visible))
            yield
            events.append("resume")

        monkeypatch.setattr(
            pipeline_module,
            "suspend_progress",
            fake_suspend_progress,
        )

        Pipeline([InteractiveStep()]).run(MagicMock())

        assert events == [
            ("suspend", True),
            "execute",
            "resume",
        ]

    def test_hidden_pipeline_disables_rich_rendering(self, monkeypatch):
        """Prevents hidden pipelines from redrawing interactive prompts."""

        class InteractiveStep:
            requires_exclusive_terminal = True

            def execute(self, context):
                return None

        suspend = MagicMock()
        progress = MagicMock()
        progress.__enter__.return_value = progress
        progress.add_task.return_value = 1
        progress_factory = MagicMock(return_value=progress)

        monkeypatch.setattr(
            pipeline_module,
            "suspend_progress",
            suspend,
        )
        monkeypatch.setattr(
            pipeline_module,
            "Progress",
            progress_factory,
        )

        Pipeline([InteractiveStep()], isVisible=False).run(MagicMock())

        assert progress_factory.call_args.kwargs["disable"] is True
        suspend.assert_not_called()
