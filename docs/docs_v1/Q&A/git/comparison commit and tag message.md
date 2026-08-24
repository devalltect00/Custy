<!-- docs/docs_v1/Q&A/git/comparison commit and tag message.md -->

# Questions

```text
So on the body, We use
=====
This beta includes several bug fixes and enhancements:
- *(Nothing yet)* – See tag message for full context.
=====

Instead of
=====
- Add automation for structured commit-msg.txt and tag-msg.txt generation
- Improve format clarity, flexibility, and fallback behavior
- Fix issues with backup and staging of message templates
- Update internal docs: docs\git\commit_message.md
====
, like that? why?
```

# Answers

Excellent question — this is about audience, timing, and maintainability.

Let’s compare the two styles side by side:

## 🅰 Summary Placeholder Style (you used)

```text
This beta includes several bug fixes and enhancements:
- *(Nothing yet)* – See tag message for full context.
```

✅ Pros:

-   ✅ Clean and minimal
-   ✅ Useful when you haven't collected or finalized the list yet
-   ✅ Encourages using the more detailed tag-msg.txt for changelog-like info
-   ✅ Consistent and automation-friendly
-   ✅ Fast to generate and edit

❌ Cons:

-   ❌ Less informative for git log or CLI-only users unless they check the tag

## 🅱 Full Descriptive List (I provided earlier)

```text
- Add automation for structured `commit-msg.txt` and `tag-msg.txt` generation
- Improve format clarity, flexibility, and fallback behavior
- Fix issues with backup and staging of message templates
- Update internal docs: docs\git\commit_message.md
```

✅ Pros:

-   ✅ Immediately informative for developers running git log
-   ✅ More expressive and detailed
-   ✅ Doesn’t require opening tag-msg.txt

❌ Cons:

-   ❌ Can be redundant if already copied into tag-msg.txt
-   ❌ More work to maintain manually or automate
-   ❌ May feel verbose for beta/alpha releases with partial changes

🧠 So which to use when?

| Situation                                                 | Use Summary Placeholder 🅰 | Use Full List 🅱 |
| --------------------------------------------------------- | ------------------------- | --------------- |
| Beta/alpha, partial or WIP release                        | ✅                        | Maybe           |
| Final release                                             | Maybe                     | ✅              |
| You want to keep commit-msg shorter and cleaner           | ✅                        | ❌              |
| You don’t want duplication across tag and commit messages | ✅                        | ❌              |
| You want `git log` to be highly informative without tags  | ❌                        | ✅              |

💡 Recommendation (best of both worlds):

Use Placeholder Style 🅰 for:

-   alpha / beta / rc
-   automated dry-run commits
-   smaller or less important releases

Use Full List Style 🅱 for:

-   final releases
-   changelog-driven commits
-   hand-written, user-facing commits

And optionally combine them like this:

```text
This beta includes several bug fixes and enhancements:
- *(Nothing yet)* – See tag message for full context.

Examples of improvements:
- Add automation for structured message generation
- Improve staging and backup behavior

```

## ✅ When to Use Summary Placeholder 🅰 vs Full List 🅱 (By Release Type)

| **Situation / Release Type**                                | **Use Summary Placeholder 🅰** | **Use Full List 🅱** | **Notes**                                                              |
| ----------------------------------------------------------- | ----------------------------- | ------------------- | ---------------------------------------------------------------------- |
| 🧪 **Alpha / Beta (WIP, partial)**                          | ✅                            | Maybe               | Still unstable. Prefer minimal, avoid duplicating full detail.         |
| 🧪 **RC (Release Candidate)**                               | ✅ (if stable enough)         | ✅ (if confident)   | Important checkpoint. Summary is okay, full list helpful if validated. |
| ✅ **Final release**                                        | Maybe                         | ✅                  | User-facing, changelog-worthy — full list preferred.                   |
| 🛠️ **Dev release (e.g. `1.5.0.dev3`)**                      | ✅                            | ❌                  | Internal/experimental — short, fast iteration. Avoid verbosity.        |
| 🔁 **Post release (e.g. `1.5.0.post1`)**                    | ✅                            | Maybe               | Often hotfixes or docs — short message is usually enough.              |
| 🐞 **Hotfix / Patch**                                       | ✅                            | ✅                  | Depends on urgency. Quick fix = summary; more context = full list.     |
| ✨ **You want clean and minimal commit logs**               | ✅                            | ❌                  | Commit remains short, tag carries full details.                        |
| 📜 **You want informative `git log` w/o viewing tag**       | ❌                            | ✅                  | Full list gives instant clarity in terminal/CLI-only workflows.        |
| 🔄 **You’re generating both commit & tag from same script** | ✅                            | ❌                  | Prevents duplication, especially in automated pipelines.               |
| ✍️ **Manual, curated release commit**                       | Maybe                         | ✅                  | Fine to repeat highlights if message is hand-written.                  |

## 💡 Summary by Release Type

| Release Type     | Preferred Commit Body Style | Why                                                            |
| ---------------- | --------------------------- | -------------------------------------------------------------- |
| **dev**          | 🅰 Summary only              | Too fast-changing, not worth listing everything                |
| **alpha / beta** | 🅰 Summary + optional hints  | Feature-incomplete. Summary enough, but may include 1–2 lines  |
| **rc**           | 🅱 Full list (if stable)     | Considered stable. Worth describing features in commit         |
| **final**        | 🅱 Full list preferred       | Be complete — useful for git log, changelog, releases          |
| **post**         | 🅰 Summary or 🅱 light list   | Bug/doc fix? Short is fine. More details if major backport/fix |

## ✅ Suggested Format for Dev/RC/Post

### 🧪 Dev Example:

```text
chore(release): 1.5.0.dev3 – early dev iteration

This dev build includes internal tweaks and early test scaffolding.
- *(Nothing yet)* – See tag message or changelog for details.

Tag: 1.5.0.dev3
```

### 🔄 RC Example:

```text
chore(release): 1.5.0rc1 – release candidate for v1.5.0

This RC prepares the final build of Custy 1.5.0 with validated features.

- Add structured message templates
- Improve dry-run automation logic
- Final documentation touches

Tag: 1.5.0rc1
```

### 📌 Post Example:

```text
chore(release): 1.5.0.post1 – follow-up patch release

Applies minor documentation and backup-related fixes.
- *(Nothing yet)* – See tag for full breakdown.

Tag: 1.5.0.post1
```
