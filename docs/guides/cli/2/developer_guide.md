<!-- docs/guides/cli/2/developer_guide.md -->

# 👨‍💻 Developer Guide

This guide explains how to extend Custy CLI safely and consistently.

---

## 🧩 Adding a New Command

### Step 1: Create CLI command

```python
@app.command()
def my_command(ctx: typer.Context):
    app_ctx = get_context(ctx)
    my_service(app_ctx)
````

---

### Step 2: Add service logic

```python
def my_service(ctx: AppContext):
    ...
```

---

### Step 3 (optional): Add step for pipeline

```python
def my_step(ctx: AppContext):
    my_service(ctx)
```

---

### Step 4: Register in pipeline

```python
PIPELINE["my-step"] = my_step
```

---

## 🧩 Adding a New Pipeline Step

1. Create step function
2. Register in `registry.py`
3. Ensure it accepts `AppContext`

---

## 🧩 Adding a Service

Use class if:

* complex logic
* reusable
* needs internal state

Example:

```python
class MyService:
    def run(self, ctx: AppContext):
        ...
```

---

## 🧩 Context Usage

Always use:

```python
app_ctx = get_context(ctx)
```

Never pass raw CLI args directly to services.

---

## 🧩 Logging

Use structured logging (Rich if enabled):

```python
logger.info("[primary]Running step...[/primary]")
```

---

## 🧩 Best Practices

* Keep services pure
* Keep steps thin
* Avoid duplicating logic in CLI + pipeline
* Use context consistently

---

## ⚠️ Common Mistakes

❌ Calling service with `typer.Context`
❌ Skipping context
❌ Mixing CLI args and service args

---

## ✅ Summary

* CLI = input
* Context = state
* Step = adapter
* Service = logic
