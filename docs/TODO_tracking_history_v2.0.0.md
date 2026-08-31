<!-- docs/TODO_tracking_history_v2.0.0.md -->

# Custy TODO Tracking History — v2.0.0

> Cumulative snapshot for **v2.0.0**. Earlier history, unfinished work,
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
