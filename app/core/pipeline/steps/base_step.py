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

    Examples:
        class MyStep(BaseStep):
            def execute(self, ctx):
                pass
    """

    def execute(self, context) -> None:
        raise NotImplementedError("Step must implement execute()")
