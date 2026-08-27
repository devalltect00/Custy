# tests/core/pipeline/steps/initialization/test_init_step.py

"""
tests/pipeline/steps/finalization/test_init_step.py

Unit tests for InitStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.initialization.init_step import (
    InitStep,
)


class TestInitStep:
    """
    Tests for InitStep.
    """

    def test_execute_calls_init_main(self, monkeypatch):
        """
        execute() should delegate to InitMain.execute(args).
        """
        ctx = MagicMock()

        init_main = MagicMock()

        monkeypatch.setattr(
            "app.core.pipeline.steps.initialization.init_step.InitMain",
            lambda: init_main,
        )

        step = InitStep()

        step.execute(ctx)

        init_main.execute.assert_called_once_with(ctx.args)
