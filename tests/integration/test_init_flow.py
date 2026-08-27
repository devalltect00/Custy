# tests/integration/test_init_flow.py

"""
tests/integration/test_init_flow.py

Integration tests for the initialization workflow.
"""

from unittest.mock import MagicMock

from app.core.pipeline.pipeline import Pipeline
from app.core.pipeline.steps.initialization.init_step import (
    InitStep,
)


class TestInitFlow:
    """
    Integration tests for the initialization workflow.
    """

    def test_init_pipeline_executes_init_main(self, monkeypatch):
        ctx = MagicMock()

        init_main = MagicMock()

        monkeypatch.setattr(
            "app.core.pipeline.steps.initialization.init_step.InitMain",
            lambda: init_main,
        )

        pipeline = Pipeline(
            [
                InitStep(),
            ],
            isVisible=False,
        )

        pipeline.run(ctx)

        init_main.execute.assert_called_once_with(ctx.args)

    def test_init_pipeline_executes_once(self, monkeypatch):
        ctx = MagicMock()

        init_main = MagicMock()

        monkeypatch.setattr(
            "app.core.pipeline.steps.initialization.init_step.InitMain",
            lambda: init_main,
        )

        Pipeline(
            [
                InitStep(),
            ],
            isVisible=False,
        ).run(ctx)

        assert init_main.execute.call_count == 1
