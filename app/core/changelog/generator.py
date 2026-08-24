# app/core/changelog/generator.py

"""
Changelog generator.

This module coordinates Git message collection, semantic
processing, release-family planning, and Jinja rendering for
``CHANGELOG.md``. Git operations remain delegated to the
existing Git service.
"""

from __future__ import annotations

from pathlib import Path
import re

from rich.markup import escape

from app.cli.constants.enums import StrategyChoices
from app.constants.path import (
    CHANGELOG_PATH,
    CUSTY_CHANGELOG_J2,
    CUSTY_COMMIT_MESSAGE_TEMPLATE,
)
from app.core.changelog.config.resolver import ChangelogConfigResolver
from app.core.changelog.models.changelog import Changelog
from app.core.changelog.models.commit import Commit
from app.core.changelog.models.commit_group import CommitGroup
from app.core.changelog.models.metadata import ReleaseMetadata
from app.core.changelog.models.release import Release
from app.core.changelog.processing.pipeline import ChangelogProcessingPipeline
from app.core.changelog.processing.tag_behavior import ReleaseBehaviorProcessor
from app.core.changelog.providers.factory import MessageProviderFactory
from app.core.changelog.rendering.jinja_renderer import JinjaRenderer
from app.core.changelog.sorting.release_sorter import DefaultReleaseSorter
from app.core.dry_run import DryRunSupport
from app.core.git_ops.git.factory import create_git_service
from app.ui.progress import progress_task


class ChangelogGenerator(DryRunSupport):
    """
    Generate a semantic Markdown changelog from Git history.

    Responsibilities:
        - Plan correct Git ranges for stable and prerelease tags.
        - Collect messages through configured providers.
        - Build release-level summaries, metadata, and tags.
        - Process change items and render the final document.
    """

    VERSION_PATTERN = re.compile(
        r"^v?(?P<base>\d+(?:\.\d+){1,})"
        r"(?:[-.]?(?P<label>alpha|a|beta|b|rc|dev|post)"
        r"(?:[.-]?(?P<number>\d+))?)?$",
        re.IGNORECASE,
    )

    VERSION_TOKEN_PATTERN = re.compile(
        r"v?\d+(?:\.\d+){1,}"
        r"(?:[-.]?(?:alpha|a|beta|b|rc|dev|post)"
        r"(?:[.-]?\d+)?)?",
        re.IGNORECASE,
    )

    TAG_ENTRY_PATTERN = re.compile(
        r"^[-*+•]\s*(.+?):\s*(.+)$",
    )

    GROUP_TAGS = {
        "feat": "feature",
        "fix": "bugfix",
        "docs": "docs",
        "perf": "performance",
        "test": "tests",
        "ci": "ci",
        "build": "build",
        "release": "release",
        "revert": "revert",
        "style": "style",
        "breaking": "breaking-change",
        "template": "template",
    }

    TAG_PRIORITY = (
        "release",
        "workflow",
        "feature",
        "bugfix",
        "docs",
        "template",
        "security",
        "breaking-change",
        "performance",
        "tests",
        "ci",
        "build",
        "revert",
        "style",
        "stable",
        "beta",
        "rc",
        "alpha",
        "dev",
        "post-release",
    )

    GENERIC_SCOPES = {
        "",
        "main",
        "core",
        "general",
        "default",
        "root",
        "changelog",
        "release",
    }

    def __init__(
        self,
        *,
        dry_run: bool = False,
        strategy: StrategyChoices | None = None,
        template_path: Path = CUSTY_CHANGELOG_J2,
        pending_commit_path: Path | None = CUSTY_COMMIT_MESSAGE_TEMPLATE,
    ) -> None:
        """
        Initialize the changelog generator.

        Args:
            dry_run:
                Enable dry-run behavior for file output.

            strategy:
                Optional project version sorting strategy.

            template_path:
                Jinja template used to render the changelog.

            pending_commit_path:
                Optional pending commit-message template.
        """

        super().__init__(dry_run=dry_run)

        self.config = ChangelogConfigResolver().load()
        self.git_service = create_git_service(
            dry_run=dry_run,
            strategy=strategy,
        )
        self.processing_pipeline = ChangelogProcessingPipeline(self.config)
        self.release_behavior = ReleaseBehaviorProcessor(
            self.config.release_behavior,
        )
        self.release_sorter = DefaultReleaseSorter()

        with template_path.open(encoding="utf-8") as file:
            self.renderer = JinjaRenderer(
                template=file.read(),
                config=self.config,
            )

        self.pending_commit_path = pending_commit_path

    def generate(self) -> str:
        """
        Generate changelog Markdown.

        Returns:
            Complete rendered changelog document.
        """

        changelog = self._collect_releases()
        changelog = self.release_behavior.apply(changelog)
        changelog = self.release_sorter.sort(changelog)

        return self.renderer.render(changelog)

    def _collect_releases(self) -> Changelog:
        """
        Collect released and unreleased changes from Git.

        Stable tags use the previous stable tag as their range
        boundary, which aggregates their complete prerelease
        family. Prerelease tags continue to use adjacent tags.

        Returns:
            Generated changelog domain model.
        """

        tags = self.git_service.get_tags()
        providers = MessageProviderFactory.create(
            git_service=self.git_service,
            config=self.config,
            pending_commit_loader=self._load_pending_commit,
        )
        changelog = Changelog()

        with progress_task(
            "Generating changelog",
            total=len(tags) + 1,
        ) as progress:
            latest_tag = tags[0] if tags else ""
            progress.update("Processing Unreleased changes")
            unreleased_messages = self._collect_messages(
                providers=providers,
                previous=latest_tag,
                current="",
                is_latest_release=True,
            )

            if unreleased_messages:
                changelog.releases.append(
                    self._build_release(
                        version="Unreleased",
                        release_date=None,
                        compare_url=self._build_compare_url(latest_tag, "HEAD"),
                        messages=unreleased_messages,
                        promoted_from=[],
                    )
                )

            progress.advance()

            for index, current in enumerate(tags):
                progress.update(f"Processing release {escape(current)}")
                previous, previous_index = self._previous_boundary(tags, index)
                messages = self._collect_messages(
                    providers=providers,
                    previous=previous,
                    current=current,
                    is_latest_release=False,
                )

                if messages:
                    promoted_from = self._promoted_tags(
                        tags=tags,
                        current_index=index,
                        previous_index=previous_index,
                    )

                    changelog.releases.append(
                        self._build_release(
                            version=current,
                            release_date=self.git_service.get_tag_date(current),
                            compare_url=self._build_compare_url(previous, current),
                            messages=messages,
                            promoted_from=promoted_from,
                        )
                    )

                progress.advance()

        return changelog

    @staticmethod
    def _collect_messages(
        *,
        providers: list,
        previous: str,
        current: str,
        is_latest_release: bool,
    ) -> list[str]:
        """
        Collect messages from all configured providers.

        Args:
            providers:
                Configured message providers.

            previous:
                Lower Git range boundary.

            current:
                Upper Git range boundary; empty means ``HEAD``.

            is_latest_release:
                Whether pending content may participate.

        Returns:
            Raw messages in provider order.
        """

        messages: list[str] = []

        for provider in providers:
            messages.extend(
                provider.get_messages(
                    previous,
                    current,
                    is_latest_release=is_latest_release,
                )
            )

        return messages

    def _previous_boundary(
        self,
        tags: list[str],
        current_index: int,
    ) -> tuple[str, int | None]:
        """
        Resolve the correct lower boundary for a release.

        Args:
            tags:
                Tags ordered newest to oldest.

            current_index:
                Index of the release being planned.

        Returns:
            Previous tag and its index when one exists.
        """

        current = tags[current_index]

        if self._release_stage(current) == "stable":
            for index in range(current_index + 1, len(tags)):
                if self._release_stage(tags[index]) == "stable":
                    return tags[index], index

            return "", None

        next_index = current_index + 1

        if next_index < len(tags):
            return tags[next_index], next_index

        return "", None

    def _promoted_tags(
        self,
        *,
        tags: list[str],
        current_index: int,
        previous_index: int | None,
    ) -> list[str]:
        """
        Return prerelease tags promoted into a stable release.

        Args:
            tags:
                Tags ordered newest to oldest.

            current_index:
                Stable release index.

            previous_index:
                Previous stable release index.

        Returns:
            Matching prereleases ordered newest to oldest.
        """

        current = tags[current_index]

        if self._release_stage(current) != "stable":
            return []

        stop = previous_index if previous_index is not None else len(tags)
        base = self._base_version(current)

        return [
            tag
            for tag in tags[current_index + 1 : stop]
            if (
                self._base_version(tag) == base
                and self._release_stage(tag) != "stable"
            )
        ]

    def _build_compare_url(self, previous: str, current: str) -> str | None:
        """
        Build a repository comparison URL.

        Args:
            previous:
                Lower comparison boundary.

            current:
                Upper comparison boundary.

        Returns:
            Compare URL when configured and both boundaries exist.
        """

        if (
            not self.config.links.enable_compare
            or not self.config.links.repository
            or not previous
            or not current
        ):
            return None

        repository = self.config.links.repository.rstrip("/")

        return f"{repository}/compare/{previous}...{current}"

    def _determine_release_status(self, version: str) -> str:
        """
        Determine a human-readable release status.

        Args:
            version:
                Version or ``Unreleased`` identifier.

        Returns:
            Display release status.
        """

        stages = {
            "unreleased": "Unreleased",
            "dev": "Development",
            "alpha": "Alpha",
            "beta": "Beta",
            "rc": "Release Candidate",
            "post": "Post Release",
            "stable": "Stable Release",
        }

        return stages[self._release_stage(version)]

    def _release_stage(self, version: str) -> str:
        """
        Parse the release stage from PEP 440 or SemVer tags.

        Args:
            version:
                Version identifier.

        Returns:
            Normalized stage key.
        """

        if version.casefold() == "unreleased":
            return "unreleased"

        match = self.VERSION_PATTERN.fullmatch(version.strip())

        if not match or not match.group("label"):
            return "stable"

        label = match.group("label").casefold()

        if label in {"a", "alpha"}:
            return "alpha"

        if label in {"b", "beta"}:
            return "beta"

        return label

    def _base_version(self, version: str) -> str:
        """
        Return a tag's numeric release-family base.

        Args:
            version:
                Version identifier.

        Returns:
            Numeric base version, or the normalized input when
            the tag does not match a supported version form.
        """

        match = self.VERSION_PATTERN.fullmatch(version.strip())

        if match:
            return match.group("base")

        return version.strip().lstrip("vV").casefold()

    def _build_release(
        self,
        *,
        version: str,
        release_date: str | None,
        compare_url: str | None,
        messages: list[str],
        promoted_from: list[str],
    ) -> Release:
        """
        Build one release from collected messages.

        Args:
            version:
                Release version.

            release_date:
                ISO-8601 tag date.

            compare_url:
                Optional repository comparison URL.

            messages:
                Raw commit messages in the planned range.

            promoted_from:
                Prerelease versions aggregated into this release.

        Returns:
            Complete release domain model.
        """

        parsed_commits = self.processing_pipeline.parse_messages(messages)
        release_commit = self._select_release_commit(parsed_commits, version)
        status = self._determine_release_status(version)
        groups = self.processing_pipeline.process_messages(messages)

        explicit_promotions = (
            self._extract_promoted_from(release_commit.body)
            if release_commit
            else []
        )

        promotions = self._valid_promotions(
            versions=[*promoted_from, *explicit_promotions],
            current=version,
        )

        return Release(
            version=version,
            release_date=release_date,
            compare_url=compare_url,
            status=status,
            summary=(
                self._extract_summary(release_commit.body)
                if release_commit
                else None
            ),
            promoted_from=promotions,
            metadata=self._extract_release_metadata(
                release_commit=release_commit,
                status=status,
                version=version,
                groups=groups,
            ),
            groups=groups,
        )

    def _select_release_commit(
        self,
        commits: list[Commit],
        version: str,
    ) -> Commit | None:
        """
        Select the commit that describes a release.

        Matching the current version has priority, followed by
        explicit release scopes and release commit types. This
        avoids taking summaries from arbitrary change commits.

        Args:
            commits:
                Parsed commits in Git/provider order.

            version:
                Release being assembled.

        Returns:
            Best matching release commit, if found.
        """

        if not commits:
            return None

        if version.casefold() == "unreleased":
            return commits[-1]

        version_key = version.lstrip("vV").casefold()
        ranked: list[tuple[int, int, Commit]] = []

        for index, commit in enumerate(commits):
            subject_key = commit.subject.lstrip("vV").casefold()
            score = 0

            if version_key and version_key in subject_key:
                score = 4

            if score:
                ranked.append((score, -index, commit))

        if not ranked:
            return None

        return max(ranked, key=lambda candidate: candidate[:2])[2]

    def _valid_promotions(
        self,
        *,
        versions: list[str],
        current: str,
    ) -> list[str]:
        """
        Keep only prereleases belonging to a stable release family.

        Args:
            versions:
                Derived and explicitly documented promotion values.

            current:
                Release receiving the promoted versions.

        Returns:
            Ordered unique prerelease versions.
        """

        if self._release_stage(current) != "stable":
            return []

        current_base = self._base_version(current)

        return self._ordered_unique(
            [
                version
                for version in versions
                if (
                    version.casefold() != current.casefold()
                    and self._base_version(version) == current_base
                    and self._release_stage(version) != "stable"
                )
            ]
        )

    def _extract_summary(self, body: str) -> str | None:
        """
        Extract clean release narrative before semantic sections.

        Args:
            body:
                Release commit body.

        Returns:
            Normalized narrative summary, if present.
        """

        lines: list[str] = []

        for line in body.splitlines():
            stripped = line.strip()
            normalized = stripped.replace("**", "").casefold()

            if stripped.startswith("###"):
                break

            if self._is_tag_footer(stripped):
                break

            if (
                stripped in {"---", "***", "==="}
                or normalized.startswith("tag:")
                or normalized.startswith("_tag:")
                or normalized.startswith("changelog:")
                or normalized.startswith("promoted from:")
                or (
                    "pre-release" in normalized
                    and "from" in normalized
                )
            ):
                continue

            if re.match(r"^[-*+•]\s+", stripped):
                break

            lines.append(line.rstrip())

        summary = self._normalize_paragraphs(lines)

        return summary or None

    def _extract_promoted_from(self, body: str) -> list[str]:
        """
        Extract explicitly documented promoted prereleases.

        Args:
            body:
                Release commit body.

        Returns:
            Ordered unique version identifiers.
        """

        versions: list[str] = []
        collecting = False

        for line in body.splitlines():
            stripped = line.strip()
            normalized = stripped.casefold()

            if (
                "promoted from" in normalized
                or ("pre-release" in normalized and "from" in normalized)
            ):
                collecting = True
                versions.extend(self.VERSION_TOKEN_PATTERN.findall(stripped))
                continue

            if collecting and re.match(r"^[-*+•]\s+", stripped):
                versions.extend(self.VERSION_TOKEN_PATTERN.findall(stripped))
                continue

            if collecting and stripped:
                break

        return self._ordered_unique(versions)

    def _extract_tags(self, body: str) -> dict[str, list[str]]:
        """
        Extract and flatten the structured tag footer.

        Args:
            body:
                Release commit body.

        Returns:
            Tag values grouped by normalized footer category.
        """

        tags: dict[str, list[str]] = {}
        in_tags = False

        for line in body.splitlines():
            stripped = line.strip()

            if self._is_tag_footer(stripped):
                in_tags = True
                continue

            if not in_tags:
                continue

            if stripped.startswith("###"):
                break

            match = self.TAG_ENTRY_PATTERN.match(stripped)

            if not match:
                if stripped and stripped not in {"---", "***", "==="}:
                    break
                continue

            category = re.sub(
                r"[^\w/ -]",
                "",
                match.group(1),
            ).strip().casefold()
            grouped_values = tags.setdefault(category, [])

            for value in re.split(r"[,•]", match.group(2)):
                tag = self._normalize_tag(value)

                if tag:
                    grouped_values.append(tag)

        return {
            category: self._ordered_unique(values)
            for category, values in tags.items()
        }

    def _extract_release_metadata(
        self,
        *,
        release_commit: Commit | None,
        status: str,
        version: str,
        groups: list[CommitGroup],
    ) -> ReleaseMetadata:
        """
        Build deterministic metadata and inline release tags.

        Args:
            release_commit:
                Commit selected as the release announcement.

            status:
                Human-readable release status.

            version:
                Release version.

            groups:
                Semantic change groups in the release.

        Returns:
            Structured release metadata.
        """

        raw_tags = (
            self._extract_tags(release_commit.body)
            if release_commit
            else {}
        )
        tags: list[str] = []

        if version.casefold() != "unreleased":
            tags.append("release")

        scope = release_commit.scope if release_commit else None

        if scope and scope.casefold() not in self.GENERIC_SCOPES:
            tags.append(scope)

        active_group_tags = [
            self.GROUP_TAGS[group.commit_type]
            for group in groups
            if group.commit_type in self.GROUP_TAGS
        ]

        for category, values in raw_tags.items():
            if any(
                name in category
                for name in ("workflow", "scope", "component")
            ):
                tags.extend(values)

        tags.extend(active_group_tags)

        active_tag_keys = {
            tag.casefold()
            for tag in active_group_tags
        }

        for values in raw_tags.values():
            tags.extend(
                tag
                for tag in values
                if tag.casefold() in active_tag_keys
            )

        stage = self._release_stage(version)
        stage_tags = {
            "stable": "stable",
            "beta": "beta",
            "rc": "rc",
            "alpha": "alpha",
            "dev": "dev",
            "post": "post-release",
        }

        if stage in stage_tags:
            tags.append(stage_tags[stage])

        tags = self._ordered_unique(tags)
        priority = {
            tag: index
            for index, tag in enumerate(self.TAG_PRIORITY)
        }
        source_order = {
            tag: index
            for index, tag in enumerate(tags)
        }
        tags.sort(
            key=lambda tag: (
                priority.get(tag.casefold(), len(priority)),
                source_order[tag],
            )
        )

        return ReleaseMetadata(
            release_type=status,
            scope=scope,
            classifications=[],
            tags={"Tags": tags},
        )

    @staticmethod
    def _is_tag_footer(line: str) -> bool:
        """
        Return whether a line starts a structured Tags footer.

        Args:
            line:
                Stripped line to evaluate.
        """

        normalized = line.replace("**", "").strip().casefold()

        if normalized.startswith("🔖"):
            normalized = normalized.removeprefix("🔖").strip()

        return normalized.rstrip(":") == "tags"

    @staticmethod
    def _normalize_tag(value: str) -> str:
        """
        Normalize a tag extracted from a commit footer.

        Args:
            value:
                Raw footer value.

        Returns:
            Lowercase tag without Markdown or hash markers.
        """

        tag = value.strip().strip("`*_\"")
        tag = tag.lstrip("#").strip()
        tag = re.sub(r"\s+", "-", tag)

        return tag.casefold()

    @staticmethod
    def _normalize_paragraphs(lines: list[str]) -> str:
        """
        Collapse repeated blank lines while preserving paragraphs.

        Args:
            lines:
                Source narrative lines.

        Returns:
            Clean paragraph text.
        """

        normalized: list[str] = []
        previous_blank = True

        for line in lines:
            blank = not line.strip()

            if blank and previous_blank:
                continue

            normalized.append(line.strip() if not blank else "")
            previous_blank = blank

        while normalized and not normalized[-1]:
            normalized.pop()

        return "\n".join(normalized).strip()

    @staticmethod
    def _ordered_unique(values: list[str]) -> list[str]:
        """
        Return non-empty values once, preserving source order.

        Args:
            values:
                Values to deduplicate.

        Returns:
            Ordered unique values.
        """

        unique: list[str] = []
        seen: set[str] = set()

        for value in values:
            cleaned = value.strip()
            key = cleaned.casefold()

            if not cleaned or key in seen:
                continue

            seen.add(key)
            unique.append(cleaned)

        return unique

    def write_to_file(
        self,
        content: str,
        path: Path = CHANGELOG_PATH,
    ) -> None:
        """
        Write rendered changelog content to disk.

        Args:
            content:
                Rendered Markdown.

            path:
                Destination changelog path.
        """

        if self.runner.is_dry_run:
            print(f"(dry-run) Would write changelog to: {path}")
            print("\n--- Begin Preview ---\n")
            print(content)
            print("\n--- End Preview ---\n")
            return

        path.write_text(content, encoding="utf-8")

    def _load_pending_commit(self) -> str:
        """
        Load the configured pending commit message.

        Returns:
            Pending message content, or an empty string when no
            pending template exists.
        """

        if self.pending_commit_path is None:
            return ""

        if not self.pending_commit_path.exists():
            return ""

        return self.pending_commit_path.read_text(encoding="utf-8").strip()
