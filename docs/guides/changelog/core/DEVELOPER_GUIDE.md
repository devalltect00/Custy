<!-- docs/guides/changelog/core/DEVELOPER_GUIDE.md -->

# Changelog Developer Guide

The changelog subsystem is a config-driven pipeline with a strict
domain-to-rendering contract.

## Architecture

```text
Git and pending providers
        ↓
ChangelogGenerator release planning
        ↓
Cleaner and CommitParser
        ↓
Semantic section expansion and filtering
        ↓
Type and scope grouping
        ↓
ChangelogRenderContext adapter
        ↓
JinjaRenderer
        ↓
CHANGELOG.md
```

### Providers

Providers return raw messages only. They do not parse, clean, group,
or render content. Git behavior remains isolated behind `GitService`.

### Generator

`ChangelogGenerator` owns release orchestration:

- stable versus prerelease range selection;
- stable-release prerelease aggregation;
- comparison URLs;
- release announcement selection;
- summaries, promoted versions, and display tags;
- final release ordering and rendering.

### Processing pipeline

`ChangelogProcessingPipeline` performs:

1. Safe line-oriented cleaning.
2. Conventional Commit parsing.
3. Semantic expansion of `###` sections.
4. Merge, ignored-type, and breaking-change handling.
5. Content-aware deduplication.
6. Type and scope grouping.

A body containing Features, Bug Fixes, and Documentation is expanded
into three semantic groups even when its Conventional Commit header
has only one type.

### Domain model

The active hierarchy is:

```text
Changelog
└── Release
    └── CommitGroup
        └── CommitScope
            └── Commit
                └── CommitSection
                    └── CommitSubsection
```

Domain attributes include:

- `CommitGroup.commit_type`
- `CommitScope.commits`
- `CommitSection.items`
- `CommitSection.subsections`

Templates must not invent alternate attributes such as
`scope.sections`, `section.body`, or `section.children`.

### Rendering adapter

`ChangelogRenderContext` converts domain groups into `RenderedGroup`
and `RenderedSubsection` values. It is responsible for:

- mapped group and scope titles;
- generic-scope collapsing;
- item and tag normalization;
- rendered-item deduplication;
- configured sorting;
- fallback subjects for commits without body bullets.

Jinja uses only this documented adapter. `StrictUndefined` is enabled
so future model/template mismatches fail immediately instead of
silently producing empty sections.

## Configuration

Changelog settings live under `[tool.custy.changelog.*]` in
`.config/custy/config.toml`. Runtime and packaged defaults must remain
synchronized in:

```text
.config/custy/config.toml
app/templates/config.toml
```

The runtime and packaged templates must also remain synchronized:

```text
.config/custy/templates/changelog/changelog.j2
app/templates/changelog/changelog.j2
```

## Testing requirements

Changes to the subsystem should cover:

- parser and processing behavior;
- stable and prerelease boundaries;
- release ordering;
- rendering against the golden ideal-output fixture;
- raw tag and Markdown normalization.

The golden fixture is intentionally model-based. It catches both
template regressions and domain/template contract mismatches.
