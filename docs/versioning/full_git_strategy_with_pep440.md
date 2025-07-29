# 🧾 Complete Git Workflow Strategy with PEP 440, Branching, Commit Types, and Dual Remote Integration

This document combines all best practices discussed in the session. It serves as a comprehensive reference for Python-based projects using Git, following [PEP 440](https://www.python.org/dev/peps/pep-0440/) versioning, GitLab-GitHub dual-remote strategy, branching conventions, and conventional commit types.

---

## 🔢 PEP 440 Version Format

Python packaging follows this format:

```
[Epoch!]MAJOR.MINOR.PATCH[Pre-release][Post-release][Development][+Local]
```

### Examples:

| Format Component | Example          | Meaning                           |
| ---------------- | ---------------- | --------------------------------- |
| Release          | `1.2.3`          | Stable release                    |
| Pre-release      | `1.2.3a1`, `rc2` | Alpha/Beta/Release Candidate      |
| Post-release     | `1.2.3.post1`    | Fixes after release               |
| Development      | `1.2.3.dev2`     | Snapshot before a release         |
| Local Metadata   | `+sha.abc123`    | Commit or build-specific metadata |
| Epoch            | `2!1.0.0`        | Overrides older release order     |

---

## 🔧 Commit Type → Version Bump Mapping

Following [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/), commit types affect version numbers:

| Type       | Affects    | Version Bump |
| ---------- | ---------- | ------------ |
| `feat`     | MINOR      | +1 MINOR     |
| `fix`      | PATCH      | +1 PATCH     |
| `perf`     | PATCH      | +1 PATCH     |
| `docs`     | PATCH/None | Optional     |
| `style`    | None       | No bump      |
| `refactor` | PATCH      | Optional     |
| `test`     | None       | No bump      |
| `chore`    | None       | No bump      |
| `ci`       | None       | No bump      |
| `build`    | None       | No bump      |
| `other`    | None       | No bump      |

---

## 🌿 Git Branching Strategy

| Branch         | Purpose                                   | Keep Permanent? | Tag Version Examples      |
| -------------- | ----------------------------------------- | --------------- | ------------------------- |
| `main`         | Production/stable releases                | ✅ Yes          | `1.2.0`, `1.2.1`, `2.0.0` |
| `develop`      | Development and pre-releases              | ✅ Yes          | `1.3.0a1`, `1.3.0.dev2`   |
| `release/x.y`  | Prepare for release and RCs               | ❌ No           | `1.3.0rc1`, `1.3.0`       |
| `hotfix/x.y.z` | Patch urgent production issues            | ❌ No           | `1.3.0.post1`             |
| `feature/*`    | Isolated feature development              | ❌ No           | Not tagged directly       |
| `ci/*`         | Pipeline and CI/CD job testing            | ❌ No           | Not tagged                |
| `sandbox/*`    | Debug, experimental or throwaway branches | ❌ No           | Not tagged                |

---

## 🔁 Workflow Lifecycle Summary

1. Work on `develop` using `dev`, `a`, or `b` versions
2. Create `release/x.y` to prep release, tag `rc` versions
3. Merge `release/x.y` to `main` and tag stable release (e.g., `v1.3.0`)
4. Create `hotfix/x.y.z` if production bug is found after release
5. Test pipelines on `ci/test-*` branch
6. All other branches (release, hotfix, feature, ci) are deleted after merge

---

## 🌐 Dual Remote Strategy

| Remote   | Role                 | Keep in Sync?    |
| -------- | -------------------- | ---------------- |
| `origin` | GitLab (main repo)   | ✅ Always        |
| `backup` | GitHub (mirror only) | ✅ Critical only |

### Branch Push Rules:

| Branch      | Push to `origin`? | Push to `backup`? | Why                            |
| ----------- | ----------------- | ----------------- | ------------------------------ |
| `main`      | ✅                | ✅                | Production stable releases     |
| `develop`   | ✅                | ✅                | Ongoing dev                    |
| `release/*` | ✅                | 🔄 Optional       | RC builds (optional to mirror) |
| `hotfix/*`  | ✅                | ✅                | Critical production patches    |
| `feature/*` | 🔄 Optional       | ❌                | Internal dev only              |
| `ci/*`      | ✅                | ❌                | GitLab-only CI/CD jobs         |
| `sandbox/*` | 🔄 Optional       | ❌                | Temporary/debugging            |

---

## 🗂️ Tagging Strategy

| Branch         | Tag Style        | Example                 |
| -------------- | ---------------- | ----------------------- |
| `develop`      | Dev, Alpha, Beta | `2.1.0.dev3`, `2.1.0a1` |
| `release/x.y`  | RC               | `2.1.0rc1`              |
| `main`         | Stable           | `2.1.0`, `2.1.1`        |
| `hotfix/x.y.z` | Post-release     | `2.1.0.post1`           |

---

## 🧠 Best Practices Summary

-   Keep `main` and `develop` permanently
-   Always tag on `main` for final release
-   Tag on `release/*` only for RC (`rc1`, `rc2`)
-   Never tag on `feature/*`, `ci/*`, or `sandbox/*`
-   Push everything to GitLab; push only key branches to GitHub
-   Clean up merged branches to avoid clutter

---

## 🗂️ Git Branch Lifecycle Diagram

![Git Branch Lifecycle](git_branch_lifecycle.png)

---

## 📚 References

-   [PEP 440 – Version Identification](https://www.python.org/dev/peps/pep-0440/)
-   [GitLab CI/CD Docs](https://docs.gitlab.com/ee/ci/)
-   [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
-   [Semantic Versioning](https://semver.org/)
-   [Git Basics](https://git-scm.com/book/en/v2)

---
