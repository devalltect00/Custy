# app/core/changelog/models/statistics.py

"""
Release Statistics Model

Represents optional release statistics that may be
displayed in the generated changelog.

Statistics are intended to summarize repository activity
for a release and are independent from the actual
changelog content.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ReleaseStatistics:
    """
    Release statistics.

    Attributes:
        commit_count:
            Number of commits included in the release.

        files_changed:
            Total number of modified files.

        insertions:
            Total inserted lines.

        deletions:
            Total deleted lines.
    """

    commit_count: int = 0

    files_changed: int = 0

    insertions: int = 0

    deletions: int = 0
