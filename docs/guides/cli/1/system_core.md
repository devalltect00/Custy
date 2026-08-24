<!-- docs/guides/cli/1/system_core.md -->

# ⚙️ System Core Design

This document focuses on the internal core systems of Custy.

---

## 🔁 Pipeline Engine

The pipeline engine allows dynamic execution:

```bash
custy run commit tag push
````

---

### Registry

```python
PIPELINE = {
    "commit": commit_changes,
    "tag": tag_bump,
}
```

---

### Execution

```python
for step in steps:
    PIPELINE[step]()
```

---

## 🧠 Context System

Context ensures consistent execution:

```python
ctx.obj = AppContext()
```

---

### Usage

```python
app_ctx = get_context(ctx)
```

---

## 📊 Step Runner

Reusable execution helper:

```python
run_steps(title, steps)
```

Supports:

* progress bar
* error handling
* step tracking

---

## 🛡️ Error System

Custom exceptions:

```python
class ValidationError(Exception):
```

---

## 🎨 Theme System

Centralized styling:

```python
console = Console(theme=theme.to_rich_theme())
```

---

## 🔄 Validation System

Split into atomic functions:

```python
ensure_git_repo()
ensure_version_file()
```

---

## 🧩 Design Pattern Used

| Pattern          | Usage         |
| ---------------- | ------------- |
| Command Pattern  | CLI commands  |
| Pipeline Pattern | run execution |
| Decorator        | validation    |
| Strategy         | versioning    |
| Facade           | service layer |

---

## 🚀 Summary

Core system is:

* modular
* testable
* extensible
