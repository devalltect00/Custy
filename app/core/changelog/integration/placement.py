# app/core/changelog/integration/placement.py

"""
Pending Commit Placement

Defines where the pending commit should be inserted
relative to the generated changelog.

Used by:
    - PendingCommitIntegrator
    - ConfigResolver
"""

from enum import Enum


class PendingCommitPlacement(str, Enum):
    """
    Placement strategy for the pending commit.

    BEFORE
        Insert the pending commit before the generated releases.

    AFTER
        Insert the pending commit after the generated releases.
    """

    BEFORE = "before"
    AFTER = "after"
