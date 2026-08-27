# app/core/changelog/config/resolver.py

"""
Changelog Configuration Resolver

Loads and converts changelog configuration from
``config.toml`` into strongly typed configuration
models.

This is the only component within the changelog
subsystem that directly accesses ``ConfigLoader``.
"""

from __future__ import annotations

from enum import Enum
from typing import TypeVar

from app.config.config_loader import ConfigLoader
from app.core.changelog.config.models import (
    AdvancedConfig,
    BreakingConfig,
    ChangelogConfig,
    CleaningConfig,
    CoreConfig,
    LinksConfig,
    PendingCommitConfig,
    ReleaseBehavior,
    ReleaseBehaviorConfig,
    ReleaseConfig,
    RenderingConfig,
    ScopeMappingConfig,
    TypeMappingConfig,
)
from app.core.changelog.integration.generation import (
    PendingCommitGeneration,
)
from app.core.changelog.integration.placement import (
    PendingCommitPlacement,
)

EnumType = TypeVar("EnumType", bound=Enum)


class ChangelogConfigResolver:
    """
    Resolve changelog configuration from
    ``config.toml``.
    """

    def __init__(self) -> None:
        """
        Initialize the configuration resolver.
        """

        self._loader = ConfigLoader()

    def load(self) -> ChangelogConfig:
        """
        Load changelog configuration.

        Returns:
            Strongly typed changelog configuration.
        """

        return ChangelogConfig(
            core=self._load_core(),
            pending_commit=self._load_pending_commit(),
            cleaning=self._load_cleaning(),
            release=self._load_release(),
            release_behavior=self._load_release_behavior(),
            links=self._load_links(),
            rendering=self._load_rendering(),
            breaking=self._load_breaking(),
            scope_mapping=self._load_scope_mapping(),
            type_mapping=self._load_type_mapping(),
            advanced=self._load_advanced(),
        )

    # ======================================================
    # Core
    # ======================================================

    def _load_core(
        self,
    ) -> CoreConfig:
        """
        Load core changelog configuration.
        """

        config = self._loader.get(
            "changelog",
            "core",
            default={},
        )

        return CoreConfig(
            ignore_merge_commits=config.get(
                "ignore_merge_commits",
                True,
            ),
            ignore_types=config.get(
                "ignore_types",
                [],
            ),
        )

    # ======================================================
    # Pending Commit
    # ======================================================

    def _as_dict(self, value: object) -> dict:
        """
        Normalize config section value to dictionary.

        Any non-dict value is treated as an empty dict
        to prevent shape-related runtime errors.
        """

        if isinstance(value, dict):
            return value

        return {}

    def _safe_enum_value(
        self,
        enum_cls: type[EnumType],
        raw_value: object,
        default_enum: EnumType,
    ) -> EnumType:
        """
        Safely coerce config value to enum.

        Falls back to default when input is invalid.
        """

        if isinstance(raw_value, enum_cls):
            return raw_value

        try:
            return enum_cls(raw_value)
        except Exception:
            return default_enum

    def _non_negative_int(
        self,
        value: object,
        default: int,
    ) -> int:
        """
        Normalize integer values used by rendering config.

        Invalid values fall back to default.
        Negative values are clamped to 0.
        """

        if not isinstance(value, int):
            return default

        return max(0, value)

    def _load_pending_commit(
        self,
    ) -> PendingCommitConfig:
        """
        Load pending commit configuration.
        """

        config = self._as_dict(
            self._loader.get(
                "changelog",
                "pending_commit",
                default={},
            )
        )

        return PendingCommitConfig(
            enabled=config.get(
                "enabled",
                False,
            ),
            generation=self._safe_enum_value(
                PendingCommitGeneration,
                config.get(
                    "generation",
                    PendingCommitGeneration.APPEND.value,
                ),
                PendingCommitGeneration.APPEND,
            ),
            placement=self._safe_enum_value(
                PendingCommitPlacement,
                config.get(
                    "placement",
                    PendingCommitPlacement.BEFORE.value,
                ),
                PendingCommitPlacement.BEFORE,
            ),
        )

    # ======================================================
    # Cleaning
    # ======================================================

    def _load_cleaning(
        self,
    ) -> CleaningConfig:
        """
        Load cleaning configuration.
        """

        config = self._loader.get(
            "changelog",
            "cleaning",
            default={},
        )

        return CleaningConfig(
            remove_separators=config.get(
                "remove_separators",
                ["---"],
            ),
            remove_headers=config.get(
                "remove_headers",
                False,
            ),
            remove_hash_lines=config.get(
                "remove_hash_lines",
                False,
            ),
            remove_release_summary=config.get(
                "remove_release_summary",
                False,
            ),
            remove_metadata=config.get(
                "remove_metadata",
                False,
            ),
            remove_keywords=config.get(
                "remove_keywords",
                [],
            ),
        )

    # ======================================================
    # Release
    # ======================================================

    def _load_release(
        self,
    ) -> ReleaseConfig:
        """
        Load release processing configuration.
        """

        config = self._loader.get(
            "changelog",
            "release",
            default={},
        )

        return ReleaseConfig(
            extract_bullets_only=config.get(
                "extract_bullets_only",
                True,
            ),
            fallback_to_subject=config.get(
                "fallback_to_subject",
                True,
            ),
        )

    # ======================================================
    # Release Behavior
    # ======================================================

    def _load_release_behavior(
        self,
    ) -> ReleaseBehaviorConfig:
        """
        Load release behavior configuration.
        """

        config = self._as_dict(
            self._loader.get(
                "changelog",
                "release_behavior",
                default={},
            )
        )

        behavior: dict[
            str,
            ReleaseBehavior,
        ] = {}

        for version, values in config.items():
            value_dict = self._as_dict(values)

            release_behavior = ReleaseBehavior(
                hidden=value_dict.get(
                    "hidden",
                    False,
                ),
                title_only=value_dict.get(
                    "title_only",
                    False,
                ),
                custom_message=value_dict.get(
                    "custom_message",
                ),
            )

            # Normalize conflicting state:
            # hidden overrides title_only/custom_message.
            if release_behavior.hidden:
                release_behavior.title_only = False
                release_behavior.custom_message = None

            behavior[version] = release_behavior

        return ReleaseBehaviorConfig(
            behavior=behavior,
        )

    # ======================================================
    # Links
    # ======================================================

    def _load_links(
        self,
    ) -> LinksConfig:
        """
        Load repository link configuration.
        """

        config = self._loader.get(
            "changelog",
            "links",
            default={},
        )

        return LinksConfig(
            repository=config.get(
                "repository",
            ),
            enable_compare=config.get(
                "enable_compare",
                False,
            ),
        )

    # ======================================================
    # Rendering
    # ======================================================

    def _load_rendering(
        self,
    ) -> RenderingConfig:
        """
        Load rendering configuration.
        """

        config = self._as_dict(
            self._loader.get(
                "changelog",
                "render",
                default={},
            )
        )

        return RenderingConfig(
            #
            # ==================================================
            # General
            # ==================================================
            #
            show_title=config.get(
                "show_title",
                True,
            ),
            show_description=config.get(
                "show_description",
                True,
            ),
            show_release_status=config.get(
                "show_release_status",
                True,
            ),
            show_summary=config.get(
                "show_summary",
                True,
            ),
            show_promoted_from=config.get(
                "show_promoted_from",
                True,
            ),
            show_compare_link=config.get(
                "show_compare_link",
                True,
            ),
            #
            # ==================================================
            # Layout
            # ==================================================
            #
            group_by_scope=config.get(
                "group_by_scope",
                True,
            ),
            collapse_generic_scopes=config.get(
                "collapse_generic_scopes",
                True,
            ),
            generic_scopes=[
                str(scope).strip().lower()
                for scope in config.get(
                    "generic_scopes",
                    [
                        "",
                        "main",
                        "core",
                        "general",
                        "default",
                        "root",
                        "changelog",
                        "release",
                    ],
                )
            ],
            deduplicate=config.get(
                "deduplicate",
                True,
            ),
            show_empty_sections=config.get(
                "show_empty_sections",
                False,
            ),
            show_empty_groups=config.get(
                "show_empty_groups",
                False,
            ),
            show_empty_scopes=config.get(
                "show_empty_scopes",
                False,
            ),
            show_empty_metadata=config.get(
                "show_empty_metadata",
                False,
            ),
            show_empty_tags=config.get(
                "show_empty_tags",
                False,
            ),
            #
            # ==================================================
            # Metadata
            # ==================================================
            #
            show_metadata=config.get(
                "show_metadata",
                True,
            ),
            show_tags=config.get(
                "show_tags",
                True,
            ),
            show_contributors=config.get(
                "show_contributors",
                False,
            ),
            show_statistics=config.get(
                "show_statistics",
                False,
            ),
            #
            # ==================================================
            # Formatting
            # ==================================================
            #
            bullet=config.get(
                "bullet",
                "-",
            ),
            indent=self._non_negative_int(
                config.get(
                    "indent",
                    0,
                ),
                0,
            ),
            blank_lines_between_releases=self._non_negative_int(
                config.get(
                    "blank_lines_between_releases",
                    2,
                ),
                2,
            ),
            blank_lines_between_commit_groups=self._non_negative_int(
                config.get(
                    "blank_lines_between_commit_groups",
                    1,
                ),
                1,
            ),
            #
            # ==================================================
            # Sorting
            # ==================================================
            #
            sort_groups=config.get(
                "sort_groups",
                False,
            ),
            sort_scopes=config.get(
                "sort_scopes",
                True,
            ),
            sort_items=config.get(
                "sort_items",
                False,
            ),
            #
            # ==================================================
            # Visual
            # ==================================================
            #
            show_section_icons=config.get(
                "show_section_icons",
                True,
            ),
            show_footer=config.get(
                "show_footer",
                False,
            ),
        )

    # ======================================================
    # Breaking
    # ======================================================

    def _load_breaking(
        self,
    ) -> BreakingConfig:
        """
        Load breaking change configuration.
        """

        config = self._loader.get(
            "changelog",
            "breaking",
            default={},
        )

        return BreakingConfig(
            enabled=config.get(
                "enabled",
                False,
            ),
            keywords=config.get(
                "keywords",
                [],
            ),
            label=config.get(
                "label",
                "Breaking Changes",
            ),
        )

    # ======================================================
    # Scope Mapping
    # ======================================================

    def _load_scope_mapping(
        self,
    ) -> ScopeMappingConfig:
        """
        Load scope mapping configuration.
        """

        config = self._as_dict(
            self._loader.get(
                "changelog",
                "scope_map",
                default={},
            )
        )

        return ScopeMappingConfig(
            mapping=config,
        )

    # ======================================================
    # Type Mapping
    # ======================================================

    def _load_type_mapping(
        self,
    ) -> TypeMappingConfig:
        """
        Load commit type mapping configuration.
        """

        config = self._as_dict(
            self._loader.get(
                "changelog",
                "type_map",
                default={},
            )
        )

        return TypeMappingConfig(
            mapping=config,
        )

    # ======================================================
    # Advanced
    # ======================================================

    def _load_advanced(
        self,
    ) -> AdvancedConfig:
        """
        Load advanced changelog configuration.
        """

        config = self._as_dict(
            self._loader.get(
                "changelog",
                "advanced",
                default={},
            )
        )

        return AdvancedConfig(
            auto_detect_type=config.get(
                "auto_detect_type",
                False,
            ),
            detect_breaking_changes=config.get(
                "detect_breaking_changes",
                False,
            ),
            smart_formatting=config.get(
                "smart_formatting",
                False,
            ),
        )
