# app/core/pipeline/steps/base_step.py

"""
Base Step Interface

All pipeline steps must inherit from this class.
"""


class BaseStep:
    """
    Abstract base class for pipeline steps.

    Each step must implement:
        execute(context)

    Attributes:
        requires_exclusive_terminal:
            Whether the visible pipeline must pause its live display while the
            step runs. Interactive terminal steps should override this marker.

    Examples:
        class MyStep(BaseStep):
            def execute(self, ctx):
                pass
    """

    requires_exclusive_terminal: bool = False

    def execute(self, context) -> None:
        raise NotImplementedError("Step must implement execute()")
