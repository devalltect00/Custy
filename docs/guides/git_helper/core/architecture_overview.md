<!-- docs/guides/git_helper/core/architecture_overview.md -->

# 🏗️ Custy Git Architecture Overview

## 🎯 Purpose

This document explains the architecture of Custy’s Git system after refactoring from a **monolithic GitHelper** into a **layered, extensible design**.

The goal is to make the system:
- easier to maintain
- easier to test
- easier to extend (multi-remote, config-driven, workflow automation)

---

## ❌ Before (Legacy Design)

Previously, everything lived inside:

```

GitHelper (God Class)

```

Responsibilities mixed together:
- subprocess execution
- logging
- error handling
- business logic
- parsing
- config handling

### Problems:
- hard to debug
- tightly coupled
- difficult to extend
- not testable

---

## ✅ After (Current Design)

We now use a **layered architecture**:

```

CLI / Workflow
↓
GitWorkflowManager
↓
GitService
↓
IGitCommandExecutor (Protocol)
↓
GitCommandExecutor
↓
Runner (subprocess)

````

---

## 🧱 Core Components

### 1. `GitCommandExecutor`
Low-level command execution.

- builds git commands
- executes via subprocess
- returns `CommandResult`
- no business logic

---

### 2. `GitService`
Business logic layer.

- interprets results
- applies rules
- integrates config
- orchestrates executor calls

---

### 3. `IGitCommandExecutor` (Protocol)
Type-safe interface.

- defines expected executor behavior
- allows swapping implementations
- enables testing with mocks

---

### 4. `CommandResult`
Standard result object.

```python
CommandResult(
    returncode=0,
    stdout="...",
    stderr="...",
    skipped=False
)
````

Prevents:

* `None` ambiguity
* inconsistent return types

---

### 5. `create_git_service()` (Factory)

Responsible for wiring:

* Runner
* Executor
* Service
* Config

---

### 6. `log_execution` (Decorator)

Used for:

* tracing execution
* debugging
* consistent logging

---

## 🧠 Design Principles Used

### ✅ Separation of Concerns

Each layer has one responsibility.

---

### ✅ Dependency Inversion

`GitService` depends on `IGitCommandExecutor`, not concrete class.

---

### ✅ Factory Pattern

Object creation is centralized.

---

### ✅ Protocol-Based Design

Flexible, testable, no forced inheritance.

---

### ✅ Layered Architecture

Clear flow from high-level → low-level.

---

## 🔁 Data Flow Example

```
WorkflowManager → GitService → Executor → Runner → Git
```

---

## 🚀 Benefits

* ✅ clean codebase
* ✅ easy testing (mock executor)
* ✅ flexible config support
* ✅ multi-remote ready
* ✅ scalable for workflows

---

## 🔚 Summary

We moved from:

```
❌ GitHelper (God Class)
```

to:

```
✅ Modular, layered architecture
```

This enables long-term scalability and maintainability.
