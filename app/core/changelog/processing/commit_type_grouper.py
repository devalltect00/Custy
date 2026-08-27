# app/core/changelog/processing/commit_type_grouper.py

"""
Commit Type Grouper

Groups commits into Conventional Commit types.
"""

from __future__ import annotations

from collections import OrderedDict

from app.core.changelog.models.commit import Commit
from app.core.changelog.models.commit_group import (
    CommitGroup,
)
from app.core.changelog.processing.commit_scope_grouper import (
    CommitScopeGrouper,
)


class CommitTypeGrouper:
    """
    Group commits by Conventional Commit type.
    """

    def __init__(self) -> None:
        """
        Initialize the commit type grouper.
        """

        self.scope_grouper = CommitScopeGrouper()

    def group(
        self,
        commits: list[Commit],
    ) -> list[CommitGroup]:
        """
        Group commits by Conventional Commit type.

        Args:
            commits:
                Parsed commits.

        Returns:
            Ordered commit groups.
        """

        grouped: OrderedDict[
            str,
            list[Commit],
        ] = OrderedDict()

        for commit in commits:
            grouped.setdefault(
                commit.commit_type,
                [],
            ).append(commit)

        return [
            CommitGroup(
                commit_type=commit_type,
                scopes=self.scope_grouper.group(grouped_commits),
            )
            for commit_type, grouped_commits in grouped.items()
        ]
