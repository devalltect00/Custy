<!-- docs/guides/cli/1/architecture_overview.md -->

# 🏗️ Custy Architecture Overview

This document explains the system design and architecture of Custy CLI.

---

## 🧠 High-Level Design

Custy is designed as a **layered CLI system**:

````

CLI Layer (Typer)
↓
Context Layer
↓
Service Layer
↓
Utility Layer

```

---

## 📦 Layers Explained

### 1. CLI Layer

- Handles user input
- Defines commands
- Formats output

Location:
```

app/cli/

````

---

### 2. Context Layer

Shared runtime state:

```python
class AppContext:
    dry_run: bool
    debug: bool
    validated: bool
````

---

### 3. Service Layer

Core logic:

* Git operations
* Validation
* Changelog
* Workflow

Location:

```
app/services/
```

---

### 4. Utility Layer

Reusable helpers:

* Progress runner
* Subprocess runner
* Config loader

---

## 🔄 Execution Lifecycle

1. CLI invoked
2. Context initialized
3. Command triggered
4. Validation (optional)
5. Service executed
6. Output rendered

---

## 🔗 Pipeline System

Instead of many commands:

```bash
custy run commit tag push
```

Pipeline registry:

```python
PIPELINE = {
    "commit": func,
    "tag": func,
}
```

---

## 🛡️ Error Handling Strategy

| Layer   | Responsibility   |
| ------- | ---------------- |
| Service | raise exceptions |
| CLI     | format output    |

---

## 🎨 UI System

* Built with Rich
* Uses semantic theming
* Centralized styling

---

## ⚙️ Design Decisions

### Why not many commands?

→ Avoid combinatorial explosion

---

### Why pipeline?

→ Flexible and scalable

---

### Why context?

→ Shared state across execution

---

## 🧩 Summary

* Modular architecture
* Clear separation of concerns
* Extensible design
