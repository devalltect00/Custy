<!-- docs/guides/cli/2/architecture.md -->

# 🏗️ Custy CLI Architecture

Custy is a modular CLI tool designed for Git automation, versioning, changelog generation, and workflow orchestration.

This document explains the **core architecture**, how components interact, and the design principles behind the system.

---

## 🎯 Design Goals

- Clear separation of concerns
- Pipeline-driven execution
- Scalable and extensible
- Consistent CLI experience
- Decoupled from Typer in core logic

---

## 🧱 High-Level Architecture

```

CLI (Typer)
↓
Context (AppContext)
↓
Pipeline (run / registry)
↓
Step Layer (adapters)
↓
Service Layer (business logic)

```

---

## 🧩 Core Components

### 1. CLI Layer (Typer)

Handles:
- Parsing user input
- CLI options & arguments
- Command routing

Example:
```

custy commit
custy run commit tag push
custy changelog generate

````

---

### 2. Context Layer (`AppContext`)

Acts as shared runtime state across all steps.

Contains:
- global flags (`dry_run`, `debug`, `log_level`)
- shared inputs (`commit_message_file`, etc.)
- runtime state (`validated`)
- resolved args

---

### 3. Registry (`registry.py`)

Maps pipeline step names → executable functions.

Example:
```python
PIPELINE = {
    "validate": validate_step,
    "commit": commit_changes,
}
````

Also defines presets:

```python
PRESETS = {
    "release": ["validate", "commit", "tag", "push"]
}
```

---

### 4. Pipeline (`run` command)

Responsible for:

* expanding presets
* resolving steps
* executing steps sequentially

Example:

```
custy run commit tag push
```

---

### 5. Step Layer

Acts as adapter between pipeline and services.

Responsibilities:

* build service instances
* prepare inputs
* call service methods

---

### 6. Service Layer

Contains core business logic.

Examples:

* `ValidationService`
* `ChangelogService`
* `WorkflowService`

Services:

* do NOT depend on Typer
* operate using `AppContext` + resolved args

---

### 7. Decorators

Used in CLI layer only.

Example:

```python
@require_validation
def commit(...):
```

⚠️ Important:

* Decorators DO NOT run in pipeline mode
* Pipeline must handle dependencies separately

---

### 8. Rich (Output Layer)

Used for:

* colored logs
* structured output
* better UX

---

## 🔁 Execution Modes

### 1. Direct Command

```
custy commit
```

Flow:

```
CLI → decorator → step/service
```

---

### 2. Pipeline Mode

```
custy run commit tag push
```

Flow:

```
CLI → run → registry → step → service
```

---

## ⚠️ Important Design Rules

### Rule 1: Services must be CLI-independent

❌ Bad:

```python
def commit(ctx: typer.Context)
```

✅ Good:

```python
def commit(ctx: AppContext)
```

---

### Rule 2: Steps are required for class-based services

Pipeline should NOT call class methods directly.

---

### Rule 3: Context is the single source of truth

Avoid multiple sources:

* CLI args
* service args
* global variables

Use `AppContext` instead.

---

## 🚀 Future Extensions

* Step dependency system
* Config-driven pipeline (`custy.yml`)
* Plugin system
* Middleware hooks

---

## 📌 Summary

Custy uses a layered architecture:

* CLI handles input
* Context stores state
* Pipeline orchestrates execution
* Steps adapt logic
* Services execute business rules

This ensures scalability, maintainability, and clarity.
