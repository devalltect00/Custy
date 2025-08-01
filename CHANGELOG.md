# 🧾 CHANGELOG




## Unreleased (2025-08-02)
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
- Fix the file name from `pep404_strategy.py` â†’ `pep440_strategy.py`
- Rename class from `PEP404Strategy` â†’ `PEP440Strategy`
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
- Bug fixed case example changes from 1.5.0.post1 â†’ 1.5.0.post2
- Bug fixed on `Makefile`
- modified documentation `docs/TODO.md`

Tag: 1.6.0.post2
Changelog: handled separately
  
### 📝 Documentation
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
### Release
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

ðŸ›  Final tweaks after rc2:
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
  
### 📦 Others
- **general**: merge release 1.7.1 into main

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
- *(Nothing yet)* â€” See tag message for full context.

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
- *(Nothing yet)* â€” See tag message for full context.

Tag: 1.5.0b1
  
- **core**: implement advanced versioning rules and CLI behavior controls
  
  This commit introduces a series of improvements across versioning, tagging, changelog generation, and backup handling in Custy CLI.

- Prevents major.minor.patch bump when incrementing within same pre-release tier (e.g. rc1 â†’ rc2)
- Generates changelog only on final releases (e.g. v1.2.3), skipping pre-releases
- Enforces bump/tag only for specific types [feat, fix, perf, docs, refactor]; others require CLI override
- Detects project type (Python or JavaScript) to apply correct versioning scheme (PEP 440 or SemVer)
- Tag messages now opened in external file like commit-msg.txt; supports default message via flag
- For release tags, auto-generates commit/tag message template from all prereleases (pre, dev, etc.)
- Prevents bump from rc â†’ final from incrementing patch (v1.2.3rc1 â†’ v1.2.3, not v1.2.4)
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
- *(Nothing yet)* â€” See tag message for full context.

Tag: 1.5.0b3
  
- **release**: 1.5.0b2
  
  Beta release for **Custy 1.5.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- *(Nothing yet)* â€” See tag message for full context.

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
- *(Nothing yet)* â€” See tag message for full context.

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
- Version bump protection within pre-release tier (e.g., rc1 â†’ rc2)
- Restriction of changelog to final releases only
- Commit type validation for bump/tag operations
- Project type detection (PEP 440 or SemVer) for versioning
- External tag message support (`tag-msg.txt`)
- Auto-generation of release commit/tag message templates
- RC â†’ final bump without patch increment
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
### Release
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

ðŸ›  Final tweaks after rc2:
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
### Release
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

ðŸ›  Final tweaks after rc2:
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
- Fix the file name from `pep404_strategy.py` â†’ `pep440_strategy.py`
- Rename class from `PEP404Strategy` â†’ `PEP440Strategy`
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
- Bug fixed case example changes from 1.5.0.post1 â†’ 1.5.0.post2
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
- *(Nothing yet)* â€” See tag message for full context.

Tag: 1.5.0rc1
  

## 1.5.0b3 (2025-07-31)
### 🐛 Bug Fixes
- **release**: 1.5.0b3
  
  Beta release for **Custy 1.5.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- *(Nothing yet)* â€” See tag message for full context.

Tag: 1.5.0b3
  

## 1.5.0b2 (2025-07-30)
### 🐛 Bug Fixes
- **release**: 1.5.0b2
  
  Beta release for **Custy 1.5.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- *(Nothing yet)* â€” See tag message for full context.

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
- *(Nothing yet)* â€” See tag message for full context.

Tag: 1.5.0b1
  
### 📝 Documentation
- **release**: 1.5.0rc1
  
  Release candidate for **Custy 1.5.0**, consolidating all pre-release changes and preparing for stable release.
Feature-complete and undergoing final validation before stable release.

This release candidate consolidates finalized features and bug fixes before the stable release:
- *(Nothing yet)* â€” See tag message for full context.

Tag: 1.5.0rc1
  
- **changelog**: update changelog
### 🐛 Bug Fixes
- **release**: 1.5.0b3
  
  Beta release for **Custy 1.5.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- *(Nothing yet)* â€” See tag message for full context.

Tag: 1.5.0b3
  
- **release**: 1.5.0b2
  
  Beta release for **Custy 1.5.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- *(Nothing yet)* â€” See tag message for full context.

Tag: 1.5.0b2
  
### 🔧 Chores
- **release**: 1.5.0b1
  
  Beta release for **Custy 1.5.0**, introducing mid-stage features and workflow improvements.
Partially validated features and improvements. Some issue still remain.

This beta includes several bug fixes and enhancements:
- *(Nothing yet)* â€” See tag message for full context.

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
- Version bump protection within pre-release tier (e.g., rc1 â†’ rc2)
- Restriction of changelog to final releases only
- Commit type validation for bump/tag operations
- Project type detection (PEP 440 or SemVer) for versioning
- External tag message support (`tag-msg.txt`)
- Auto-generation of release commit/tag message templates
- RC â†’ final bump without patch increment
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
- Version bump protection within pre-release tier (e.g., rc1 â†’ rc2)
- Restriction of changelog to final releases only
- Commit type validation for bump/tag operations
- Project type detection (PEP 440 or SemVer) for versioning
- External tag message support (`tag-msg.txt`)
- Auto-generation of release commit/tag message templates
- RC â†’ final bump without patch increment
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

- Prevents major.minor.patch bump when incrementing within same pre-release tier (e.g. rc1 â†’ rc2)
- Generates changelog only on final releases (e.g. v1.2.3), skipping pre-releases
- Enforces bump/tag only for specific types [feat, fix, perf, docs, refactor]; others require CLI override
- Detects project type (Python or JavaScript) to apply correct versioning scheme (PEP 440 or SemVer)
- Tag messages now opened in external file like commit-msg.txt; supports default message via flag
- For release tags, auto-generates commit/tag message template from all prereleases (pre, dev, etc.)
- Prevents bump from rc â†’ final from incrementing patch (v1.2.3rc1 â†’ v1.2.3, not v1.2.4)
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