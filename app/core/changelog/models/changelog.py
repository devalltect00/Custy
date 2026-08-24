# app/core/changelog/models/changelog.py

"""
Changelog Model

Represents the complete changelog that will be rendered
into ``CHANGELOG.md``.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.core.changelog.models.release import Release


@dataclass(slots=True)
class Changelog:
    """
    Complete changelog.

    Attributes:
        releases:
            Ordered releases to render.
    """

    releases: list[Release] = field(
        default_factory=list
    )
