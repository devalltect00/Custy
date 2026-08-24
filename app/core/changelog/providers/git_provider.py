# app/core/changelog/providers/git_provider.py

"""
Git Message Provider

Collects commit messages from Git history.

This provider communicates only with ``GitService`` and
does not perform any processing or transformation.
"""

from __future__ import annotations

from app.core.changelog.providers.base import (
    MessageProvider,
)
from app.core.git_ops.git.service import GitService


class GitProvider(MessageProvider):
    """
    Collect commit messages from Git history.
    """

    def __init__(
        self,
        git_service: GitService,
    ) -> None:
        """
        Initialize the Git provider.

        Args:
            git_service:
                High-level Git service.
        """

        self.git_service = git_service

    def get_messages(
        self,
        previous_tag: str,
        current_tag: str,
        *,
        is_latest_release: bool = False,
    ) -> list[str]:
        """
        Retrieve commit messages between two Git tags.

        Args:
            previous_tag:
                Previous Git tag.

            current_tag:
                Current Git tag.

            is_latest_release:
                Unused for Git history but kept to satisfy
                the provider interface.

        Returns:
            Raw commit messages.
        """

        return self.git_service.get_commits_between(
            previous_tag,
            current_tag,
        )
