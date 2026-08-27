# app/core/pipeline/steps/initialization/init_step.py


from app.core.initialize.main import InitMain
from app.core.pipeline.decorators.log_step import log_step
from app.core.pipeline.steps.base_step import BaseStep


class InitStep(BaseStep):
    """
    Initialization Step

    Executes project initialization using pipeline architecture.

    Source of truth:
        - ctx.args (from CLI)

    Responsibilities:
        - Build InitConfig from args
        - Build InitSpec via InitBuilder
        - Execute ScaffoldGenerator

    Notes:
        - No constructor args needed
        - Fully driven by CLI/context
    """

    @log_step(label="initialization")
    def execute(self, ctx):
        args = ctx.args

        InitMain().execute(args)
