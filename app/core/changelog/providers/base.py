# app/core/changelog/providers/base.py

"""
Message Provider Protocol

Defines the interface for all changelog message providers.

A provider is responsible only for collecting raw commit
messages from a particular source.

Examples:
    - Git history
    - Pending commit
    - Future providers
"""

from __future__ import annotations

from typing import Protocol


class MessageProvider(Protocol):
    """
    Protocol implemented by all changelog message providers.
    """

    def get_messages(
        self,
        previous_tag: str,
        current_tag: str,
        *,
        is_latest_release: bool = False,
    ) -> list[str]:
        """
        Collect raw commit messages.

        Args:
            previous_tag:
                Previous Git tag.

            current_tag:
                Current Git tag.

            is_latest_release:
                Indicates whether the current release is the
                latest release being processed.

        Returns:
            List of raw commit messages.
        """
        ...
