# app/core/exceptions/validation_error.py

"""
validation_error.py

Defines the ValidationError class used across the workflow engine.

This module provides a structured, Rich-renderable exception designed for:
- CLI applications
- workflow validation pipelines
- consistent error reporting across services

Key features:
- Rich-based formatted output (Panel UI)
- structured metadata (code, hint, context)
- CLI-friendly display via `.show()`
- machine-friendly export via `.to_dict()`

Usage:
    raise ValidationError(
        message="No staged changes to commit.",
        hint="Use `git add .`",
        code="NO_STAGED_CHANGES"
    )
"""

from dataclasses import dataclass
from typing import Any, Optional

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


@dataclass
class ValidationError(Exception):
    """
    Domain-level validation error for workflow execution.

    This exception is designed to be:
    - Human-readable (via Rich rendering)
    - Machine-readable (via structured fields)
    - CLI-friendly (via `.show()`)

    Attributes:
        message (str):
            Primary error description. This should clearly explain
            what went wrong.

        hint (Optional[str]):
            Actionable suggestion for the user to resolve the issue.

        code (Optional[str]):
            Optional error code for categorization, debugging,
            or telemetry (e.g., "NO_STAGED_CHANGES").

        exit_code (int):
            Process exit code used when terminating CLI execution.

        context (Optional[Dict[str, Any]]):
            Additional debugging or contextual information.
            Useful for logging, tracing, or advanced CLI output.
    """

    message: str
    hint: Optional[str] = None
    code: Optional[str] = None
    exit_code: int = 1
    context: Optional[dict[str, Any]] = None

    # =========================================================
    # Core Behavior
    # =========================================================
    def __str__(self) -> str:
        """
        Return the plain error message.

        This is used when:
        - printing the exception directly
        - logging systems fallback to string conversion

        Returns:
            str: The main error message.
        """
        return self.message

    # =========================================================
    # Rich Rendering
    # =========================================================
    def render(self) -> Panel:
        """
        Build a Rich Panel representation of the error.

        This method constructs a visually structured error block
        suitable for CLI display.

        Layout:
            - Title: "Validation Error"
            - Body:
                - main message (bold red)
                - optional code (yellow)
                - optional hint (cyan)
                - optional context (dim/magenta)

        Returns:
            Panel: Rich Panel object ready for rendering.
        """

        content = []

        # Main message
        content.append(Text(self.message, style="bold red"))

        # Error code (optional)
        if self.code:
            content.append(Text(f"\nCode: {self.code}", style="yellow"))

        # Hint (optional)
        if self.hint:
            content.append(Text(f"\nHint: {self.hint}", style="cyan"))

        # Context (optional debug info)
        if self.context:
            content.append(Text("\nContext:", style="magenta"))

            for key, value in self.context.items():
                content.append(Text(f"  • {key}: {value}", style="dim"))

        body = Text("\n").join(content)

        return Panel(
            body,
            title="❌ Validation Error",
            border_style="red",
            expand=False,
        )

    def show(self) -> None:
        """
        Render and print the error using Rich.

        This is the recommended method for CLI output.

        Example:
            try:
                ...
            except ValidationError as e:
                e.show()

        Side Effects:
            Prints formatted output to terminal.
        """
        console.print(self.render())

    # =========================================================
    # Serialization
    # =========================================================
    def to_dict(self) -> dict[str, Any]:
        """
        Convert the error into a structured dictionary.

        Useful for:
        - logging systems
        - JSON output (API / telemetry)
        - debugging tools

        Returns:
            dict: Structured representation of the error.
        """
        return {
            "message": self.message,
            "hint": self.hint,
            "code": self.code,
            "exit_code": self.exit_code,
            "context": self.context or {},
        }
