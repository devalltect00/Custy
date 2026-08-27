# app/core/shared/__init__.py

"""
Shared core models and utilities.
"""

from .exceptions import (
    ConfigurationError,
    CustyError,
    GitOperationError,
    ValidationError,
)
from .result import CommandResult

__all__ = [
    "CommandResult",
    "CustyError",
    "GitOperationError",
    "ConfigurationError",
    "ValidationError",
]
