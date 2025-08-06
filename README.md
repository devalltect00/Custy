# 🧠 Custy — Git Commit & Version Automation Tool

[![Build Status](https://gitlab.com/devalltects-group/custy/badges/main/pipeline.svg)](https://gitlab.com/devalltects-group/custy/-/pipelines)
[![Coverage](https://gitlab.com/devalltects-group/custy/badges/main/coverage.svg)](https://gitlab.com/devalltects-group/custy/-/graphs/main/charts)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-Proprietary-red.svg)
![Versioning](https://img.shields.io/badge/versioning-PEP%20440-blueviolet.svg)
![Commitizen](https://img.shields.io/badge/commitizen-friendly-brightgreen.svg)

**Custy** helps you automate Git commit + versioning workflows with ease.
It supports SemVer and PEP 440 versioning, changelog generation, commit/tag templating, dual remote push, and workflow validation.

---

## ✨ Features

-   ✅ Commit with message file or Commitizen
-   🔖 Auto bump and tag using:
    -   SemVer (`1.2.3`, `1.2.3-beta.1`)
    -   PEP 440 (`1!1.2.3`, `1.2.3rc1`, `1.2.3.post1+sha.abc`)
    -   Date and Git commit count
-   📁 Auto-update `__version__.py` and `.cz.toml`
-   📝 Generate and commit changelog (`CHANGELOG.md`)
-   🔁 Push to origin and backup (e.g. GitLab + GitHub)
-   💡 Smart workflow checks and enforcement
-   🧪 Dry-run mode, force options, and tag validation
-   🧼 Backup commit and tag message files
-   🧹 Cleanup old backup and temporary branches

---

## 🗂 Project Structure

Project layout follows best practices. See full structure in [`project_structure.md`](docs/project_structure.md).

---

## 🚀 Quick Start

### ▶️ Run from CLI

```bash
python app/__main__.py all templates/commit-msg.txt \
  --strategy pep440 \
  --bump patch \
  --force-changelog \
  --sync-backup
```

Or use `make`:

```bash
make run-main
```

---

## 🧪 Installation

### 📌 From requirements.txt

```bash
pip install -r requirements.txt
```

### 📦 From `pyproject.toml`

```bash
pip install .
```

### 🛠️ With dev dependencies

```bash
pip install .[dev]
```

Includes `commitizen`, `ruff`, etc.

## 🌐 From Git Repository (Recommended for Other Projects)

Install `custor` into another project directly from Github or Gitlab

### ✅ From Github

```bash
pip install git+https://github.com/<user-or-org>/<repo>.git<tag-or-branch>
```

### ✅ From Gitlab

```bash
pip install git+https://gitlab.com/<user-or-org>/<repo>.git<tag-or-branch>
```

📌 Replace:

-   `<user-or-org>` with GitHub or GitLab username or group
-   `<repo>` with the repository name (e.g., `Custy`)
-   `<tag-or-branch>` with a version tag like `v1.2.3`, or a branch like `main`

### 🔁 Examples

```bash
pip install git+https://github.com/devalltect00/Custy.git
```

install latest from `main`

```bash
pip install git+https://github.com/devalltect00/Custy.git@main
```

install pinned version

```bash
pip install git+https://github.com/devalltect00/Custy.git@1.2.3
```

✅ This method is ideal when using `Custy` as a shared CLI tool across multiple projects.

---

## 🛠️ Makefile Commands

| Command                      | Description                                 |
| ---------------------------- | ------------------------------------------- |
| `make run-main`              | Run main app entrypoint                     |
| `make format-all`            | Format code using `ruff`                    |
| `make structure`             | Print and validate project structure        |
| `make generate_ignore_files` | Generate .gitignore and .dockerignore files |

---

## 🧰 Useful Docs

-   📘 [How TO Use Custy](docs\HOW_TO_USE.md)
-   📖 [CLI Commands Reference](docs/cli_commands_custy.md)
-   🧠 [Git Branch Strategy](docs/git/branch_workflow.md)
-   📄 [Versioning Guide](docs/versioning/versioning.md)
-   🔀 [PEP 440 vs SemVer Comparison](docs/versioning/git_branching_strategy_pep440.md)
-   🌐 [Dual Remote Strategy](docs/versioning/git_dual_remote_strategy.md)

---

## 📦 CLI Usage Examples

### Commit with auto tag bump (SemVer)

```bash
custy commit-tag-bump commit-msg.txt --strategy semver --bump patch
```

### Final Release with changelog (PEP 440)

```bash
custy all commit-msg.txt --strategy pep440 --bump patch --force-changelog
```

### Push only

```bash
custy push
```

---

## 🧼 Maintenance Commands

| Command                    | Description                          |
| -------------------------- | ------------------------------------ |
| `custy backup`             | Backup current commit message        |
| `custy cleaned-backups`    | Cleanup old backup messages          |
| `custy clean-branches`     | Delete temporary Git branches        |
| `custy changelog`          | Generate changelog manually          |
| `custy validate`           | Validate commit and repository state |
| `custy workflow --enforce` | Enforce Git workflow policy          |

---

## 📜 Changelog

See [`CHANGELOG.md`](CHANGELOG.md)

---

## 📄 License

Copyright © 2025
This software is **not open source**.
You may not copy, distribute, or modify any part of this project without prior written permission from the author.

📧 Contact for permission: `rizkypffdev37@gmail.com`

---

_Handcrafted with ❤️ by Devalltect / Rizky Fernandes_
