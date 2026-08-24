# app/core/changelog/integration/generation.py

"""
Pending Commit Generation Strategy

Defines how the pending commit should be incorporated into
the generated changelog.

Used by:
    - ChangelogConfigResolver
    - ChangelogGenerator
    - PendingCommitIntegrator
"""

from enum import Enum


class PendingCommitGeneration(str, Enum):
    """
    Generation strategy for pending commit integration.

    APPEND
        Preserve the existing release ordering and insert
        the pending commit according to the configured
        placement.

    REGENERATE
        Regenerate the changelog from the complete commit
        history before inserting the pending commit.
    """

    APPEND = "append"

    REGENERATE = "regenerate"
