<!-- docs/TODO_tracking_history.md -->

# Custy TODO Tracking History

> Current status: see the [2026-09-02 checkpoint update](#checkpoint-6-2026-09-02).
> Older checkboxes, test counts, plans, and decisions are preserved as recorded;
> they are historical context, not proof that every current release gate passed.

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

Since v2.1.0 development checkpoint 3

- [x] Add a backward-compatible native-first Git credential policy for container pushes.
- [x] Add optional GitHub and GitLab HTTPS token fallback from protected external files or environment variables.
- [x] Keep tokens out of project configuration, command arguments, message templates, remote URLs, and image layers.
- [x] Add guided `custy configure credentials` setup plus provider set, status, read-only test, and removal commands.
- [x] Add opt-in Docker, Compose, and remote-image Make helpers that use writable mounts only for credential setup and read-only mounts for status, testing, and runtime pushes.
- [x] Preserve local Git credential managers and SSH behavior with `container_only = true` as the recommended boundary.
- [x] Inject `git-credential-custy` per push without modifying persistent Git credential-helper configuration.
- [x] Prevent non-interactive prompt hangs and keep dry-run free from token reads and remote contact.
- [x] Give manual Git authentication direct terminal ownership so username/PAT and SSH prompts remain visible.
- [x] Disable Rich rendering for hidden direct-command pipelines so `custy push` preserves interactive prompts like `custy run push`.
- [x] Reject hidden PAT setup without an interactive TTY instead of allowing echoed token input.
- [x] Add focused credential storage, resolution, CLI, helper, push, and compatibility tests.
- [x] Align the shipped configuration and canonical English/Indonesian documentation with the credential behavior matrix, Docker bind mounts, source-status interpretation, and manual fallback.
- [x] Validate the complete 1,340-test suite at 83% coverage, Ruff, Black,
      pre-commit, and English/Indonesian documentation builds.
- [ ] Rebuild and validate the credential-enabled production image when the
      Docker host has sufficient pagefile memory.

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
