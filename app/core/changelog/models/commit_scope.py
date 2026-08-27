# app/core/changelog/models/commit_scope.py

"""
Commit Scope Model

Represents a collection of commits belonging to the same
Conventional Commit scope within a commit group.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.core.changelog.models.commit import Commit


@dataclass(slots=True)
class CommitScope:
    """
    Collection of commits sharing the same Conventional
    Commit scope.

    Attributes:
        scope:
            Conventional Commit scope.

        commits:
            Parsed commits belonging to this scope.
    """

    scope: str

    commits: list[Commit] = field(default_factory=list)
