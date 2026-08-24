<!-- docs/docs_v1/versioning/git_branching_strategy_pep440.md -->

# 🧾 Git Branching Strategy and Versioning with PEP 440

This document summarizes the best practices for managing Git branches in a Python project using PEP 440-compliant versioning, along with commit type mappings and CI strategies.

---

## 🔢 PEP 440 Version Format

```
[Epoch!]MAJOR.MINOR.PATCH[Pre-release][Post-release][Development][+Local]
```

### Examples:

-   `1.2.3` → stable release
-   `1.2.3a1` → alpha pre-release
-   `1.2.3rc2` → release candidate
-   `1.2.3.post1` → post-release patch
-   `1.2.3.dev4` → development snapshot
-   `1.2.3+sha.abc123` → local version with build metadata

---

## 🔧 Commit Type → Version Bump

| Type       | Affects    | Bump     |
| ---------- | ---------- | -------- |
| `feat`     | MINOR      | +1 MINOR |
| `fix`      | PATCH      | +1 PATCH |
| `perf`     | PATCH      | +1 PATCH |
| `docs`     | PATCH/None | Optional |
| `style`    | None       | No bump  |
| `refactor` | PATCH      | Optional |
| `test`     | None       | No bump  |
| `chore`    | None       | No bump  |
| `ci`       | None       | No bump  |
| `build`    | None       | No bump  |
| `other`    | None       | No bump  |

---

## 🌿 Permanent vs Temporary Branches

| Branch         | Purpose                    | Keep?  |
| -------------- | -------------------------- | ------ |
| `main`         | Stable production releases | ✅ Yes |
| `develop`      | Next version dev/testing   | ✅ Yes |
| `release/x.y`  | Release prep (rc tags)     | ❌ No  |
| `hotfix/x.y.z` | Patch fixes to main        | ❌ No  |
| `feature/*`    | New feature dev            | ❌ No  |
| `ci/*`         | GitLab CI testing          | ❌ No  |

---

## 🔁 Git Workflow Summary

### 1. Develop

-   Daily integration branch
-   Use versions like: `2.1.0a1`, `2.1.0b1`, `2.1.0.dev1`

### 2. Release

-   Create `release/2.1` from `develop`
-   Tag `2.1.0rc1`, `2.1.0rc2`
-   Final merge → `main`, tag: `2.1.0`

### 3. Hotfix

-   Branch from `main`: `hotfix/2.1.0-post1`
-   Tag `2.1.0.post1`, merge to `main` and `develop`

### 4. CI Testing

-   Create `ci/test-*` for GitLab pipeline test
-   Delete after use

---

## 🗂️ Diagram

![Git Branch Lifecycle](git_branch_lifecycle.png)

---

## 📚 References

-   [PEP 440 – Version Identification](https://www.python.org/dev/peps/pep-0440/)
-   [GitLab CI/CD Pipelines](https://docs.gitlab.com/ee/ci/)
-   [Semantic Versioning](https://semver.org/)
-   [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)

---
