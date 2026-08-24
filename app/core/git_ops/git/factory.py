# app/core/git_ops/git/factory.py

from app.core.dry_run.dry_run import Runner
from app.core.git_ops.git.executor import GitCommandExecutor
from app.core.git_ops.git.service import GitService
from app.config.config_loader import get_config
from app.cli.constants.enums import (
    StrategyChoices,
)

def create_git_service(
    dry_run: bool = False,
    no_debug: bool = False,
    strategy: StrategyChoices | None = None,
) -> GitService:
    """
    Create a fully configured Git service.

    This factory wires together the Git executor, configuration loader,
    and Git service into a ready-to-use instance.

    The factory centralizes dependency construction so callers do not need
    to know how Git services are instantiated.

    Parameters
    ----------
    dry_run:
        Enable dry-run mode.

    no_debug:
        Suppress executor debug output.

    Returns
    -------
    GitService
        Fully configured Git service instance.
    """

    """ (old)
    Factory function to create a fully wired GitService.

    Args:
        dry_run (bool): Whether to simulate commands.
        no_debug (bool): Whether to suppress debug output.

    Returns:
        GitService: Ready-to-use service instance.
    """
    # runner = Runner(is_dry_run=dry_run)
    # executor = GitCommandExecutor(dry_run=dry_run, no_debug=no_debug)
    executor = GitCommandExecutor(
        dry_run=dry_run,
        is_silent=no_debug,
    )

    config = get_config()

    return GitService(
        executor=executor,
        config=config,
        strategy=strategy,
    )
