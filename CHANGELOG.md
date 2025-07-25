# 🧾 CHANGELOG




## Unreleased (2025-07-25)
### ✨ Features
- **versioning**: Improve pre-release and full versioning support with PEP 440
  
  - Fix pre-release version format to comply with pep440 for python
- Add support for full format: [Epoch!]MAJOR.MINOR.PATCH[Pre-release][Post-release][Development][+Local]
- Additionally support Post-release, development, local identifiers, and epoch segment

Changelog: handled separately
  
### 📝 Documentation
- **changelog**: update changelog

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