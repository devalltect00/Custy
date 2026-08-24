# app/ui/console.py

"""
Shared Rich console instance.

This module provides the single Rich Console object used
throughout the application.

Why a shared console?
---------------------

Using a single Console instance ensures:

- Consistent styling
- Consistent terminal detection
- Consistent width calculations
- Easier testing and mocking

This console is also injected into Typer so all CLI help
screens use the same Rich configuration.

Example
-------

from app.ui.console import console

console.print("[green]Success[/green]")
"""

from rich.console import Console

from app.theme.theme import theme

console = Console(theme=theme.to_rich_theme())
