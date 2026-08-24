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
    """
    Raised when a Git operation fails.
    """


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
