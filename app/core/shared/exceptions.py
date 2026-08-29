# app/core/shared/exceptions.py

"""
Shared exceptions used by Custy.

This module contains application-specific exceptions used
throughout the project.

Using dedicated exception types makes error handling,
testing, and debugging easier.
"""


class CustyError(Exception):
    """
    Base exception for Custy.

    All custom Custy exceptions should inherit from this
    exception.
    """


# =====================================================
# Git
# =====================================================


class GitOperationError(CustyError):
    """Raised when a Git operation fails with captured command diagnostics."""

    def __init__(
        self,
        message: str,
        *,
        operation: str | None = None,
        returncode: int | None = None,
        stdout: str = "",
        stderr: str = "",
    ) -> None:
        """Initialize a Git failure without discarding subprocess output."""

        super().__init__(message)
        self.operation = operation
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr

    @property
    def detail(self) -> str:
        """Return the most useful captured Git diagnostic text."""

        return (self.stderr or self.stdout or str(self)).strip()


# =====================================================
# Configuration
# =====================================================


class ConfigurationError(CustyError):
    """
    Raised when configuration is invalid.
    """


# =====================================================
# Validation
# =====================================================


class ValidationError(CustyError):
    """
    Raised when validation fails.
    """
