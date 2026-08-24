# app/core/changelog/models/commit.py

"""
Commit Model

Represents a parsed Git commit used during changelog
generation.

The model acts as the common data structure shared
between providers, processors, sorters, and renderers.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.core.changelog.models.commit_section import (
    CommitSection,
)


@dataclass(slots=True)
class Commit:
    """
    Parsed Git commit.

    Attributes:

        subject:
            Commit subject line.

        body:
            Commit body.

        sections:
            Structured Markdown sections extracted
            from the commit body.

        commit_type:
            Conventional Commit type.

        scope:
            Conventional Commit scope.

        breaking:
            Indicates whether the commit introduces
            a breaking change.

        commit_date:
            Commit creation date.

        hash:
            Git commit hash.
    """

    subject: str

    body: str

    commit_type: str

    scope: str | None

    breaking: bool

    commit_date: str

    hash: str

    sections: list[CommitSection] = field(
        default_factory=list,
    )
