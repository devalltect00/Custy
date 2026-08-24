# app/core/pipeline/progress.py

from contextlib import contextmanager
from rich.progress import Progress, SpinnerColumn, TextColumn

@contextmanager
def step_progress(description: str):
    """
    Lightweight transient progress for step-level operations.
    Appears at bottom and disappears after completion.
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[cyan]{task.description}"),
        transient=True,   # 👈 key
    ) as progress:
        task = progress.add_task(description, total=None)
        yield progress
        progress.update(task, completed=1)
