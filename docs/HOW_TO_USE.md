<!-- docs/HOW_TO_USE.md -->

# 📘 HOW TO USE `Custy`

`Custy` is a CLI tool to automate Git commit, tagging, versioning, changelog generation, and enforcing branching workflows. It supports SemVer, PEP 440, and other strategies.

## 🛠️ Installation

Ensure the required dependencies are installed (Python, Git, etc). To use:

```bash
python app/__main__.py <command> [options]
```

---

## 🔀 Available Commands

### 1. `commit-tag-bump`

Automates commit + tag creation + version bumping.

```bash
python app/__main__.py commit-tag-bump [message_file] [options]
```

**Options:**

-   `--strategy`: `semver` | `pep440` | `date` | `gitcount` | `commitizen`
-   `--bump`: `major` | `minor` | `patch` | `auto`
-   `--tag`: Manual tag (e.g., `v1.2.3`)
-   `--tag-msg`: Custom tag message
-   `--pre-release`: Pre-label (e.g., `alpha`, `beta`, `rc`)
-   `--post-release`: Mark as post-release
-   `--dev-release`: Mark as development version
-   `--meta`: Metadata (e.g., `sha.abc123`)
-   `--epoch`: Epoch number (PEP 440)
-   `--force-tag`: Bypass commit-type check
-   `--version-file`: Defaults to `app/__version__.py`
-   `--dry-run`: Simulate without applying
-   `--force-commit`: Allow commit even with no staged changes
-   `--sync-backup`: Also push to `backup` remote (e.g., GitHub)

---

### 2. `all`

Run the **full workflow**:

-   Commit + tag
-   Push to origin (and backup)
-   Generate & commit `CHANGELOG.md`
-   Backup commit message

```bash
python app/__main__.py all [message_file] [options]
```

**Includes all `commit-tag-bump` options plus:**

-   `--stage-mode`: `all` | `update`
-   `--skip-checks`: Skip workflow validation
-   `--force-changelog`: Allow changelog even for prereleases
-   `--no-debug`: Silence debug info

---

### 3. `push`

Push latest commit + tag to `origin` and optionally to `backup`.

```bash
python app/__main__.py push
```

---

### 4. `changelog`

Generate a structured `CHANGELOG.md` from Git log between last two tags.

```bash
python app/__main__.py changelog [options]
```

**Options:**

-   `--force-changelog`: Allow changelog even for pre-releases

---

### 5. `validate`

Check commit message and Git state before committing.

```bash
python app/__main__.py validate [message_file]
```

---

### 6. `backup`

Backup current commit message file into `backups/commit/`.

```bash
python app/__main__.py backup
```

---

### 7. `cleaned-backups`

Prune older backup files.

```bash
python app/__main__.py cleaned-backups [--type] [--keep]
```

**Options:**

-   `--type`: `commit` | `tag` | `all` (default)
-   `--keep`: Number of recent backups to keep (default: `10`)

---

### 8. `clean-branches`

Delete old or merged branches.

```bash
python app/__main__.py clean-branches --prefix <prefix> [--merged-only] [--older-than <N>d]
```

**Examples:**

```bash
python app/__main__.py clean-branches --prefix feature/ --merged-only
python app/__main__.py clean-branches --prefix release/ --older-than 30d
```

---

### 9. `workflow`

Validate or enforce Git branch→tag strategy.

```bash
python app/__main__.py workflow [--enforce] [--check_transition] [options]
```

**Options:**

-   `--enforce`: Enforce naming rules and transition logic
-   `--check_transition`: Check if a version bump between branches is valid
-   `--from-branch` / `--from-tag` / `--to-branch` / `--to-tag`: Custom transition override

---

## 🔁 Tagging Strategies

| Strategy     | Description                                                             |
| ------------ | ----------------------------------------------------------------------- |
| `semver`     | Uses `major.minor.patch` + optional pre-release (e.g., `v1.2.3-beta.1`) |
| `pep440`     | Python standard (e.g., `1.2.3`, `1.2.3rc1`, `1!1.2.3+sha.abc`)          |
| `date`       | Uses current date for tag (e.g., `20250804`)                            |
| `gitcount`   | Tag is generated based on commit count (e.g., `v0.1.53`)                |
| `commitizen` | Uses cz config to auto infer bump and generate tag                      |

---

## 💡 Usage Examples

### Commit with SemVer bump:

```bash
python app/__main__.py commit-tag-bump commit-msg.txt --strategy semver --bump patch
```

### Final Release with PEP 440 + changelog + push:

```bash
python app/__main__.py all commit-msg.txt \
  --strategy pep440 \
  --bump patch \
  --version-file app/__version__.py \
  --force-changelog \
  --sync-backup
```

### Push only:

```bash
python app/__main__.py push
```

### Changelog only:

```bash
python app/__main__.py changelog --force-changelog
```

### Validate message:

```bash
python app/__main__.py validate commit-msg.txt
```

### Cleanup old feature branches older than 30 days:

```bash
python app/__main__.py clean-branches --prefix feature/ --older-than 30d
```

---

## 📁 Default Files and Locations

| File / Dir                 | Purpose                                      |
| -------------------------- | -------------------------------------------- |
| `app/__version__.py`       | Holds version string `__version__ = "x.y.z"` |
| `templates/commit-msg.txt` | Commit message template                      |
| `templates/tag-msg.txt`    | Tag message template                         |
| `backups/commit/`          | Backup of commit messages                    |
| `backups/tag/`             | Backup of tag messages                       |
