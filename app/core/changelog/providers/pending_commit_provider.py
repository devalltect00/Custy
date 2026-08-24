# app/core/changelog/providers/pending_commit_provider.py

"""
Pending Commit Provider

Loads the pending commit message from the configured
commit message file.

The pending commit represents the next commit that has
not yet been committed into Git.
"""

from __future__ import annotations

from collections.abc import Callable

from app.core.changelog.providers.base import (
    MessageProvider,
)


class PendingCommitProvider(MessageProvider):
    """
    Load the pending commit message.
    """

    def __init__(
        self,
        loader: Callable[[], str],
    ) -> None:
        """
        Initialize the provider.

        Args:
            loader:
                Callable responsible for loading the pending
                commit message.
        """

        self.loader = loader

    def get_messages(
        self,
        previous_tag: str,
        current_tag: str,
        *,
        is_latest_release: bool = False,
    ) -> list[str]:
        """
        Load the pending commit.

        The pending commit is included only when generating
        the latest release.

        Returns:
            A single pending commit message or an empty list.
        """

        if not is_latest_release:
            return []

        message = self.loader().strip()

        if not message:
            return []

        return [message]
