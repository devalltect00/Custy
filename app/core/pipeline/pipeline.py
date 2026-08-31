# app/core/pipeline/pipeline.py

"""
Pipeline Engine

Executes a sequence of steps in a defined order.
Executes pipeline steps sequentially with progress visualization.

This is the core orchestrator that replaces the monolithic flow
previously inside GitWorkflowEngine.execute_all().

Each step must implement:
    execute(context)

Responsibilities:
- Execute steps in order
- Display progress bar
- Handle step errors
- Provide clean CLI UX

Design:
- Simple
- Explicit
- Extensible
- Progress handles visualization
- Steps handle logic
- Decorators handle logging (optional)

You can insert/remove/reorder steps easily.

Example:
    pipeline = Pipeline([
        ValidateStep(),
        CommitStep(),
    ])
    pipeline.run(ctx)
"""

import logging

from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn

from app.ui.console import console
from app.ui.progress import suspend_progress

logger = logging.getLogger(__name__)


class Pipeline:
    """
    Pipeline orchestrator that executes steps sequentially.

    Args:
        steps (List): List of step instances.

    Returns:
        None

    Raises:
        Exception: Propagates any exception from steps.

    Examples:
        >>> pipeline = Pipeline([StepA(), StepB()])
        >>> pipeline.run(context)
    """

    def __init__(self, steps: list, isVisible: bool = True):
        self.steps = steps

        # level = logger.getEffectiveLevel()
        # level_name = logging.getLevelName(level)

        self.visible = isVisible

    def run(self, context) -> None:
        """
        Execute all steps in order.

        Args:
            context: Shared context object.

        Returns:
            None

        Raises:
            Exception: If any step fails.
        """
        total = len(self.steps)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            console=console,
            # A hidden task still leaves Rich's live display active. Disable
            # rendering entirely for direct commands so Git and terminal
            # editors retain stable ownership of interactive prompts.
            disable=not self.visible,
        ) as progress:
            task = progress.add_task(
                "[bold]Executing pipeline...[/bold]", total=total, visible=self.visible
            )

            for step in self.steps:
                step_name = getattr(step, "name", step.__class__.__name__)

                # logger.info(f"[cyan]→ {step_name}[/cyan]")

                # 👇 Update progress UI
                progress.update(
                    task,
                    description=f"[cyan]→ {step_name}[/cyan]",
                )

                try:
                    if self.visible and getattr(
                        step, "requires_exclusive_terminal", False
                    ):
                        with suspend_progress(
                            progress,
                            task,
                            restore_visible=self.visible,
                        ):
                            step.execute(context)
                    else:
                        step.execute(context)
                except Exception:
                    progress.stop()
                    console.print(
                        f"[red]❌ Pipeline failed at step:[/red] [bold]{step_name}[/bold]"
                    )
                    raise

                progress.advance(task)

            logger.debug("")

            progress.console.print("[green]✔ Pipeline completed successfully![/green]")


class SimplePipeline:
    """
    Pipeline orchestrator that executes steps sequentially.

    Args:
        steps (List): List of step instances.

    Returns:
        None

    Raises:
        Exception: Propagates any exception from steps.

    Examples:
        >>> pipeline = Pipeline([StepA(), StepB()])
        >>> pipeline.run(context)
    """

    def __init__(self, steps: list, useCompletedMessage: bool = True):
        self.steps = steps
        self.useCompletedMessage = useCompletedMessage

    def run(self, context) -> None:
        """
        Execute all steps in order.

        Args:
            context: Shared context object.

        Returns:
            None

        Raises:
            Exception: If any step fails.
        """
        for step in self.steps:
            logger.info(f"➡️ Running step: {step.__class__.__name__}")
            step.execute(context)

        logger.debug("")

        # logger.info("✅ Pipeline execution completed.")
        logger.info("\n✅ Execution completed!")
