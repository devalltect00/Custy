# app/cli/error_handler.py

"""Top-level Custy CLI exception boundary."""

from __future__ import annotations

import logging
import sys
from collections.abc import Callable
from typing import Any

from app.core.exceptions.validation_error import (
    ValidationError as WorkflowValidationError,
)
from app.core.shared import CustyError
from app.errors.validation import ValidationError as LegacyValidationError
from app.ui.exceptions import show_error, show_structured_error

logger = logging.getLogger(__name__)


def _debug_requested() -> bool:
    """Return whether the current CLI invocation explicitly enabled debug."""

    return "--debug" in sys.argv


def handle_cli_errors(callback: Callable[[], Any]) -> Any:
    """Execute the CLI and present uncaught failures consistently.

    Known validation and Custy errors are rendered without a Python traceback.
    Unexpected exceptions are also summarized in normal mode; ``--debug``
    preserves the original traceback for diagnosis.

    Args:
        callback: Zero-argument function that imports and invokes the Typer app.

    Returns:
        Callback result.

    Raises:
        SystemExit: With a non-zero status after presenting an error.
        Exception: The original unexpected exception in debug mode.
    """

    try:
        return callback()
    except SystemExit, KeyboardInterrupt:
        raise
    except WorkflowValidationError as exc:
        logger.debug("Custy validation failed: %s", exc)
        show_structured_error(exc)
        raise SystemExit(exc.exit_code) from None
    except LegacyValidationError as exc:
        logger.debug("Legacy Custy validation failed: %s", exc)
        message = exc.message
        if exc.hint:
            message += f"\n\nHint: {exc.hint}"
        show_error(message)
        raise SystemExit(1) from None
    except CustyError as exc:
        logger.debug("Custy operation failed: %s", exc)
        show_error(str(exc))
        raise SystemExit(1) from None
    except Exception as exc:
        if _debug_requested():
            raise

        logger.error("Unexpected Custy failure: %s", exc)
        show_error(
            "Custy could not complete the command.\n\n"
            f"Details: {exc}\n\n"
            "Hint: rerun the command with --debug for a detailed traceback."
        )
        raise SystemExit(1) from None
