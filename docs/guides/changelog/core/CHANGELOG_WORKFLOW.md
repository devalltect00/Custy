<!-- docs/guides/changelog/core/CHANGELOG_WORKFLOW.md -->

# Changelog Workflow

Custy generates `CHANGELOG.md` from Conventional Commit messages,
structured Markdown sections, Git tags, and the optional pending
commit template.

## Recommended commit format

Simple commits may use a subject and optional bullets:

```text
fix(workflow): prevent unsafe release execution

- Prevent execution when staged files exist.
- Improve merge validation.
```

Rich release commits may contain several semantic sections:

```markdown
feat(release): 1.10.6

Final release of Custy 1.10.6.

### Bug Fixes

- Prevent unsafe execution.

### Templates

- Expand the commit template.

### Documentation

#### Project Structure

- Update the architecture guide.
```

Custy preserves meaningful subsections such as `Workflow` and
`Project Structure`. Generic scopes such as `main`, `core`,
`general`, `changelog`, and `release` are flattened by default.

## Generate the changelog

Run:

```powershell
custy changelog generate
```

Generation performs these steps:

1. Read tags and commit messages through the Git service.
2. Add the pending commit message to `Unreleased` when enabled.
3. Parse semantic sections and top-level bullets.
4. Filter merge commits and configured commit types.
5. Group and deduplicate user-facing changes.
6. Build release summaries, comparisons, promoted versions, and tags.
7. Render `CHANGELOG.md` through the configured Jinja template.

## Release comparison rules

- `Unreleased` compares the latest tag with `HEAD`.
- A beta compares with the previous stable release.
- A release candidate compares with the adjacent beta or release candidate.
- A final stable release compares with the previous stable release.
- The final stable release aggregates changes from its prerelease family.
- Individual beta and release-candidate entries remain visible.

For example:

```text
1.10.5...1.10.6b1
1.10.6b1...1.10.6rc1
1.10.6rc3...1.10.6rc4
1.10.5...1.10.6
```

## Review checklist

After generation, verify:

- `Unreleased` is first when it contains changes.
- Version and date share one heading line.
- Stable releases use previous-stable comparisons.
- Sections contain real change items.
- Generic scopes do not create redundant headings.
- Tags contain no raw hash or backtick markers.
- List items use valid Markdown indentation.

Do not manually repair generated output. Fix the source commit,
configuration, parser, or template and generate it again.
