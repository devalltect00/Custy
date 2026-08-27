# app/core/changelog/processing/deduplicator.py

"""
Commit Deduplicator

Provides utilities for removing duplicate parsed
commits while preserving their original order.
"""

from __future__ import annotations

import re

from app.core.changelog.models.commit import Commit


class CommitDeduplicator:
    """
    Remove duplicate parsed commits.
    """

    @classmethod
    def deduplicate(
        cls,
        commits: list[Commit],
    ) -> list[Commit]:
        """
        Remove duplicate parsed commits while preserving
        their original order.

        Args:
            commits:
                Parsed commits.

        Returns:
            Deduplicated commits.
        """

        seen: set[tuple[object, ...]] = set()

        unique: list[Commit] = []

        for commit in commits:
            key = cls._fingerprint(commit)

            if key in seen:
                continue

            seen.add(key)

            unique.append(commit)

        return unique

    @classmethod
    def _fingerprint(
        cls,
        commit: Commit,
    ) -> tuple[object, ...]:
        """
        Build a content-aware commit fingerprint.

        The commit body and semantic sections are included so
        commits sharing a subject do not lose distinct changes.

        Args:
            commit:
                Commit to fingerprint.

        Returns:
            Hashable normalized commit representation.
        """

        sections = tuple(
            (
                cls._normalize(section.title),
                tuple(cls._normalize(item) for item in section.items),
                tuple(
                    (
                        cls._normalize(subsection.title),
                        tuple(cls._normalize(item) for item in subsection.items),
                    )
                    for subsection in section.subsections
                ),
            )
            for section in commit.sections
        )

        return (
            commit.commit_type.casefold(),
            (commit.scope or "").casefold(),
            cls._normalize(commit.subject),
            cls._normalize(commit.body),
            sections,
        )

    @staticmethod
    def _normalize(value: str) -> str:
        """
        Normalize text for duplicate comparison.

        Args:
            value:
                Text to normalize.

        Returns:
            Case-folded text with collapsed whitespace.
        """

        return re.sub(r"\s+", " ", value).strip().casefold()
