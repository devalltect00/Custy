# Custy

**Custy** — Automate your Git commits, bumps, tags, and changelogs.

---

## 📦 Features

Custy simplifies and automates your Git workflow with feature like:

-   Validate git repository, files, etc
-   Add stage if needed
-   Open editor for commit message
-   Check commit message
-   Determine next version (tag)
-   Update **version**.py with that tag
-   Update cz.toml version with that tag
-   Stage and commit all changes (including version bump)
-   Tag that commit
-   Push commit and tag
-   generate CHANGELOG.md
-   Commit and push CHANGELOG.md
-   backup commit message. Not the commit message for changelog.md changes

---

## 📁 Project Structure

You can see the project structure on [project_structure.md](./docs/project_structure.md)

## 🚀 Getting Started

### ▶️ Run the main app

```bash
make run-main
```

## 🧪 Dependencies

### 📌 Install via requirements.txt:

```bash
pip install -r requirements.txt
```

### 📦 Or install via PEP 621 (`pyproject.toml`):

(setup in pyproject.toml)

```bash
pip install .
```

### 🛠️ Or want to install with Development Dependencies too:

Use the --extra flag like this.

```bash
pip install .[dev]
```

This tells pip to install the optional group named `dev` inside `pyproject.toml`.

## 🛠️ Makefile Commands

| Command                | Description                                 |
| ---------------------- | ------------------------------------------- |
| make run-main          | Run the main application                    |
| make format-all        | Format code using `ruff`                    |
| make structure         | print and validate project structure        |
| generate_ignore_files: | Generate .gitignore and .dockerignore files |

For CLI usage examples and arguments, see [cli_commands_custy.md](./docs/cli_commands_custy.md)

## 📜 Changelog

See [CHANGELOG.md](./CHANGELOG.md) for a list of changes and version history

## 📄 License

Copyright © 2025

This software is not open source. You may not copy, distribute, or modify any part of this project without prior written permission from the author.

To request permission, contact: rizkypffdev37@gmail.com
