# 📦 Versioning and Conventional Commits

This document describes how versioning works in this project, based on **Semantic Versioning (SemVer)** and **Conventional Commits**.

---

## ✅ Version Format

We follow the **SemVer 2.0.0** format:

```
<major>.<minor>.<patch>[-<pre-release>][+<build>]
```

### Examples:
- `1.0.0`
- `1.2.3-alpha`
- `2.1.0-rc.1+build.2025`

---

## 🚀 Conventional Commit Types

| Type      | Description                           | Triggers Version Bump? |
|-----------|---------------------------------------|--------------------------|
| `feat`    | New feature                           | ✅ Minor (`+0.1.0`)       |
| `fix`     | Bug fix                               | ✅ Patch (`+0.0.1`)       |
| `perf`    | Performance improvements              | ✅ Patch (`+0.0.1`)       |
| `docs`    | Documentation changes                 | ❌ None (optional patch) |
| `style`   | Code style (formatting, lint, etc.)   | ❌ None                  |
| `refactor`| Code refactor (no behavior change)    | ❌ None (optional patch) |
| `test`    | Add or update tests                   | ❌ None                  |
| `chore`   | Maintenance, build scripts, etc.      | ❌ None (optional patch) |
| `ci`      | CI configuration changes              | ❌ None                  |
| `build`   | Build system changes or deps update   | ❌ None (optional patch) |
| `other`   | Unclassified change                   | ❌ Manual review         |

---

## 💥 Breaking Changes

A **MAJOR** version bump (`X.0.0`) happens when:

- You introduce a breaking API change
- You explicitly mark the commit using:
  - `type!`, e.g. `feat!`
  - or `BREAKING CHANGE:` in the commit body

### Example:
```text
feat!: remove deprecated auth system

BREAKING CHANGE: The legacy authentication flow was removed.
```

---

## 🔁 Pre-release Versions

Use pre-release when you want to release **unstable or test versions**:

### Valid format:
```
<major>.<minor>.<patch>-<identifier>[.<number>]
```

### Common Identifiers:

| Identifier | Purpose                                 | Example Version      |
|------------|------------------------------------------|----------------------|
| `alpha`    | Early prototype, not feature complete    | `1.2.0-alpha`        |
| `beta`     | Feature complete but testing in progress | `1.2.0-beta.1`       |
| `rc`       | Release candidate                        | `1.2.0-rc.1`         |
| `dev`      | Developer/internal preview               | `1.2.0-dev.1`        |
| Custom     | Any identifier (e.g. `next`, `preview`)  | `1.2.0-next.3`       |

---

## 🔢 Version Bump Matrix

| Commit Type       | Breaking? | Resulting Version (from `1.0.0`) |
|-------------------|-----------|----------------------------------|
| `feat`            | No        | `1.1.0`                          |
| `feat!`           | Yes       | `2.0.0`                          |
| `fix`             | No        | `1.0.1`                          |
| `fix!`            | Yes       | `2.0.0`                          |
| `perf`            | No        | `1.0.1`                          |
| `docs`, `style`, `test`, `ci`, `chore`, `build`, `refactor`, `other` | No | `1.0.0` (unchanged) |

---

## 🧪 Sample Workflow

```text
1. Current version: 1.0.0
2. Commit: feat: add user login → bump to 1.1.0
3. Commit: fix: resolve login bug → bump to 1.1.1
4. Commit: feat!: remove legacy system → bump to 2.0.0
5. Pre-release: rc.1 of v2.0.0 → version 2.0.0-rc.1
```

---

## 📁 Notes

- Pre-release tags are sorted lexically:
  - `alpha` < `beta` < `rc` < (no suffix)
- Final version (`1.3.0`) is considered **more stable** than any pre-release (`1.3.0-rc.2`)

---

## 📚 References

- [Semantic Versioning 2.0.0](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)