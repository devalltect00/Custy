# app/core/changelog/integration/pending_commit_integrator.py

"""
Pending Commit Integrator

Integrates the pending release into an existing
changelog according to the configured generation and
placement strategies.
"""

from __future__ import annotations

from app.core.changelog.integration.generation import (
    PendingCommitGeneration,
)
from app.core.changelog.integration.placement import (
    PendingCommitPlacement,
)
from app.core.changelog.models.changelog import (
    Changelog,
)
from app.core.changelog.models.release import (
    Release,
)


class PendingCommitIntegrator:
    """
    Integrate the pending release into a changelog.
    """

    def __init__(
        self,
        *,
        generation: PendingCommitGeneration,
        placement: PendingCommitPlacement,
    ) -> None:
        """
        Initialize the integrator.

        Args:
            generation:
                Pending commit generation strategy.

            placement:
                Pending commit placement strategy.
        """

        self.generation = generation

        self.placement = placement

    def integrate(
        self,
        changelog: Changelog,
        pending_release: Release | None,
    ) -> Changelog:
        """
        Integrate the pending release.

        Args:
            changelog:
                Existing changelog.

            pending_release:
                Pending release generated from the
                pending commit.

        Returns:
            Updated changelog.
        """

        if pending_release is None:
            return changelog

        if (
            self.generation
            is PendingCommitGeneration.APPEND
        ):
            return self._append(
                changelog,
                pending_release,
            )

        return self._regenerate(
            changelog,
            pending_release,
        )

    def _append(
        self,
        changelog: Changelog,
        pending_release: Release,
    ) -> Changelog:
        """
        Append the pending release.
        """

        releases = list(
            changelog.releases
        )

        if (
            self.placement
            is PendingCommitPlacement.BEFORE
        ):
            releases.insert(
                0,
                pending_release,
            )

        else:
            releases.append(
                pending_release,
            )

        return Changelog(
            releases=releases,
        )

    def _regenerate(
        self,
        changelog: Changelog,
        pending_release: Release,
    ) -> Changelog:
        """
        Regenerate the changelog.

        Placeholder implementation.

        Full regeneration logic will be implemented
        when the generator orchestration is completed.
        """

        return self._append(
            changelog,
            pending_release,
        )
