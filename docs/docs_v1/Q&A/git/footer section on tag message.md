<!-- docs/docs_v1/Q&A/git/footer section on tag message.md -->

# Questions

```text
I want to use
_Author: devalltect00_
_Date: 2025-07-31_
Btw where and when?

Option1: devrelease
Option2: pre release
Option3: Beta/alpha,
Option4: Release candidate (rc)
Option5: Final release
Option6: post release
Option7: Other options/maybe there are a better solutions
```

# Answers

Excellent — including

```markdown
_Author: devalltect00_
_Date: 2025-07-31_
```

is a great touch for traceability and polish.

Now let's decide **where and when** you should include this, based on the **release type**.

## ✅ Best Practice Summary

| Release Type                         | Include Author/Date?      | Reason                                                                 |
| ------------------------------------ | ------------------------- | ---------------------------------------------------------------------- |
| **Option 1: Dev release** (devN)     | ❌ Optional or skip       | Too volatile; often auto-generated. No need for signature.             |
| **Option 2: Pre-release** (umbrella) | ✅ Yes (if manual)        | Adds clarity during alpha/beta/rc series. Shows who cut the release.   |
| **Option 3: Alpha / Beta**           | ✅ Recommended            | Traceable but still in active test. Good for internal coordination.    |
| **Option 4: RC (release candidate)** | ✅ Yes                    | Important milestone. Often reviewed before final — show author/date.   |
| **Option 5: Final release**          | ✅ Strongly recommended   | Final, public, stable release — clearly mark who released and when.    |
| **Option 6: Post release**           | ✅ Optional (recommended) | If manually written, include for traceability. Skip if auto-generated. |
| **Option 7: Hotfix / Patch**         | ✅ Recommended            | Shows fast-tracked fix ownership. Helpful in audit/recovery.           |

## 📍 Where to put it?

✅ **In `tag-msg.txt` (Recommended)**
Always place at the end, after a horizontal divider or spacing:

```markdown
---

_Author: devalltect00_
_Date: 2025-07-31_
```

🚫 **In `commit-msg.txt`**
Avoid it in `commit-msg.txt` unless you're writing a **multi-line commit** that acts as a changelog entry (which is rare and usually discouraged). Commit logs already store author/date via Git metadata.

## ✅ Final Example for tag-msg.txt (e.g. for RC):

```markdown
🧪 Release Candidate: Custy 1.5.0rc1

This RC includes final validations before Custy v1.5.0.

### ✨ Features

-   Message formatting automation for releases
-   Improved fallback handling in dry-run flow

### 🐛 Bug Fixes

-   Fix: template backup before staging
-   Fix: version detection edge cases for PEP 440

---

_Author: devalltect00_
_Date: 2025-07-31_
```

## 💡 Optional Enhancement

You can also make the author/date block configurable in your automation, e.g.:

```python
if self.settings.get("include_author_date", True):
    lines.append("")
    lines.append(f"_Author: {self.settings.get('custom_author', 'devalltect00')}_")
    lines.append(f"_Date: {datetime.now().strftime('%Y-%m-%d')}_")
```
