<!-- docs/guides/changelog/core/SYSTEM_WORKFLOW.md -->

# 🔄 Changelog System Workflow

This document explains **how data flows through the system**, from raw input to final `CHANGELOG.md`.

---

## 🎯 Overview

The changelog system transforms:

```id="d0xq9x"
Git commits + Template message
```

into:

```id="tq9c4k"
Structured, readable CHANGELOG.md
```

---

## 🧠 High-Level Flow

```id="4kq6k1"
Message Sources
    ↓
Message Aggregator
    ↓
Commit Pipeline
    ↓
Grouping & Deduplication
    ↓
Template Rendering
    ↓
CHANGELOG.md
```

---

## 🧩 Step-by-Step Breakdown

---

### 1️⃣ Message Sources

Messages come from:

* Git history
* Optional template (`commit-msg.txt`)

```id="v3y2s1"
GitMessageProvider
TemplateMessageProvider
```

Each provider returns:

```id="l7lm1p"
list[str]
```

(raw commit messages)

---

### 2️⃣ Message Aggregation

Messages are combined using a strategy:

```id="0z0f4p"
append_top
append_bottom
merge
override
```

Example:

```id="m0x6eh"
template + git commits
```

---

### 3️⃣ Commit Pipeline (Core Engine)

Each message is processed individually.

---

#### 🔹 Step 3.1 Parse Commit

```id="3h9a9j"
parse_commit()
```

Converts string → structured dict:

```id="v6j3kl"
{
  "type": "feat",
  "scope": "core",
  "subject": "...",
  "body": "..."
}
```

---

#### 🔹 Step 3.2 Pipeline Stages

Each commit goes through:

```id="w2q3rt"
SkipMergeStage
CleanStage
BreakingChangeStage
ReleaseTransformStage
NormalTransformStage
```

---

#### 🔹 Step 3.3 Output

Each commit becomes:

```id="u6rj3y"
{
  "type": "feat",
  "scope": "core",
  "subject": "add feature"
}
```

---

### 4️⃣ Grouping

Commits are grouped by:

```id="m4g4fy"
type → scope → messages
```

Example:

```id="7lmz1h"
feat
 └── core
      ├── add feature
      ├── improve logic
```

---

### 5️⃣ Deduplication

Duplicates are removed using:

```id="7d7l5l"
(type, scope, subject)
```

This prevents repeated entries.

---

### 6️⃣ Version Mapping

Each group belongs to a version:

```id="y3j3dx"
tags = [""] + sorted_tags
```

* `""` → Unreleased
* others → actual versions

---

### 7️⃣ Rendering

Uses:

```id="f5c1xw"
changelog.j2
```

Template receives:

```id="bnl3i8"
releases = [...]
```

Output:

```id="k8f9wr"
CHANGELOG.md
```

---

## 🔍 Visual Example

```id="3kjm0y"
Raw commit:

feat(auth): add login

- support OAuth
```

---

### Pipeline result:

```id="9x1m3z"
type: feat
scope: auth
subject: support OAuth
```

---

### Final output:

```id="7t2d1k"
### ✨ Features

#### auth
- support OAuth
```

---

## 🧠 Special Case: Template Message

Template (`commit-msg.txt`) is treated as:

```id="v5m0vk"
ONE virtual commit
```

It:

* goes through pipeline
* appears under **Unreleased**
* behaves like normal commit

---

## ⚠️ Common Pitfalls

### ❌ Raw message injection

Do NOT:

```id="k2o4q1"
template + rendered_output
```

This breaks the system.

---

### ❌ Skipping pipeline

All messages MUST go through pipeline.

---

### ❌ Incorrect splitting

Template should NOT be split into multiple commits.

---

## ✅ Key Design Principles

### 1. Single Source of Truth

All messages go through the same pipeline.

---

### 2. Separation of Concerns

| Layer      | Responsibility    |
| ---------- | ----------------- |
| Provider   | fetch data        |
| Aggregator | combine data      |
| Pipeline   | transform data    |
| Generator  | organize + render |

---

### 3. Config-Driven Behavior

Everything is controlled via:

```id="c4wqkz"
custy.toml
```

---

## 🚀 Summary

```id="s1j8kp"
Input (Git + Template)
    ↓
Normalize (parse)
    ↓
Clean + Analyze
    ↓
Transform
    ↓
Group
    ↓
Render
    ↓
CHANGELOG.md
```

---

This workflow ensures:

* consistency
* readability
* maintainability
