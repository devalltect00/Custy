# app/core/changelog/processing/commit_scope_grouper.py

"""
Commit Scope Grouper

Groups commits belonging to the same Conventional Commit
scope.
"""

from __future__ import annotations

from collections import OrderedDict

from app.core.changelog.models.commit import Commit
from app.core.changelog.models.commit_scope import (
    CommitScope,
)


class CommitScopeGrouper:
    """
    Group commits by Conventional Commit scope.
    """

    DEFAULT_SCOPE = "general"

    def group(
        self,
        commits: list[Commit],
    ) -> list[CommitScope]:
        """
        Group commits by scope.

        Args:
            commits:
                Parsed commits belonging to the same
                Conventional Commit type.

        Returns:
            Ordered commit scopes.
        """

        grouped: OrderedDict[
            str,
            list[Commit],
        ] = OrderedDict()

        for commit in commits:

            scope = (
                commit.scope
                or self.DEFAULT_SCOPE
            )

            grouped.setdefault(
                scope,
                [],
            ).append(commit)

        return [
            CommitScope(
                scope=scope,
                commits=commits,
            )
            for scope, commits in grouped.items()
        ]
