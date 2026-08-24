# app/cli/utils/validators.py

import re
import typer

from typing import List, Optional
from rich import print as rprint

from app.cli.constants import StepChoices

def validate_tag(value: str | None) -> str | None:
    if value is None:
        return value

    # Normalize: add "v" prefix if missing
    if not value.startswith("v"):
        value = f"v{value}"

    # Simple semver check (you can extend later)
    pattern = r"^v\d+\.\d+\.\d+$"
    if not re.match(pattern, value):
        raise typer.BadParameter(
            "Tag must follow format vX.Y.Z (e.g. v1.2.3)"
        )

    return value

def validate_steps(
    value: Optional[List[StepChoices]],
) -> List[StepChoices]:
    """
    Validate step input with strong UX feedback
    """

    # -------------------------------------------------
    # ❌ No steps provided
    # -------------------------------------------------
    if not value:
        rprint(
            """
[bold red]❌ No steps provided[/bold red]

[dim]You need to tell custy what workflow to run.[/dim]

👉 [bold]Try one of these:[/bold]

  [yellow]custy run commit[/yellow]
  [yellow]custy run commit tag push[/yellow]
  [yellow]custy run dev[/yellow]
  [yellow]custy run release[/yellow]

💡 [bold]Tip:[/bold] Run [cyan]custy run --help[/cyan] to see all options
"""
        )
        raise typer.Exit(code=1)

    # -------------------------------------------------
    # Normalize (convert enum → string)
    # -------------------------------------------------
    step_values = [step.value for step in value]

    core_steps = {"commit", "tag", "push"}
    presets = {"dev", "release", "all"}

    selected_core = core_steps.intersection(step_values)
    selected_presets = presets.intersection(step_values)

    # -------------------------------------------------
    # ❌ Mixing preset + manual steps
    # -------------------------------------------------
    if selected_core and selected_presets:
        rprint(
            f"""
[bold red]❌ Invalid step combination[/bold red]

You cannot mix [yellow]preset workflows[/yellow] with [green]manual steps[/green].

👉 [bold]Choose one approach:[/bold]

[bold]Option 1 — Manual steps[/bold]
  [cyan]custy run commit tag push[/cyan]

[bold]Option 2 — Preset[/bold]
  [cyan]custy run release[/cyan]
  [cyan]custy run dev[/cyan]

[dim]Presets already include multiple steps internally.[/dim]
"""
        )
        raise typer.Exit(code=1)

    # -------------------------------------------------
    # ❌ Duplicate steps (optional but clean UX)
    # -------------------------------------------------
    if len(step_values) != len(set(step_values)):
        rprint(
            """
[bold red]❌ Duplicate steps detected[/bold red]

Each step should only be used once.

👉 Example:
  [cyan]custy run commit tag push[/cyan]
"""
        )
        raise typer.Exit(code=1)

    # -------------------------------------------------
    # 💡 Smart hint (optional UX improvement)
    # -------------------------------------------------
    if step_values == ["commit", "push"]:
        rprint(
            """
[dim cyan]💡 Tip:[/dim cyan] You can use [bold]dev[/bold] instead:
  custy run dev
"""
        )

    if step_values == ["commit", "tag", "push"]:
        rprint(
            """
[dim cyan]💡 Tip:[/dim cyan] You can use [bold]release[/bold] instead:
  custy run release
"""
        )

    value = [step.value for step in value]

    return value
