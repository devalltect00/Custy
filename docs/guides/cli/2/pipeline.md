<!-- docs/guides/cli/2/pipeline.md -->

# 🔁 Pipeline System

The pipeline system allows executing multiple steps in sequence.

---

## 🧠 Concept

Pipeline = sequence of steps executed via `run` command.

---

## ▶️ Usage

```bash
custy run commit tag push
````

---

## 🧩 Steps

Defined in `registry.py`:

```python
PIPELINE = {
    "commit": commit_changes,
}
```

---

## 🧩 Presets

```python
PRESETS = {
    "release": ["validate", "commit", "tag", "push"]
}
```

---

## 🔄 Execution Flow

1. Parse steps
2. Expand presets
3. Resolve functions
4. Execute sequentially

---

## ⚠️ Important

* Steps must accept `AppContext`
* Steps must be independent
* No Typer dependency

---

## 🚀 Future Improvements

* Step dependencies
* Parallel execution
* Conditional steps
