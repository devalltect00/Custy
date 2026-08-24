# app/core/changelog/models/commit_section.py

"""
Commit Section Model

Represents a logical Markdown section extracted
from a structured commit message.
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from app.core.changelog.models.commit_subsection import (
    CommitSubsection,
)


@dataclass(slots=True)
class CommitSection:
    """
    Structured section inside a commit.

    A section may contain:

    • Items directly under the section.

    • Zero or more subsections.

    Example
    -------

    ### Bug Fixes

    - Fix A

    #### Workflow

    - Fix B

    #### Validation

    - Fix C

    =====

    Another example::

        ### 🐛 Fixes

        - Fix A
        - Fix B

    becomes

        title = "🐛 Fixes"

        items = [
            "Fix A",
            "Fix B",
        ]
    """

    title: str

    #
    # Items belonging directly to this section.
    #
    items: list[str] = field(
        default_factory=list,
    )

    #
    # Child subsections.
    #
    subsections: list[
        CommitSubsection
    ] = field(
        default_factory=list,
    )
