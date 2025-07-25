# 🛠️ CLI Reference: Custy

`custy` is a Git + Commitizen-inspired CLI tool that automates your commit, versioning, tagging, and changelog flow — with full customizability.

---

## 📦 Available Commands

| Command           | Description                                                              |
| ----------------- | ------------------------------------------------------------------------ |
| `commit-tag-bump` | Commit changes, bump version, create Git tag, and update version files.  |
| `changelog`       | Generate a `CHANGELOG.md` file from commit history.                      |
| `push`            | Push latest commit and Git tag to the origin remote.                     |
| `validate`        | Validate Git repo status, commit message format, and origin config.      |
| `backup`          | Backup current commit message to a timestamped file.                     |
| `all`             | Run full automation: validate → stage → commit → tag → push → changelog. |

---

## ⚙️ Common Arguments

| Argument         | Description                                                              |
| ---------------- | ------------------------------------------------------------------------ |
| `message_file`   | Path to commit message file (default: `tools/git_commit/commit-msg.txt`) |
| `--version-file` | Path to version file to bump (default: `app/__version__.py`)             |
| `--dry-run`      | Run all commands in dry-run mode (no actual changes made)                |
| `--tag`          | Manually specify a Git tag (e.g. `v1.2.3`)                               |
| `--tag-msg`      | Tag message (default: same as tag)                                       |
| `--strategy`     | Tag strategy: `semver`, `date`, `gitcount`, `commitizen`                 |
| `--bump`         | What version level to bump: `patch`, `minor`, `major`, or `auto`         |
| `--pre-release`  | Pre-release label like `alpha`, `rc`, etc.                               |
| `--stage-mode`   | Auto-stage mode: `all` (default) or `update`                             |

---

## 🧪 Example Usages

```bash
custy commit-tag-bump --bump patch --strategy semver
custy changelog
custy validate
custy all --bump minor --strategy semver --pre-release beta
```

# 🧪 CLI Command Examples: `custor`

Below are tested example commands you can run using the `custor` CLI.

---

## 🔹 Full Workflow

```bash
custor all --bump major
custor all --bump patch
custor all --bump minor
custor all --bump minor --strategy semver
custor all --bump major --strategy semver --pre-release alpha
custor all --bump major --strategy semver --pre-release beta
custor all --bump major --strategy semver --pre-release rc
custor all --bump auto --strategy commitizen
```

## 🔹 Commit + Tag + Version Bump

```bash
custor commit-tag-bump --bump patch
custor commit-tag-bump --bump minor --strategy semver
custor commit-tag-bump --bump major --strategy semver --pre-release beta
custor commit-tag-bump --bump auto --strategy commitizen
```

## 🔹 Generate Changelog

```bash
custor changelog
```

## 🔹 Validate Project State

```bash
custor validate
```

## 🔹 Push Commits and Tags

```bash
custor push
```

## 🔹 Backup Commit Message

```bash
custor backup
```
