# app/core/cleanup/branch/exceptions.py

"""
Branch cleanup exceptions.

This module defines domain-specific exceptions used by the branch
cleanup workflow.

Using dedicated exception types makes it easier to distinguish cleanup
failures from lower-level Git or infrastructure errors while keeping
the service implementation expressive and testable.
"""


class BranchCleanupError(Exception):
    """
    Base exception for branch cleanup operations.

    All cleanup-specific exceptions inherit from this class so callers
    can catch every cleanup-related failure using a single exception
    type when appropriate.
    """


class BranchDeletionError(BranchCleanupError):
    """
    Raised when a branch cannot be deleted.

    This exception represents failures encountered while deleting
    either a local or remote Git branch.
    """


class ProtectedBranchError(BranchCleanupError):
    """
    Raised when attempting to delete a protected branch.

    Protected branches are branches that must never be removed by the
    cleanup workflow, such as:

    - main
    - master
    - develop
    """
