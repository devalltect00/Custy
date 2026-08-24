# app/core/pipeline/decorators/log_step.py

"""
Pipeline Step Logging Decorator

Provides structured, consistent logging for pipeline steps.

Features:
- Standardized step start/end logs
- Rich-compatible color output
- Automatic step name detection
- Error handling with detailed logging
- Optional custom step labels

Design Goals:
- Keep step implementations clean (no manual logging)
- Centralize logging behavior
- Improve CLI readability and UX
- Separate orchestration logging from business logic

Usage:
    from app.core.pipeline.decorators.log_step import log_step

    class ValidateStep(BaseStep):

        @log_step
        def execute(self, ctx):
            ctx.engine.validate()

Advanced Usage:
    @log_step(label="validate")
    def execute(...):

Output Example:
    ➡️ Running step: validate
    ...
    ✅ Completed step: validate

On Error:
    ❌ Failed step: validate → <error>
"""

import logging
from functools import wraps
from typing import Callable, Optional

logger = logging.getLogger(__name__)


def log_step(func: Optional[Callable] = None, *, label: Optional[str] = None):
    """
    Decorator for pipeline step execution logging.

    This decorator wraps the `execute()` method of a pipeline step
    and provides consistent logging before, after, and on failure.

    Supports both:
        @log_step
        @log_step(label="custom-name")

    Args:
        func (Callable, optional):
            The function to wrap (used internally).
        label (str, optional):
            Custom name for the step. If not provided, uses class name.

    Returns:
        Callable:
            Wrapped function with logging behavior.

    Behavior:
        - Logs step start (➡️)
        - Logs step completion (✅)
        - Logs step failure (❌) with traceback
        - Uses Rich-style formatting for better CLI UX

    Example:
        @log_step
        def execute(self, ctx):
            ...

        @log_step(label="validate")
        def execute(self, ctx):
            ...
    """

    def decorator(func: Callable):

        @wraps(func)
        def wrapper(self, ctx, *args, **kwargs):
            # Determine step name
            step_name = label or getattr(self, "name", None) or self.__class__.__name__

            # 👇 Check debug flag from context
            debug = getattr(ctx.engine, "no_debug", False) is False

            # ===== START =====
            if debug:
                logger.debug("")
                logger.info(f"[cyan]➡️ STEP START[/cyan] | [bold]{step_name}[/bold]")

            try:
                result = func(self, ctx, *args, **kwargs)

                # ===== SUCCESS =====
                if debug:
                    logger.info(f"[green]✅ STEP END[/green] | [bold]{step_name}[/bold]")

                return result

            except Exception as e:
                # ===== ERROR =====
                logger.exception(
                    f"[red]❌ STEP ERROR[/red] | [bold]{step_name}[/bold] → {e}"
                )
                raise

        return wrapper

    # Support both @log_step and @log_step(...)
    if func is not None:
        return decorator(func)

    return decorator
