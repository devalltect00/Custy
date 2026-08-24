# app/ui/panels.py

"""
Reusable Rich panel helpers.

Panels provide visually distinct output sections
for:

- success messages
- warnings
- errors
- informational messages
"""

from rich.panel import Panel


def success_panel(
    message: str,
) -> Panel:
    """
    Create success panel.
    """

    return Panel.fit(
        message,
        title="Success",
        border_style="green",
    )


def success_summary_panel(
    *,
    message: str,
    elapsed_time: float,
) -> Panel:
    """
    Create success panel including execution time.
    """

    return Panel.fit(
        (f"{message}\n\nCompleted in {elapsed_time:.2f} seconds"),
        title="Success",
        border_style="green",
    )


def info_panel(
    message: str,
) -> Panel:
    """
    Create informational panel.
    """

    return Panel.fit(
        message,
        title="Info",
        border_style="cyan",
    )


def warning_panel(
    message: str,
) -> Panel:
    """
    Create warning panel.
    """

    return Panel.fit(
        message,
        title="Warning",
        border_style="yellow",
    )


def error_panel(
    message: str,
) -> Panel:
    """
    Create error panel.
    """

    return Panel.fit(
        message,
        title="Error",
        border_style="red",
    )


def summary_panel(
    *,
    title: str,
    message: str,
) -> Panel:
    """
    Create summary panel.

    Args:
        title (str):
            Panel title.

        message (str):
            Panel content.

    Returns:
        Panel
    """
    return Panel.fit(
        message,
        title=title,
        border_style="blue",
    )
