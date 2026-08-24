# app/core/changelog/rendering/context.py

"""
Changelog rendering context.

This module adapts the domain changelog model into the
small, stable view model consumed by Jinja. Keeping the
normalization here prevents templates from depending on
attributes that do not exist on domain objects.
"""

from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass, field
import re

from app.core.changelog.config.models import ChangelogConfig
from app.core.changelog.models.changelog import Changelog
from app.core.changelog.models.commit import Commit
from app.core.changelog.models.commit_group import CommitGroup
from app.core.changelog.models.commit_scope import CommitScope
from app.core.changelog.models.release import Release


@dataclass(slots=True)
class RenderedSubsection:
    """
    Render-ready subsection.

    Attributes:
        title:
            Subsection heading.

        items:
            Normalized Markdown list items.
    """

    title: str
    items: list[str] = field(default_factory=list)


@dataclass(slots=True)
class RenderedGroup:
    """
    Render-ready semantic change group.

    Attributes:
        title:
            Display title, including an optional icon.

        items:
            Items rendered directly below the group.

        subsections:
            Meaningful scope or commit-body subsections.
    """

    title: str
    items: list[str] = field(default_factory=list)
    subsections: list[RenderedSubsection] = field(default_factory=list)


@dataclass(slots=True)
class ChangelogRenderContext:
    """
    Rendering context passed to the changelog template.

    The context combines the domain model, rendering
    configuration, and deterministic presentation helpers.

    Attributes:
        changelog:
            Complete changelog domain model.

        config:
            Resolved changelog configuration.
    """

    changelog: Changelog
    config: ChangelogConfig

    def visible_releases(self) -> list[Release]:
        """
        Return releases that are not configured as hidden.

        Returns:
            Visible releases in their existing order.
        """

        return [
            release
            for release in self.changelog.releases
            if not release.hidden
        ]

    def groups_for(self, release: Release) -> list[RenderedGroup]:
        """
        Build render-ready groups for a release.

        Generic scopes are flattened while meaningful scopes
        and body subsections are preserved. Duplicate items are
        removed only when rendering deduplication is enabled.

        Args:
            release:
                Release whose groups should be adapted.

        Returns:
            Render-ready semantic groups.
        """

        groups = list(release.groups)

        if self.config.rendering.sort_groups:
            groups.sort(key=lambda group: self._group_title(group).casefold())

        rendered = [self._render_group(group) for group in groups]

        return [
            group
            for group in rendered
            if (
                group.items
                or group.subsections
                or self.config.rendering.show_empty_groups
            )
        ]

    def tags_for(self, release: Release) -> list[str]:
        """
        Flatten and normalize a release's display tags.

        Args:
            release:
                Release whose metadata should be flattened.

        Returns:
            Ordered unique tag values without Markdown markers
            or leading hash characters.
        """

        values: list[str] = []

        for grouped_values in release.metadata.tags.values():
            values.extend(grouped_values)

        values.extend(release.metadata.classifications)

        normalized: list[str] = []
        seen: set[str] = set()

        for value in values:
            tag = self._normalize_tag(value)
            key = tag.casefold()

            if not tag or key in seen:
                continue

            seen.add(key)
            normalized.append(tag)

        return normalized

    @staticmethod
    def release_label(release: Release) -> str:
        """
        Return the concise release label used by the ideal layout.

        Args:
            release:
                Release to label.

        Returns:
            Human-readable release stage.
        """

        if release.status == "Stable Release":
            return "Stable"

        return release.status or ""

    @staticmethod
    def summary_for(release: Release) -> str | None:
        """
        Resolve configured custom text or generated summary.

        Args:
            release:
                Release to summarize.

        Returns:
            Summary text, if available.
        """

        return release.custom_message or release.summary

    def _render_group(self, group: CommitGroup) -> RenderedGroup:
        """
        Adapt one domain commit group.

        Args:
            group:
                Domain group to adapt.

        Returns:
            Render-ready group.
        """

        direct_items: list[str] = []
        subsection_items: OrderedDict[str, list[str]] = OrderedDict()
        seen: set[str] = set()

        scopes = list(group.scopes)

        if self.config.rendering.sort_scopes:
            scopes.sort(key=lambda scope: self._scope_title(scope).casefold())

        for scope in scopes:
            self._collect_scope(
                scope,
                direct_items=direct_items,
                subsection_items=subsection_items,
                seen=seen,
            )

        if self.config.rendering.sort_items:
            direct_items.sort(key=str.casefold)

            for items in subsection_items.values():
                items.sort(key=str.casefold)

        subsections = [
            RenderedSubsection(title=title, items=items)
            for title, items in subsection_items.items()
            if items or self.config.rendering.show_empty_scopes
        ]

        return RenderedGroup(
            title=self._group_title(group),
            items=direct_items,
            subsections=subsections,
        )

    def _collect_scope(
        self,
        scope: CommitScope,
        *,
        direct_items: list[str],
        subsection_items: OrderedDict[str, list[str]],
        seen: set[str],
    ) -> None:
        """
        Collect the renderable content of one commit scope.

        Args:
            scope:
                Scope to collect.

            direct_items:
                Destination for flattened items.

            subsection_items:
                Destination grouped by meaningful subsection.

            seen:
                Normalized item keys already emitted.
        """

        scope_title = self._scope_title(scope)
        scoped = (
            self.config.rendering.group_by_scope
            and not self._is_generic_scope(scope.scope, scope_title)
        )

        for commit in scope.commits:
            items, nested = self._commit_content(commit)

            target = (
                subsection_items.setdefault(scope_title, [])
                if scoped
                else direct_items
            )

            for item in items:
                self._append_item(target, item, seen)

            for title, nested_items in nested:
                if self._is_generic_scope(title, title):
                    nested_target = direct_items
                else:
                    nested_target = subsection_items.setdefault(title, [])

                for item in nested_items:
                    self._append_item(nested_target, item, seen)

    def _commit_content(
        self,
        commit: Commit,
    ) -> tuple[list[str], list[tuple[str, list[str]]]]:
        """
        Extract direct and nested items from a parsed commit.

        Args:
            commit:
                Commit to adapt.

        Returns:
            Direct items and named subsection items.
        """

        items: list[str] = []
        nested: list[tuple[str, list[str]]] = []

        for section in commit.sections:
            items.extend(section.items)

            for subsection in section.subsections:
                nested.append((subsection.title, list(subsection.items)))

        if (
            not items
            and not any(nested_items for _, nested_items in nested)
            and self.config.release.fallback_to_subject
        ):
            items.append(commit.subject)

        return items, nested

    def _group_title(self, group: CommitGroup) -> str:
        """
        Resolve the configured title of a commit group.

        Args:
            group:
                Group whose title should be resolved.

        Returns:
            Configured or humanized group title.
        """

        if group.commit_type == "breaking":
            title = self.config.breaking.label
        else:
            title = self.config.type_mapping.mapping.get(group.commit_type)

        if not title:
            title = group.commit_type.replace("-", " ").title()

        if not self.config.rendering.show_section_icons:
            title = re.sub(r"^[^\w]+", "", title).strip()

        return title

    def _scope_title(self, scope: CommitScope) -> str:
        """
        Resolve a configured scope display title.

        Args:
            scope:
                Scope to resolve.

        Returns:
            Human-readable scope title.
        """

        mapped = self.config.scope_mapping.mapping.get(scope.scope, scope.scope)

        return mapped.replace("-", " ").replace("_", " ").title()

    def _is_generic_scope(self, raw_scope: str, display_scope: str) -> bool:
        """
        Return whether a scope should be flattened.

        Args:
            raw_scope:
                Original commit scope.

            display_scope:
                Mapped display scope.
        """

        if not self.config.rendering.collapse_generic_scopes:
            return False

        generic = {
            scope.casefold()
            for scope in self.config.rendering.generic_scopes
        }

        return (
            raw_scope.strip().casefold() in generic
            or display_scope.strip().casefold() in generic
        )

    def _append_item(
        self,
        destination: list[str],
        item: str,
        seen: set[str],
    ) -> None:
        """
        Normalize and append one renderable item.

        Args:
            destination:
                List receiving the item.

            item:
                Raw item text.

            seen:
                Existing normalized keys for the group.
        """

        normalized = self._normalize_item(item)
        key = re.sub(r"\s+", " ", normalized).strip().casefold()

        if not normalized:
            return

        if self.config.rendering.deduplicate:
            if key in seen:
                return

            if any(
                self._items_are_similar(key, existing)
                for existing in seen
            ):
                return

        seen.add(key)
        destination.append(normalized)

    @staticmethod
    def _items_are_similar(first: str, second: str) -> bool:
        """
        Detect near-duplicate release-announcement wording.

        The comparison uses a containment score so consolidated
        final-release wording wins over shorter prerelease variants
        while unrelated changes remain visible.

        Args:
            first:
                First normalized item.

            second:
                Second normalized item.

        Returns:
            ``True`` when the meaningful word overlap is high.
        """

        ignored = {
            "a",
            "an",
            "and",
            "for",
            "from",
            "in",
            "of",
            "on",
            "or",
            "the",
            "to",
            "via",
            "when",
            "with",
        }

        def tokens(value: str) -> set[str]:
            return {
                token
                for token in re.findall(r"[a-z0-9]+", value.casefold())
                if token not in ignored
            }

        first_tokens = tokens(first)
        second_tokens = tokens(second)
        smaller = min(len(first_tokens), len(second_tokens))

        if smaller < 3:
            return False

        overlap = len(first_tokens & second_tokens)

        return overlap >= 3 and overlap / smaller >= 0.65

    @staticmethod
    def _normalize_item(item: str) -> str:
        """
        Normalize a Markdown change item without rewriting prose.

        Args:
            item:
                Item to normalize.

        Returns:
            Clean item text.
        """

        value = item.strip()
        value = re.sub(r"^(?:[-*+]|\u2022)\s+", "", value)
        value = re.sub(r"^(?:✅|☑️|✔️)\s*", "", value)

        if value.casefold().startswith(("changelog:", "tag:")):
            return ""

        return value.strip()

    @staticmethod
    def _normalize_tag(value: str) -> str:
        """
        Normalize a release tag value for inline display.

        Args:
            value:
                Raw tag value.

        Returns:
            Clean display tag.
        """

        tag = value.strip().strip("`*_\"")
        tag = tag.lstrip("#").strip()
        tag = re.sub(r"\s+", "-", tag)

        return tag.casefold()
