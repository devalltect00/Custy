# app/core/changelog/models/metadata.py

"""
Release Metadata Model

Represents structured metadata associated with a release.

Metadata is optional information that helps classify a
release but is not part of the actual changelog content.

Examples:
    Release Type:
        Stable
        Beta
        Release Candidate

    Scope:
        Workflow

    Classification:
        Release
        Documentation

    Tags:
        workflow
        docs
        stable
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ReleaseMetadata:
    """
    Metadata describing a release.

    Attributes:
        release_type:
            Human-readable release type.

            Examples::

                Stable
                Beta
                Release Candidate
                Alpha
                Development
                Post Release

        scope:
            Primary scope of the release.

            Examples::

                Workflow
                CLI
                Core
                Parser

        classifications:
            High-level classifications used by the
            generated changelog.

            Examples::

                Release
                Documentation
                Refactoring
                Security

        tags:
            Clean tags extracted from the commit message.

            NOTE:
                These are NOT Git tags.

                Example::

                    workflow
                    docs
                    stable
                    template
        """

    release_type: str | None = None

    scope: str | None = None

    classifications: list[str] = field(
        default_factory=list
    )

    tags: dict[str, list[str]] = field(
        default_factory=dict
    )
