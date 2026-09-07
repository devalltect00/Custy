# app/cli/utils/validators.py

"""Validate shared command-line values before workflow resolution.

The validators in this module provide early, actionable CLI feedback while
keeping accepted values aligned with Custy's public workflow capabilities.
"""

import re
from typing import Optional

import typer
from rich import print as rprint

from app.cli.constants import StepChoices

_VERSION_COMPONENT = r"(?:0|[1-9]\d*)"
_SUPPORTED_TAG_PATTERN = re.compile(
    rf"^v{_VERSION_COMPONENT}\.{_VERSION_COMPONENT}\.{_VERSION_COMPONENT}"
    rf"(?:"
    rf"-(?:alpha|beta|rc|dev|post)\.{_VERSION_COMPONENT}"
    rf"|(?:a|b|rc){_VERSION_COMPONENT}"
    rf"|\.(?:dev|post){_VERSION_COMPONENT}"
    rf")?"
    rf"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


def validate_tag(value: str | None) -> str | None:
    """Validate and normalize an explicit release tag.

    Args:
        value: Stable or lifecycle version supplied by a CLI tag option. The
            leading ``v`` is optional.

    Returns:
        The accepted tag with a leading ``v``, or ``None`` when no explicit
        tag was supplied.

    Raises:
        typer.BadParameter: If the value is not a supported three-component
            SemVer-style or PEP 440-style release tag.

    Notes:
        Supported lifecycle suffixes are alpha, beta, release candidate,
        development, and post release. Build/local metadata is also accepted.

    Examples:
        ``1.2.3`` becomes ``v1.2.3``. Both ``v1.2.3-rc.1`` and
        ``1.2.3rc1`` are accepted.
    """
    if value is None:
        return value

    if not value.startswith("v"):
        value = f"v{value}"

    if not _SUPPORTED_TAG_PATTERN.fullmatch(value):
        raise typer.BadParameter(
            "Tag must use a supported SemVer or PEP 440 form "
            "(e.g. v1.2.3, v1.2.3-rc.1, or 1.2.3rc1)"
        )

    return value


def validate_steps(
    value: Optional[list[StepChoices]],
) -> list[StepChoices]:
    """
    Validate step input with strong UX feedback
    """

    # -------------------------------------------------
    # ❌ No steps provided
    # -------------------------------------------------
    if not value:
        rprint("""
[bold red]❌ No steps provided[/bold red]

[dim]You need to tell custy what workflow to run.[/dim]

👉 [bold]Try one of these:[/bold]

  [yellow]custy run commit[/yellow]
  [yellow]custy run commit tag push[/yellow]
  [yellow]custy run dev[/yellow]
  [yellow]custy run release[/yellow]

💡 [bold]Tip:[/bold] Run [cyan]custy run --help[/cyan] to see all options
""")
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
        rprint("""
[bold red]❌ Invalid step combination[/bold red]

You cannot mix [yellow]preset workflows[/yellow] with [green]manual steps[/green].

👉 [bold]Choose one approach:[/bold]

[bold]Option 1 — Manual steps[/bold]
  [cyan]custy run commit tag push[/cyan]

[bold]Option 2 — Preset[/bold]
  [cyan]custy run release[/cyan]
  [cyan]custy run dev[/cyan]

[dim]Presets already include multiple steps internally.[/dim]
""")
        raise typer.Exit(code=1)

    # -------------------------------------------------
    # ❌ Duplicate steps (optional but clean UX)
    # -------------------------------------------------
    if len(step_values) != len(set(step_values)):
        rprint("""
[bold red]❌ Duplicate steps detected[/bold red]

Each step should only be used once.

👉 Example:
  [cyan]custy run commit tag push[/cyan]
""")
        raise typer.Exit(code=1)

    # -------------------------------------------------
    # 💡 Smart hint (optional UX improvement)
    # -------------------------------------------------
    if step_values == ["commit", "push"]:
        rprint("""
[dim cyan]💡 Tip:[/dim cyan] You can use [bold]dev[/bold] instead:
  custy run dev
""")

    if step_values == ["commit", "tag", "push"]:
        rprint("""
[dim cyan]💡 Tip:[/dim cyan] You can use [bold]release[/bold] instead:
  custy run release
""")

    value = [step.value for step in value]

    return value
