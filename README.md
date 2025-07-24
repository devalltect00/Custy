# Custy

Commit and Tag Automation Script/Tool.

---

## 📦 Features

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

## 🚀 Usage

### Run the main app

```bash
make run-main
```

## 🧪 Dependencies

Install via:

```bash
pip install -r requirements.txt
```

Or via PEP 621
(setup in pyproject.toml)

```bash
pip install .
```

or want to install dev dependencies too
Use the --extra flag like this.

```bash
pip install .[dev]
```

This tells pip to install the optional group named `dev` inside `pyproject.toml`.

## 🛠️ Makefile Commands

| Command                                    | Description                                                    |
| ------------------------------------------ | -------------------------------------------------------------- |
| make run-main                              | Run the main application                                       |
| make run-risk-summary                      | Generate and export domain risk summary                        |
| make visualize-risk                        | Create Static risk chart (PNG) chart using Matplotlib          |
| make visualize-risk-html                   | Create interactive chart (HTML) using Plotly                   |
| make format-all                            | Format code using `ruff`                                       |
| make structure                             | print and validate project structure                           |
| generate_ignore_files:                     | Generate .gitignore and .dockerignore files                    |
| custom-commit-and-tag-major                | Commit using external file + bump **major** version, then push |
| custom-commit-and-tag-minor                | Commit using external file + bump **minor** version, then push |
| custom-commit-and-tag-patch                | Commit using external file + bump **tag** version, then push   |
| make custom-commit-and-push-changelog-only | Generate + push changelog only                                 |

## 📜 Changelog

See [CHANGELOG.md](./CHANGELOG.md) for a list of changes and version history

## 📄 License

MIT License © 2025
