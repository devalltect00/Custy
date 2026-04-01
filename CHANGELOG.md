# 🧾 CHANGELOG




## Unreleased (2026-04-01)
### ✨ Features
- **main**: 1.10.12
  
  Final release of **Custy 1.10.12**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: .
All functionality has been fully validated and production-ready.

- *(Nothing yet)* — See tag message for full context.

---

🎉 **Custy 1.10.12 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#feat`
- Stability: `#stable`

Changelog: handled separately
  
- **workflow**: 1.10.0b2
  
  Beta release for **Custy 1.10.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

Expands test coverage, improves documentation, and refines the logic of the WorkflowManager.

### 📄 Templates
- Added more example templates for `commit-msg.txt` and `tag-msg.txt`

### 🧪 Tests
- Introduced automated tests for `WorkflowManager` functionality

### 🐛 Fixes
- Fixed logic issues in `WorkflowManager` related to CASE transitions

### 📚 Documentation
- Added `docs/git/git_workflow_cases.md` explaining CASE logic
- Documented `WorkflowManager` classes, functions, and transitions
- Updated `docs/TODO.md` to reflect recent changes

### 🧹 Maintenance
- Linted and formatted codebase using `ruff`

---

_Tag: `1.10.0b2`_

🔖 **Tags**:
- Type: `#feature`, `#bugfix`
- Docs: `#docs`, `#template`
- Tests: `#tests`
- Maintenance: `#cleanup`
  
- **workflow**: 1.10.0b1 — CASE-based Git workflow automation
  
  Beta release for **Custy 1.10.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta release introduces full support for CASE-based Git flow automation through an upgraded `WorkflowManager`.

### ✨ Features
- ✅ CASE 1–6: core transitions (develop → release → main → post-release)
- ✅ CASE 7–9: extended transitions for `feature/*`, `ci/*`, and `archive/*` branches
- `run_initial_workflow()` sets up Git context before tag
- `run_final_workflow()` automates merge, cleanup, and post-release steps
- `get_transaction_cases()` includes a complete CASE 1–9 transition map
- Integrated backup push for critical paths

### 📚 Documentation
- Added detailed documentation for `WorkflowManager` logic and CASE transitions
- Documented branching behavior, initial/final hooks, and example flow diagrams

### ⚠️ Breaking Change
- Tag-driven branching now enforced through CASE transition rules

This version brings reliable Git automation to support structured release processes and simplify branching flows.

_Tag: `1.10.0b1`_

🔖 **Tags**:
- Type: `#feature`
- Docs: `#docs`
- Workflow: `#workflow`, `automation`
- ⚠️ Stability: `#breaking-change`
  
### 🚀 Release
- **main**: 1.10.11
  
  Final release of **Custy 1.10.11**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: .
All functionality has been fully validated and production-ready.

- modified `requirements.txt`

---

🎉 **Custy 1.10.11 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#bugfix`
- Stability: `#stable`

Changelog: handled separately
  
- **main**: 1.10.10
  
  Final release of **Custy 1.10.10**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: .
All functionality has been fully validated and production-ready.

- modified `README.md`
- modified `TODO.md`
- modified `requirements.txt`

---

🎉 **Custy 1.10.10 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#bugfix`
- Stability: `#stable`

Changelog: handled separately
  
- **main**: 1.10.9
  
  Final release of **Custy 1.10.9**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: .
All functionality has been fully validated and production-ready.

- fix issue on `.github\workflows\test.yml`

---

🎉 **Custy 1.10.9 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#bugfix`
- Stability: `#stable`

Changelog: handled separately
  
- **main**: 1.10.8
  
  Final release of **Custy 1.10.8**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: .
All functionality has been fully validated and production-ready.

- Updated `README.md`

---

🎉 **Custy 1.10.8 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`
- Docs: `#docs`
- Stability: `#stable`

Changelog: handled separately
  
- **main**: 1.10.7
  
  Final release of **Custy 1.10.7**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: .
All functionality has been fully validated and production-ready.

- Updated `README.md`

---

🎉 **Custy 1.10.7 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`
- Docs: `#docs`
- Stability: `#stable`

Changelog: handled separately
  
- **main**: 1.10.6 — improve workflow safety, templates, and user interaction
  
  Final release of **Custy 1.10.6**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: 1.10.6rc4, 1.10.6rc3, 1.10.6rc2, 1.10.6rc1, 1.10.6b1.
All functionality has been fully validated and production-ready.
It focuses on refining the WorkflowManager, enhancing commit/tag templates, and introducing safety improvements for merge operations.

### 🐛 Fixes
- Prevented unsafe execution in CASE 3, 6, and 9 if staged files exist
- Added interactive prompt when no files are staged to confirm whether to continue

### 🧠 UX Improvements
- Safer tagging and merging via confirmation-based logic
- More resilient and predictable branching flow

### 📄 Templates
- Refactored and expanded `commit-msg.txt` and `tag-msg.txt` example templates

### 📚 Documentation
- Updated project structure docs to reflect current implementation

---

🎉 **Custy 1.10.6 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#bugfix`, `#refactor
- UX: `#ux`
- docs: `#docs`, `#template`
- Workflow: `#workflow`
- Maintenance: `#cleanup``
- Stability: `#stable`

Changelog: handled separately
  
- **main**: 1.10.5
  
  Final release of **Custy 1.10.5**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: 1.10.5rc1, 1.10.5b1.
All functionality has been fully validated and production-ready.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

🎉 **Custy 1.10.5 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#bugfix`
- Stability: `#stable`

Changelog: handled separately
  
- **main**: 1.10.4
  
  Final release of **Custy 1.10.4**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: 1.10.4rc1, 1.10.4b1.
All functionality has been fully validated and production-ready.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

🎉 **Custy 1.10.4 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#bugfix`
- Stability: `#stable`

Changelog: handled separately
  
- **main**: 1.10.3
  
  Final release of **Custy 1.10.3**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: .
All functionality has been fully validated and production-ready.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

🎉 **Custy 1.10.3 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#bugfix`
- Stability: `#stable`

Changelog: handled separately
  
- **main**: 1.10.2
  
  Final release of **Custy 1.10.2**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: 1.10.2rc1, 1.10.2b1.
All functionality has been fully validated and production-ready.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

🎉 **Custy 1.10.2 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#bugfix`
- Stability: `#stable`

Changelog: handled separately
  
- **main**: 1.10.1
  
  Final release of **Custy 1.10.1**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: 1.10.1rc1, 1.10.1b2, 1.10.1b1.
All functionality has been fully validated and production-ready.

### 🧹 Maintenance & Structure
- Code formatted with `ruff`

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

🎉 **Custy 1.10.1 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#bugfix`
- Maintenance: `#cleanup`
- Stability: `#stable`

Changelog: handled separately
  
- **main**: 1.10.0
  
  Final release of **Custy 1.10.0**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: 1.10.0rc1, 1.10.0b3, 1.10.0b2, 1.10.0b1.
All functionality has been fully validated and production-ready.

### ✨ Features
- Full CASE 1–9 support in `WorkflowManager`:
  - Core flow: `develop → release → main → post-release`
  - Extended handling: `feature/*`, `ci/*`, `archive/*`
- Automatic workflow execution with `run_initial_workflow()` and `run_final_workflow()`
- Backup push handling, context setup, and cleanup automation

### 📚 Documentation
- Added `git_workflow_cases.md` for CASE logic
- Documented `WorkflowManager` classes and transition behavior
- Updated `README.md`, `TODO.md`, and added usage notes

### 📄 Templates
- Refactored and expanded example templates for commit and tag messages

### 🧪 Tests
- Introduced test coverage for `WorkflowManager` and CASE transitions

### 🐛 Fixes
- Fixed transition bugs and branching issues within `WorkflowManager`

### 🧹 Maintenance
- Linted and formatted the codebase using `ruff`
- Cleanup of legacy TODOs and refactoring for clarity

---

🎉 **Custy 1.10.0 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#feature`, `#bugfix`
- Docs: `#docs`, `#template`
- Workflow: `#workflow`, `#automation`
- QA: `#tests`
- Maintenance: `#cleanup`
- Stability: `#stable`

Changelog: handled separately
  
- **main**: 1.9.0
  
  Final release of **Custy 1.9.0**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: 1.9.0rc3, 1.9.0rc2, 1.9.0rc1, 1.9.0b3, 1.9.0b2, 1.9.0b1.
All functionality has been fully validated and production-ready.

### ✨ Features
- Redesigned CLI interface with support for `--silent` / `--debug` modes
- Smart path resolution for configs and templates to prevent ambiguity
- Improved commit/tag message template generation logic

### 📚 Documentation
- Rewrote and cleaned `README.md`, `HOW_TO_USE.md`, and `docs/TODO.md`
- Added badge list and regenerated project structure documentation

### ⚙️ CI/CD
- GitHub Actions and GitLab CI pipelines now support testing and deployment
- Makefile updated with silent execution support (`--no-debug`)

### 🧹 Maintenance & Structure
- Refactored and cleaned up the `app/` structure
- Relocated and organized all templates
- Applied code formatting using `ruff`

### 🐛 Bug Fixes
- Commit type now validated before version resolution
- Fixed pipeline creation issues due to misconfigured jobs
- Resolved internal logic bugs to improve stability
- `assert_is_final_version()` now gracefully handles pre-releases

---

🎉 **Custy 1.9.0 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#feature`, `#bugfix`, `#refactor`
- Docs: `#docs`, `#template`
- CI/CD: `#ci`
- Stability: `#stable`

Changelog: handled separately
  
- **core**: 1.8.0
  
  Final release of **Custy 1.8.0**, promoted from the latest release candidate.
includes all feature and fixes from pre-releases: 1.8.0rc2, 1.8.0rc1.

This final release includes all validated features and fixes from earlier pre-releases:
- Git workflow validation via WorkflowManager
- Temporary branch cleanup with Branch Cleaner
- Dual remote strategy: GitLab (main), GitHub (backup)
- Strategy-specific version helpers (PEP 440, SemVer)
- Cleaner code structure with VersionHelperBase
- Updated Makefile and improved documentation

🛠 Final tweaks after rc2:
- Allow `custy all` to run `--sync-backup` automatically
- Minor improvements to support `release` commit type
- Refined docs and cleaned up TODO list

Tag: 1.8.0
Changelog: handled separately
  
### 📦 Others
- **general**: Merge pull request #1 from devalltect00/develop
  
  Develop
  
- **general**: merge release 1.7.1 into main
### 📝 Documentation
- **changelog**: update changelog
- **changelog**: update changelog
- **changelog**: update changelog
- **changelog**: update changelog
- **changelog**: update changelog
- **changelog**: update changelog
- **changelog**: update changelog
- **changelog**: update changelog
- **changelog**: update changelog
- **changelog**: update changelog
- **changelog**: update changelog
- **todo**: 1.10.0rc1
  
  Release candidate for **Custy 1.10.0**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- Update `docs/TODO.md` to reflect recent changes and clean up outdated entries

---

_Tag: `1.10.0rc1`_

🔖 **Tags**:
- Type: `#docs`
  
- **template**: 1.10.0b3
  
  Beta release for **Custy 1.10.0**, introducing mid-stage docsures and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- Reorganized and renamed `commit-msg.txt` and `tag-msg.txt` templates

---

_Tag: `1.10.0b3`_

🔖 **Tags**:
- Type: `#docs`
  
- **changelog**: update changelog
- **todo.md**: 1.9.2
  
  Final release of **Custy 1.9.2**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: .
All functionality has been fully validated and production-ready.

- *(Nothing yet)* — See tag message for full context.

---

🎉 **Custy 1.9.2 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#<type>`

Changelog: handled separately
  
- **changelog**: update changelog
- **release**: 1.9.0rc1
  
  Release candidate for **Custy 1.9.0**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- Update `docs/TODO.md` to reflect recent changes and clean up outdated entries

---

_Tag: `1.9.0rc1`_

---

🔖 **Tags**: `#<type>`
  
- **changelog**: update changelog
- **changelog**: update changelog
- **changelog**: update changelog
- **changelog**: update changelog
- **changelog**: update changelog
- **release**: 1.7.0.post3
  
  Post-release patch for **Custy 1.7.0**, addressing minor updates or corrections.
Includes minor updates or documentation fixes after release 1.7.0.

This post-release includes minor updates and corrections after the official release:
- modified documentation `docs/TODO.md`

Tag: 1.7.0.post3
Changelog: handled separately
  
- **changelog**: update changelog
- **changelog**: update changelog
### 🧠 Refactoring
- **template**: 1.10.6rc4
  
  Release candidate for **Custy 1.10.6**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release.

### 📄 Templates
    - Refactored and expanded example templates for commit and tag messages

---

_Tag: `1.10.6rc4`_

🔖 **Tags**:
- Type: `#refactor`
- Stability: `#rc`
  
- **workflow**: 1.10.6rc2
  
  Release candidate for **Custy 1.10.6**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- *(Nothing yet)* — See tag message for full context.

---

_Tag: `1.10.6rc2`_

🔖 **Tags**:
- Type: `#refactor`workflow
  
- **core**: 1.10.4b1
  
  Beta release for **Custy 1.10.4**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- This release just for testing the app for release

---

_Tag: `1.10.4b1`_

🔖 **Tags**:
- Type: `#refactor`
  
- **release**: 1.10.1rc1
  
  Release candidate for **Custy 1.10.1**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- *(Nothing yet)* — See tag message for full context.

---

_Tag: `1.10.1rc1`_

🔖 **Tags**:
- Type: `#refactor`
  
- **core**: 1.9.0b1 — improve CLI, docs, pipeline, templates, and structure
  
  Beta release for **Custy 1.9.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This update delivers improved CLI usability, updated documentation, better automation, refactored project structure, and improved message templates.

### ✨ Features
- Redesigned CLI interface with clearer UX and new arguments (e.g., silent/debug flags)
- Enhanced file path resolution to avoid ambiguity for key config and template files

### 📚 Documentation
- Rewrote `README.md` and added badges (`docs/badges.md`)
- Created user guide: `docs/HOW_TO_USE.md`
- Regenerated project structure documentation

### ⚙️ CI/CD
- Added GitHub Actions workflow and GitLab CI pipeline to run tests on push

### 🧹 Maintenance
- Cleaned and refactored `app/` directory
- Code formatted with `ruff`

### 📄 Template Improvements
- Reorganized and renamed `commit-msg.txt` and `tag-msg.txt` templates
- Updated commit/tag message generation to use new structure

### 🐛 Bug Fix
- Fixed a minor internal bug affecting stability

### 🛠️ Misc
- Updated `Makefile`, `pyproject.toml`, and related config files
- Removed unused file `q`

---

_Tag: `1.9.0b1`_

---

🔖 **Tags**:
- Type: `#feature`, `#bugfix`, `#refactor`
- Docs: `#docs`, `#template`
- CI/CD: `#ci`, `#cleanup`
  
- **workflow**: 1.8.0rc2
  
  Release candidate for **Custy 1.8.0**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This refactor decouples strategy-specific logic (PEP 440, SemVer) from the core
WorkflowManager class by introducing a VersionHelperBase interface. Both
PEP440VersionHelper and SemverVersionHelper now implement:

- classify(): identify version tier
- tier_order(): precedence for tier promotion
- suggest_tag(): next tag suggestion based on branch
- get_transition_cases(): valid CASE transitions

WorkflowManager is now cleaner and delegates classification, version suggestion,
and transition validation to the appropriate strategy helper dynamically.

This release candidate consolidates finalized features and bug fixes before the stable release:
- Update `docs/TODO.md` to reflect recent changes and clean up outdated entries

Other improvements:
- Reduced branching logic in check_transition()
- Added docstrings across all helper classes
- Improved extensibility for future strategies (e.g., CalVer)

BREAKING CHANGE: version helpers must now implement VersionHelperBase interface

Tag: 1.8.0rc2
  
### 🐛 Bug Fixes
- **workflow**: 1.10.6rc3
  
  Release candidate for **Custy 1.10.6**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

### 🐛 Fixes
- Prevent unintended execution in CASE 3, 6, and 9 if staged files exist
- Ensures safety during critical merge operations inside `WorkflowManager`

### 🧠 UX Improvement
- Added interactive prompt (`y/n`) when no files are staged during validation
- Allows user to explicitly confirm whether to proceed or abort

These changes make the workflow execution more resilient and user-aware during tagging phases.

---

_Tag: `1.10.6rc3`_

🔖 **Tags**:
- Type: `#bugfix`
- Workflow: `#workflow`
- Stability: `#safety`
- Pre-release: `#rc`
  
- **workflow**: 1.10.6rc1
  
  Release candidate for **Custy 1.10.6**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

### 📚 Documentation
- 📘 update `project structure` documentation

---

_Tag: `1.10.6rc1`_

🔖 **Tags**:
- Type: `#bugfix`
  
- **workflow**: 1.10.6b1
  
  Beta release for **Custy 1.10.6**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

_Tag: `1.10.6b1`_

🔖 **Tags**:
- Type: `#bugfix`
  
- **workflow**: 1.10.5rc1
  
  Release candidate for **Custy 1.10.5**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

_Tag: `1.10.5rc1`_

🔖 **Tags**:
- Type: `#bugfix`
  
- **workflow**: 1.10.5b1
  
  Beta release for **Custy 1.10.5**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- reapplied clean branch functionality

---

_Tag: `1.10.5b1`_

🔖 **Tags**:
- Type: `#bugfix`
  
- **core**: 1.10.4rc1
  
  Release candidate for **Custy 1.10.4**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

_Tag: `1.10.4rc1`_

🔖 **Tags**:
- Type: `#bugfix`
  
- **workflow**: 1.10.2rc1
  
  Release candidate for **Custy 1.10.2**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- *(Nothing yet)* — See tag message for full context.

---

_Tag: `1.10.2rc1`_

🔖 **Tags**:
- Type: `#bugfix`
  
- **workflow**: 1.10.2b1
  
  Beta release for **Custy 1.10.2**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- 🐛 Fixed a minor internal bug to improve stability

---

_Tag: `1.10.2b1`_

🔖 **Tags**:
- Type: `#bugfix`
  
- **workflow**: 1.10.1b2
  
  Beta release for **Custy 1.10.1**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- 🐛 Fixed a minor internal bug to improve stability

---

_Tag: `1.10.1b2`_

🔖 **Tags**:
- Type: `#bugfix`
  
- **workflow**: 1.10.1b1
  
  Beta release for **Custy 1.10.1**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- Improved commit/tag message template generation logic

---

_Tag: `1.10.1b1`_

🔖 **Tags**:
- Type: `#fix`
  
- **main**: 1.9.1
  
  Final release of **Custy 1.9.1**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: .
All functionality has been fully validated and production-ready.

- 🐛 Fixed a minor internal bug to improve stability

---

🎉 **Custy 1.9.1 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#bugfix`

Changelog: handled separately
  
- **release**: 1.9.0rc3
  
  Release candidate for **Custy 1.9.0**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- 🐛 Fixed a minor internal bug to improve stability

---

_Tag: `1.9.0rc3`_

🔖 **Tags**:
- Type: `#bugfix`
  
- **release**: 1.9.0rc2
  
  Release candidate for **Custy 1.9.0**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- 🐛 Fixed a minor internal bug to improve stability

---

_Tag: `1.9.0rc2`_

---

🔖 **Tags**: `#<type>`
  
- **core**: 1.9.0b3
  
  Beta release for **Custy 1.9.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- Fixed a minor internal bug affecting stability

---

_Tag: `1.9.0b3`_

---

🔖 **Tags**:
- Type: `#bugfix`
  
- **core**: 1.9.0b2 — fix commit-type validation and pipeline creation issue
  
  Beta release for **Custy 1.9.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
### 🐛 Bug Fixes
- Fixed a bug where commit type wasn't validated before resolving version, which could lead to invalid version bumps
- Fixed issue where pipeline couldn’t be created due to misconfigured job or script condition

---

_Tag: `1.9.0b2`_

---

🔖 **Tags**:
- Type: `#bugfix`
- CI/CD: `#pipeline`
- Versioning: `#versioning`
  
- **push**: 1.8.1
  
  Final release of **Custy 1.8.1**, promoted from the latest release candidate.
includes all feature and fixes from pre-releases: .

This final release includes all validated features and fixes from earlier pre-releases:
- auto-push backup/main after changelog generation

Previously, the backup remote (`backup/main`) was not automatically pushed after generating `CHANGELOG.md`. This bug has now been fixed.

Now, after changelog generation completes, `backup/main` is automatically synced to ensure both remotes stay consistent.

Tag: 1.8.1
Changelog: handled separately
  
- **core**: 1.8.0rc1
  
  Release candidate for **Custy 1.8.0**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- use 2 permanent branches: `main` (stable) and `develop` (experimental)
- configure dual remote setup: GitLab as main, GitHub as backup
- implement branching workflow checking (WorkflowManager)
- add branch cleaner to prune temporary branches
- update Makefile with latest tasks
- expand documentation

Tag: 1.8.0rc1
  
- **release**: 1.7.1.post1
  
  Post-release patch for **Custy 1.7.1**, addressing minor updates or corrections.
Includes minor updates or documentation fixes after release 1.7.1.

This post-release includes minor updates and corrections after the official release:
- Allow CLI to accept arguments without explicitily requiring the `--bump` flag
- Fix issue in the `Makefile` execution flow
- Update `docs/TODO.md` to reflect recent changes and clean up outdated entries

Tag: 1.7.1.post1
Changelog: handled separately
  
- **release**: 1.7.1
  
  Final release of **Custy 1.7.1**, promoted from the latest release candidate.
includes all feature and fixes from pre-releases: .

This final release includes all validated features and fixes from earlier pre-releases:
- Fix the file name from `pep404_strategy.py` → `pep440_strategy.py`
- Rename class from `PEP404Strategy` → `PEP440Strategy`
- Bug fix: Switch to post-release uses `1.5.0.post1` instead of bumping minor to `1.6.0.post1`
- Refactor and clean up `SemverStrategy` and `PEP440Strategy` classes
- Add test coverage for both strategy classes
- Add documentation: `docs/versioning/switching version.md`
- Verbose step logging before changelog generation to improve debugging
- Ensure commit and tag backup files are staged before commit
- Improve dry-run flow in message generation
- Update `TODO.md` to reflect current feature status

Tag: 1.7.1
Changelog: handled separately
  
- **release**: 1.6.0.post2
  
  Post-release patch for **Custy 1.6.0**, addressing minor updates or corrections.
Includes minor updates or documentation fixes after release 1.6.0.

This post-release includes minor updates and corrections after the official release:
- Bug fixed case example changes from 1.5.0.post1 → 1.5.0.post2
- Bug fixed on `Makefile`
- modified documentation `docs/TODO.md`

Tag: 1.6.0.post2
Changelog: handled separately
  
### 🔧 Chores
- **release**: 1.10.1rc1
  
  Release candidate for **Custy 1.10.1**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- *(Nothing yet)* — See tag message for full context.

---

_Tag: `1.10.1rc1`_

🔖 **Tags**:
- Type: `#chore`
  
- **release**: 1.9.0rc1
  
  Release candidate for **Custy 1.9.0**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release.

### 📚 Documentation
- Updated `docs/TODO.md` to reflect recent changes and clean up outdated tasks
- Confirmed installation steps and usage instructions are ready and verified

---

_Tag: `1.9.0rc1`_

---

🔖 **Tags**:
- Type: `#chore`
  
- **release**: 1.9.0b2
  
  Beta release for **Custy 1.9.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements.

### 📄 Template Enhancements
- Added more example templates for `commit-msg.txt` and `tag-msg.txt` to guide custom formatting

### 🛠️ Makefile Improvements
- Updated Makefile commands to include `--no-debug` for cleaner production runs
  - Example: `custy-all-major` now includes `--no-debug` for silent execution

### ⚙️ Logic Refinement
- Tweaked `assert_is_final_version()`:
  - From blocking pre-releases to simply skipping generation with a warning
  - More graceful handling for versions like `1.9.0b2`, `rc`, `a`, etc.

---

_Tag: `1.9.0b2`_

---

🔖 **Tags**:
- Type: `#chore`, `#cleanup`
- Docs: `#template`
- Config: `#makefile`
  
### ✨ Features
- **workflow**: 1.10.0b2
  
  Beta release for **Custy 1.10.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

Expands test coverage, improves documentation, and refines the logic of the WorkflowManager.

### 📄 Templates
- Added more example templates for `commit-msg.txt` and `tag-msg.txt`

### 🧪 Tests
- Introduced automated tests for `WorkflowManager` functionality

### 🐛 Fixes
- Fixed logic issues in `WorkflowManager` related to CASE transitions

### 📚 Documentation
- Added `docs/git/git_workflow_cases.md` explaining CASE logic
- Documented `WorkflowManager` classes, functions, and transitions
- Updated `docs/TODO.md` to reflect recent changes

### 🧹 Maintenance
- Linted and formatted codebase using `ruff`

---

_Tag: `1.10.0b2`_

🔖 **Tags**:
- Type: `#feature`, `#bugfix`
- Docs: `#docs`, `#template`
- Tests: `#tests`
- Maintenance: `#cleanup`
  
- **workflow**: 1.10.0b1 — CASE-based Git workflow automation
  
  Beta release for **Custy 1.10.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta release introduces full support for CASE-based Git flow automation through an upgraded `WorkflowManager`.

### ✨ Features
- ✅ CASE 1–6: core transitions (develop → release → main → post-release)
- ✅ CASE 7–9: extended transitions for `feature/*`, `ci/*`, and `archive/*` branches
- `run_initial_workflow()` sets up Git context before tag
- `run_final_workflow()` automates merge, cleanup, and post-release steps
- `get_transaction_cases()` includes a complete CASE 1–9 transition map
- Integrated backup push for critical paths

### 📚 Documentation
- Added detailed documentation for `WorkflowManager` logic and CASE transitions
- Documented branching behavior, initial/final hooks, and example flow diagrams

### ⚠️ Breaking Change
- Tag-driven branching now enforced through CASE transition rules

This version brings reliable Git automation to support structured release processes and simplify branching flows.

_Tag: `1.10.0b1`_

🔖 **Tags**:
- Type: `#feature`
- Docs: `#docs`
- Workflow: `#workflow`, `automation`
- ⚠️ Stability: `#breaking-change`
  

## v1.5.0.post1 (2025-07-31)
### 📝 Documentation
- **release**: v1.5.0.post1
  
  Post-release patch for **Custy v1.5.0**, addressing minor updates or corrections.
Includes minor updates or documentation fixes after release v1.5.0.

This post-release includes minor updates and corrections after the official release:
- Added a new documentation `docs/Q&A/git/footer section on tag message.md`
- modified documentations `docs/Q&A/git/changelogs approach.md`, `docs/Q&A/git/comparison commit and tag message.md`, `docs/TODO.md`
- Modified Makefile by adding documentations

Tag: v1.5.0.post1
Changelog: handled separately
  
- **changelog**: update changelog
- **release**: 1.5.0rc1
  
  Release candidate for **Custy 1.5.0**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- *(Nothing yet)* — See tag message for full context.

Tag: 1.5.0rc1
  
- **changelog**: update changelog
- **changelog**: update changelog
- **changelog**: update changelog
- **release**: v1.4.1
  
  Final release of Custy v1.4.1

Includes modified documentation.

Tag: v1.4.1
Changelog: handled separately
  
- **changelog**: update changelog
- **changelog**: update changelog
- **release**: v1.4.1
  
  Final release of Custy v1.4.1

Includes bug fixes.

Tag: v1.4.1
Changelog: handled separately
  
- **changelog**: update changelog
- **changelog**: update changelog
- **TODO.md**: add or change todo
  
  - add or change todo

Changelog: handled separately
  
- **changelog**: update changelog
- **TODO.md**: add or change todo
  
  - add or change todo

Changelog: handled separately
  
- **changelog**: update changelog
- **changelog**: update changelog
- **changelog**: update changelog
### ✨ Features
- **release**: 1.5.0
  
  Final release of **Custy 1.5.0**, promoted from the latest release candidate.
includes all feature and fixes from pre-releases: 1.5.0rc1, 1.5.0b3, 1.5.0b2, 1.5.0b1.

This final release includes all validated features and fixes from earlier pre-releases:
- Add structured generation of `commit-msg.txt` and `tag-msg.txt`
- Improve message clarity, flexibility, and consistency
- Enhance template customization for different version types (alpha, beta, rc, final)
- Ensure commit/tag message files are properly staged and backed up
- Fix dry-run behavior in message generation flow
- Address minor edge cases in automation
- Reference commit/tag standards in `docs\git\commit_message.md`
- Add internal usage notes and automation guidance
- Ensure commit and tag backup files and odl files to staged and commit
- Handle staged and commit when no staged changes detected
- Updated `TODO.md`

Tag: 1.5.0
Changelog: handled separately
  
- **release**: 1.5.0b1
  
  Beta release for **Custy 1.5.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- *(Nothing yet)* — See tag message for full context.

Tag: 1.5.0b1
  
- **core**: implement advanced versioning rules and CLI behavior controls
  
  This commit introduces a series of improvements across versioning, tagging, changelog generation, and backup handling in Custy CLI.

- Prevents major.minor.patch bump when incrementing within same pre-release tier (e.g. rc1 → rc2)
- Generates changelog only on final releases (e.g. v1.2.3), skipping pre-releases
- Enforces bump/tag only for specific types [feat, fix, perf, docs, refactor]; others require CLI override
- Detects project type (Python or JavaScript) to apply correct versioning scheme (PEP 440 or SemVer)
- Tag messages now opened in external file like commit-msg.txt; supports default message via flag
- For release tags, auto-generates commit/tag message template from all prereleases (pre, dev, etc.)
- Prevents bump from rc → final from incrementing patch (v1.2.3rc1 → v1.2.3, not v1.2.4)
- Adds cleanup logic for `backups/`, keeping 10 latest (customizable via CLI)
- Fixes backup and template folder resolution; commit-msg.txt placement corrected
- Adds `cleanup-backups` CLI handler
- Updated `.gitignore` to ignore `templates/tag-msg.txt`
- Updated `.projectignore` to ignore `templates/tag-msg.txt`

Changelog: handled separately
  
- **versioning**: Improve pre-release and full versioning support with PEP 440
  
  - Fix pre-release version format to comply with pep440 for python
- Add support for full format: [Epoch!]MAJOR.MINOR.PATCH[Pre-release][Post-release][Development][+Local]
- Additionally support Post-release, development, local identifiers, and epoch segment

Changelog: handled separately
  
### 🐛 Bug Fixes
- **release**: 1.5.0b3
  
  Beta release for **Custy 1.5.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- *(Nothing yet)* — See tag message for full context.

Tag: 1.5.0b3
  
- **release**: 1.5.0b2
  
  Beta release for **Custy 1.5.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- *(Nothing yet)* — See tag message for full context.

Tag: 1.5.0b2
  
- **release**: v1.4.1
  
  Final release of Custy v1.4.1

Includes bug fixes.

Tag: v1.4.1
Changelog: handled separately
  
- **release**: v1.4.0rc5
  
  Release candidate for v1.4.0, consolidating all pre-release changes.

- Resolved issue with `get_commits_between_tags()` in `GitHelper`(`app\utils\git.py`).

Tag: v1.4.0rc5
  
- **release**: v1.4.0rc4
  
  Release candidate for v1.4.0, consolidating all pre-release changes.

- Resolved issue with `_prepare_release_message_from_prereleases()` in `GitCommitTagger`(`app\git_commit_tagger.py`).

Tag: v1.4.0rc4
  
- **release**: v1.4.0rc3
  
  Release candidate for v1.4.0, consolidating all pre-release changes.

- Resolved issue with `get_last_tag_before()` in `GitHelper`(`app\utils\git.py`).

Tag: v1.4.0rc3
  
### 🔧 Chores
- **release**: 1.5.0b1
  
  Beta release for **Custy 1.5.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- *(Nothing yet)* — See tag message for full context.

Tag: 1.5.0b1
  
- **release**: v1.5.0a1
  
  - _(Nothing yet)_

Tag: v1.5.0a1
  
- **release**: v1.5.0a2
  
  - _(Nothing yet)_

Tag: v1.5.0a2
  
- **release**: v1.5.0rc1
  
  - _(Nothing yet)_

Tag: v1.5.0rc1
  
- **release**: v1.5.0
  
  - _(Nothing yet)_

Tag: v1.5.0
  
- **release**: v1.4.2
  
  Final release of Custy v1.4.2

Includes modified documentation.

Tag: v1.4.2
Changelog: handled separately
  
- **release**: v1.4.0
  
  Final release of Custy v1.4.0 - prompted from release candidate.

Includes all feature and fixes from alpha and RC pre-releases.

Tag: v1.4.0
Changelog: handled separately
  
- **release**: v1.4.0rc2
  
  Release candidate for v1.4.0, consolidating all pre-release changes.

- Improve docs

Tag: v1.4.0rc2
  
- **release**: v1.4.0rc1
  
  Release candidate for v1.4.0, consolidating all pre-release changes.

Includes:
- Version bump protection within pre-release tier (e.g., rc1 → rc2)
- Restriction of changelog to final releases only
- Commit type validation for bump/tag operations
- Project type detection (PEP 440 or SemVer) for versioning
- External tag message support (`tag-msg.txt`)
- Auto-generation of release commit/tag message templates
- RC → final bump without patch increment
- `cleanup-backups` CLI command
- Improved dry-run behavior
- Expanded documentation and Makefile updates
- Backup/template folder resolution fixes

Tag: v1.4.0rc1
  
- **commit_msg**: support 'release' as valid Conventional Commit type
  
  - Added 'release' to allowed commit types in the validator

Changelog: handled separately
  
### 🧠 Refactoring
- **release**: v1.4.3
  
  Final release of Custy v1.4.3

Refactor Code using Ruff

Tag: v1.4.3
Changelog: handled separately
  

## v1.2.0 (2025-07-25)
### ✨ Features
- **git_commit_tagger**: replace cz check with custom commit message checker
  
  - Replaces Commitizen's `cz check` with a built-in custom validator
- Supports multi-line messages with header, body, and footer.
- Includes structured error handling via custom ValidationError exception.

Changelog: handled separately
  
### 📝 Documentation
- **changelog**: update changelog

## v1.1.5 (2025-07-25)
### 🐛 Bug Fixes
- **git_commit_tagger**: add or change todo
  
  - Fix issue where added to stage and commit after change version on `.cz.toml` and `app/__version__.py` files
- stage files before commit. stage the  `.cz.toml`, `app/__version__.py`, and backup file creared

Changelog: handled separately
  
### 📝 Documentation
- **changelog**: update changelog

## v1.1.4 (2025-07-25)
### 📝 Documentation
- **TODO.md**: add or change todo
  
  - add or change todo

Changelog: handled separately
  
- **changelog**: update changelog

## v1.1.3 (2025-07-25)
### 🐛 Bug Fixes
- **Makefile**: correct commands
  
  - Fixed broken or unclear `Makefile` commands

Changelog: handled separately
  
### 📝 Documentation
- **changelog**: update changelog

## v1.1.2 (2025-07-25)
### 🔧 Chores
- **release**: manually fix and update version to v1.1.2
  
  - Update version in `app/__version__.py
- synced version in `cz.toml`

Changelog: handled separately
  

## 1.9.2 (2025-08-05)
### 📝 Documentation
- **todo.md**: 1.9.2
  
  Final release of **Custy 1.9.2**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: .
All functionality has been fully validated and production-ready.

- *(Nothing yet)* — See tag message for full context.

---

🎉 **Custy 1.9.2 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#<type>`

Changelog: handled separately
  
- **changelog**: update changelog

## 1.9.1 (2025-08-04)
### 🐛 Bug Fixes
- **main**: 1.9.1
  
  Final release of **Custy 1.9.1**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: .
All functionality has been fully validated and production-ready.

- 🐛 Fixed a minor internal bug to improve stability

---

🎉 **Custy 1.9.1 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#bugfix`

Changelog: handled separately
  
### 🚀 Release
- **main**: 1.9.0
  
  Final release of **Custy 1.9.0**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: 1.9.0rc3, 1.9.0rc2, 1.9.0rc1, 1.9.0b3, 1.9.0b2, 1.9.0b1.
All functionality has been fully validated and production-ready.

### ✨ Features
- Redesigned CLI interface with support for `--silent` / `--debug` modes
- Smart path resolution for configs and templates to prevent ambiguity
- Improved commit/tag message template generation logic

### 📚 Documentation
- Rewrote and cleaned `README.md`, `HOW_TO_USE.md`, and `docs/TODO.md`
- Added badge list and regenerated project structure documentation

### ⚙️ CI/CD
- GitHub Actions and GitLab CI pipelines now support testing and deployment
- Makefile updated with silent execution support (`--no-debug`)

### 🧹 Maintenance & Structure
- Refactored and cleaned up the `app/` structure
- Relocated and organized all templates
- Applied code formatting using `ruff`

### 🐛 Bug Fixes
- Commit type now validated before version resolution
- Fixed pipeline creation issues due to misconfigured jobs
- Resolved internal logic bugs to improve stability
- `assert_is_final_version()` now gracefully handles pre-releases

---

🎉 **Custy 1.9.0 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#feature`, `#bugfix`, `#refactor`
- Docs: `#docs`, `#template`
- CI/CD: `#ci`
- Stability: `#stable`

Changelog: handled separately
  

## 1.9.0rc3 (2025-08-04)
### 🐛 Bug Fixes
- **release**: 1.9.0rc3
  
  Release candidate for **Custy 1.9.0**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- 🐛 Fixed a minor internal bug to improve stability

---

_Tag: `1.9.0rc3`_

🔖 **Tags**:
- Type: `#bugfix`
  

## 1.9.0rc2 (2025-08-04)
### 🐛 Bug Fixes
- **release**: 1.9.0rc2
  
  Release candidate for **Custy 1.9.0**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- 🐛 Fixed a minor internal bug to improve stability

---

_Tag: `1.9.0rc2`_

---

🔖 **Tags**: `#<type>`
  
### 🔧 Chores
- **release**: 1.9.0rc1
  
  Release candidate for **Custy 1.9.0**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release.

### 📚 Documentation
- Updated `docs/TODO.md` to reflect recent changes and clean up outdated tasks
- Confirmed installation steps and usage instructions are ready and verified

---

_Tag: `1.9.0rc1`_

---

🔖 **Tags**:
- Type: `#chore`
  

## 1.9.0rc1 (2025-08-04)
### 📝 Documentation
- **release**: 1.9.0rc1
  
  Release candidate for **Custy 1.9.0**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- Update `docs/TODO.md` to reflect recent changes and clean up outdated entries

---

_Tag: `1.9.0rc1`_

---

🔖 **Tags**: `#<type>`
  

## 1.9.0b3 (2025-08-04)
### 🐛 Bug Fixes
- **core**: 1.9.0b3
  
  Beta release for **Custy 1.9.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- Fixed a minor internal bug affecting stability

---

_Tag: `1.9.0b3`_

---

🔖 **Tags**:
- Type: `#bugfix`
  

## 1.9.0b2 (2025-08-04)
### 🐛 Bug Fixes
- **core**: 1.9.0b2 — fix commit-type validation and pipeline creation issue
  
  Beta release for **Custy 1.9.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
### 🐛 Bug Fixes
- Fixed a bug where commit type wasn't validated before resolving version, which could lead to invalid version bumps
- Fixed issue where pipeline couldn’t be created due to misconfigured job or script condition

---

_Tag: `1.9.0b2`_

---

🔖 **Tags**:
- Type: `#bugfix`
- CI/CD: `#pipeline`
- Versioning: `#versioning`
  
### 🔧 Chores
- **release**: 1.9.0b2
  
  Beta release for **Custy 1.9.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements.

### 📄 Template Enhancements
- Added more example templates for `commit-msg.txt` and `tag-msg.txt` to guide custom formatting

### 🛠️ Makefile Improvements
- Updated Makefile commands to include `--no-debug` for cleaner production runs
  - Example: `custy-all-major` now includes `--no-debug` for silent execution

### ⚙️ Logic Refinement
- Tweaked `assert_is_final_version()`:
  - From blocking pre-releases to simply skipping generation with a warning
  - More graceful handling for versions like `1.9.0b2`, `rc`, `a`, etc.

---

_Tag: `1.9.0b2`_

---

🔖 **Tags**:
- Type: `#chore`, `#cleanup`
- Docs: `#template`
- Config: `#makefile`
  

## 1.9.0 (2025-08-04)
### 🚀 Release
- **main**: 1.9.0
  
  Final release of **Custy 1.9.0**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: 1.9.0rc3, 1.9.0rc2, 1.9.0rc1, 1.9.0b3, 1.9.0b2, 1.9.0b1.
All functionality has been fully validated and production-ready.

### ✨ Features
- Redesigned CLI interface with support for `--silent` / `--debug` modes
- Smart path resolution for configs and templates to prevent ambiguity
- Improved commit/tag message template generation logic

### 📚 Documentation
- Rewrote and cleaned `README.md`, `HOW_TO_USE.md`, and `docs/TODO.md`
- Added badge list and regenerated project structure documentation

### ⚙️ CI/CD
- GitHub Actions and GitLab CI pipelines now support testing and deployment
- Makefile updated with silent execution support (`--no-debug`)

### 🧹 Maintenance & Structure
- Refactored and cleaned up the `app/` structure
- Relocated and organized all templates
- Applied code formatting using `ruff`

### 🐛 Bug Fixes
- Commit type now validated before version resolution
- Fixed pipeline creation issues due to misconfigured jobs
- Resolved internal logic bugs to improve stability
- `assert_is_final_version()` now gracefully handles pre-releases

---

🎉 **Custy 1.9.0 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#feature`, `#bugfix`, `#refactor`
- Docs: `#docs`, `#template`
- CI/CD: `#ci`
- Stability: `#stable`

Changelog: handled separately
  
### 🐛 Bug Fixes
- **release**: 1.9.0rc3
  
  Release candidate for **Custy 1.9.0**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- 🐛 Fixed a minor internal bug to improve stability

---

_Tag: `1.9.0rc3`_

🔖 **Tags**:
- Type: `#bugfix`
  
- **release**: 1.9.0rc2
  
  Release candidate for **Custy 1.9.0**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- 🐛 Fixed a minor internal bug to improve stability

---

_Tag: `1.9.0rc2`_

---

🔖 **Tags**: `#<type>`
  
- **core**: 1.9.0b3
  
  Beta release for **Custy 1.9.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- Fixed a minor internal bug affecting stability

---

_Tag: `1.9.0b3`_

---

🔖 **Tags**:
- Type: `#bugfix`
  
- **core**: 1.9.0b2 — fix commit-type validation and pipeline creation issue
  
  Beta release for **Custy 1.9.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
### 🐛 Bug Fixes
- Fixed a bug where commit type wasn't validated before resolving version, which could lead to invalid version bumps
- Fixed issue where pipeline couldn’t be created due to misconfigured job or script condition

---

_Tag: `1.9.0b2`_

---

🔖 **Tags**:
- Type: `#bugfix`
- CI/CD: `#pipeline`
- Versioning: `#versioning`
  
### 🔧 Chores
- **release**: 1.9.0rc1
  
  Release candidate for **Custy 1.9.0**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release.

### 📚 Documentation
- Updated `docs/TODO.md` to reflect recent changes and clean up outdated tasks
- Confirmed installation steps and usage instructions are ready and verified

---

_Tag: `1.9.0rc1`_

---

🔖 **Tags**:
- Type: `#chore`
  
- **release**: 1.9.0b2
  
  Beta release for **Custy 1.9.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements.

### 📄 Template Enhancements
- Added more example templates for `commit-msg.txt` and `tag-msg.txt` to guide custom formatting

### 🛠️ Makefile Improvements
- Updated Makefile commands to include `--no-debug` for cleaner production runs
  - Example: `custy-all-major` now includes `--no-debug` for silent execution

### ⚙️ Logic Refinement
- Tweaked `assert_is_final_version()`:
  - From blocking pre-releases to simply skipping generation with a warning
  - More graceful handling for versions like `1.9.0b2`, `rc`, `a`, etc.

---

_Tag: `1.9.0b2`_

---

🔖 **Tags**:
- Type: `#chore`, `#cleanup`
- Docs: `#template`
- Config: `#makefile`
  
### 📝 Documentation
- **release**: 1.9.0rc1
  
  Release candidate for **Custy 1.9.0**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- Update `docs/TODO.md` to reflect recent changes and clean up outdated entries

---

_Tag: `1.9.0rc1`_

---

🔖 **Tags**: `#<type>`
  
- **changelog**: update changelog
### 🧠 Refactoring
- **core**: 1.9.0b1 — improve CLI, docs, pipeline, templates, and structure
  
  Beta release for **Custy 1.9.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This update delivers improved CLI usability, updated documentation, better automation, refactored project structure, and improved message templates.

### ✨ Features
- Redesigned CLI interface with clearer UX and new arguments (e.g., silent/debug flags)
- Enhanced file path resolution to avoid ambiguity for key config and template files

### 📚 Documentation
- Rewrote `README.md` and added badges (`docs/badges.md`)
- Created user guide: `docs/HOW_TO_USE.md`
- Regenerated project structure documentation

### ⚙️ CI/CD
- Added GitHub Actions workflow and GitLab CI pipeline to run tests on push

### 🧹 Maintenance
- Cleaned and refactored `app/` directory
- Code formatted with `ruff`

### 📄 Template Improvements
- Reorganized and renamed `commit-msg.txt` and `tag-msg.txt` templates
- Updated commit/tag message generation to use new structure

### 🐛 Bug Fix
- Fixed a minor internal bug affecting stability

### 🛠️ Misc
- Updated `Makefile`, `pyproject.toml`, and related config files
- Removed unused file `q`

---

_Tag: `1.9.0b1`_

---

🔖 **Tags**:
- Type: `#feature`, `#bugfix`, `#refactor`
- Docs: `#docs`, `#template`
- CI/CD: `#ci`, `#cleanup`
  

## 1.8.1 (2025-08-02)
### 🐛 Bug Fixes
- **push**: 1.8.1
  
  Final release of **Custy 1.8.1**, promoted from the latest release candidate.
includes all feature and fixes from pre-releases: .

This final release includes all validated features and fixes from earlier pre-releases:
- auto-push backup/main after changelog generation

Previously, the backup remote (`backup/main`) was not automatically pushed after generating `CHANGELOG.md`. This bug has now been fixed.

Now, after changelog generation completes, `backup/main` is automatically synced to ensure both remotes stay consistent.

Tag: 1.8.1
Changelog: handled separately
  
### 📝 Documentation
- **changelog**: update changelog
### 🚀 Release
- **core**: 1.8.0
  
  Final release of **Custy 1.8.0**, promoted from the latest release candidate.
includes all feature and fixes from pre-releases: 1.8.0rc2, 1.8.0rc1.

This final release includes all validated features and fixes from earlier pre-releases:
- Git workflow validation via WorkflowManager
- Temporary branch cleanup with Branch Cleaner
- Dual remote strategy: GitLab (main), GitHub (backup)
- Strategy-specific version helpers (PEP 440, SemVer)
- Cleaner code structure with VersionHelperBase
- Updated Makefile and improved documentation

🛠 Final tweaks after rc2:
- Allow `custy all` to run `--sync-backup` automatically
- Minor improvements to support `release` commit type
- Refined docs and cleaned up TODO list

Tag: 1.8.0
Changelog: handled separately
  

## 1.8.0rc2 (2025-08-01)
### 🧠 Refactoring
- **workflow**: 1.8.0rc2
  
  Release candidate for **Custy 1.8.0**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This refactor decouples strategy-specific logic (PEP 440, SemVer) from the core
WorkflowManager class by introducing a VersionHelperBase interface. Both
PEP440VersionHelper and SemverVersionHelper now implement:

- classify(): identify version tier
- tier_order(): precedence for tier promotion
- suggest_tag(): next tag suggestion based on branch
- get_transition_cases(): valid CASE transitions

WorkflowManager is now cleaner and delegates classification, version suggestion,
and transition validation to the appropriate strategy helper dynamically.

This release candidate consolidates finalized features and bug fixes before the stable release:
- Update `docs/TODO.md` to reflect recent changes and clean up outdated entries

Other improvements:
- Reduced branching logic in check_transition()
- Added docstrings across all helper classes
- Improved extensibility for future strategies (e.g., CalVer)

BREAKING CHANGE: version helpers must now implement VersionHelperBase interface

Tag: 1.8.0rc2
  

## 1.8.0 (2025-08-02)
### 🚀 Release
- **core**: 1.8.0
  
  Final release of **Custy 1.8.0**, promoted from the latest release candidate.
includes all feature and fixes from pre-releases: 1.8.0rc2, 1.8.0rc1.

This final release includes all validated features and fixes from earlier pre-releases:
- Git workflow validation via WorkflowManager
- Temporary branch cleanup with Branch Cleaner
- Dual remote strategy: GitLab (main), GitHub (backup)
- Strategy-specific version helpers (PEP 440, SemVer)
- Cleaner code structure with VersionHelperBase
- Updated Makefile and improved documentation

🛠 Final tweaks after rc2:
- Allow `custy all` to run `--sync-backup` automatically
- Minor improvements to support `release` commit type
- Refined docs and cleaned up TODO list

Tag: 1.8.0
Changelog: handled separately
  
### 🧠 Refactoring
- **workflow**: 1.8.0rc2
  
  Release candidate for **Custy 1.8.0**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This refactor decouples strategy-specific logic (PEP 440, SemVer) from the core
WorkflowManager class by introducing a VersionHelperBase interface. Both
PEP440VersionHelper and SemverVersionHelper now implement:

- classify(): identify version tier
- tier_order(): precedence for tier promotion
- suggest_tag(): next tag suggestion based on branch
- get_transition_cases(): valid CASE transitions

WorkflowManager is now cleaner and delegates classification, version suggestion,
and transition validation to the appropriate strategy helper dynamically.

This release candidate consolidates finalized features and bug fixes before the stable release:
- Update `docs/TODO.md` to reflect recent changes and clean up outdated entries

Other improvements:
- Reduced branching logic in check_transition()
- Added docstrings across all helper classes
- Improved extensibility for future strategies (e.g., CalVer)

BREAKING CHANGE: version helpers must now implement VersionHelperBase interface

Tag: 1.8.0rc2
  
### 🐛 Bug Fixes
- **core**: 1.8.0rc1
  
  Release candidate for **Custy 1.8.0**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- use 2 permanent branches: `main` (stable) and `develop` (experimental)
- configure dual remote setup: GitLab as main, GitHub as backup
- implement branching workflow checking (WorkflowManager)
- add branch cleaner to prune temporary branches
- update Makefile with latest tasks
- expand documentation

Tag: 1.8.0rc1
  
### 📝 Documentation
- **changelog**: update changelog

## 1.7.1.post1 (2025-08-01)
### 🐛 Bug Fixes
- **release**: 1.7.1.post1
  
  Post-release patch for **Custy 1.7.1**, addressing minor updates or corrections.
Includes minor updates or documentation fixes after release 1.7.1.

This post-release includes minor updates and corrections after the official release:
- Allow CLI to accept arguments without explicitily requiring the `--bump` flag
- Fix issue in the `Makefile` execution flow
- Update `docs/TODO.md` to reflect recent changes and clean up outdated entries

Tag: 1.7.1.post1
Changelog: handled separately
  
### 📦 Others
- **general**: merge release 1.7.1 into main
### 📝 Documentation
- **changelog**: update changelog

## 1.7.1 (2025-08-01)
### 🐛 Bug Fixes
- **release**: 1.7.1
  
  Final release of **Custy 1.7.1**, promoted from the latest release candidate.
includes all feature and fixes from pre-releases: .

This final release includes all validated features and fixes from earlier pre-releases:
- Fix the file name from `pep404_strategy.py` → `pep440_strategy.py`
- Rename class from `PEP404Strategy` → `PEP440Strategy`
- Bug fix: Switch to post-release uses `1.5.0.post1` instead of bumping minor to `1.6.0.post1`
- Refactor and clean up `SemverStrategy` and `PEP440Strategy` classes
- Add test coverage for both strategy classes
- Add documentation: `docs/versioning/switching version.md`
- Verbose step logging before changelog generation to improve debugging
- Ensure commit and tag backup files are staged before commit
- Improve dry-run flow in message generation
- Update `TODO.md` to reflect current feature status

Tag: 1.7.1
Changelog: handled separately
  
### 📝 Documentation
- **changelog**: update changelog

## 1.7.0.post3 (2025-07-31)
### 📝 Documentation
- **release**: 1.7.0.post3
  
  Post-release patch for **Custy 1.7.0**, addressing minor updates or corrections.
Includes minor updates or documentation fixes after release 1.7.0.

This post-release includes minor updates and corrections after the official release:
- modified documentation `docs/TODO.md`

Tag: 1.7.0.post3
Changelog: handled separately
  
- **changelog**: update changelog

## 1.6.0.post2 (2025-07-31)
### 🐛 Bug Fixes
- **release**: 1.6.0.post2
  
  Post-release patch for **Custy 1.6.0**, addressing minor updates or corrections.
Includes minor updates or documentation fixes after release 1.6.0.

This post-release includes minor updates and corrections after the official release:
- Bug fixed case example changes from 1.5.0.post1 → 1.5.0.post2
- Bug fixed on `Makefile`
- modified documentation `docs/TODO.md`

Tag: 1.6.0.post2
Changelog: handled separately
  
### 📝 Documentation
- **changelog**: update changelog
- **release**: v1.5.0.post1
  
  Post-release patch for **Custy v1.5.0**, addressing minor updates or corrections.
Includes minor updates or documentation fixes after release v1.5.0.

This post-release includes minor updates and corrections after the official release:
- Added a new documentation `docs/Q&A/git/footer section on tag message.md`
- modified documentations `docs/Q&A/git/changelogs approach.md`, `docs/Q&A/git/comparison commit and tag message.md`, `docs/TODO.md`
- Modified Makefile by adding documentations

Tag: v1.5.0.post1
Changelog: handled separately
  
- **changelog**: update changelog
### ✨ Features
- **release**: 1.5.0
  
  Final release of **Custy 1.5.0**, promoted from the latest release candidate.
includes all feature and fixes from pre-releases: 1.5.0rc1, 1.5.0b3, 1.5.0b2, 1.5.0b1.

This final release includes all validated features and fixes from earlier pre-releases:
- Add structured generation of `commit-msg.txt` and `tag-msg.txt`
- Improve message clarity, flexibility, and consistency
- Enhance template customization for different version types (alpha, beta, rc, final)
- Ensure commit/tag message files are properly staged and backed up
- Fix dry-run behavior in message generation flow
- Address minor edge cases in automation
- Reference commit/tag standards in `docs\git\commit_message.md`
- Add internal usage notes and automation guidance
- Ensure commit and tag backup files and odl files to staged and commit
- Handle staged and commit when no staged changes detected
- Updated `TODO.md`

Tag: 1.5.0
Changelog: handled separately
  

## 1.5.0rc1 (2025-07-31)
### 📝 Documentation
- **release**: 1.5.0rc1
  
  Release candidate for **Custy 1.5.0**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- *(Nothing yet)* — See tag message for full context.

Tag: 1.5.0rc1
  

## 1.5.0b3 (2025-07-31)
### 🐛 Bug Fixes
- **release**: 1.5.0b3
  
  Beta release for **Custy 1.5.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- *(Nothing yet)* — See tag message for full context.

Tag: 1.5.0b3
  

## 1.5.0b2 (2025-07-30)
### 🐛 Bug Fixes
- **release**: 1.5.0b2
  
  Beta release for **Custy 1.5.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- *(Nothing yet)* — See tag message for full context.

Tag: 1.5.0b2
  

## 1.5.0 (2025-07-31)
### ✨ Features
- **release**: 1.5.0
  
  Final release of **Custy 1.5.0**, promoted from the latest release candidate.
includes all feature and fixes from pre-releases: 1.5.0rc1, 1.5.0b3, 1.5.0b2, 1.5.0b1.

This final release includes all validated features and fixes from earlier pre-releases:
- Add structured generation of `commit-msg.txt` and `tag-msg.txt`
- Improve message clarity, flexibility, and consistency
- Enhance template customization for different version types (alpha, beta, rc, final)
- Ensure commit/tag message files are properly staged and backed up
- Fix dry-run behavior in message generation flow
- Address minor edge cases in automation
- Reference commit/tag standards in `docs\git\commit_message.md`
- Add internal usage notes and automation guidance
- Ensure commit and tag backup files and odl files to staged and commit
- Handle staged and commit when no staged changes detected
- Updated `TODO.md`

Tag: 1.5.0
Changelog: handled separately
  
- **release**: 1.5.0b1
  
  Beta release for **Custy 1.5.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- *(Nothing yet)* — See tag message for full context.

Tag: 1.5.0b1
  
### 📝 Documentation
- **release**: 1.5.0rc1
  
  Release candidate for **Custy 1.5.0**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- *(Nothing yet)* — See tag message for full context.

Tag: 1.5.0rc1
  
- **changelog**: update changelog
### 🐛 Bug Fixes
- **release**: 1.5.0b3
  
  Beta release for **Custy 1.5.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- *(Nothing yet)* — See tag message for full context.

Tag: 1.5.0b3
  
- **release**: 1.5.0b2
  
  Beta release for **Custy 1.5.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- *(Nothing yet)* — See tag message for full context.

Tag: 1.5.0b2
  
### 🔧 Chores
- **release**: 1.5.0b1
  
  Beta release for **Custy 1.5.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- *(Nothing yet)* — See tag message for full context.

Tag: 1.5.0b1
  
- **release**: v1.5.0a1
  
  - _(Nothing yet)_

Tag: v1.5.0a1
  
- **release**: v1.5.0a2
  
  - _(Nothing yet)_

Tag: v1.5.0a2
  
- **release**: v1.5.0rc1
  
  - _(Nothing yet)_

Tag: v1.5.0rc1
  
- **release**: v1.5.0
  
  - _(Nothing yet)_

Tag: v1.5.0
  

## 1.4.3 (2025-07-29)
### 🧠 Refactoring
- **release**: v1.4.3
  
  Final release of Custy v1.4.3

Refactor Code using Ruff

Tag: v1.4.3
Changelog: handled separately
  
### 📝 Documentation
- **changelog**: update changelog
- **changelog**: update changelog
### 🔧 Chores
- **release**: v1.4.2
  
  Final release of Custy v1.4.2

Includes modified documentation.

Tag: v1.4.2
Changelog: handled separately
  

## 1.4.2 (2025-07-29)
### 📝 Documentation
- **release**: v1.4.1
  
  Final release of Custy v1.4.1

Includes modified documentation.

Tag: v1.4.1
Changelog: handled separately
  
- **changelog**: update changelog

## 1.4.1 (2025-07-29)
### 🐛 Bug Fixes
- **release**: v1.4.1
  
  Final release of Custy v1.4.1

Includes bug fixes.

Tag: v1.4.1
Changelog: handled separately
  
### 📝 Documentation
- **changelog**: update changelog
- **release**: v1.4.1
  
  Final release of Custy v1.4.1

Includes bug fixes.

Tag: v1.4.1
Changelog: handled separately
  
- **changelog**: update changelog
### 🔧 Chores
- **release**: v1.4.0
  
  Final release of Custy v1.4.0 - prompted from release candidate.

Includes all feature and fixes from alpha and RC pre-releases.

Tag: v1.4.0
Changelog: handled separately
  

## 1.4.0rc3 (2025-07-29)
### 🐛 Bug Fixes
- **release**: v1.4.0rc5
  
  Release candidate for v1.4.0, consolidating all pre-release changes.

- Resolved issue with `get_commits_between_tags()` in `GitHelper`(`app\utils\git.py`).

Tag: v1.4.0rc5
  

## 1.4.0rc2 (2025-07-29)
### 🐛 Bug Fixes
- **release**: v1.4.0rc4
  
  Release candidate for v1.4.0, consolidating all pre-release changes.

- Resolved issue with `_prepare_release_message_from_prereleases()` in `GitCommitTagger`(`app\git_commit_tagger.py`).

Tag: v1.4.0rc4
  

## 1.4.0rc1 (2025-07-29)
### 🐛 Bug Fixes
- **release**: v1.4.0rc3
  
  Release candidate for v1.4.0, consolidating all pre-release changes.

- Resolved issue with `get_last_tag_before()` in `GitHelper`(`app\utils\git.py`).

Tag: v1.4.0rc3
  
### 🔧 Chores
- **release**: v1.4.0rc2
  
  Release candidate for v1.4.0, consolidating all pre-release changes.

- Improve docs

Tag: v1.4.0rc2
  
- **release**: v1.4.0rc1
  
  Release candidate for v1.4.0, consolidating all pre-release changes.

Includes:
- Version bump protection within pre-release tier (e.g., rc1 → rc2)
- Restriction of changelog to final releases only
- Commit type validation for bump/tag operations
- Project type detection (PEP 440 or SemVer) for versioning
- External tag message support (`tag-msg.txt`)
- Auto-generation of release commit/tag message templates
- RC → final bump without patch increment
- `cleanup-backups` CLI command
- Improved dry-run behavior
- Expanded documentation and Makefile updates
- Backup/template folder resolution fixes

Tag: v1.4.0rc1
  

## 1.4.0 (2025-07-29)
### 📝 Documentation
- **release**: v1.4.1
  
  Final release of Custy v1.4.1

Includes bug fixes.

Tag: v1.4.1
Changelog: handled separately
  
- **changelog**: update changelog
- **changelog**: update changelog
### 🔧 Chores
- **release**: v1.4.0
  
  Final release of Custy v1.4.0 - prompted from release candidate.

Includes all feature and fixes from alpha and RC pre-releases.

Tag: v1.4.0
Changelog: handled separately
  
- **release**: v1.4.0rc2
  
  Release candidate for v1.4.0, consolidating all pre-release changes.

- Improve docs

Tag: v1.4.0rc2
  
- **release**: v1.4.0rc1
  
  Release candidate for v1.4.0, consolidating all pre-release changes.

Includes:
- Version bump protection within pre-release tier (e.g., rc1 → rc2)
- Restriction of changelog to final releases only
- Commit type validation for bump/tag operations
- Project type detection (PEP 440 or SemVer) for versioning
- External tag message support (`tag-msg.txt`)
- Auto-generation of release commit/tag message templates
- RC → final bump without patch increment
- `cleanup-backups` CLI command
- Improved dry-run behavior
- Expanded documentation and Makefile updates
- Backup/template folder resolution fixes

Tag: v1.4.0rc1
  
### 🐛 Bug Fixes
- **release**: v1.4.0rc5
  
  Release candidate for v1.4.0, consolidating all pre-release changes.

- Resolved issue with `get_commits_between_tags()` in `GitHelper`(`app\utils\git.py`).

Tag: v1.4.0rc5
  
- **release**: v1.4.0rc4
  
  Release candidate for v1.4.0, consolidating all pre-release changes.

- Resolved issue with `_prepare_release_message_from_prereleases()` in `GitCommitTagger`(`app\git_commit_tagger.py`).

Tag: v1.4.0rc4
  
- **release**: v1.4.0rc3
  
  Release candidate for v1.4.0, consolidating all pre-release changes.

- Resolved issue with `get_last_tag_before()` in `GitHelper`(`app\utils\git.py`).

Tag: v1.4.0rc3
  
### ✨ Features
- **core**: implement advanced versioning rules and CLI behavior controls
  
  This commit introduces a series of improvements across versioning, tagging, changelog generation, and backup handling in Custy CLI.

- Prevents major.minor.patch bump when incrementing within same pre-release tier (e.g. rc1 → rc2)
- Generates changelog only on final releases (e.g. v1.2.3), skipping pre-releases
- Enforces bump/tag only for specific types [feat, fix, perf, docs, refactor]; others require CLI override
- Detects project type (Python or JavaScript) to apply correct versioning scheme (PEP 440 or SemVer)
- Tag messages now opened in external file like commit-msg.txt; supports default message via flag
- For release tags, auto-generates commit/tag message template from all prereleases (pre, dev, etc.)
- Prevents bump from rc → final from incrementing patch (v1.2.3rc1 → v1.2.3, not v1.2.4)
- Adds cleanup logic for `backups/`, keeping 10 latest (customizable via CLI)
- Fixes backup and template folder resolution; commit-msg.txt placement corrected
- Adds `cleanup-backups` CLI handler
- Updated `.gitignore` to ignore `templates/tag-msg.txt`
- Updated `.projectignore` to ignore `templates/tag-msg.txt`

Changelog: handled separately
  

## 1.3.3 (2025-07-25)
### 📝 Documentation
- **TODO.md**: add or change todo
  
  - add or change todo

Changelog: handled separately
  
- **changelog**: update changelog

## 1.3.2 (2025-07-25)
### 📝 Documentation
- **TODO.md**: add or change todo
  
  - add or change todo

Changelog: handled separately
  
- **changelog**: update changelog

## 1.3.1rc2 (2025-07-25)
### 🔧 Chores
- **commit_msg**: support 'release' as valid Conventional Commit type
  
  - Added 'release' to allowed commit types in the validator

Changelog: handled separately
  
### 📝 Documentation
- **changelog**: update changelog

## 1.10.9 (2025-08-07)
### 🚀 Release
- **main**: 1.10.9
  
  Final release of **Custy 1.10.9**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: .
All functionality has been fully validated and production-ready.

- fix issue on `.github\workflows\test.yml`

---

🎉 **Custy 1.10.9 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#bugfix`
- Stability: `#stable`

Changelog: handled separately
  
### 📝 Documentation
- **changelog**: update changelog

## 1.10.8 (2025-08-07)
### 🚀 Release
- **main**: 1.10.8
  
  Final release of **Custy 1.10.8**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: .
All functionality has been fully validated and production-ready.

- Updated `README.md`

---

🎉 **Custy 1.10.8 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`
- Docs: `#docs`
- Stability: `#stable`

Changelog: handled separately
  
### 📝 Documentation
- **changelog**: update changelog

## 1.10.7 (2025-08-07)
### 🚀 Release
- **main**: 1.10.7
  
  Final release of **Custy 1.10.7**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: .
All functionality has been fully validated and production-ready.

- Updated `README.md`

---

🎉 **Custy 1.10.7 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`
- Docs: `#docs`
- Stability: `#stable`

Changelog: handled separately
  
- **main**: 1.10.6 — improve workflow safety, templates, and user interaction
  
  Final release of **Custy 1.10.6**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: 1.10.6rc4, 1.10.6rc3, 1.10.6rc2, 1.10.6rc1, 1.10.6b1.
All functionality has been fully validated and production-ready.
It focuses on refining the WorkflowManager, enhancing commit/tag templates, and introducing safety improvements for merge operations.

### 🐛 Fixes
- Prevented unsafe execution in CASE 3, 6, and 9 if staged files exist
- Added interactive prompt when no files are staged to confirm whether to continue

### 🧠 UX Improvements
- Safer tagging and merging via confirmation-based logic
- More resilient and predictable branching flow

### 📄 Templates
- Refactored and expanded `commit-msg.txt` and `tag-msg.txt` example templates

### 📚 Documentation
- Updated project structure docs to reflect current implementation

---

🎉 **Custy 1.10.6 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#bugfix`, `#refactor
- UX: `#ux`
- docs: `#docs`, `#template`
- Workflow: `#workflow`
- Maintenance: `#cleanup``
- Stability: `#stable`

Changelog: handled separately
  
### 📝 Documentation
- **changelog**: update changelog

## 1.10.6rc4 (2025-08-06)
### 🧠 Refactoring
- **template**: 1.10.6rc4
  
  Release candidate for **Custy 1.10.6**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release.

### 📄 Templates
    - Refactored and expanded example templates for commit and tag messages

---

_Tag: `1.10.6rc4`_

🔖 **Tags**:
- Type: `#refactor`
- Stability: `#rc`
  

## 1.10.6rc3 (2025-08-06)
### 🐛 Bug Fixes
- **workflow**: 1.10.6rc3
  
  Release candidate for **Custy 1.10.6**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

### 🐛 Fixes
- Prevent unintended execution in CASE 3, 6, and 9 if staged files exist
- Ensures safety during critical merge operations inside `WorkflowManager`

### 🧠 UX Improvement
- Added interactive prompt (`y/n`) when no files are staged during validation
- Allows user to explicitly confirm whether to proceed or abort

These changes make the workflow execution more resilient and user-aware during tagging phases.

---

_Tag: `1.10.6rc3`_

🔖 **Tags**:
- Type: `#bugfix`
- Workflow: `#workflow`
- Stability: `#safety`
- Pre-release: `#rc`
  

## 1.10.6rc2 (2025-08-06)
### 🧠 Refactoring
- **workflow**: 1.10.6rc2
  
  Release candidate for **Custy 1.10.6**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- *(Nothing yet)* — See tag message for full context.

---

_Tag: `1.10.6rc2`_

🔖 **Tags**:
- Type: `#refactor`workflow
  

## 1.10.6rc1 (2025-08-06)
### 🐛 Bug Fixes
- **workflow**: 1.10.6rc1
  
  Release candidate for **Custy 1.10.6**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

### 📚 Documentation
- 📘 update `project structure` documentation

---

_Tag: `1.10.6rc1`_

🔖 **Tags**:
- Type: `#bugfix`
  

## 1.10.6 (2025-08-06)
### 🚀 Release
- **main**: 1.10.6 — improve workflow safety, templates, and user interaction
  
  Final release of **Custy 1.10.6**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: 1.10.6rc4, 1.10.6rc3, 1.10.6rc2, 1.10.6rc1, 1.10.6b1.
All functionality has been fully validated and production-ready.
It focuses on refining the WorkflowManager, enhancing commit/tag templates, and introducing safety improvements for merge operations.

### 🐛 Fixes
- Prevented unsafe execution in CASE 3, 6, and 9 if staged files exist
- Added interactive prompt when no files are staged to confirm whether to continue

### 🧠 UX Improvements
- Safer tagging and merging via confirmation-based logic
- More resilient and predictable branching flow

### 📄 Templates
- Refactored and expanded `commit-msg.txt` and `tag-msg.txt` example templates

### 📚 Documentation
- Updated project structure docs to reflect current implementation

---

🎉 **Custy 1.10.6 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#bugfix`, `#refactor
- UX: `#ux`
- docs: `#docs`, `#template`
- Workflow: `#workflow`
- Maintenance: `#cleanup``
- Stability: `#stable`

Changelog: handled separately
  
- **main**: 1.10.5
  
  Final release of **Custy 1.10.5**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: 1.10.5rc1, 1.10.5b1.
All functionality has been fully validated and production-ready.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

🎉 **Custy 1.10.5 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#bugfix`
- Stability: `#stable`

Changelog: handled separately
  
### 🧠 Refactoring
- **template**: 1.10.6rc4
  
  Release candidate for **Custy 1.10.6**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release.

### 📄 Templates
    - Refactored and expanded example templates for commit and tag messages

---

_Tag: `1.10.6rc4`_

🔖 **Tags**:
- Type: `#refactor`
- Stability: `#rc`
  
- **workflow**: 1.10.6rc2
  
  Release candidate for **Custy 1.10.6**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- *(Nothing yet)* — See tag message for full context.

---

_Tag: `1.10.6rc2`_

🔖 **Tags**:
- Type: `#refactor`workflow
  
### 🐛 Bug Fixes
- **workflow**: 1.10.6rc3
  
  Release candidate for **Custy 1.10.6**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

### 🐛 Fixes
- Prevent unintended execution in CASE 3, 6, and 9 if staged files exist
- Ensures safety during critical merge operations inside `WorkflowManager`

### 🧠 UX Improvement
- Added interactive prompt (`y/n`) when no files are staged during validation
- Allows user to explicitly confirm whether to proceed or abort

These changes make the workflow execution more resilient and user-aware during tagging phases.

---

_Tag: `1.10.6rc3`_

🔖 **Tags**:
- Type: `#bugfix`
- Workflow: `#workflow`
- Stability: `#safety`
- Pre-release: `#rc`
  
- **workflow**: 1.10.6rc1
  
  Release candidate for **Custy 1.10.6**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

### 📚 Documentation
- 📘 update `project structure` documentation

---

_Tag: `1.10.6rc1`_

🔖 **Tags**:
- Type: `#bugfix`
  
- **workflow**: 1.10.6b1
  
  Beta release for **Custy 1.10.6**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

_Tag: `1.10.6b1`_

🔖 **Tags**:
- Type: `#bugfix`
  
### 📝 Documentation
- **changelog**: update changelog

## 1.10.5rc1 (2025-08-06)
### 🐛 Bug Fixes
- **workflow**: 1.10.5rc1
  
  Release candidate for **Custy 1.10.5**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

_Tag: `1.10.5rc1`_

🔖 **Tags**:
- Type: `#bugfix`
  

## 1.10.5 (2025-08-06)
### 🚀 Release
- **main**: 1.10.5
  
  Final release of **Custy 1.10.5**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: 1.10.5rc1, 1.10.5b1.
All functionality has been fully validated and production-ready.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

🎉 **Custy 1.10.5 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#bugfix`
- Stability: `#stable`

Changelog: handled separately
  
- **main**: 1.10.4
  
  Final release of **Custy 1.10.4**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: 1.10.4rc1, 1.10.4b1.
All functionality has been fully validated and production-ready.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

🎉 **Custy 1.10.4 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#bugfix`
- Stability: `#stable`

Changelog: handled separately
  
### 🐛 Bug Fixes
- **workflow**: 1.10.5rc1
  
  Release candidate for **Custy 1.10.5**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

_Tag: `1.10.5rc1`_

🔖 **Tags**:
- Type: `#bugfix`
  
- **workflow**: 1.10.5b1
  
  Beta release for **Custy 1.10.5**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- reapplied clean branch functionality

---

_Tag: `1.10.5b1`_

🔖 **Tags**:
- Type: `#bugfix`
  
### 📝 Documentation
- **changelog**: update changelog

## 1.10.4rc1 (2025-08-06)
### 🐛 Bug Fixes
- **core**: 1.10.4rc1
  
  Release candidate for **Custy 1.10.4**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

_Tag: `1.10.4rc1`_

🔖 **Tags**:
- Type: `#bugfix`
  

## 1.10.4 (2025-08-06)
### 🚀 Release
- **main**: 1.10.4
  
  Final release of **Custy 1.10.4**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: 1.10.4rc1, 1.10.4b1.
All functionality has been fully validated and production-ready.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

🎉 **Custy 1.10.4 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#bugfix`
- Stability: `#stable`

Changelog: handled separately
  
### 🐛 Bug Fixes
- **core**: 1.10.4rc1
  
  Release candidate for **Custy 1.10.4**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

_Tag: `1.10.4rc1`_

🔖 **Tags**:
- Type: `#bugfix`
  
### 🧠 Refactoring
- **core**: 1.10.4b1
  
  Beta release for **Custy 1.10.4**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- This release just for testing the app for release

---

_Tag: `1.10.4b1`_

🔖 **Tags**:
- Type: `#refactor`
  
### 📝 Documentation
- **changelog**: update changelog

## 1.10.3 (2025-08-06)
### 🚀 Release
- **main**: 1.10.3
  
  Final release of **Custy 1.10.3**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: .
All functionality has been fully validated and production-ready.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

🎉 **Custy 1.10.3 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#bugfix`
- Stability: `#stable`

Changelog: handled separately
  
- **main**: 1.10.2
  
  Final release of **Custy 1.10.2**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: 1.10.2rc1, 1.10.2b1.
All functionality has been fully validated and production-ready.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

🎉 **Custy 1.10.2 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#bugfix`
- Stability: `#stable`

Changelog: handled separately
  
### 📝 Documentation
- **changelog**: update changelog

## 1.10.2rc1 (2025-08-06)
### 🐛 Bug Fixes
- **workflow**: 1.10.2rc1
  
  Release candidate for **Custy 1.10.2**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- *(Nothing yet)* — See tag message for full context.

---

_Tag: `1.10.2rc1`_

🔖 **Tags**:
- Type: `#bugfix`
  

## 1.10.2 (2025-08-06)
### 🚀 Release
- **main**: 1.10.2
  
  Final release of **Custy 1.10.2**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: 1.10.2rc1, 1.10.2b1.
All functionality has been fully validated and production-ready.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

🎉 **Custy 1.10.2 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#bugfix`
- Stability: `#stable`

Changelog: handled separately
  
- **main**: 1.10.1
  
  Final release of **Custy 1.10.1**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: 1.10.1rc1, 1.10.1b2, 1.10.1b1.
All functionality has been fully validated and production-ready.

### 🧹 Maintenance & Structure
- Code formatted with `ruff`

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

🎉 **Custy 1.10.1 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#bugfix`
- Maintenance: `#cleanup`
- Stability: `#stable`

Changelog: handled separately
  
### 🐛 Bug Fixes
- **workflow**: 1.10.2rc1
  
  Release candidate for **Custy 1.10.2**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- *(Nothing yet)* — See tag message for full context.

---

_Tag: `1.10.2rc1`_

🔖 **Tags**:
- Type: `#bugfix`
  
- **workflow**: 1.10.2b1
  
  Beta release for **Custy 1.10.2**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- 🐛 Fixed a minor internal bug to improve stability

---

_Tag: `1.10.2b1`_

🔖 **Tags**:
- Type: `#bugfix`
  
### 📝 Documentation
- **changelog**: update changelog

## 1.10.1rc1 (2025-08-06)
### 🧠 Refactoring
- **release**: 1.10.1rc1
  
  Release candidate for **Custy 1.10.1**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- *(Nothing yet)* — See tag message for full context.

---

_Tag: `1.10.1rc1`_

🔖 **Tags**:
- Type: `#refactor`
  
### 🔧 Chores
- **release**: 1.10.1rc1
  
  Release candidate for **Custy 1.10.1**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- *(Nothing yet)* — See tag message for full context.

---

_Tag: `1.10.1rc1`_

🔖 **Tags**:
- Type: `#chore`
  

## 1.10.1b2 (2025-08-06)
### 🐛 Bug Fixes
- **workflow**: 1.10.1b2
  
  Beta release for **Custy 1.10.1**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- 🐛 Fixed a minor internal bug to improve stability

---

_Tag: `1.10.1b2`_

🔖 **Tags**:
- Type: `#bugfix`
  

## 1.10.11 (2025-11-11)
### 🚀 Release
- **main**: 1.10.11
  
  Final release of **Custy 1.10.11**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: .
All functionality has been fully validated and production-ready.

- modified `requirements.txt`

---

🎉 **Custy 1.10.11 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#bugfix`
- Stability: `#stable`

Changelog: handled separately
  
### 📦 Others
- **general**: Merge pull request #1 from devalltect00/develop
  
  Develop
  
### 📝 Documentation
- **changelog**: update changelog

## 1.10.10 (2025-11-11)
### 🚀 Release
- **main**: 1.10.10
  
  Final release of **Custy 1.10.10**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: .
All functionality has been fully validated and production-ready.

- modified `README.md`
- modified `TODO.md`
- modified `requirements.txt`

---

🎉 **Custy 1.10.10 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#bugfix`
- Stability: `#stable`

Changelog: handled separately
  
- **main**: 1.10.9
  
  Final release of **Custy 1.10.9**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: .
All functionality has been fully validated and production-ready.

- fix issue on `.github\workflows\test.yml`

---

🎉 **Custy 1.10.9 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#bugfix`
- Stability: `#stable`

Changelog: handled separately
  
- **main**: 1.10.8
  
  Final release of **Custy 1.10.8**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: .
All functionality has been fully validated and production-ready.

- Updated `README.md`

---

🎉 **Custy 1.10.8 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`
- Docs: `#docs`
- Stability: `#stable`

Changelog: handled separately
  
- **main**: 1.10.7
  
  Final release of **Custy 1.10.7**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: .
All functionality has been fully validated and production-ready.

- Updated `README.md`

---

🎉 **Custy 1.10.7 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`
- Docs: `#docs`
- Stability: `#stable`

Changelog: handled separately
  
- **main**: 1.10.6 — improve workflow safety, templates, and user interaction
  
  Final release of **Custy 1.10.6**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: 1.10.6rc4, 1.10.6rc3, 1.10.6rc2, 1.10.6rc1, 1.10.6b1.
All functionality has been fully validated and production-ready.
It focuses on refining the WorkflowManager, enhancing commit/tag templates, and introducing safety improvements for merge operations.

### 🐛 Fixes
- Prevented unsafe execution in CASE 3, 6, and 9 if staged files exist
- Added interactive prompt when no files are staged to confirm whether to continue

### 🧠 UX Improvements
- Safer tagging and merging via confirmation-based logic
- More resilient and predictable branching flow

### 📄 Templates
- Refactored and expanded `commit-msg.txt` and `tag-msg.txt` example templates

### 📚 Documentation
- Updated project structure docs to reflect current implementation

---

🎉 **Custy 1.10.6 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#bugfix`, `#refactor
- UX: `#ux`
- docs: `#docs`, `#template`
- Workflow: `#workflow`
- Maintenance: `#cleanup``
- Stability: `#stable`

Changelog: handled separately
  
- **main**: 1.10.5
  
  Final release of **Custy 1.10.5**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: 1.10.5rc1, 1.10.5b1.
All functionality has been fully validated and production-ready.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

🎉 **Custy 1.10.5 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#bugfix`
- Stability: `#stable`

Changelog: handled separately
  
- **main**: 1.10.4
  
  Final release of **Custy 1.10.4**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: 1.10.4rc1, 1.10.4b1.
All functionality has been fully validated and production-ready.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

🎉 **Custy 1.10.4 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#bugfix`
- Stability: `#stable`

Changelog: handled separately
  
- **main**: 1.10.3
  
  Final release of **Custy 1.10.3**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: .
All functionality has been fully validated and production-ready.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

🎉 **Custy 1.10.3 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#bugfix`
- Stability: `#stable`

Changelog: handled separately
  
- **main**: 1.10.2
  
  Final release of **Custy 1.10.2**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: 1.10.2rc1, 1.10.2b1.
All functionality has been fully validated and production-ready.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

🎉 **Custy 1.10.2 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#bugfix`
- Stability: `#stable`

Changelog: handled separately
  
### 📝 Documentation
- **changelog**: update changelog
- **changelog**: update changelog
- **changelog**: update changelog
- **changelog**: update changelog
- **changelog**: update changelog
- **changelog**: update changelog
- **changelog**: update changelog
- **changelog**: update changelog
- **changelog**: update changelog
### 🧠 Refactoring
- **template**: 1.10.6rc4
  
  Release candidate for **Custy 1.10.6**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release.

### 📄 Templates
    - Refactored and expanded example templates for commit and tag messages

---

_Tag: `1.10.6rc4`_

🔖 **Tags**:
- Type: `#refactor`
- Stability: `#rc`
  
- **workflow**: 1.10.6rc2
  
  Release candidate for **Custy 1.10.6**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- *(Nothing yet)* — See tag message for full context.

---

_Tag: `1.10.6rc2`_

🔖 **Tags**:
- Type: `#refactor`workflow
  
- **core**: 1.10.4b1
  
  Beta release for **Custy 1.10.4**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- This release just for testing the app for release

---

_Tag: `1.10.4b1`_

🔖 **Tags**:
- Type: `#refactor`
  
### 🐛 Bug Fixes
- **workflow**: 1.10.6rc3
  
  Release candidate for **Custy 1.10.6**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

### 🐛 Fixes
- Prevent unintended execution in CASE 3, 6, and 9 if staged files exist
- Ensures safety during critical merge operations inside `WorkflowManager`

### 🧠 UX Improvement
- Added interactive prompt (`y/n`) when no files are staged during validation
- Allows user to explicitly confirm whether to proceed or abort

These changes make the workflow execution more resilient and user-aware during tagging phases.

---

_Tag: `1.10.6rc3`_

🔖 **Tags**:
- Type: `#bugfix`
- Workflow: `#workflow`
- Stability: `#safety`
- Pre-release: `#rc`
  
- **workflow**: 1.10.6rc1
  
  Release candidate for **Custy 1.10.6**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

### 📚 Documentation
- 📘 update `project structure` documentation

---

_Tag: `1.10.6rc1`_

🔖 **Tags**:
- Type: `#bugfix`
  
- **workflow**: 1.10.6b1
  
  Beta release for **Custy 1.10.6**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

_Tag: `1.10.6b1`_

🔖 **Tags**:
- Type: `#bugfix`
  
- **workflow**: 1.10.5rc1
  
  Release candidate for **Custy 1.10.5**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

_Tag: `1.10.5rc1`_

🔖 **Tags**:
- Type: `#bugfix`
  
- **workflow**: 1.10.5b1
  
  Beta release for **Custy 1.10.5**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- reapplied clean branch functionality

---

_Tag: `1.10.5b1`_

🔖 **Tags**:
- Type: `#bugfix`
  
- **core**: 1.10.4rc1
  
  Release candidate for **Custy 1.10.4**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release.

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

_Tag: `1.10.4rc1`_

🔖 **Tags**:
- Type: `#bugfix`
  
- **workflow**: 1.10.2rc1
  
  Release candidate for **Custy 1.10.2**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- *(Nothing yet)* — See tag message for full context.

---

_Tag: `1.10.2rc1`_

🔖 **Tags**:
- Type: `#bugfix`
  
- **workflow**: 1.10.2b1
  
  Beta release for **Custy 1.10.2**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- 🐛 Fixed a minor internal bug to improve stability

---

_Tag: `1.10.2b1`_

🔖 **Tags**:
- Type: `#bugfix`
  

## 1.10.1 (2025-08-06)
### 🚀 Release
- **main**: 1.10.1
  
  Final release of **Custy 1.10.1**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: 1.10.1rc1, 1.10.1b2, 1.10.1b1.
All functionality has been fully validated and production-ready.

### 🧹 Maintenance & Structure
- Code formatted with `ruff`

### 🐛 Bug Fixes
- Minor internal logic bugs resolved for better stability

---

🎉 **Custy 1.10.1 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#bugfix`
- Maintenance: `#cleanup`
- Stability: `#stable`

Changelog: handled separately
  
- **main**: 1.10.0
  
  Final release of **Custy 1.10.0**, promoted from the latest release candidate.

Includes all feature and fixes from pre-releases: 1.10.0rc1, 1.10.0b3, 1.10.0b2, 1.10.0b1.
All functionality has been fully validated and production-ready.

### ✨ Features
- Full CASE 1–9 support in `WorkflowManager`:
  - Core flow: `develop → release → main → post-release`
  - Extended handling: `feature/*`, `ci/*`, `archive/*`
- Automatic workflow execution with `run_initial_workflow()` and `run_final_workflow()`
- Backup push handling, context setup, and cleanup automation

### 📚 Documentation
- Added `git_workflow_cases.md` for CASE logic
- Documented `WorkflowManager` classes and transition behavior
- Updated `README.md`, `TODO.md`, and added usage notes

### 📄 Templates
- Refactored and expanded example templates for commit and tag messages

### 🧪 Tests
- Introduced test coverage for `WorkflowManager` and CASE transitions

### 🐛 Fixes
- Fixed transition bugs and branching issues within `WorkflowManager`

### 🧹 Maintenance
- Linted and formatted the codebase using `ruff`
- Cleanup of legacy TODOs and refactoring for clarity

---

🎉 **Custy 1.10.0 is now stable and ready for production use.**

🔖 **Tags**:
- Type: `#release`, `#feature`, `#bugfix`
- Docs: `#docs`, `#template`
- Workflow: `#workflow`, `#automation`
- QA: `#tests`
- Maintenance: `#cleanup`
- Stability: `#stable`

Changelog: handled separately
  
### 🧠 Refactoring
- **release**: 1.10.1rc1
  
  Release candidate for **Custy 1.10.1**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- *(Nothing yet)* — See tag message for full context.

---

_Tag: `1.10.1rc1`_

🔖 **Tags**:
- Type: `#refactor`
  
### 🔧 Chores
- **release**: 1.10.1rc1
  
  Release candidate for **Custy 1.10.1**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- *(Nothing yet)* — See tag message for full context.

---

_Tag: `1.10.1rc1`_

🔖 **Tags**:
- Type: `#chore`
  
### 🐛 Bug Fixes
- **workflow**: 1.10.1b2
  
  Beta release for **Custy 1.10.1**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- 🐛 Fixed a minor internal bug to improve stability

---

_Tag: `1.10.1b2`_

🔖 **Tags**:
- Type: `#bugfix`
  
- **workflow**: 1.10.1b1
  
  Beta release for **Custy 1.10.1**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- Improved commit/tag message template generation logic

---

_Tag: `1.10.1b1`_

🔖 **Tags**:
- Type: `#fix`
  
### 📝 Documentation
- **changelog**: update changelog

## 1.10.0rc1 (2025-08-06)
### 📝 Documentation
- **todo**: 1.10.0rc1
  
  Release candidate for **Custy 1.10.0**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- Update `docs/TODO.md` to reflect recent changes and clean up outdated entries

---

_Tag: `1.10.0rc1`_

🔖 **Tags**:
- Type: `#docs`
  

## 1.10.0b3 (2025-08-06)
### 📝 Documentation
- **template**: 1.10.0b3
  
  Beta release for **Custy 1.10.0**, introducing mid-stage docsures and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- Reorganized and renamed `commit-msg.txt` and `tag-msg.txt` templates

---

_Tag: `1.10.0b3`_

🔖 **Tags**:
- Type: `#docs`
  

## 1.10.0b2 (2025-08-06)
### ✨ Features
- **workflow**: 1.10.0b2
  
  Beta release for **Custy 1.10.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

Expands test coverage, improves documentation, and refines the logic of the WorkflowManager.

### 📄 Templates
- Added more example templates for `commit-msg.txt` and `tag-msg.txt`

### 🧪 Tests
- Introduced automated tests for `WorkflowManager` functionality

### 🐛 Fixes
- Fixed logic issues in `WorkflowManager` related to CASE transitions

### 📚 Documentation
- Added `docs/git/git_workflow_cases.md` explaining CASE logic
- Documented `WorkflowManager` classes, functions, and transitions
- Updated `docs/TODO.md` to reflect recent changes

### 🧹 Maintenance
- Linted and formatted codebase using `ruff`

---

_Tag: `1.10.0b2`_

🔖 **Tags**:
- Type: `#feature`, `#bugfix`
- Docs: `#docs`, `#template`
- Tests: `#tests`
- Maintenance: `#cleanup`