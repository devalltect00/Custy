# app/core/decorators/log_decorators.py

import logging
from functools import wraps

logger = logging.getLogger(__name__)

def log_execution(func):
    """
    Decorator for logging function execution lifecycle.

    Logs:
    - START before function execution
    - END after successful execution
    - ERROR if exception occurs

    Args:
        func (Callable): Function to wrap.

    Returns:
        Callable: Wrapped function.
    """
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__

        # print("logger.level",logger.getEffectiveLevel())

        # logger.debug(f"\n[cyan]▶ COMMAND START[/cyan] | [dim]{func_name}[/dim]")
        logger.debug(f"[cyan]▶ COMMAND START[/cyan] | [dim]{func_name}[/dim]")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"[green]✔ COMMAND END[/green] | [dim]{func_name}[/dim]")
            return result
        except Exception as e:
            logger.exception(
                f"[red]✖ COMMAND ERROR[/red] | [dim]{func_name}[/dim]\n"
                f"[red]{e}[/red]"
            )
            raise
    return wrapper
