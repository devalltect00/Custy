<!-- docs/guides/git_helper/core/developer_guide.md -->

# 👨‍💻 Developer Guide: Git System

## 🎯 Purpose

This guide explains how to work with the new Git system in Custy.

---

## 🚀 Quick Start

```python
from app.core.git_ops.factory import create_git_service

git = create_git_service(dry_run=False)

git.commit(message="feat: add feature")
git.tag("v1.0.0", message="Release v1.0.0")
git.push(push_to="all")
````

---

## 🧱 Key Components

### GitService

Main entry point for developers.

Use this for:

* commit
* tag
* push
* querying git state

---

### GitCommandExecutor

Do NOT use directly unless needed.

Used internally by GitService.

---

### CommandResult

Returned by executor:

```python
result.success
result.stdout
result.stderr
```

---

## ⚙️ Config Integration

Uses `.custy.toml`:

```toml
[tool.custy.git]
main_remotes = ["origin"]
backup_remotes = ["backup"]
push_to = "all"
```

---

## 🔁 Priority System

Values resolved in order:

```
1. CLI / function argument
2. Config (.custy.toml)
3. Default value
```

Handled by:

```python
config.resolve(...)
```

---

## 🔄 Multi-Remote Push

```python
git.push(push_to="all")
```

Options:

* `main`
* `backup`
* `all`

---

## 🧪 Testing

Use mock executor:

```python
class FakeExecutor:
    def push(self, remote, ref):
        return CommandResult(returncode=0)
```

---

## ⚠️ Rules

* ❌ Do NOT use subprocess directly
* ❌ Do NOT put logic in executor
* ✅ Always go through GitService
* ✅ Use config via service

---

## 🧠 Best Practices

* Keep executor pure
* Keep service smart
* Keep workflow orchestration separate

---

## 🔚 Summary

| Layer    | Responsibility |
| -------- | -------------- |
| Service  | logic          |
| Executor | commands       |
| Config   | values         |
| Workflow | orchestration  |
