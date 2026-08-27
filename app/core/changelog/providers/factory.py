# app/core/changelog/providers/factory.py

"""
Message Provider Factory

Creates the collection of message providers used during
changelog generation.
"""

from __future__ import annotations

from app.core.changelog.config.models import (
    ChangelogConfig,
)
from app.core.changelog.providers.base import (
    MessageProvider,
)
from app.core.changelog.providers.git_provider import (
    GitProvider,
)
from app.core.changelog.providers.pending_commit_provider import (
    PendingCommitProvider,
)
from app.core.git_ops.git.service import GitService


class MessageProviderFactory:
    """
    Factory responsible for constructing the message
    providers used during changelog generation.
    """

    @staticmethod
    def create(
        *,
        git_service: GitService,
        config: ChangelogConfig,
        pending_commit_loader,
    ) -> list[MessageProvider]:
        """
        Build the configured message providers.
        """

        providers: list[MessageProvider] = [GitProvider(git_service)]

        if config.pending_commit.enabled:
            providers.append(
                PendingCommitProvider(
                    loader=pending_commit_loader,
                )
            )

        return providers
