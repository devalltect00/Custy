# app/core/changelog/models/contributors.py

"""
Release Contributor Model

Represents a contributor that participated in a release.

Contributors are optional and are intended for
CHANGELOG rendering only.

They are typically collected from Git history,
but may also be provided through configuration
or future integrations.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ReleaseContributor:
    """
    Contributor information.

    Attributes:
        name:
            Display name.

        email:
            Contributor email.

            Optional because some projects may
            choose not to expose emails.

        profile:
            Optional profile URL.

            Examples::

                https://github.com/devalltect00

                https://gitlab.com/devalltect00

        commit_count:
            Number of commits contributed to
            the release.
    """

    name: str

    email: str | None = None

    profile: str | None = None

    commit_count: int = 0
