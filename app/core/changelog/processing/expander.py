# app/core/changelog/processing/expander.py

"""
Commit Expander

Expand parsed commits into one or more changelog
entries.

Version announcement commits may expand into
multiple changelog entries.
"""

from __future__ import annotations

import re

from app.core.changelog.models.commit import (
    Commit,
)


_VERSION_PATTERN = re.compile(
    r"""
    ^
    \d+
    (?:\.\d+)+
    (?:
        a\d+
        |b\d+
        |rc\d+
        |post\d+
        |dev\d+
    )?
    $
    """,
    re.VERBOSE,
)


class CommitExpander:
    """
    Expand parsed commits.

    Responsibilities:

    - Preserve ordinary commits.
    - Expand version announcement commits.
    """

    def expand(
        self,
        commits: list[Commit],
    ) -> list[Commit]:
        """
        Expand commits.

        Args:
            commits:
                Parsed commits.

        Returns:
            Expanded commits.
        """

        expanded: list[Commit] = []

        for commit in commits:

            if self._should_expand(
                commit,
            ):

                expanded.extend(
                    self._expand_commit(
                        commit,
                    )
                )

            else:

                expanded.append(
                    commit,
                )

        return expanded

    def _should_expand(
        self,
        commit: Commit,
    ) -> bool:
        """
        Determine whether the commit should
        expand into multiple changelog entries.
        """

        if not commit.body.strip():
            return False

        return bool(
            _VERSION_PATTERN.fullmatch(
                commit.subject.strip(),
            )
        )

    def _expand_commit(
        self,
        commit: Commit,
    ) -> list[Commit]:
        """
        Expand a version commit.
        """

        entries = self._extract_entries(
            commit.body,
        )

        if not entries:
            return [commit]

        return [
            self._clone_commit(
                original=commit,
                subject=entry,
            )
            for entry in entries
        ]

    @staticmethod
    def _extract_entries(
        body: str,
    ) -> list[str]:
        """
        Extract individual changelog entries.
        """

        entries: list[str] = []

        for line in body.splitlines():

            line = line.strip()

            if not line:
                continue

            if line.startswith("- "):
                line = line[2:].strip()

            if not line:
                continue

            entries.append(
                line,
            )

        return entries

    @staticmethod
    def _clone_commit(
        *,
        original: Commit,
        subject: str,
    ) -> Commit:
        """
        Clone a commit while preserving
        metadata.
        """

        return Commit(
            subject=subject,
            body="",
            commit_type=original.commit_type,
            scope=original.scope,
            breaking=original.breaking,
            commit_date=original.commit_date,
            hash=original.hash,
        )
