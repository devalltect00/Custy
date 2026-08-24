# app/core/changelog/processing/pipeline.py

"""
Changelog Processing Pipeline

Transforms raw commit messages into grouped commit
models ready to be included in a release.
"""

from __future__ import annotations

import re

from app.core.changelog.config.models import (
    ChangelogConfig,
)
from app.core.changelog.models.commit_group import (
    CommitGroup,
)
from app.core.changelog.models.commit import Commit
from app.core.changelog.models.commit_section import CommitSection
from app.core.changelog.models.commit_subsection import CommitSubsection
from app.core.changelog.processing.cleaner import (
    CommitMessageCleaner,
)
from app.core.changelog.processing.commit_type_grouper import (
    CommitTypeGrouper,
)
from app.core.changelog.processing.deduplicator import (
    CommitDeduplicator,
)
from app.core.changelog.processing.parser import (
    CommitParser,
)


class ChangelogProcessingPipeline:
    """
    Process raw commit messages into grouped commit
    models.
    """

    SECTION_TYPE_ALIASES: tuple[tuple[tuple[str, ...], str], ...] = (
        (("breaking change", "breaking changes"), "breaking"),
        (("bug fix", "bug fixes", "bugfix", "fix", "fixes"), "fix"),
        (("template improvement", "template improvements", "template", "templates"), "template"),
        (("documentation", "docs", "document"), "docs"),
        (("feature", "features"), "feat"),
        (
            (
                "improvement",
                "improvements",
                "ux improvement",
                "ux improvements",
                "enhancement",
                "enhancements",
                "refinement",
                "refinements",
            ),
            "improvement",
        ),
        (("refactor", "refactoring", "maintenance structure"), "refactor"),
        (("performance", "performance improvements"), "perf"),
        (("test", "tests", "testing", "qa"), "test"),
        (("ci", "ci cd", "cicd", "continuous integration"), "ci"),
        (("build", "builds"), "build"),
        (("maintenance", "chore", "chores", "cleanup"), "chore"),
        (("release", "releases"), "release"),
        (("revert", "reverts"), "revert"),
        (("style", "styling"), "style"),
        (("misc", "miscellaneous", "other", "others"), "other"),
    )

    VERSION_SUBJECT_PATTERN = re.compile(
        r"^v?\d+(?:\.\d+){1,}"
        r"(?:[-.]?(?:alpha|a|beta|b|rc|dev|post)"
        r"(?:[.-]?\d+)?)?$",
        re.IGNORECASE,
    )

    SHELL_TRANSCRIPT_PATTERN = re.compile(
        r"(?:^|>)\s*git\s+(?:log|show|status|branch)\b",
        re.IGNORECASE,
    )

    LOW_INFORMATION_SUBJECTS = {
        "checkpoint",
        "fixed",
        "just some checkpoint",
        "update",
        "updated",
    }

    def __init__(
        self,
        config: ChangelogConfig,
    ) -> None:
        """
        Initialize the processing pipeline.

        Args:
            config:
                Changelog configuration.
        """

        self.config = config

        self.cleaner = CommitMessageCleaner(
            config.cleaning,
        )

        self.parser = CommitParser()

        self.deduplicator = (
            CommitDeduplicator()
        )

        self.commit_type_grouper = (
            CommitTypeGrouper()
        )

        self._mapped_section_types = {
            self._normalize_heading(title): commit_type
            for commit_type, title in config.type_mapping.mapping.items()
        }

        self._generic_scopes = {
            scope.casefold()
            for scope in config.rendering.generic_scopes
        }

    def parse_messages(
        self,
        messages: list[str],
    ) -> list[Commit]:
        """
        Clean and parse raw messages without grouping them.

        This view is used by release-level extraction so the
        generator can select the correct release announcement
        before normal change filtering is applied.

        Args:
            messages:
                Raw commit messages.

        Returns:
            Parsed, non-empty commits in their original order.
        """

        commits: list[Commit] = []

        for message in messages:
            cleaned = self.cleaner.clean(message)

            if not cleaned:
                continue

            commits.append(self.parser.parse(cleaned))

        return commits

    def process_messages(
        self,
        messages: list[str],
    ) -> list[CommitGroup]:
        """
        Process raw commit messages.

        Processing stages:

            1. Clean and parse messages.
            2. Expand semantic Markdown sections.
            3. Apply ignore and breaking-change rules.
            4. Remove duplicates when configured.
            5. Group commits by semantic change type.

        Args:
            messages:
                Raw commit messages.

        Returns:
            Ordered commit groups.
        """

        commits = self.parse_messages(messages)

        expanded_commits = [
            expanded
            for commit in commits
            for expanded in self._expand_semantic_sections(commit)
        ]

        filtered_commits: list[Commit] = []

        for commit in expanded_commits:
            self._apply_breaking_type(commit)

            if self._is_ignored(commit):
                continue

            filtered_commits.append(commit)

        unique_commits = filtered_commits

        if self.config.rendering.deduplicate:
            unique_commits = self.deduplicator.deduplicate(
                filtered_commits,
            )

        groups = (
            self.commit_type_grouper.group(
                unique_commits,
            )
        )

        return groups

    def _expand_semantic_sections(
        self,
        commit: Commit,
    ) -> list[Commit]:
        """
        Expand titled body sections into semantic commits.

        A release commit may contain Features, Bug Fixes,
        Templates, and Documentation in one body. Expanding
        those sections prevents the Conventional Commit header
        from incorrectly placing every item in one group.

        Args:
            commit:
                Parsed source commit.

        Returns:
            One commit per semantic section, or the original
            commit when no titled sections exist.
        """

        if not any(section.title.strip() for section in commit.sections):
            return [commit]

        expanded: list[Commit] = []

        for section in commit.sections:
            if not self._section_has_items(section):
                continue

            commit_type = (
                self._section_type(section.title)
                if section.title.strip()
                else commit.commit_type
            )

            semantic_section = CommitSection(
                title="",
                items=list(section.items),
                subsections=[
                    CommitSubsection(
                        title=subsection.title,
                        items=list(subsection.items),
                    )
                    for subsection in section.subsections
                ],
            )

            scope = commit.scope

            if (
                semantic_section.subsections
                or (scope or "").casefold() in self._generic_scopes
            ):
                scope = None

            expanded.append(
                Commit(
                    subject=commit.subject,
                    body="",
                    commit_type=commit_type,
                    scope=scope,
                    breaking=commit_type == "breaking",
                    commit_date=commit.commit_date,
                    hash=commit.hash,
                    sections=[semantic_section],
                )
            )

        return expanded

    def _section_type(
        self,
        title: str,
    ) -> str:
        """
        Resolve a Markdown section title to a change type.

        Args:
            title:
                Section heading text, optionally containing an
                icon.

        Returns:
            Conventional or semantic change type key.
        """

        normalized = self._normalize_heading(title)

        mapped = self._mapped_section_types.get(normalized)

        if mapped:
            return mapped

        for aliases, commit_type in self.SECTION_TYPE_ALIASES:
            for alias in aliases:
                if (
                    normalized == alias
                    or normalized.startswith(f"{alias} ")
                    or normalized.endswith(f" {alias}")
                ):
                    return commit_type

        slug = re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")

        return slug or "other"

    def _apply_breaking_type(
        self,
        commit: Commit,
    ) -> None:
        """
        Move a detected breaking commit into its own group.

        Args:
            commit:
                Commit updated in place.
        """

        if not self.config.breaking.enabled:
            return

        content = f"{commit.subject}\n{commit.body}".casefold()
        has_keyword = any(
            keyword.casefold() in content
            for keyword in self.config.breaking.keywords
        )

        if commit.breaking or has_keyword:
            commit.commit_type = "breaking"

    def _is_ignored(
        self,
        commit: Commit,
    ) -> bool:
        """
        Determine whether a parsed commit should be excluded.

        Args:
            commit:
                Commit to evaluate.

        Returns:
            ``True`` when configured collection rules exclude
            the commit.
        """

        if (
            self.config.core.ignore_merge_commits
            and commit.subject.casefold().startswith("merge ")
        ):
            return True

        if self.SHELL_TRANSCRIPT_PATTERN.search(commit.subject):
            return True

        normalized_subject = re.sub(
            r"\s+",
            " ",
            commit.subject,
        ).strip().casefold()

        if (
            commit.commit_type.casefold() == "other"
            and normalized_subject in self.LOW_INFORMATION_SUBJECTS
        ):
            return True

        if (
            commit.commit_type.casefold() == "docs"
            and (commit.scope or "").casefold() == "changelog"
            and normalized_subject in {"update changelog", "updated changelog"}
        ):
            return True

        ignored_types = {
            commit_type.casefold()
            for commit_type in self.config.core.ignore_types
        }

        if commit.commit_type.casefold() in ignored_types:
            return True

        is_release_announcement = (
            commit.commit_type.casefold() == "release"
            or (commit.scope or "").casefold() == "release"
            or bool(
                self.VERSION_SUBJECT_PATTERN.fullmatch(
                    commit.subject.strip()
                )
            )
        )

        return is_release_announcement and not self._commit_has_items(commit)

    @staticmethod
    def _commit_has_items(
        commit: Commit,
    ) -> bool:
        """
        Return whether a commit contains renderable items.

        Args:
            commit:
                Commit to inspect.
        """

        return any(
            ChangelogProcessingPipeline._section_has_items(section)
            for section in commit.sections
        )

    @staticmethod
    def _section_has_items(
        section: CommitSection,
    ) -> bool:
        """
        Return whether a section or its subsections has items.

        Args:
            section:
                Section to inspect.
        """

        return bool(
            section.items
            or any(subsection.items for subsection in section.subsections)
        )

    @staticmethod
    def _normalize_heading(
        title: str,
    ) -> str:
        """
        Normalize a display heading for semantic matching.

        Args:
            title:
                Heading to normalize.

        Returns:
            Lowercase words without Markdown or icons.
        """

        words = re.sub(r"[^\w\s]", " ", title, flags=re.UNICODE)
        words = words.replace("_", " ")

        return re.sub(r"\s+", " ", words).strip().casefold()
