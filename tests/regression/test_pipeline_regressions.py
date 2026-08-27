# tests/regression/test_pipeline_regressions.py

"""
tests/regression/test_pipeline_regressions.py

Regression tests for Pipeline.

These tests protect against bugs that have previously occurred
or could easily reappear during future refactoring.
"""

from unittest.mock import MagicMock

from app.core.pipeline.pipeline import Pipeline
from app.core.pipeline.steps.base_step import BaseStep


class DummyStep(BaseStep):
    """
    Simple step used for regression testing.
    """

    def __init__(self, name: str, calls: list[str]):
        self._name = name
        self.calls = calls

    @property
    def name(self) -> str:
        return self._name

    def execute(self, ctx):
        self.calls.append(self._name)


class TestPipelineRegressions:
    """
    Regression tests for Pipeline.
    """

    def test_steps_execute_in_order(self):
        """
        Regression:
        Steps must execute in the order they were added.
        """
        calls = []

        pipeline = Pipeline(
            [
                DummyStep("step1", calls),
                DummyStep("step2", calls),
                DummyStep("step3", calls),
            ],
            isVisible=False,
        )

        pipeline.run(MagicMock())

        assert calls == [
            "step1",
            "step2",
            "step3",
        ]

    def test_pipeline_with_no_steps(self):
        """
        Regression:
        Empty pipelines should execute successfully.
        """
        pipeline = Pipeline([], isVisible=False)

        pipeline.run(MagicMock())

    def test_step_executed_exactly_once(self):
        """
        Regression:
        A step must never execute twice.
        """
        step = MagicMock(spec=BaseStep)

        pipeline = Pipeline(
            [step],
            isVisible=False,
        )

        pipeline.run(MagicMock())

        step.execute.assert_called_once()

    def test_pipeline_stops_after_exception(self):
        """
        Regression:
        Execution should stop after the first failing step.
        """
        executed = []

        class GoodStep(BaseStep):
            @property
            def name(self):
                return "good"

            def execute(self, ctx):
                executed.append("good")

        class BadStep(BaseStep):
            @property
            def name(self):
                return "bad"

            def execute(self, ctx):
                executed.append("bad")
                raise RuntimeError("boom")

        class LastStep(BaseStep):
            @property
            def name(self):
                return "last"

            def execute(self, ctx):
                executed.append("last")

        pipeline = Pipeline(
            [
                GoodStep(),
                BadStep(),
                LastStep(),
            ],
            isVisible=False,
        )

        try:
            pipeline.run(MagicMock())
        except RuntimeError:
            pass

        assert executed == [
            "good",
            "bad",
        ]
