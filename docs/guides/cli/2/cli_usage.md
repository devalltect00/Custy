<!-- docs/guides/cli/2/cli_usage.md -->

# 🧑‍💻 CLI Usage

---

## Basic Commands

````

custy validate
custy commit
custy tag
custy push

```

---

## Pipeline

```

custy run commit tag push
custy run release
custy run full

```

---

## Changelog

```

custy changelog generate
custy changelog preview
custy changelog validate

```

---

## Backup & Cleanup

```

custy backup commit
custy cleanup branches

```

---

## Global Options

```

--dry-run
--debug
--log-level

```

---

## Examples

```

custy run commit tag push --dry-run
custy commit -m "feat: add login"

```
