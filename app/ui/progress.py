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
