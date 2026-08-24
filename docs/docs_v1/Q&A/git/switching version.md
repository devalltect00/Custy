<!-- docs/docs_v1/Q&A/git/switching version.md -->

# Questions

```text
From dev-> dev
From dev-> alpha
From dev-> beta
From dev-> rc
From dev-> final release
From dev-> post
From alpha-> dev
From alpha-> alpha
From alpha-> beta
From alpha-> rc
From alpha-> final release
From alpha-> post
From beta-> dev
From beta-> alpha
From beta-> beta
From beta-> rc
From beta-> final release
From beta-> post
From rc-> dev
From rc-> alpha
From rc-> beta
From rc-> rc
From rc-> final release
From rc-> post
From final release-> dev
From final release-> alpha
From final release-> beta
From final release-> rc
From final release-> final release
From final release-> post
From post-> dev
From post-> alpha
From post-> beta
From post-> rc
From post-> final release
From post-> post


From these which one the transition or swithc version is possible and if it si possible from what and what the next to
```

# Answers

Here is a full breakdown of each transition **from a current version state to a target** based on your tier precedence:

```cpp
dev < alpha < beta < rc < final < post
```

We'll show:

-   ✅ = Valid transition
-   ❌ = Invalid or not recommended
-   🔁 = Requires bump to next base version (e.g. 1.2.3.dev3 → 1.2.4a1)

### 🔍 Legend for Output:

-   ✅ = allowed (same base)
-   🔁 = allowed, but requires bump (e.g. minor, patch)
-   ❌ = not allowed (tier regression)

## ✅ Transitions Table

| From  | To    | Valid? | Next Version Example              |
| ----- | ----- | ------ | --------------------------------- |
| dev   | dev   | ✅     | `1.2.3.dev1` → `1.2.3.dev2`       |
| dev   | alpha | ✅     | `1.2.3.dev3` → `1.2.3a1`          |
| dev   | beta  | ✅     | `1.2.3.dev3` → `1.2.3b1`          |
| dev   | rc    | ✅     | `1.2.3.dev3` → `1.2.3rc1`         |
| dev   | final | ✅     | `1.2.3.dev3` → `1.2.3`            |
| dev   | post  | ❌     | **post only allowed after final** |
| alpha | dev   | ❌     | **tier regression**               |
| alpha | alpha | ✅     | `1.2.3a1` → `1.2.3a2`             |
| alpha | beta  | ✅     | `1.2.3a3` → `1.2.3b1`             |
| alpha | rc    | ✅     | `1.2.3a3` → `1.2.3rc1`            |
| alpha | final | ✅     | `1.2.3a3` → `1.2.3`               |
| alpha | post  | ❌     | **post only allowed after final** |
| beta  | dev   | ❌     | **tier regression**               |
| beta  | alpha | ❌     | **tier regression**               |
| beta  | beta  | ✅     | `1.2.3b1` → `1.2.3b2`             |
| beta  | rc    | ✅     | `1.2.3b2` → `1.2.3rc1`            |
| beta  | final | ✅     | `1.2.3b2` → `1.2.3`               |
| beta  | post  | ❌     | **post only allowed after final** |
| rc    | dev   | ❌     | **tier regression**               |
| rc    | alpha | ❌     | **tier regression**               |
| rc    | beta  | ❌     | **tier regression**               |
| rc    | rc    | ✅     | `1.2.3rc1` → `1.2.3rc2`           |
| rc    | final | ✅     | `1.2.3rc2` → `1.2.3`              |
| rc    | post  | ❌     | **post only allowed after final** |
| final | dev   | 🔁     | `1.2.3` → `1.2.4.dev1`            |
| final | alpha | 🔁     | `1.2.3` → `1.2.4a1`               |
| final | beta  | 🔁     | `1.2.3` → `1.2.4b1`               |
| final | rc    | 🔁     | `1.2.3` → `1.2.4rc1`              |
| final | final | 🔁     | `1.2.3` → `1.2.4`                 |
| final | post  | ✅     | `1.2.3` → `1.2.3.post1`           |
| post  | dev   | 🔁     | `1.2.3.post3` → `1.2.4.dev1`      |
| post  | alpha | 🔁     | `1.2.3.post3` → `1.2.4a1`         |
| post  | beta  | 🔁     | `1.2.3.post3` → `1.2.4b1`         |
| post  | rc    | 🔁     | `1.2.3.post3` → `1.2.4rc1`        |
| post  | final | ❌     | **regression (already released)** |
| post  | post  | ✅     | `1.2.3.post3` → `1.2.3.post4`     |

## 📌 Notes

Post-release must come after final release

You can’t go backwards in tier

After post, to go to next cycle (dev, alpha, rc), you must bump base version

## 🧠 Suggested Automation Rule

If current tier is lower than target tier, keep base version
If current tier is equal, just increment
If current tier is higher, ❌ deny or require bump
