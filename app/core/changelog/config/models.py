# app/core/changelog/config/models.py

"""
Changelog Configuration Models

Typed configuration models used by the changelog subsystem.

These models provide a strongly typed representation of the
configuration loaded from ``config.toml``.

Used by:
    - ChangelogConfigResolver
    - ChangelogGenerator
    - Processing
    - Rendering
    - Integration
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.core.changelog.integration.placement import (
    PendingCommitPlacement,
)
from app.core.changelog.integration.generation import (
    PendingCommitGeneration,
)


# ==========================================================
# Core
# ==========================================================


@dataclass(slots=True)
class CoreConfig:
    """
    Core changelog generation configuration.

    Controls which commits participate in
    changelog generation before preprocessing
    and rendering begin.
    """

    ignore_merge_commits: bool = True

    ignore_types: list[str] = field(
        default_factory=list,
    )


# ==========================================================
# Pending Commit
# ==========================================================


@dataclass(slots=True)
class PendingCommitConfig:
    """
    Configuration for pending commit integration.

    Attributes:
        enabled:
            Enable pending commit integration.

        generation:
            Generation strategy.

            Supported values:
                - append
                - regenerate

        placement:
            Placement of the pending commit relative to the
            generated changelog.
    """

    enabled: bool = False

    generation: PendingCommitGeneration = (
        PendingCommitGeneration.APPEND
    )

    placement: PendingCommitPlacement = (
        PendingCommitPlacement.BEFORE
    )


# ==========================================================
# Cleaning
# ==========================================================


@dataclass(slots=True)
class CleaningConfig:
    """
    Commit cleaning configuration.
    """

    remove_separators: list[str] = field(
        default_factory=lambda: ["---"]
    )

    remove_headers: bool = False

    remove_hash_lines: bool = False

    remove_release_summary: bool = False

    remove_metadata: bool = False

    remove_keywords: list[str] = field(
        default_factory=list
    )


# ==========================================================
# Release Processing
# ==========================================================


@dataclass(slots=True)
class ReleaseConfig:
    """
    Release processing configuration.
    """

    extract_bullets_only: bool = True

    fallback_to_subject: bool = True


# ==========================================================
# Release Behavior
# ==========================================================


@dataclass(slots=True)
class ReleaseBehavior:
    """
    Rendering behavior for a specific release.
    """

    hidden: bool = False

    title_only: bool = False

    custom_message: str | None = None


@dataclass(slots=True)
class ReleaseBehaviorConfig:
    """
    Release rendering behavior configuration.

    Stores rendering behavior for specific release
    versions.
    """

    behavior: dict[
        str,
        ReleaseBehavior,
    ] = field(
        default_factory=dict
    )


# ==========================================================
# Repository Links
# ==========================================================


@dataclass(slots=True)
class LinksConfig:
    """
    Repository link configuration.
    """

    repository: str | None = None

    enable_compare: bool = False


# ==========================================================
# Rendering
# ==========================================================


@dataclass(slots=True)
class RenderingConfig:
    """
    Rendering configuration.

    Controls how the generated changelog is rendered.

    These settings affect presentation only and never
    modify commit collection, preprocessing, grouping,
    or release processing.
    """

    # ======================================================
    # General
    # ======================================================

    show_title: bool = True

    show_description: bool = True

    show_release_status: bool = True

    show_summary: bool = True

    show_promoted_from: bool = True

    show_compare_link: bool = True

    # ======================================================
    # Layout
    # ======================================================

    group_by_scope: bool = True

    collapse_generic_scopes: bool = True

    generic_scopes: list[str] = field(
        default_factory=lambda: [
            "",
            "main",
            "core",
            "general",
            "default",
            "root",
            "changelog",
            "release",
        ]
    )

    deduplicate: bool = True

    show_empty_sections: bool = False

    show_empty_groups: bool = False

    show_empty_scopes: bool = False

    show_empty_metadata: bool = False

    show_empty_tags: bool = False

    # ======================================================
    # Metadata
    # ======================================================

    show_metadata: bool = True

    show_tags: bool = True

    show_contributors: bool = False

    show_statistics: bool = False

    # ======================================================
    # Formatting
    # ======================================================

    bullet: str = "-"

    indent: int = 0

    blank_lines_between_releases: int = 2

    blank_lines_between_commit_groups: int = 1

    # ======================================================
    # Sorting
    # ======================================================

    sort_groups: bool = False

    sort_scopes: bool = True

    sort_items: bool = False

    # ======================================================
    # Visual
    # ======================================================

    show_section_icons: bool = True

    show_footer: bool = False


# ==========================================================
# Breaking Changes
# ==========================================================


@dataclass(slots=True)
class BreakingConfig:
    """
    Breaking change detection configuration.
    """

    enabled: bool = False

    keywords: list[str] = field(
        default_factory=list
    )

    label: str = "Breaking Changes"


# ==========================================================
# Scope Mapping
# ==========================================================


@dataclass(slots=True)
class ScopeMappingConfig:
    """
    Commit scope mapping configuration.

    Maps commit scopes to display scopes used
    during changelog rendering.
    """

    mapping: dict[str, str] = field(
        default_factory=dict
    )


# ==========================================================
# Type Mapping
# ==========================================================


@dataclass(slots=True)
class TypeMappingConfig:
    """
    Commit type mapping configuration.

    Maps Conventional Commit types to
    display titles used during changelog
    rendering.
    """

    mapping: dict[str, str] = field(
        default_factory=dict,
    )


# ==========================================================
# Advanced
# ==========================================================


@dataclass(slots=True)
class AdvancedConfig:
    """
    Experimental changelog features.
    """

    auto_detect_type: bool = False

    detect_breaking_changes: bool = False

    smart_formatting: bool = False


# ==========================================================
# Root Configuration
# ==========================================================


@dataclass(slots=True)
class ChangelogConfig:
    """
    Root changelog configuration.

    Every changelog component receives this
    object instead of reading directly from
    ConfigLoader.
    """

    core: CoreConfig = field(
        default_factory=CoreConfig,
    )

    pending_commit: PendingCommitConfig = field(
        default_factory=PendingCommitConfig,
    )

    cleaning: CleaningConfig = field(
        default_factory=CleaningConfig,
    )

    release: ReleaseConfig = field(
        default_factory=ReleaseConfig,
    )

    release_behavior: ReleaseBehaviorConfig = field(
        default_factory=ReleaseBehaviorConfig,
    )

    links: LinksConfig = field(
        default_factory=LinksConfig,
    )

    rendering: RenderingConfig = field(
        default_factory=RenderingConfig,
    )

    breaking: BreakingConfig = field(
        default_factory=BreakingConfig,
    )

    scope_mapping: ScopeMappingConfig = field(
        default_factory=ScopeMappingConfig,
    )

    type_mapping: TypeMappingConfig = field(
        default_factory=TypeMappingConfig,
    )

    advanced: AdvancedConfig = field(
        default_factory=AdvancedConfig,
    )
