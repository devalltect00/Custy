# app/utils/cli_formatter.py
"""
Custom argparse formatter that adds color to CLI help output.

This formatter uses `colorama` to add ANSI color codes to the argparse help screen,
enhancing readability without altering the actual structure of the help output.

The output will:
- Add green left borders (`|`) and cyan right borders (`|`) around each line.
- Automatically reset color after each line using `autoreset=True`.

Example usage in an ArgumentParser:

    parser = argparse.ArgumentParser(
        description="My CLI Tool",
        formatter_class=ColoredHelpFormatter,
    )

Place this in `app/utils/cli_formatter.py` and import where needed.
"""

import argparse
from argparse import Action

from colorama import Fore, Style
from colorama import init as colorama_init

colorama_init(autoreset=True)


class ColoredHelpFormatter(argparse.HelpFormatter):
    """
    Custom HelpFormatter that wraps each help line in colored borders.

    - Left border: green `|`
    - Right border: cyan `|`
    - All colors are reset after each line to avoid bleed.

    This subclass overrides:
    - `format_help()` for the overall help output
    - `_format_action()` for formatting each subcommand or argument line
    """

    def _format_action(self, action: Action) -> str:
        """
        Format an individual action (argument or subcommand) line with color borders.

        Args:
            action (argparse.Action): The argparse action being formatted.

        Returns:
            str: Colored and bordered action help line.

        """
        parts = super()._format_action(action).splitlines()
        return (
            "\n".join(
                f"{Fore.GREEN}| {line} {Fore.CYAN}|{Style.RESET_ALL}" for line in parts
            )
            + "\n"
        )

    def format_help(self) -> str:
        """
        Format the full help message with color borders.

        Returns:
            str: Entire help message with each line bordered in color.

        """
        help_text = super().format_help().splitlines()
        return (
            "\n".join(
                f"{Fore.GREEN}| {line} {Fore.CYAN}|{Style.RESET_ALL}"
                for line in help_text
            )
            + "\n"
        )
