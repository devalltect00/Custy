# app/core/changelog/processing/cleaner.py

"""
Commit Message Cleaner

Applies configurable cleaning rules to commit messages
before parsing.
"""

from __future__ import annotations

from app.core.changelog.config.models import (
    CleaningConfig,
)


class CommitMessageCleaner:
    """
    Clean raw commit messages.
    """

    def __init__(
        self,
        config: CleaningConfig,
    ) -> None:
        """
        Initialize the cleaner.

        Args:
            config:
                Cleaning configuration.
        """

        self.config = config

    def clean(
        self,
        message: str,
    ) -> str:
        """
        Clean a commit message.

        Args:
            message:
                Raw commit message.

        Returns:
            Cleaned commit message.
        """

        cleaned = message

        cleaned = self._remove_separators(
            cleaned,
        )

        cleaned = self._remove_headers(
            cleaned,
        )

        cleaned = self._remove_hash_lines(
            cleaned,
        )

        cleaned = self._remove_metadata(
            cleaned,
        )

        cleaned = self._remove_release_summary(
            cleaned,
        )

        cleaned = self._remove_keywords(
            cleaned,
        )

        cleaned = self._normalize_blank_lines(
            cleaned,
        )

        return cleaned.strip()

    def _remove_separators(
        self,
        message: str,
    ) -> str:
        """
        Remove configured separator lines.

        Only complete lines are removed. Substrings inside
        release prose and changelog items are preserved.
        """

        separators = {
            separator.strip()
            for separator in self.config.remove_separators
            if separator.strip()
        }

        return "\n".join(
            line
            for line in message.splitlines()
            if line.strip() not in separators
        )

    def _remove_headers(
        self,
        message: str,
    ) -> str:
        """
        Remove Markdown headers.
        """

        if not self.config.remove_headers:
            return message

        lines: list[str] = []

        for line in message.splitlines():

            stripped = line.lstrip()

            if stripped.startswith("#"):
                continue

            lines.append(line)

        return "\n".join(lines)

    def _remove_hash_lines(
        self,
        message: str,
    ) -> str:
        """
        Remove comment lines beginning with '#'.
        """

        if not self.config.remove_hash_lines:
            return message

        lines: list[str] = []

        for line in message.splitlines():

            if line.lstrip().startswith("#"):
                continue

            lines.append(line)

        return "\n".join(lines)

    def _remove_metadata(
        self,
        message: str,
    ) -> str:
        """
        Remove metadata-oriented lines.
        """

        if not self.config.remove_metadata:
            return message

        metadata_prefixes = (
            "Type:",
            "Stability:",
            "Workflow:",
            "Versioning:",
            "Docs:",
            "Tests:",
            "QA:",
            "CI/CD:",
            "Config:",
            "Maintenance:",
            "Tag:",
            "UX:",
            "Pre-release:",
        )

        lines: list[str] = []

        for line in message.splitlines():

            stripped = line.strip().lstrip("-*+• ")
            stripped = stripped.replace("**", "")

            if any(
                stripped.startswith(prefix)
                for prefix in metadata_prefixes
            ):
                continue

            lines.append(line)

        return "\n".join(lines)

    def _remove_release_summary(
        self,
        message: str,
    ) -> str:
        """
        Remove release narrative lines when configured.
        """

        if not self.config.remove_release_summary:
            return message

        ignored_prefixes = (
            "Final release of",
            "Production-ready",
            "Stable release",
        )

        lines: list[str] = []

        for line in message.splitlines():

            stripped = line.strip()

            if any(
                stripped.startswith(prefix)
                for prefix in ignored_prefixes
            ):
                continue

            lines.append(line)

        return "\n".join(lines)

    def _remove_keywords(
        self,
        message: str,
    ) -> str:
        """
        Remove lines containing configured keywords.

        Removing complete lines avoids corrupting valid
        prose when a keyword appears inside a sentence.
        """

        keywords = [
            keyword
            for keyword in self.config.remove_keywords
            if keyword
        ]

        return "\n".join(
            line
            for line in message.splitlines()
            if not any(
                keyword in line
                for keyword in keywords
            )
        )

    @staticmethod
    def _normalize_blank_lines(
        message: str,
    ) -> str:
        """
        Collapse consecutive blank lines.
        """

        normalized: list[str] = []

        previous_blank = False

        for line in message.splitlines():

            blank = not line.strip()

            if blank and previous_blank:
                continue

            normalized.append(line)

            previous_blank = blank

        return "\n".join(normalized)
