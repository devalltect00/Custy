<!-- docs/TODO_tracking_history_v2.1.0.md -->

# Custy TODO Tracking History — v2.1.0

> Current status: see the [2026-09-06 checkpoint update](#checkpoint-8-2026-09-06).
> Older checkboxes, test counts, plans, and decisions are preserved as recorded;
> they are historical context, not proof that every current release gate passed.

> Cumulative snapshot for **v2.1.0**. Earlier history, unfinished work,
> considerations, ideas, cancelled items, and notes are intentionally retained.

Personal notes, planning, and roadmap for **Custy**

---

## ✨ Feature

### ✅ Completed

Earlier

- [x] handle custy Full workflow
- [x] handle custy "git add ."
- [x] handle custy generate changelog
- [x] handle custy as a tool
- [x] handle custy command and put in makefile
- [x] Fix issue where added to stage and commit after change version on `.cz.toml` and `app/__version__.py` files
- [x] Make own feature like/inspired by/like command `cz check`
- [x] fixing pre-release version format using pep440 for python
- [x] Use format [Epoch!]MAJOR.MINOR.PATCH[Pre-release][Post-release][Development][+Local] the pep440 for python
- [x] support Post-release, development, local identifiers, and epoch segment
- [x] support 'release' on commit type

Since v1.4.0

- [x] if the current version is pre-release or post or dev and so on. If we want to increment. let's say from rc, next version is rc, the major, minor, and patch won't change. same as from alpha to beta. but not beta to alpha because beta 1 higher level than alpha. for example from v.1.2.3rc1 to v.1.2.3rc2 instead of v.1.2.3rc1 to v.1.2.4rc2; another example from v.1.2.3b1 to v.1.2.3b2 instead of v.1.2.3b1 to v.1.2.4b2;
- [x] generate changelog when on release version. So check if the version is major.minor.patch. So allowed to generate changelog and push the changelog
- [x] Check if the commit type not [feat, fix, perf, docs, refactor] don't bump or use tagging. Id use types [feat, fix, perf, docs, refactor] we need to use specific parameter if we want to force bump or tagging; or maybe there are better suggestion.
  - Option 1: keep/still bumping and tagging but give warning;
  - Option 2: prevent bumping and tagging;
  - Option 3: must use additional specific parameter if want to use bumping or tagging;
  - Option 4: must use additional specific CLI parameter if want to use bumping or tagging;
  - or other better options
- [x] need to check what type of project before making the versioning. We already have versioning custom format configuration for python. at least we have python and javascript whether for electron js, react js, next js, and so on
- [x] when tagging. instead of put message on CLI args. it's better to open files as tagging message same like we already have for commit-msg. If we also specify specific parameter that tells use default tagging message. maybe there are a better solutions
- [x] for release version, check all pre-lease, develop (and so on that needed) version commit message combine the all the commit body, description (etc that needed) into 1 as template for release version when for example from pre-release to release and put to external txt file (commit-msg.txt)
- [x] from pre-release or dev, etc to release. No need to change the major.minor.patch. for example from v.1.2.3rc1 to v.1.2.3 instead of v.1.2.3rc1 to v.1.2.4
  - Option 1. level the tag message be like that (no changes)
  - Option 2. the tag message based on commit message
  - Option 3. manually every time commit the tag
  - Option 4. maybe there are some better and best options and solutions
- [x] Backup just 10 maxiumum. 10 lastest/newest backup or we can set on CLI. by default 10
- [x] Fix issue where to put backups, templates folders/directory. also with commit-msg.txt if needed
- [x] handle cleanup backups CLI

Since v1.5.0

- [x] Bug fix and Make commit-msg.txt and tag-msg.txt with some automation if possible. Ref: docs\git\commit_message.md
- [x] Make sure backup and add all of them to stages before commit and push
- [x] add feature to force commit even no staged changes detected
- [x] bug fix error where now on post tag and now bump in the same post tag for example 1.5.0.post1 → 1.5.0.post2
- [x] Give template commit message git-msg.txt

Since v1.7.1

- [x] fix the file name from pep404_strategy.py to pep440_strategy.py and class name from PEP404Strategy to PEP440Strategy
- [x] bug fix when switch from release to post-release use the same version as release but use the post-release format so for example: from 1.5.0 → 1.5.0.post1 instead of from 1.5.0 → 1.6.0.post1
- [x] bug fixed, docs, and refactor the SemverStrategy and PEP440Strategy class
- [x] Add tests to test SemverStrategy and PEP440Strategy class
- [x] add new documentation `switching version.md`
- [x] handle verbose results, the process before generating CHANGELOG.md

Since v1.8.0

- [x] use 2 branch; `main` and `develop`; `main` is stable one and `develop` is more experimental
- [x] use 2 git remote, gitlab as main, and github as backup
- [x] use and applied branching workflow checking
- [x] Fix bug amd refactor WorkflowManager

Since v1.9.0

- [x] Make better CLI
- [x] Make sure they use valid path, to prevent ambiguity. ["app/__version__.py", ".cz.toml", "template" (and its child), "docs", "tests", "tools/templates/changelog.j2", ".cz_changelog.j2", ".custor.toml", ".editorconfig", ".gitignore", ".projectignore", "CHANGELOG.md", "Makefile", "pyproject.toml"]
- [x] Add specific args CLI, if true don't debug, or silent run
- [x] add gitlab pipeline job at least run test on gitlab and github workflow
- [x] make `how to use` documentation. We can use the formal or friendly language style
- [x] Make better documentations, Readme.md file
- [x] bug fixed where need to check the allowed commit type before resolve version
- [x] bug fixed where unable to create pipeline
- [x] clean project app
- [x] Regenerate project structure documentation
- [x] Format code
- [x] Make sure it is ready to use, installing and usage

Since v1.10.0

- [x] advancing workflow manager functionality
- [x] add test for transition_case on workflow_manager and its helper
- [x] fix bug. Bugs: handling errors when the repository detected is new and no commits yet
- [x] fix little bugs and typo.

## Since v2.0.0-rc.1

### Version context

| Field                 | Value                                                                                                            |
| --------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Version               | `v2.0.0-rc.1`                                                                                                    |
| Previous release line | `1.10.x`                                                                                                         |
| Release type          | Major release candidate                                                                                          |
| Version strategy      | Semantic Versioning                                                                                              |
| Runtime policy        | Python 3.14+                                                                                                     |
| Purpose               | Validate the redesigned CLI, configuration, pipelines, changelog, and release foundation before stable promotion |

### Completed release-candidate scope

#### CLI and workflows

- [x] Replace the monolithic `argparse` entry point with a Typer and Rich CLI.
- [x] Add focused `init`, `validate`, `version`, `changelog`, `backup`, `cleanup`, `commit`, `tag`, and `push` commands.
- [x] Add `custy run dev`, `custy run release`, and `custy run full` profiles plus ordered custom steps.
- [x] Add global dry-run, debug, logging, progress, summaries, and actionable error output.
- [x] Keep the workflow-policy command explicitly experimental.

#### Configuration and templates

- [x] Replace `.custor.toml` with `.config/custy/config.toml`.
- [x] Add CLI → configuration → default resolution across project, Git, workflow, cleanup, logging, and changelog settings.
- [x] Separate packaged defaults under `app/templates` from project-owned files under `.config/custy`.
- [x] Support selective initialization and nested template/example copying.

#### Changelog, versioning, and Git

- [x] Rebuild changelog generation around parsing, cleaning, grouping, deduplication, sorting, integration, links, statistics, and Jinja rendering.
- [x] Add determinate progress for `Unreleased` and every discovered Git tag.
- [x] Preserve SemVer, PEP 440, Commitizen, date, and Git-count strategies behind focused interfaces.
- [x] Separate Git execution and service responsibilities with structured results and clearer failures.
- [x] Add multi-remote behavior, staging modes, annotated tags, message backups, retention cleanup, and protected branch cleanup.

#### Safety and maintainability

- [x] Apply the dry-run contract to initialization, versioning, changelog, backup, cleanup, commit, tag, push, pipelines, and experimental workflows.
- [x] Allow read-only discovery during dry-run while simulating file, editor, Git, and remote mutations.
- [x] Separate CLI, core, pipeline, Git, configuration, UI, template, and shared-error responsibilities.
- [x] Add centralized console and rotating-file logging without exposing secrets.

#### Delivery and documentation

- [x] Add modular Make, Docker, Docker Compose, GitHub Actions, GitLab CI, packaging, and pre-commit workflows.
- [x] Expand CLI, core, integration, regression, dry-run, changelog, cleanup, logging, and UI tests.
- [x] Refresh the README and project metadata for the 2.0 command and packaging model.
- [x] Publish comprehensive English and Indonesian guidance in the Devalltect documentation portal.
- [x] Prepare distinct internal commit and public tag/release messages for RC.1 and stable 2.0.0.

### Breaking-change checklist

- [x] Document the Python 3.14+ requirement.
- [x] Document migration from `.custor.toml` to `.config/custy/config.toml`.
- [x] Document the new command hierarchy and `custy run` profiles.
- [x] Document replacement cleanup and changelog commands.
- [x] Document the new template layout, entry point, pipeline model, and internal extension boundaries.

### RC validation and release checklist

- [ ] Validate initialization and configuration migration in a disposable 1.x-style repository.
- [ ] Run `custy validate` against representative supported projects.
- [ ] Verify `custy --dry-run run dev` and `custy --dry-run run release` do not mutate project, Git, or remote state.
- [ ] Validate message templates, changelog output, backup retention, cleanup rules, and configured remotes.
- [ ] Complete approved tests, coverage, lint, format, package, Make, Docker, Compose, and documentation checks.
- [ ] Commit, tag, publish, and verify `v2.0.0-rc.1` only with explicit release approval.

### Deferred beyond RC.1

- [ ] Complete stable-release repository cleanup after RC validation.
- [ ] Incorporate only release-blocking fixes, documentation corrections, and migration clarifications before `v2.0.0`.
- [ ] Review configured registry image names and destinations before publication.
- [ ] Keep custom tag-format conversion as future work unless separately approved.

### Notes

- This snapshot records the intended RC scope; it does not prove that Git tags,
  releases, packages, or container images were published.
- The rolling `docs/TODO_tracking_history.md` remains the source for broader
  historical notes and long-term ideas.

---

## Since v2.0.0

### Version context

| Field            | Value                                        |
| ---------------- | -------------------------------------------- |
| Version          | `v2.0.0`                                     |
| Previous version | `v2.0.0-rc.1`                                |
| Release type     | Stable major release                         |
| Version strategy | Semantic Versioning                          |
| Feature baseline | The behavior validated in `v2.0.0-rc.1`      |
| Promotion rule   | No new supported-command behavior after RC.1 |

### Stable feature baseline

- [x] Carry forward the Typer and Rich command hierarchy introduced in RC.1.
- [x] Carry forward namespaced `.config/custy/config.toml` configuration and project-owned templates.
- [x] Carry forward composable `dev`, `release`, and `full` pipelines with visible step ordering.
- [x] Carry forward rebuilt changelog parsing, integration, sorting, links, statistics, and rendering.
- [x] Carry forward SemVer, PEP 440, Commitizen, date, and Git-count version strategies.
- [x] Carry forward separated Git services, multi-remote behavior, message backups, and guarded cleanup.
- [x] Carry forward consistent dry-run simulation across project, Git, editor, and remote mutation boundaries.
- [x] Carry forward Rich UI, progress, logging, actionable errors, expanded tests, modular tooling, containers, and CI/CD.
- [x] Keep `custy workflow` experimental and visibly documented as such.

### Changes since v2.0.0-rc.1

- [x] Define stable promotion as cleanup and release finalization rather than feature expansion.
- [x] Archive the 2.0 development scope, decisions, completed work, and remaining ideas in project history.
- [x] Document historical tag normalization from PEP 440-style prerelease notation to SemVer notation.
- [x] Document recovery of missing historical GitHub Releases from their source tags.
- [x] Document rebuilding and publishing missing historical GHCR images with Reflow.
- [x] Record that reconstructed publication timestamps may differ from original software release dates.

### Repository cleanup checklist

- [ ] Remove temporary root development notes and scratch change lists after final review.
- [ ] Remove completed root and version-specific TODO files that are intentionally excluded from the stable repository.
- [ ] Confirm personal, backup, generated, and temporary artifacts are not included unintentionally.
- [ ] Preserve required source templates, documentation, tests, and release metadata.
- [ ] Review the final repository diff before release operations.

### Stable validation and publication checklist

- [ ] Run the approved full test and coverage suite.
- [ ] Run lint, formatting, pre-commit, package, and distribution validation.
- [ ] Validate CLI help, initialization, configuration, changelog, and dry-run workflows.
- [ ] Validate Make, Docker, Compose, GitHub Actions, and GitLab CI configuration.
- [ ] Verify English and Indonesian documentation links and migration guidance.
- [ ] Commit and create the `v2.0.0` tag only with explicit release approval.
- [ ] Verify GitHub and GitLab tags/releases, distributions, and container packages after publication.

### Deferred after v2.0.0

- [ ] Add project-aware source and version metadata detection across non-`app/` repository layouts.
- [ ] Improve initialization for Python, Node.js, PHP, documentation-only, mixed, and generic repositories.
- [ ] Strengthen changelog template fallback, backup routing, and CLI error boundaries.
- [ ] Refresh the Python 3.14 pre-commit toolchain and related Make workflows.
- [ ] Validate configured registry image names and destinations before publication.

### Notes

- Stable 2.0 is intended to preserve the RC.1 product contract.
- This file records preparation and verification status; unchecked publication
  tasks must not be interpreted as completed external release operations.

---

## Since v2.1.0

### Version context

| Field            | Value                                                                                       |
| ---------------- | ------------------------------------------------------------------------------------------- |
| Version          | `v2.1.0`                                                                                    |
| Previous version | `v2.0.0`                                                                                    |
| Release type     | Stable minor release                                                                        |
| Version strategy | Semantic Versioning                                                                         |
| Primary goal     | Run safely across Python, Node.js, mixed, PHP, documentation-only, and generic repositories |
| Compatibility    | Existing explicit paths remain strict; new projects default to automatic discovery          |

### Completed implementation scope

#### Project discovery

- [x] Detect Python, Node.js, PHP, mixed, and generic repository layouts from root metadata.
- [x] Resolve source directories at command runtime rather than requiring a global `app/` directory.
- [x] Prefer conventional `app/` or `src/` layouts by ecosystem and safely fall back to the project root.
- [x] Preserve strict validation for explicit `project_source` overrides.
- [x] Treat missing Custy configuration as an expected uninitialized-project state.

#### Version metadata

- [x] Discover Python `__version__.py`, static `pyproject.toml` versions, and `package.json` versions automatically.
- [x] Synchronize supported Python and Node.js metadata in mixed repositories.
- [x] Update supported root Node.js lockfile metadata.
- [x] Remove a leading `v` before storing versions in project metadata.
- [x] Preserve or add the final newline when updating Python `__version__` modules so generated metadata passes end-of-file pre-commit checks.
- [x] Support Git-tag-only versioning when no compatible version file exists.

#### Initialization and templates

- [x] Generate `project_source = "auto"` and `version_file = "auto"` for newly initialized projects.
- [x] Preserve existing Python and Node.js version metadata.
- [x] Create a Python version module only for a detected Python project that needs one.
- [x] Avoid artificial Python files in Node.js, Docusaurus, PHP, documentation-only, and generic projects.
- [x] Preserve recursive copying of nested commit and tag message examples.
- [x] Fall back to the packaged changelog template before project initialization.
- [x] Preserve project templates as overrides and reject missing explicitly configured templates clearly.
- [x] Route tag-message backups to the configured backup directory.

#### CLI, developer workflow, and containers

- [x] Route console and module execution through a protected CLI entry point.
- [x] Present expected configuration and validation failures without duplicate tracebacks.
- [x] Keep full unexpected-error tracebacks available through `--debug`.
- [x] Make a no-subcommand invocation display help and exit successfully.
- [x] Add `[tool.custy.editor]` configuration with `VISUAL` and `EDITOR` precedence, platform-specific candidate lists, and controlled fallback behavior.
- [x] Resolve Windows `code.cmd` correctly and skip unavailable editor candidates without hiding launched-process failures.
- [x] Bundle Micro, Nano, Vim, and Vi in the production image with conflict-aware undo and redo key bindings.
- [x] Suspend live Rich pipeline progress while a blocking editor owns the terminal, then restore the current step after successful or failed editing.
- [x] Expand Make targets for installing, validating, running, cleaning, updating, and refreshing pre-commit.
- [x] Run pre-commit through `python -m pre_commit` in the active virtual environment.
- [x] Refresh Ruff, pre-commit-hooks, and Black for the Python 3.14 toolchain.
- [x] Protect historical, copied, deprecated, development, and temporary files from automated formatting.
- [x] Validate production-container startup and dry-run initialization from a Docusaurus repository without `app/`.
- [x] Add adaptive `auto`, `custy`, `commitizen`, and `git` commit-message validation providers.
- [x] Detect project-owned Commitizen configuration without requiring Commitizen in every target repository.
- [x] Preserve `--check-cz` as a backward-compatible strict Commitizen override.
- [x] Preserve Git stdout, stderr, operation, and exit status when commits fail.
- [x] Classify hook failures separately from ordinary Git commit failures and surface actionable diagnostics.
- [x] Include the optional Commitizen extra in the production image.
- [x] Add native-first GitHub and GitLab HTTPS token fallback for containers without inherited host credential-manager sessions.
- [x] Add secure external file and environment sources without storing token values in project configuration.
- [x] Add `custy configure credentials` with guided setup plus `set`, `status`, `test`, and `remove` operations.
- [x] Add opt-in Docker, Compose, and remote-image Make helpers that use writable mounts only for credential setup and read-only mounts for status, testing, and runtime pushes.
- [x] Keep SSH, normal Git credential helpers, and local authentication authoritative; inject Custy's helper only for an enabled supported HTTPS push.
- [x] Prevent non-interactive credential hangs while preserving approved interactive Git prompts.
- [x] Give manual Git authentication direct terminal ownership and explain PAT input before an HTTPS prompt.
- [x] Disable Rich rendering for hidden direct-command pipelines so standalone push prompts remain stable.
- [x] Reject hidden PAT setup without an interactive TTY instead of accepting potentially echoed input.
- [x] Keep dry-run free from token reads, credential writes, and remote access tests.
- [x] Keep ordinary `main` commits on the validation path without publishing a GitHub production image.
- [x] Publish GitHub and GitLab production images only from supported annotated release tags with non-empty messages.
- [x] Publish the exact stable or prerelease tag and update `latest` only for stable releases.
- [x] Remove the redundant commit-SHA production tag while retaining Buildx provenance metadata.
- [x] Align GitLab with GitHub's annotated-tag, non-empty-message, and normalized build-version production policy.
- [x] Generate GitLab Release descriptions from reviewed annotated tag messages with project, pipeline, container, and artifact details.

#### Tests and documentation

- [x] Add detector coverage for Python, Node.js, mixed, PHP, and generic projects.
- [x] Add version-update coverage for Python modules, `pyproject.toml`, `package.json`, lockfiles, mixed projects, and tag-only projects.
- [x] Add regression coverage for final-newline preservation through direct Python metadata updates and the release workflow.
- [x] Add protected-entry-point, structured-error, no-command, template-fallback, backup-routing, and cross-project regression tests.
- [x] Add editor settings, editor service, Docker asset, workflow delegation, and exclusive-terminal progress lifecycle coverage.
- [x] Add commit-validation settings, Commitizen inspection, provider resolution, structured Git error, and hook-classification coverage.
- [x] Add credential settings, secure storage, source precedence, exact-host matching, helper protocol, CLI secrecy, dry-run, and per-push injection coverage.
- [x] Add hidden-pipeline rendering and direct Git-command routing regression coverage.
- [x] Validate 1,340 tests with 83% overall coverage and all configured quality hooks.
- [x] Validate Ruff, Black, diff whitespace, and the complete pre-commit configuration.
- [x] Validate corrected GitHub Actions and GitLab CI pipelines with active source, tests, and helper files included.
- [x] Keep generated `.pyc` files ignored and untracked without excluding active cleanup-backup packages.
- [x] Make CLI help assertions deterministic across ANSI output and different CI terminal widths.
- [ ] Rebuild the credential-enabled production image and verify the packaged
      `git-credential-custy` entry point plus a container push dry-run before
      publication. The current local attempt reached Dockerfile execution but was
      blocked by Windows pagefile/memory exhaustion rather than a source failure.
- [x] Validate the earlier editor-enabled production image baseline, resolved
      source version, editor-progress marker, and Rich suspend/restart lifecycle.
- [x] Update canonical English and Indonesian documentation for discovery, initialization, versioning, errors, Docker, editors, terminal-progress handoff, commit validation, Git hooks, pre-commit, testing, and contributing.

### Upgrade checklist from v2.0.0

- [x] Document that existing explicit paths are not rewritten automatically.
- [x] Document switching `project_source` and `version_file` to `"auto"` when discovery is preferred.
- [x] Document reviewing initialization through dry-run before replacing customized configuration.
- [x] Document reinstalling editable checkouts so the console script uses the protected entry point.
- [x] Document the commit-validation behavior matrix and the difference between version strategy and message validation.
- [x] Preserve the experimental status of `custy workflow`.
- [x] Document native/auto credentials, container-only behavior, external paths, environment variables, SSH boundaries, and Docker secret usage.
- [x] Document Docker bind-mount mapping, persistent versus disposable token files, status-column interpretation, and manual username/PAT fallback.

### Release checklist

- [x] Prepare internal commit and public release messages for `v2.1.0`.
- [x] Confirm implementation, tests, documentation, tooling, and container validation are recorded.
- [x] Record development checkpoint 4 for CI/CD reliability and release-tag-only production images.
- [ ] Review the final repository diff and generated artifacts.
- [ ] Commit, tag, publish, and verify `v2.1.0` only with explicit release approval.
- [ ] Verify packages, container images, and English/Indonesian documentation after publication.

### Future work

- [ ] Extend automatic project detection only when a new ecosystem has clear metadata and tests.
- [ ] Add custom version/tag formats without weakening current normalization and validation guarantees.
- [ ] Continue validating configured GitHub and GitLab container destinations before publication.
- [ ] Keep hook upgrades intentional and review formatter changes before applying them repository-wide.

### Notes

- This snapshot distinguishes completed implementation and validation from
  external release operations that still require explicit authorization.
- No claim is made here that the `v2.1.0` tag or release has already been
  published.

---

## Additional status carried from repository TODO files

### Changelog configuration hardening

The root `TODO.md` records follow-up work that is not fully represented in the
rolling history:

- [x] Inspect resolver consumers and related tests for compatibility.
- [x] Harden `app/core/changelog/config/resolver.py` with safe enum parsing, section type guards, numeric normalization, and release-behavior conflict normalization.
- [ ] Add or update tests for malformed configuration and fallback behavior.
- [ ] Run the focused changelog configuration resolver tests.
- [ ] Record the final fixes and validation results.

### Historical implementation notes from `docs/TODO.md`

- [x] Separate CLI presentation under `app/cli` from core behavior under `app/core`.
- [x] Replace the former giant Git/workflow responsibilities with focused workflow, pipeline, strategy, factory, service, and UI components.
- [x] Move personal project configuration and templates into `.config/custy`.
- [x] Add external logging, Rich UI improvements, modular Make workflows, containers, CI/CD, pre-commit, metadata, and expanded tests.
- [x] Keep deprecated or personal backup files preserved rather than treating them as active source.
- [x] Move canonical user documentation to the Devalltect documentation portal while retaining repository-local history and reference material.

Until v2.0.0

- [x] Replaced the former monolithic CLI and workflow responsibilities with separated `app/cli`, `app/core`, `app/ui`, pipeline, Git-service, configuration, and template layers.
- [x] Migrated project configuration from `.custor.toml` to the namespaced `.config/custy/config.toml` system with packaged defaults under `app/templates`.
- [x] Added focused `init`, `validate`, `version`, `changelog`, `backup`, `cleanup`, `commit`, `tag`, and `push` commands.
- [x] Added ordered `custy run dev`, `custy run release`, and `custy run full` profiles plus custom step composition.
- [x] Rebuilt changelog generation with parsing, cleaning, grouping, deduplication, release behavior, sorting, pending-commit integration, links, metadata, statistics, and configurable Jinja rendering.
- [x] Corrected generated `CHANGELOG.md` structure, release boundaries, summaries, comparison links, grouping, and formatting.
- [x] Added determinate changelog progress for `Unreleased` content and every discovered Git tag.
- [x] Added consistent dry-run behavior that keeps read-only discovery and validation available while simulating intended file, editor, Git, and remote mutations.
- [x] Added separated Git executor and service boundaries, structured operation results, multi-remote behavior, staging modes, tag sorting, and clearer failures.
- [x] Added message-template backups, configurable retention cleanup, and safer branch cleanup with protected-branch, merge-status, and age rules.
- [x] Added centralized Rich console and rotating file logging, configurable log levels, clearer command help, progress displays, summaries, and actionable errors.
- [x] Added Docker, Docker Compose, modular Make targets, GitHub Actions, GitLab CI, pre-commit, Ruff, Black, Pytest, packaging, and release automation support.
- [x] Expanded CLI, core, integration, regression, configuration, logging, UI, workflow, cleanup, dry-run, and changelog test coverage.
- [x] Updated README, badges, installation methods, Docker/GHCR instructions, Make guidance, project metadata, contribution guidance, and licensing information.
- [x] Added comprehensive English and Indonesian Custy documentation to the Devalltect Docusaurus portal.
- [x] Prepared and reviewed the `v2.0.0-rc.1` internal commit message and public release notes.

---

### 🚀 v2.0.0 Stable Release Preparation

- [ ] Promote the validated `v2.0.0-rc.1` feature set to stable `v2.0.0` without adding new user-facing behavior.
- [ ] Remove root development scratch files: `CHANGES FOR THIS ANOTHER.txt`, `CHANGES FOR THIS.txt`, `NOTES_WHILE_DEVELOPMENT.txt`, and `WHAT_TO_DO.txt`.
- [ ] Remove the completed root `TODO.md` and version-specific `docs/TODO.md` files.
- [x] Archive the v2.0.0 development scope, decisions, completed work, pending cleanup, and future ideas in this tracking-history file.
- [ ] Review the final repository diff and ensure temporary or personal planning files are not included unintentionally.
- [ ] Run the final approved test, validation, packaging, and release checks.
- [ ] Commit, tag, and push `v2.0.0` using Custy after all checks pass.
- [ ] Verify GitHub/GitLab tags, releases, packages, container publications, and documentation links after publishing.

---

### 🧠 Planning

- [x] Use centralized logging where it improves diagnostics and observability while keeping user-facing Rich output readable.
- [ ] Add conversion support between PEP 440, SemVer, and supported custom tag formats.
- [ ] Validate configured GitHub and GitLab container image URLs and image names before publication.
- [ ] Review and update `.pre-commit-config.yaml` so hook versions, Python targets, and validation commands align with the current Custy project. This is planning only; do not update the configuration as part of the current release-planning work.
- [ ] Add options to push all tags

---

### 🗑️ Cancelled / Dropped

- for version use this format major.minor.patch-pre_release.pre_release_number
- change the pre-release format
- Update the major, minor, and patch on `main` branch. But on `dev` branch `main`, I just update pre_release and pre_release
- remote on gitlab push `main` and `dev`. but on github just push `main`
- on CLI parameters, on --bump, add option `final`. So the bump from v1.4.0rc[n] to -> v1.4.0
- bug fixes or improvements, if switch to `release/x/y` or `rc` version tag get all message from `dev` branch like `alpha`, `beta`, `rc`, `dev`, etc

---

## ⚖️ considerations

- allow to and stages, commit, and push TODO.md on gitlab but not on github

---

## 💡Ideas

- Automatically set template commit-msg.txt based on stages which one is added and modified.
- Automatically create and delete commit-msg.txt when needed if we set argument on CLI or by default like that.
- Backup before delete the commit-msg.txt
- optionally, we can just see what would the next version by include additional CLI parameters or another ideas or just use --dry-run
- Automate the build meta or local
- Use .git/config (Local/Repo-specific)
- if post release the commit message header initial commit type is `docs` or maybe `<docs>`
- If there is a abandoned branch or experiment or deprecated branch version and want to go back to `main` branch. I choose to rename branch use format like archive/{feature}-{date} or experiment/{feature}-{date}. If I just don't care about archiving the branch I can use option to reset `dev` back to `main`
- if when running custy is failed prevent or handle the backup files that just created
- Use docker

---

## 🧾 Notes

### Branch Stratgies

If I have 2 branch
**case 1**: abandon current `dev` branch
solution1: rename and archieving branch. Go back to `main` branch (prefered)
solution2: Reset back `dev` to `main`
**case 2**: finalize and release the code on `dev` branch on `main`
solution1: go back to `main` branch. merge them. tagging and push the `main`. Update the `dev` to start the next experiment cycle. use new version for `dev` and push the `dev`
**case 3**: Let's say there is a scenario I want to just see if the pipline job in gitlab is working let's say I havemore than 5 stages let's say 7 stages on gilab pipline. of course I will commit and push to gitlab. many commit and pushes with many failed pipline jobs. I try after one of commits and push one is success for 7 stages. It kinda messy you know. What should I do. my CHANGELOG.md will become messy with many commits that unused where many failed pipline jobs.
✅ **Solutions**:

1. Use a Temporary Pipeline Test Branch
2. Squash Commits Before Merging into dev or main
3. Use [skip ci] or [ci skip] in Commit Messages like `git commit -m "ci: testing YAML [skip ci]"` or `git commit -m "docs: update README [ci skip]"`
4. Cleanup Before Tagging/Changelog

### Usage

if the commit type not [feat, fix, perf, docs, refactor] the version will not bump. 💡Hint: use --dry-run before run the actual to see what the next version would be

===============

bug fix and improvement GitHelper.branch_exists()
bug fix and improvement GitHelper.get_current_branch()
bug fix and improvement GitHelper.commit_and_push_changelog()
new method GitHelper.is_repo_empty()
new method GitHelper.is_repo_empty()
bug fix and improvement GitCommitTagger.push_changes()
bug fix and improvement GitCommitTagger.validate()

fix the bug where the branch does not exists or when get branch but the no commit on git repo. So make sure the repo has a branch and HEAD.

modified and improve README.md

new cli command to handle when the repo branch

branch name can custom name get from configuration file

---

<a id="checkpoint-6-2026-09-02"></a>

## 2026-09-02 status update — untagged checkpoint 6

Version scope: **v2.1.0**.
The [checkpoint commit message](../.config/custy/templates/commit-message_2.1.0_development-checkpoint-6.txt)
has **no associated tag or tag message**. Earlier checkpoint files remain unchanged.

### ✅ Current application and developer workflow

- [x] Retain automatic project and version-target discovery, configured-remote selection, and the focused standalone push workflow.
- [x] Keep public `run` profiles centered on commit, tag, push, dev, release, and full.
- [x] Keep interactive editor/authentication handoff, actionable Git/hook diagnostics, and native-first credentials with an optional protected container fallback.
- [x] Keep the standalone metadata script's `gh`/`glab` authentication separate from Custy's Git credential fallback.

All earlier v1.x and v2.0.0 notes, alternatives, and cancelled ideas remain
historical records. This supplement belongs to v2.1.0 preparation and does not
change the v2.0.0 or v2.0.0-rc.1 snapshots.

### ✅ Delivery work carried forward

- [x] Align local, Docker/Compose, Make, pre-commit, and hosted CI validation with the active project rather than the old standalone layout.
- [x] Validate annotated release-tag metadata and package versions; publish exact prerelease/stable image tags and update `latest` only for stable releases.
- [x] Add private GitLab Python package build, artifact checks, clean-install verification, and protected-tag publication using `CI_JOB_TOKEN`.
- [x] Normalize supported release tags to PEP 440 package versions; reject unsupported or ambiguous versions rather than guessing.
- [x] Keep unprotected GitLab tag pipelines validation-only, skipping production-image, package-upload, and provider-release jobs.
- [x] Document installation of an available package version from the selected project registry, independently of cloning source or pulling a container.
- [x] Record the maintainer's report that hosted pipelines passed and the GitLab package registry was populated. This is historical reported validation, not a new pipeline run for this documentation checkpoint.

### ✅ Optional repository metadata helper

- [x] Add `scripts/repository/src/sync_metadata.py` outside the core application and installed CLI.
- [x] Read `[project].description` and independent GitHub/GitLab topics from `pyproject.toml`; do not reinterpret package keywords as repository topics.
- [x] Resolve one repository per provider from ordered remote candidates; the current defaults are GitHub `origin` and GitLab `backup`, using fetch URLs.
- [x] Provide a `--dry-run` path with read-only Git discovery and no provider API calls.
- [x] Document authenticated `gh`/`glab` for live updates, topic replacement and empty-list clearing, no confirmation prompt, and possible partial updates on failure.
- [x] Refresh the README against active commands, configuration, runtime requirements, installation methods, and the helper's actual `src/` path.
- [x] Keep helper details in checkpoint/release commit messages; leave user-facing tag-message templates unchanged for this maintainer-only addition.

### ⏳ Follow-up and release gates

- [ ] Correct the helper docstring examples that omit `src/` and reconcile its GitHub topic-limit constant (currently 50) with the provider maximum of 20.
- [ ] Add isolated mocked coverage for metadata validation, remote selection, dry-run API suppression, topic clearing, and provider failures before treating the helper as fully validated.
- [ ] Review actual targets, credentials, topic lists, and provider permissions before a separately authorized live metadata synchronization; no live synchronization was performed for this checkpoint.
- [ ] Re-run the relevant checks against the exact candidate commit before creating the v2.1.0 tag. A passing temporary-tag pipeline is not a formal release.
- [ ] Review and update pre-commit configuration in a future maintenance task. Existing pre-commit setup is complete; this pending item means a later refresh, not that hooks were never configured.

### Notes and evidence

- [README](../README.md) and [metadata helper](../scripts/repository/src/sync_metadata.py) describe the current setup.
- [GitLab package pipeline](../.gitlab/python-package.yml) defines the validation/publication boundary.
- Earlier test/coverage figures and release-checklist statuses remain attached to their original milestones.
- No existing history, ideas, alternatives, cancelled work, backup snapshots, or earlier checkpoint messages were removed.

---

<a id="checkpoint-7-2026-09-05"></a>

## 2026-09-05 status update — untagged checkpoint 7

Version scope: **v2.1.0**.
The [checkpoint commit message](../.config/custy/templates/commit-message_2.1.0_development-checkpoint-7.txt)
has **no associated tag or tag message**. It becomes part of the cumulative
v2.1.0 stable release history.

### ✅ Explicit lifecycle-tag validation

- [x] Replace the stable-only explicit-tag validator with support for approved stable, alpha, beta, release-candidate, development, post-release, and metadata-bearing values.
- [x] Accept Custy's SemVer-style forms such as `v2.1.0-rc.1` and common PEP 440 forms such as `2.1.0rc1`.
- [x] Preserve automatic `v` prefix normalization while rejecting malformed, incomplete, unknown, and unsupported lifecycle forms.
- [x] Apply the same validator and `VERSION` help contract to direct Git operations, Version Update, Run profiles, and experimental workflow transition overrides.
- [x] Keep explicit tags independent from automatic generation and preserve downstream Git, push, and dry-run behavior.

### ✅ Tests and documentation

- [x] Focused validator suite: 32 tests passed.
- [x] Complete Custy suite: 1,360 tests passed with 83% overall coverage.
- [x] Full-project Ruff and Black validation passed.
- [x] Updated CLI help rendered with stable, SemVer RC, and PEP 440 RC examples.
- [x] English and Indonesian documentation now explain the supported lifecycle formats and include explicit release-candidate examples.
- [x] Documentation TypeScript validation and both-locale production builds passed.

### Notes and evidence

- [Shared CLI validator](../app/cli/utils/validators.py) owns the accepted explicit-tag contract.
- [Validator tests](../tests/cli/utils/test_validators.py) record supported and rejected forms.
- [Checkpoint 7 commit message](../.config/custy/templates/commit-message_2.1.0_development-checkpoint-7.txt) records the internal implementation details.
- The cumulative v2.1.0 commit and tag messages include checkpoint 7; this checkpoint itself remains untagged.
- The next untagged checkpoint records GitHub release-note rendering as checkpoint 8.
- The v2.0.0-rc.1 and v2.0.0 histories remain unchanged because this work belongs to v2.1.0.

---

<a id="checkpoint-8-2026-09-06"></a>

## 2026-09-06 status update — untagged checkpoint 8

Version scope: **v2.1.0**.
The [checkpoint commit message](../.config/custy/templates/commit-message_2.1.0_development-checkpoint-8.txt)
has **no associated tag or tag message**. It becomes part of the cumulative
v2.1.0 stable release history.

### ✅ GitHub release-note rendering

- [x] Replace the fragile escaped Markdown heredoc with explicit `printf` generation so release content no longer depends on manually escaping every backtick.
- [x] Preserve the complete reviewed annotated tag message as the main GitHub Release description.
- [x] Append populated version, release type, repository, commit, and workflow metadata.
- [x] Present concise literal Docker pull and Custy CLI verification commands without executing them or capturing runner output.
- [x] Preserve exact prerelease image tags and stable-only `latest` behavior.
- [x] Add regression coverage while keeping GitLab release and package publication behavior unchanged.

### ✅ Validation recorded

- [x] Complete Custy test suite: 1,360 passed with 83% overall coverage.
- [x] Targeted release-workflow regression checks passed.
- [x] Pre-commit validation passed for the checkpoint and cumulative v2.1.0 release-message templates.
- [x] Diff whitespace and mirrored-template consistency checks passed.

### Notes and evidence

- [GitHub release workflow](../.github/workflows/release.yml) contains the hardened release-note generation.
- [Checkpoint 8 commit message](../.config/custy/templates/commit-message_2.1.0_development-checkpoint-8.txt) records the internal implementation details.
- The cumulative v2.1.0 commit and tag messages include checkpoint 8; this checkpoint itself remains untagged.
- The v2.0.0-rc.1 and v2.0.0 histories remain unchanged because this work belongs to v2.1.0.
- No existing history, plans, ideas, cancelled work, or earlier checkpoint evidence was removed.
