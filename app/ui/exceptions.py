# app/ui/exceptions.py

"""
Exception and error presentation helpers.

This module centralizes how runtime errors are displayed
to the user.

Responsibilities
----------------

- Display user-friendly error panels
- Hide implementation details from normal users
- Keep error rendering consistent across commands

Examples
--------

show_error(
    "Failed to generate documentation."
)

show_error(
    "Target directory does not exist."
)
"""

from typing import Protocol

from rich.console import RenderableType
from rich.traceback import install

from app.ui.console import console
from app.ui.panels import error_panel

#
# Enable Rich tracebacks globally.
#
install(
    show_locals=False,
)


def show_error(
    message: str,
) -> None:
    """
    Display error message using a Rich panel.

    Parameters
    ----------
    message:
        Human-readable error message.
    """

    console.print(error_panel(message))


class StructuredError(Protocol):
    """Protocol for exceptions that provide their own Rich rendering."""

    def render(self) -> RenderableType:
        """Build the Rich representation for the exception."""


def show_structured_error(error: StructuredError) -> None:
    """Display a structured exception through Custy's shared console.

    Args:
        error: Exception-like object exposing a Rich ``render`` method.
    """

    console.print(error.render())
