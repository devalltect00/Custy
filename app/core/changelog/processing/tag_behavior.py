# app/core/changelog/processing/tag_behavior.py

"""
Release Behavior Processor

Applies configured rendering behavior to generated
changelogs.
"""

from __future__ import annotations

from app.core.changelog.config.models import (
    ReleaseBehaviorConfig,
)
from app.core.changelog.models.changelog import (
    Changelog,
)


class ReleaseBehaviorProcessor:
    """
    Apply configured rendering behavior to releases
    contained in a changelog.
    """

    def __init__(
        self,
        config: ReleaseBehaviorConfig,
    ) -> None:
        """
        Initialize the release behavior processor.

        Args:
            config:
                Release behavior configuration.
        """

        self.config = config

    def apply(
        self,
        changelog: Changelog,
    ) -> Changelog:
        """
        Apply configured behavior to every release in the
        changelog.

        Args:
            changelog:
                Changelog to update.

        Returns:
            Updated changelog.
        """

        for release in changelog.releases:
            behavior = self.config.behavior.get(
                release.version,
            )

            if behavior is None:
                continue

            release.hidden = behavior.hidden

            release.title_only = behavior.title_only

            release.custom_message = behavior.custom_message

        return changelog
