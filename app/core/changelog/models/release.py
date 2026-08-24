# app/core/changelog/models/release.py

"""
Release Model

Represents a single released version in the generated
changelog.

A release is the highest-level unit of a changelog and
contains grouped commits together with optional metadata
used during rendering.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.core.changelog.models.commit_group import (
    CommitGroup,
)
from app.core.changelog.models.contributors import (
    ReleaseContributor,
)
from app.core.changelog.models.metadata import (
    ReleaseMetadata,
)
from app.core.changelog.models.statistics import (
    ReleaseStatistics,
)


@dataclass(slots=True)
class Release:
    """
    Represents a released version.

    Hierarchy::

        Release
            ├── CommitGroup
            │       ├── CommitScope
            │       │       ├── Commit
            │       │       └── Commit
            │       └── CommitScope
            └── CommitGroup

    Attributes:
        version:
            Version identifier.

        release_date:
            ISO-8601 release date.

        compare_url:
            Optional repository compare URL.

        status:
            Human-readable release status.

            Examples::

                Stable Release
                Beta
                Release Candidate
                Alpha
                Development

        summary:
            Optional high-level summary shown before
            the detailed changelog.

        promoted_from:
            Previous versions promoted into this release.

            Example::

                1.2.0rc1
                1.2.0rc2
                1.2.0b1

        groups:
            Commit groups organized by type.

        metadata:
            Optional release metadata.

        contributors:
            Contributors participating in this release.

        statistics:
            Optional release statistics.

        hidden:
            Do not render this release.

        title_only:
            Render only the release heading.

        custom_message:
            Replace generated content with custom text.
    """

    version: str

    release_date: str | None = None

    compare_url: str | None = None

    status: str | None = None

    summary: str | None = None

    promoted_from: list[str] = field(
        default_factory=list
    )

    groups: list[CommitGroup] = field(
        default_factory=list
    )

    metadata: ReleaseMetadata = field(
        default_factory=ReleaseMetadata
    )

    contributors: list[
        ReleaseContributor
    ] = field(
        default_factory=list
    )

    statistics: ReleaseStatistics = field(
        default_factory=ReleaseStatistics
    )

    hidden: bool = False

    title_only: bool = False

    custom_message: str | None = None


"""
Changelog
│
├── Release (v1.17.0)
│      │
│      ├── CommitGroup ("Features")
│      │       ├── Commit
│      │       └── Commit
│      │
│      ├── CommitGroup ("Bug Fixes")
│      │       ├── Commit
│      │       └── Commit
│      │
│      └── CommitGroup ("Documentation")
│              └── Commit
│
└── Release (v1.16.0)
"""
