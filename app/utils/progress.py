# app/utils/progress.py

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from app.ui.console import console
from app.errors.validation import ValidationError
from app.cli.context.app_context import get_context

def run_steps(ctx: typer.Context, title: str, steps: list[tuple[str, callable]], visible=True):
    app_ctx = get_context(ctx=ctx)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        console=console,
    ) as progress:

        task = progress.add_task(f"[progress.title]{title}[/progress.title]", total=len(steps), visible=visible)

        for desc, func in steps:
            progress.update(task, description=f"[progress.step]{desc}[/progress.step]")
            try:
                func()
            except ValidationError as e:
                progress.stop()

                if app_ctx.debug:
                    raise  # full traceback

                console.print(f"[error]✖ {desc}[/error]")
                console.print(f"[error]{e}[/error]")

                if e.hint:
                    console.print(f"[warning]💡 {e.hint}[/warning]")

                raise typer.Exit(code=1)
            except Exception as e:
                progress.stop()

                if app_ctx.debug:
                    raise  # full traceback

                console.print(f"[error]Unexpected error: {e}")
                # raise
                raise typer.Exit(code=1)
            progress.advance(task)

        progress.console.print(f"[success]✔ {title} completed![/success]")



def run_steps_by_show_all_tasks(ctx: typer.Context, title: str, steps: list[tuple[str, callable]]):
    app_ctx = get_context(ctx)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        console=console,
    ) as progress:
        tasks = []

        for desc, func in steps:
            task = progress.add_task(f"[progress.step]{desc}[/progress.step]", total=1, visible=False)
            tasks.append(task)

        for (desc, func), task_id in zip(steps, tasks):
            try:
                progress.update(task_id, description=f"[progress.step]{desc}[/progress.step]", visible=True)
                func()
                progress.update(task_id, advance=1)
            except ValidationError as e:
                progress.stop()

                if app_ctx.debug:
                    raise  # full traceback

                console.print(f"[error]✖ {desc}[/error]")
                console.print(f"[error]{e}[/error]")

                if e.hint:
                    console.print(f"[warning]💡 {e.hint}[/warning]")

                raise typer.Exit(code=1)
            except Exception as e:
                progress.stop()

                if app_ctx.debug:
                    raise  # full traceback

                console.print(f"[error]Unexpected error: {e}")
                # raise
                raise typer.Exit(code=1)
            # progress.advance(task)

        progress.console.print(f"[success]✔ {title} completed![/success]")
