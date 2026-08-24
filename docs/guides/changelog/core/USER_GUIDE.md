<!-- docs/guides/changelog/core/USER_GUIDE.md -->

# Changelog User Guide

Custy generates a release-oriented `CHANGELOG.md` from Git history and
structured commit messages.

## Basic usage

Write a Conventional Commit:

```text
feat(cli): add release confirmation

- Ask before continuing with an unsafe release.
```

Then generate the changelog:

```powershell
custy changelog generate
```

The result is written to `CHANGELOG.md`.

## Structured commit bodies

Section headings are optional. A simple body bullet is placed beneath
the commit's Conventional Commit type:

```text
fix(core): correct documentation typo

- Correct the installation example.
```

For a rich commit, use semantic sections:

```markdown
feat(workflow): improve release safety

### Features

- Add workflow validation.

### Bug Fixes

#### Git

- Prevent invalid tag creation.
```

Custy preserves the meaningful `Git` subsection. Generic scopes such
as `main` and `core` are hidden by default because they add little
reader-facing information.

## Generated release layout

Each release can contain:

```markdown
## 1.10.6 (2025-08-06)

🔗 Compare:
https://github.com/example/project/compare/1.10.5...1.10.6

**Release**
Stable

**Summary**

Final release of Custy 1.10.6.

Promoted from:

- 1.10.6rc1
- 1.10.6b1

### Bug Fixes

- Prevent unsafe execution.

**Tags**

release • workflow • bugfix • stable
```

## Pending changes

When `[tool.custy.changelog.pending_commit].enabled` is `true`, the
configured commit-message template participates in `Unreleased`.
Placeholder lines configured in `remove_keywords` are omitted.

## Important configuration

Settings are read from `.config/custy/config.toml`:

```toml
[tool.custy.changelog.core]
ignore_merge_commits = true
ignore_types = ["chore"]

[tool.custy.changelog.render]
group_by_scope = true
collapse_generic_scopes = true
generic_scopes = ["", "main", "core", "general", "changelog", "release"]
deduplicate = true
bullet = "-"
indent = 0
```

Use zero indentation with `-` for normal Markdown list items. Four
leading spaces turn a list into a Markdown code block.

## Troubleshooting

If a commit is missing, check whether:

- it is a merge commit;
- its type appears in `ignore_types`;
- its body contains only configured placeholder text;
- the commit follows `type(scope): subject` syntax.

If a scope heading is missing, it may be intentionally collapsed as a
generic scope. Remove it from `generic_scopes` to preserve the heading.
