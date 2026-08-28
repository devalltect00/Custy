# app/ui/progress.py

"""
Progress utilities.

Provides reusable Rich progress indicators for long-running
operations such as:

- scanning repositories
- generating markdown
- writing files
- analyzing repositories
- tag conversion
- docker image publishing
"""

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass

from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskID,
    TextColumn,
    TimeElapsedColumn,
)

from app.ui.console import console


@dataclass(slots=True)
class ProgressTask:
    """Control one task displayed by a shared Rich progress instance.

    Attributes:
        progress:
            Rich progress instance that owns the task.

        task_id:
            Identifier of the task being controlled.

        description:
            Stable description used for the completion message.
    """

    progress: Progress
    task_id: TaskID
    description: str

    def update(self, description: str) -> None:
        """Update the current task description without advancing it.

        Args:
            description:
                User-facing description of the current operation.
        """

        self.progress.update(
            self.task_id,
            description=description,
        )

    def advance(self, amount: int = 1) -> None:
        """Advance the task by a completed unit of work.

        Args:
            amount:
                Number of completed units to add.
        """

        self.progress.advance(self.task_id, amount)


def create_progress() -> Progress:
    """
    Create standard application progress bar.

    Returns:
        Progress:
            Configured Rich progress instance.

    Example:
        with create_progress() as progress:
            task = progress.add_task(
                "Processing...",
                total=100,
            )
    """
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        console=console,
    )


@contextmanager
def suspend_progress(
    progress: Progress,
    task_id: TaskID,
    *,
    restore_visible: bool = True,
) -> Iterator[None]:
    """Temporarily release the terminal from a live progress display.

    Description:
        Hide the current task and stop Rich's live refresh loop while an
        interactive subprocess, such as Nano, Micro, or Vim, owns the
        terminal.

    Logic:
        The task is hidden and the display is refreshed before progress is
        stopped. After the caller finishes, the original visibility is
        restored and live progress starts again.

    Args:
        progress:
            Active Rich progress instance to suspend.

        task_id:
            Identifier of the task whose rendered row must be hidden.

        restore_visible:
            Visibility to restore after the interactive operation finishes.

    Yields:
        Control while the progress display is stopped.

    Notes:
        Restoration happens even when the interactive operation raises an
        exception, allowing the pipeline's normal error presentation to take
        over without leaving a live-refresh thread behind.

    Examples:
        with suspend_progress(progress, task_id):
            open_terminal_editor()
    """

    progress.update(task_id, visible=False)
    progress.refresh()
    progress.stop()

    try:
        yield
    finally:
        progress.update(task_id, visible=restore_visible)
        progress.start()
        progress.refresh()


@contextmanager
def progress_task(
    description: str,
    *,
    total: int,
) -> Iterator[ProgressTask]:
    """Display and control a determinate application progress task.

    Args:
        description:
            Stable description for the overall operation.

        total:
            Number of work units expected to complete.

    Yields:
        A task controller that can update the visible description and
        advance the progress counter.

    Notes:
        Successful operations finish with a checked description. When
        an exception escapes the context, Rich closes the live display
        normally and the original exception remains unchanged.

    Example:
        with progress_task("Generating changelog", total=2) as task:
            task.update("Processing Unreleased changes")
            task.advance()
            task.update("Processing v1.0.0")
            task.advance()
    """

    with create_progress() as progress:
        task_id = progress.add_task(
            description=description,
            total=total,
        )
        task = ProgressTask(
            progress=progress,
            task_id=task_id,
            description=description,
        )

        yield task

        progress.update(
            task_id,
            completed=total,
            description=f"{description} ✔",
        )


@contextmanager
def progress_spinner(
    message: str,
):
    """
    Display a temporary spinner.

    Parameters
    ----------
    message:
        Description displayed beside the spinner.

    Example
    -------

    with progress_spinner("Scanning repository"):
        scan()

    with progress_spinner("Generating markdown"):
        build_document()

    Notes
    -----
    The progress indicator automatically disappears when
    the operation completes.
    """

    progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=console,
    )

    with progress:
        task = progress.add_task(
            description=message,
            total=None,
        )

        yield

        progress.update(
            task,
            description=f"{message} ✔",
        )
