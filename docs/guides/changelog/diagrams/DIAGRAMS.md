<!-- docs/guides/changelog/diagrams/DIAGRAMS.md -->

# 🔄 1. System Overview

## 🧩 Mermaid Diagram

```mermaid
flowchart TD
    A[Git Commits] --> B[Message Providers]
    T["Template commit-msg.txt"] --> B

    B --> C[Message Aggregator]

    C --> D[Commit Pipeline]

    D --> D1[Skip Merge]
    D --> D2[Clean Stage]
    D --> D3[Breaking Detection]
    D --> D4[Release Transform]
    D --> D5[Normal Transform]

    D --> E[Structured Commits]

    E --> F[Grouping]
    F --> G[Deduplication]

    G --> H["Renderer (Jinja2)"]
    H --> I["CHANGELOG.md"]
```

---

## 🧾 ASCII Diagram (Fallback)

```
Git Commits ───────┐
                   ├──► Message Providers ───► Aggregator ───► Pipeline ───► Group ───► Render ───► CHANGELOG.md
Template Message ──┘
```

---

# 🔁 2. Commit Processing Flow

## 🧩 Mermaid

```mermaid
flowchart TD
    A[Raw Commit Message] --> B["parse_commit()"]

    B --> C{Valid?}
    C -->|No| X[Skip]
    C -->|Yes| D[CleanStage]

    D --> E[BreakingChangeStage]

    E --> F{Type == release?}
    F -->|Yes| G[ReleaseTransformStage]
    F -->|No| H[NormalTransformStage]

    G --> I[Structured Output]
    H --> I
```

---

## 🧾 ASCII

```
Raw Message
   ↓
parse_commit
   ↓
Clean
   ↓
Breaking Detection
   ↓
[Release?]
   ├── Yes → ReleaseTransform
   └── No  → NormalTransform
   ↓
Structured Commit
```

---

# 🧾 3. Changelog Generation Flow

## 🧩 Mermaid

```mermaid
flowchart TD
    A[Tags List] --> B[Loop Tags]

    B --> C["Get Messages (Git + Template)"]

    C --> D["Pipeline.run()"]

    D --> E[Parsed Commits]

    E --> F[Group by Type]
    F --> G[Group by Scope]

    G --> H[Deduplicate]

    H --> I[Build Release Object]

    I --> J[Render Template]

    J --> K["CHANGELOG.md"]
```

---

## 🧾 ASCII

```
Tags
  ↓
Loop
  ↓
Get Messages
  ↓
Pipeline
  ↓
Group
  ↓
Deduplicate
  ↓
Render
  ↓
CHANGELOG.md
```

---

# 🧠 4. Template Integration Flow

## 🧩 Mermaid

```mermaid
flowchart TD
    A["commit-msg.txt"] --> B[TemplateMessageProvider]

    B --> C{Unreleased?}
    C -->|Yes| D[Include]
    C -->|No| E[Skip]

    D --> F[Aggregator]

    F --> G[Pipeline]
```

---

## 🧾 ASCII

```
commit-msg.txt
      ↓
Template Provider
      ↓
[Unreleased Only]
      ↓
Aggregator
      ↓
Pipeline
```

---

# ⚙️ 5. Configuration Influence Flow

## 🧩 Mermaid

```mermaid
flowchart TD
    A["custy.toml"] --> B[Cleaner Config]
    A --> C[Breaking Config]
    A --> D[Template Config]
    A --> E[Scope Map]

    B --> F[CleanStage]
    C --> G[BreakingStage]
    D --> H[TemplateProvider]
    E --> I[Grouping]
```

---

## 🧾 ASCII

```
custy.toml
   ├── cleaning → CleanStage
   ├── breaking → BreakingStage
   ├── template → TemplateProvider
   └── scope_map → Grouping
```

---

# 🖼️ 6. Image Diagram (Export Version)

Use this description if you want to generate a PNG (e.g., draw.io / Excalidraw / Figma):

---

## 🎨 System Diagram (Image Layout)

```
[Git Commits]        [Template File]
       │                     │
       └──────► [Providers] ◄┘
                     │
              [Aggregator]
                     │
               [Pipeline]
     ┌─────────┬──────────┬──────────┬──────────┐
     │ Skip    │ Clean    │ Breaking │ Transform│
     └─────────┴──────────┴──────────┴──────────┘
                     │
               [Structured Data]
                     │
               [Grouping]
                     │
              [Deduplication]
                     │
                [Renderer]
                     │
              [CHANGELOG.md]
```

---

# 🎯 Notes

* Mermaid diagrams work in:

  * GitHub
  * VSCode (Markdown Preview)
* ASCII diagrams work everywhere
* Image layout can be recreated in:

  * draw.io
  * Figma
  * Excalidraw

---

# 🚀 Summary

Now there are:

* System overview diagram
* Pipeline flow diagram
* Changelog generation flow
* Template integration flow
* Config influence flow
* Image-ready diagram

These diagrams help:

* onboarding developers
* explaining architecture
* debugging flow
