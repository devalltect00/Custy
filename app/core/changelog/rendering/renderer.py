# app/core/changelog/rendering/renderer.py

"""
Changelog Renderer Protocol

Defines the contract implemented by changelog
renderers.
"""

from __future__ import annotations

from typing import Protocol

from app.core.changelog.models.changelog import (
    Changelog,
)


class ChangelogRenderer(Protocol):
    """
    Protocol implemented by changelog renderers.
    """

    def render(
        self,
        changelog: Changelog,
    ) -> str:
        """
        Render a changelog.

        Args:
            changelog:
                Changelog to render.

        Returns:
            Rendered markdown.
        """
        ...
