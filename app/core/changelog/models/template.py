# app/core/changelog/models/template.py

"""
Pending Commit Model

Represents the commit message that has been prepared
by the user but has not yet been committed.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class PendingCommit:
    """
    Pending commit.

    Attributes:
        message:
            Full commit message loaded from the configured
            commit message file.
    """

    message: str
