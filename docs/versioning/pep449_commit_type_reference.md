# 🧾 Versioning and Commit Types Reference (Python + PEP 440)

This document explains how commit types (e.g. feat, fix, etc.) relate to Python versioning based on PEP 440 format:

## 📌 PEP 440 Version Format

```
[Epoch!]Release[Pre-release][Post-release][Development][+Local]
```

### Components:

| Segment        | Description                                             | Example               |
| -------------- | ------------------------------------------------------- | --------------------- |
| `Epoch!`       | Forces version precedence (rarely used)                 | `2!1.0.0`             |
| `Release`      | Main version - MAJOR.MINOR[.PATCH[.SUB]]                | `1.2.3`               |
| `Pre-release`  | Preview version before final (`a`, `b`, `rc`)           | `1.2.3a1`, `1.2.3rc2` |
| `Post-release` | Fixes after stable release                              | `1.2.3.post1`         |
| `Development`  | Snapshot builds leading up to pre/final release         | `1.2.3.dev4`          |
| `+Local`       | Metadata for traceability (commit hash, platform, etc.) | `1.2.3+sha.abc123`    |

---

## 🔧 Commit Types and Version Bumping

| Type       | Affects  | Version bump | Notes                             |
| ---------- | -------- | ------------ | --------------------------------- |
| `feat`     | MINOR    | +1 MINOR     | Adds a new feature                |
| `fix`      | PATCH    | +1 PATCH     | Bug fix                           |
| `perf`     | PATCH    | +1 PATCH     | Performance fix (non-breaking)    |
| `docs`     | Optional | PATCH/None   | Docs only (version bump optional) |
| `style`    | None     | None         | Code formatting                   |
| `refactor` | PATCH    | Optional     | Code change w/o feature or fix    |
| `test`     | None     | None         | Adds or updates tests             |
| `chore`    | None     | None         | Tooling or CI setup               |
| `ci`       | None     | None         | CI/CD configuration               |
| `build`    | None     | None         | Build scripts and tools           |
| `other`    | None     | None         | Fallback                          |

---

## 🧪 Full Example Versions

| Version                          | Meaning                                        |
| -------------------------------- | ---------------------------------------------- |
| `1.2.3`                          | Final stable release                           |
| `1.2.3a1`                        | Alpha 1                                        |
| `1.2.3rc1`                       | Release candidate                              |
| `1.2.3.dev2`                     | Development snapshot                           |
| `1.2.3.post1`                    | Fix after release                              |
| `1.2.3rc1.post2.dev4+sha.abc123` | Dev build after RC1 post2, with build metadata |

---

## ✅ Summary

-   Commit types only affect **MAJOR.MINOR.PATCH**
-   `Pre-release`, `Post-release`, `dev`, `+local`, and `Epoch!` must be managed manually or with tools
-   Follow PEP 440 for full compatibility with Python tools (pip, setuptools, poetry, etc.)
