<!-- docs/docs_v2/ALL.md -->

Great move. Documenting this now will save you a lot of confusion later—especially since your system is already evolving into a **framework-level tool**, not just a script.

I’ll give you a **clean, organized docs structure + full markdown files** ready to drop into your `docs/` folder.

---

# 📁 Recommended Docs Structure

```bash
docs/
├── architecture/
│   ├── overview.md
│   ├── git_layer.md
│   ├── versioning_system.md
│   ├── changelog_pipeline.md
│   ├── tag_strategies.md
│
├── guides/
│   ├── developer_guide.md
│   ├── migration_guide.md
│
├── diagrams/
│   ├── architecture_diagram.md
│   ├── changelog_pipeline_diagram.md
│   ├── version_flow_diagram.md
```

---

# 📘 1. `docs/architecture/overview.md`

```md
# 🧠 System Architecture Overview

This project is designed as a **modular Git automation and versioning system** with clean separation of concerns.

The architecture follows a layered approach:

```

CLI
└── Workflow / Strategy Layer
└── Version Helpers (PEP440 / SemVer)
└── GitService (Domain Layer)
└── GitCommandExecutor (Infrastructure Layer)

```

---

## 🎯 Goals

- Decouple Git operations from business logic
- Support multiple versioning standards (PEP440, SemVer)
- Provide extensible strategy-based workflows
- Enable testability and maintainability

---

## 🧩 Core Components

### 1. Git Layer
Handles all Git operations through:
- `GitService`
- `GitCommandExecutor`

### 2. Versioning System
Handles version logic:
- `PEP440VersionHelper`
- `SemverVersionHelper`
- `VersionBridge` (conversion only)

### 3. Changelog System
Processes commit messages:
- Pipeline-based architecture
- Config-driven behavior

### 4. Tag Strategies
Determines how versions are generated:
- PEP440Strategy
- SemverStrategy
- CommitizenStrategy

---

## 🔑 Key Principles

- **Single Responsibility**
- **Separation of Concerns**
- **Strategy Pattern**
- **Pipeline Pattern**
- **Dependency Injection**

---

## 🚀 Result

- Clean architecture
- Easy to extend
- Supports multiple ecosystems
- Production-ready design
```

---

# 📘 2. `docs/architecture/git_layer.md`

```md
# 🔧 Git Layer Architecture

The Git layer is responsible for executing all Git operations in a clean and controlled way.

---

## 🧩 Structure

```

GitService
↓
GitCommandExecutor
↓
Runner (dry-run support)

````

---

## 🧠 Components

### GitService (Domain Layer)

Handles:
- Getting tags
- Getting commits
- Parsing commits
- Branch operations

Example:
```python
git.get_latest_tag()
git.get_commits_between(prev, current)
````

---

### GitCommandExecutor (Infra Layer)

Handles:

* Raw Git command execution
* No business logic

Example:

```bash
git log
git tag
git checkout
```

---

### Runner (Execution Layer)

From DryRunSupport:

* Executes subprocess
* Supports dry-run mode
* Handles logging

---

## 🎯 Why This Design?

Before:

* GitHelper mixed everything (bad)

Now:

* Clear separation:

  * Execution
  * Logic
  * Workflow

---

## ✅ Benefits

* Testable
* Replaceable
* Safe (dry-run support)
* Clean error handling

````

---

# 📘 3. `docs/architecture/versioning_system.md`

```md
# 🔢 Versioning System

This system supports **two versioning standards**:

- PEP 440 (Python)
- Semantic Versioning (SemVer)

---

## 🧩 Structure

````

VersionHelperBase
├── PEP440VersionHelper
└── SemverVersionHelper

VersionBridge (conversion layer)

```

---

## 🧠 Version Lifecycle

Unified lifecycle:

```

dev < alpha < beta < rc < release < post

````

---

## 🔧 Helpers

### PEP440VersionHelper

Supports:
- dev (.dev1)
- alpha (a1)
- beta (b1)
- rc (rc1)
- post (.post1)
- local (+meta)
- epoch (1!)

---

### SemverVersionHelper (Extended)

Supports:
- dev → -dev.1
- alpha → -alpha.1
- beta → -beta.1
- rc → -rc.1
- post → -post.1
- metadata → +meta

---

## 🔄 VersionBridge

Used ONLY at boundaries.

### Example:

```python
VersionBridge.pep440_to_semver("1.2.3rc1")
# → v1.2.3-rc.1
````

---

## ⚠️ Important Rule

Do NOT use VersionBridge inside:

* Version helpers
* GitService

Use it only for:

* Input normalization
* Output formatting
* Migration

---

## ✅ Benefits

* Unified version logic
* Cross-ecosystem support
* Extensible

````

---

# 📘 4. `docs/architecture/changelog_pipeline.md`

```md
# 🧾 Changelog Pipeline

The changelog system uses a **pipeline pattern** to process commit messages.

---

## 🧩 Flow

1. Fetch commits
2. Process through pipeline
3. Group results
4. Render template

---

## 🧠 Pipeline Stages

- SkipMergeStage
- CleanStage
- BreakingChangeStage
- ReleaseTransformStage
- NormalTransformStage

---

## 🧱 Example Flow

````

Raw Commit
↓
Parse
↓
Clean
↓
Detect Breaking
↓
Transform
↓
Structured Output

```

---

## 🎯 Why Pipeline?

- Modular
- Extensible
- Easy to debug
- Clean transformation flow

---

## ✅ Benefits

- Easy to add new stages
- Clear data flow
- Reusable components
```

---

# 📘 5. `docs/architecture/tag_strategies.md`

```md
# 🏷️ Tag Strategies

Tag strategies define how the next version is generated.

---

## 🧩 Available Strategies

- PEP440Strategy
- SemverStrategy
- CommitizenStrategy
- DateStrategy
- GitCountStrategy

---

## 🧠 Pattern Used

Strategy Pattern

```

Strategy → VersionHelper → GitService

````

---

## 🔧 Example

```python
strategy = SemverStrategy(bump="minor")
next_tag = strategy.get_next_tag()
````

---

## 🧠 CommitizenStrategy

* Uses `cz bump --dry-run`
* Detects bump level
* Delegates to SemVer

---

## ✅ Benefits

* Pluggable logic
* Easy to extend
* Clean separation

````

---

# 📘 6. `docs/guides/developer_guide.md`

```md
# 👨‍💻 Developer Guide

This guide helps you understand how to work with the system.

---

## 🧠 Core Rules

### 1. Do NOT use GitHelper
Use:
```python
GitService
````

---

### 2. Do NOT mix layers

❌ Bad:

* Git logic inside strategy

✅ Good:

* Strategy → GitService

---

### 3. Use Version Helpers

```python
helper = SemverVersionHelper("v1.2.3")
helper.get_bump_version(...)
```

---

### 4. Use VersionBridge only at boundaries

---

## 🧩 Adding New Strategy

1. Create class
2. Implement `get_next_tag()`
3. Use GitService
4. Use VersionHelper

---

## 🧪 Testing Tips

* Mock GitService
* Test helpers independently
* Avoid subprocess in tests

````

---

# 📘 7. `docs/guides/migration_guide.md`

```md
# 🔄 Migration Guide

This project has been refactored from `GitHelper` to a clean architecture.

---

## ❌ Before

- GitHelper used everywhere
- Mixed logic
- Hard to test

---

## ✅ After

- GitService (domain)
- Executor (infra)
- Strategy pattern

---

## 🔁 Migration Rules

### Replace:

```python
GitHelper.get_latest_tag()
````

→

```python
git_service.get_latest_tag()
```

---

### Remove:

* print()
* sys.exit()

Replace with:

* logger
* exceptions

---

## 🧠 Result

* Cleaner code
* Better architecture
* Easier to maintain

````

---

# 📘 8. `docs/diagrams/architecture_diagram.md`

```md
# 🧩 Mermaid — Architecture Overview

```mermaid
flowchart TD

CLI --> Strategy
Strategy --> VersionHelper
VersionHelper --> GitService
GitService --> Executor
Executor --> Runner
````

````

---

# 📘 9. `docs/diagrams/changelog_pipeline_diagram.md`

```md
# 🧩 Mermaid — Changelog Pipeline

```mermaid
flowchart TD

A[Raw Commit Message] --> B[parse_commit]

B --> C{Valid?}
C -->|No| X[Skip]
C -->|Yes| D[CleanStage]

D --> E[BreakingChangeStage]

E --> F{Type == release?}
F -->|Yes| G[ReleaseTransformStage]
F -->|No| H[NormalTransformStage]

G --> I[Structured Output]
H --> I
````

````

---

# 📘 10. `docs/diagrams/version_flow_diagram.md`

```md
# 🧩 Mermaid — Version Flow

```mermaid
flowchart TD

A[Git Tag] --> B{Strategy}

B -->|PEP440| C[PEP440Helper]
B -->|SemVer| D[SemverHelper]

C --> E[Next Version]
D --> E

E --> F[Tag Strategy]

F --> G[GitService]
G --> H[Create Tag]
````

```

---

# ✅ DONE

You now have:

- 📘 Architecture docs
- 📘 Developer guide
- 📘 Migration guide
- 📊 Mermaid diagrams
- 📁 Clean structure

---

## 🚀 Next Recommended Step

Now you are ready for:

👉 **WorkflowManager refactor (most powerful layer)**

or

👉 **CLI UX design**

Just tell me 👍
```
