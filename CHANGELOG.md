# 🧾 CHANGELOG




## Unreleased (2025-07-29)
### 📝 Documentation
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
  
- **commit_msg**: support 'release' as valid Conventional Commit type
  
  - Added 'release' to allowed commit types in the validator

Changelog: handled separately
  
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
  
- **versioning**: Improve pre-release and full versioning support with PEP 440
  
  - Fix pre-release version format to comply with pep440 for python
- Add support for full format: [Epoch!]MAJOR.MINOR.PATCH[Pre-release][Post-release][Development][+Local]
- Additionally support Post-release, development, local identifiers, and epoch segment

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