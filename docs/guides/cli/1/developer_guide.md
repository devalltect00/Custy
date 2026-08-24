<!-- docs/guides/cli/1/developer_guide.md -->

# 📄 `docs/developer_guide.md`

```md
# 🧑‍💻 Custy Developer Guide

This document helps developers understand how to work with Custy CLI, extend features, and follow consistent patterns.

---

## 🎯 Core Principles

Custy follows these principles:

- **Atomic Commands** → Each command does one thing
- **Pipeline Execution** → Combine commands dynamically
- **Separation of Concerns** → CLI ≠ Business Logic
- **Context-driven Execution** → Shared runtime state
- **User-friendly Output** → Clean CLI UX (no raw tracebacks)

---

## 📁 Project Overview

```

app/
├── cli/           # CLI layer (Typer)
├── services/      # Business logic
├── utils/         # Helpers (runner, progress, etc.)
├── theme/         # Styling system
├── errors/        # Custom exceptions

```

---

## 🧠 Execution Flow

1. CLI starts (`__main__.py`)
2. `@app.callback()` initializes context
3. Command is executed
4. Context is accessed via `get_context()`
5. Service layer is called
6. Output formatted via Rich

---

## ⚙️ Adding a New Command

### Step 1 — Create service logic

```

app/services/my_service.py

````

```python
def do_something():
    ...
````

---

### Step 2 — Create CLI command

```
app/cli/commands/my_command.py
```

```python
import typer
from app.services.my_service import do_something

def my_command(ctx: typer.Context):
    do_something()
```

---

### Step 3 — Register command

```
app/cli/main.py
```

```python
app.command()(my_command)
```

---

## 🔄 Using Context

Always access context like this:

```python
from app.cli.context import get_context

def command(ctx: typer.Context):
    app_ctx = get_context(ctx)
```

### Available properties:

| Property    | Description                  |
| ----------- | ---------------------------- |
| `dry_run`   | simulate execution           |
| `debug`     | show full traceback          |
| `validated` | prevent duplicate validation |

---

## 🛡️ Validation Pattern

Do NOT use:

```python
print("error")
sys.exit(1)
```

Use:

```python
raise ValidationError("Message", hint="Fix suggestion")
```

Handled in CLI layer → clean output.

---

## 🔁 Pipeline Execution

Use:

```bash
custy run commit tag push
```

Internally:

```python
PIPELINE = {
    "commit": commit_changes,
    "tag": tag_bump,
}
```

---

## 📊 Progress Execution

Use reusable helper:

```python
run_steps("Title", [
    ("Step 1", func1),
    ("Step 2", lambda: func2(arg)),
])
```

---

## 🎨 Styling

Use semantic styles:

```python
console.print("[success]Done")
console.print("[error]Failed")
```

DO NOT hardcode colors like `[green]`.

---

## ⚠️ Common Mistakes

| Mistake               | Fix              |
| --------------------- | ---------------- |
| Using `print()`       | Use Rich console |
| Using `sys.exit()`    | Raise exception  |
| Hardcoding colors     | Use theme        |
| Business logic in CLI | Move to services |

---

## 🚀 Recommended Workflow

```bash
custy run validate commit tag push changelog
```

---

## 🧩 Summary

* CLI = orchestration
* Services = logic
* Context = state
* Theme = UI consistency
* Pipeline = flexibility
