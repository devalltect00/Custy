# app/core/changelog/models/commit_subsection.py

"""
Commit Subsection Model

Represents a Markdown subsection extracted
from a structured commit message.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class CommitSubsection:
    """
    Structured subsection inside a commit section.
    """

    title: str

    items: list[str] = field(
        default_factory=list,
    )
