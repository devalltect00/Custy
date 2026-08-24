# app/core/changelog/models/commit_group.py

"""
Commit Group Model

Represents a collection of commit scopes that belong to
the same Conventional Commit type.

Examples:
    - feat
    - fix
    - docs
    - refactor
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.core.changelog.models.commit_scope import (
    CommitScope,
)


@dataclass(slots=True)
class CommitGroup:
    """
    Group of commit scopes sharing the same Conventional
    Commit type.

    Attributes:
        commit_type:
            Conventional Commit type represented by this
            group (for example: ``feat``, ``fix``,
            ``docs``).

        scopes:
            Ordered commit scopes belonging to this
            commit type.
    """

    commit_type: str

    scopes: list[CommitScope] = field(
        default_factory=list
    )
