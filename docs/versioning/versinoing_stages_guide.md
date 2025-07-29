# 📦 Versioning Guide: Dev, Alpha, Beta, RC, and Stable Releases

This document explains the meaning and proper usage of version suffixes like **alpha**, **beta**, **rc**, and **dev**, as well as the structure of **MAJOR.MINOR.PATCH** versions commonly used in software versioning.

---

## 🔢 Semantic Versioning: `MAJOR.MINOR.PATCH`

This is the base versioning structure defined by [Semantic Versioning (SemVer)](https://semver.org/) and also supported in [PEP 440](https://peps.python.org/pep-0440/) (used in Python).

```
MAJOR.MINOR.PATCH
```

### Explanation

| Part    | Description                                    |
| ------- | ---------------------------------------------- |
| `MAJOR` | Breaking/incompatible API changes              |
| `MINOR` | New backward-compatible functionality/features |
| `PATCH` | Backward-compatible bug fixes only             |

### Examples

-   `1.0.0`: First stable release
-   `1.1.0`: Added features
-   `1.1.1`: Bug fixes

---

## 🧪 Pre-release Versions

Pre-release versions are used to indicate that a version is **not yet final**. These include development snapshots, alpha previews, beta versions, and release candidates.

### 🔧 Dev (`dev`)

-   Internal or in-progress versions
-   May be unstable or incomplete
-   Python format: `1.2.3.dev1`

### 🧪 Alpha (`a` / `alpha`)

-   Early testing phase
-   Expect breaking changes and incomplete features
-   Python format: `1.2.3a1`, SemVer: `1.2.3-alpha.1`

### 🔬 Beta (`b` / `beta`)

-   Feature-complete but may contain bugs
-   Meant for wider testing
-   Python format: `1.2.3b1`, SemVer: `1.2.3-beta.1`

### 🚦 Release Candidate (`rc`)

-   Nearly final version
-   Final testing before stable release
-   Python format: `1.2.3rc1`, SemVer: `1.2.3-rc.1`

### ✅ Final / Stable

-   Production-ready
-   No pre-release tag
-   Example: `1.2.3`

---

## ⏳ Pre-release Stability Order

From lowest to highest:

```
dev < alpha < beta < rc < final (stable)
```

---

## 📊 Summary Table

| Label   | Stage             | Stability   | PEP 440 Example | SemVer Example  |
| ------- | ----------------- | ----------- | --------------- | --------------- |
| `dev`   | In development    | 🔴 Very Low | `1.2.3.dev1`    | N/A             |
| `alpha` | Initial testing   | 🔴 Low      | `1.2.3a1`       | `1.2.3-alpha.1` |
| `beta`  | Feature complete  | 🟠 Medium   | `1.2.3b1`       | `1.2.3-beta.1`  |
| `rc`    | Release candidate | 🟡 High     | `1.2.3rc1`      | `1.2.3-rc.1`    |
| `final` | Stable release    | 🟢 Stable   | `1.2.3`         | `1.2.3`         |

---

## 🆚 PEP 440 vs Semantic Versioning (SemVer)

| Feature            | PEP 440 (Python)       | SemVer (JavaScript/general) |
| ------------------ | ---------------------- | --------------------------- |
| Pre-release format | `1.2.3a1`, `b1`, `rc1` | `1.2.3-alpha.1`, `-beta.1`  |
| Dev versions       | `1.2.3.dev1`           | Not standardized            |
| Post-releases      | `1.2.3.post1`          | Not standardized            |
| Local identifiers  | `+local`               | `+build.metadata`           |

---

Let us know if you'd like an automated version bumping or changelog generator script that understands these versions.
