<!-- docs/guides/GitWorkflowEngine/custy_pipeline_system/developer_guide.md -->

# 🧑‍💻 Developer Guide — Custy Pipeline System

## 📌 Overview

Custy uses a **pipeline-based architecture** to orchestrate Git operations such as:

- validation
- commit message editing
- changelog generation
- commit & tagging
- backup & cleanup
- workflow transitions

Instead of a monolithic flow, the system is broken into **small, reusable steps** executed sequentially.

---

## 🧱 Core Concepts

### 1. Pipeline

The pipeline is the **orchestrator** that runs steps in order.

```python
pipeline.run(context)
````

Each step performs a single responsibility.

---

### 2. Step

A step is a unit of execution.

```python
class CommitStep(BaseStep):
    def execute(self, ctx):
        ...
```

Rules:

* Must implement `execute(context)`
* Should only do **one thing**
* Should not depend on other steps directly

---

### 3. Context

The context is a shared object passed across all steps.

```python
ctx.tag
ctx.files_to_stage
ctx.git
```

Purpose:

* Share state between steps
* Avoid tight coupling

---

### 4. Step Registry

Steps are registered globally and referenced by name.

```python
StepRegistry.register("commit", CommitStep)
```

This enables:

* dynamic pipelines
* plugin system
* decoupling

---

### 5. Pipeline Builder

Builds pipeline from configuration.

```python
builder.build([
    {"name": "validate"},
    {"name": "commit"},
])
```

---

## 🔁 Execution Flow

```text
GitCommitTagger
    ↓
PipelineBuilder
    ↓
Pipeline
    ↓
Steps (execute one by one)
    ↓
Domain Logic (Git / Changelog / Workflow)
```

---

## 🧩 Available Steps

| Step          | Responsibility                       |
| ------------- | ------------------------------------ |
| validate      | Validate repo, files, tag            |
| workflow_init | Validate transition & prepare branch |
| edit_commit   | Generate + edit commit message       |
| changelog     | Generate CHANGELOG.md                |
| commit        | Stage + commit                       |
| tag           | Create git tag                       |
| backup        | Backup messages                      |
| push          | Push to remote                       |
| cleanup       | Cleanup backups/branches             |
| finalize      | Final workflow actions               |

---

## ➕ Adding a New Step

### 1. Create step

```python
class NotifyStep(BaseStep):
    def execute(self, ctx):
        print("Notify!")
```

### 2. Register step

```python
StepRegistry.register("notify", NotifyStep)
```

### 3. Use in pipeline

```python
{"name": "notify"}
```

---

## 🔧 Modifying Pipeline

Change order easily:

```python
pipeline_config = [
    {"name": "validate"},
    {"name": "changelog"},
    {"name": "commit"},
]
```

---

## 🧪 Testing Strategy

Each step is testable independently:

```python
step.execute(mock_context)
```

Recommended:

* mock `ctx.git`
* mock filesystem
* assert side effects

---

## 🧠 Design Principles

* Single Responsibility Principle (SRP)
* Separation of Concerns
* Explicit flow over implicit logic
* Composition over inheritance

---

## ⚠️ Guidelines

### DO

* keep steps small
* use logging (not print)
* pass data via context

### DON'T

* call other steps directly
* store global state
* mix responsibilities

---

## 🚀 Future Extensions

* conditional steps
* config-driven pipelines (`.custy.toml`)
* hooks (before/after step)
* retry / rollback system

---

## ✅ Summary

Custy is now:

* modular
* extensible
* testable
* production-ready

Think of it as a **mini workflow engine for Git automation**.
