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
