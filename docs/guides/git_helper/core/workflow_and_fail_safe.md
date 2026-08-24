<!-- docs/guides/git_helper/core/workflow_and_fail_safe.md -->

# 🔄 Workflow & Fail-Safe Strategy

## 🎯 Purpose

This document explains how Custy handles:

- commit → tag → push pipeline
- fail-safe push
- retry strategy
- partial success handling

---

## 🚀 Release Flow

```

1. Validate
2. Commit
3. Tag
4. Push (multi-remote)

```

---

## 🔁 Fail-Safe Push

### Strategy

- retry failed push
- track success & failure
- do not silently fail

---

## 🔧 Retry Logic

```

attempt <= retries

```

Default:
- retries = 2

---

## 📊 Partial Success

Example:

```

success = ["origin"]
failed = ["backup"]

````

System returns:

```python
OperationResult(
    success=False,
    message="Push partially failed",
    data={...}
)
````

---

## ⚠️ No Silent Failure

All failures are:

* logged
* returned
* visible to caller

---

## 🔄 Rollback Strategy (Optional)

Not enforced automatically.

Possible future:

* delete tag
* revert commit
* manual intervention

---

## 🧠 Design Decision

We prefer:

```
Visibility > Silent Automation
```

---

## 🔚 Summary

* retry improves reliability
* partial success is tracked
* system remains predictable
