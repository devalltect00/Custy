# Questions

```text
What the most use and common for changelog, use git commit message or git tag message or both or none of them or something else?
```

# Answers

ChatGPT said:
✅ Most commonly used and recommended approach for changelogs is:

🔹 Use Git commit messages (especially with Conventional Commits).
🔍 Why commit messages are the standard:

| Reason                        | Description                                                                                              |
| ----------------------------- | -------------------------------------------------------------------------------------------------------- |
| ✅ **Most granular**          | Every feature, fix, chore is captured as a commit.                                                       |
| ✅ **Automatable**            | Tools like Commitizen, Semantic Release, Git-Cliff, etc., parse commit logs to generate changelogs.      |
| ✅ **Semantic grouping**      | Commit types (`feat`, `fix`, etc.) help categorize changelog entries.                                    |
| ✅ **Standardized workflows** | Most teams and CI/CD pipelines rely on commit logs to determine versions, changelogs, and release notes. |

🏷️ What about Git tag messages?

| Tag Messages                             | Usage                                                   |
| ---------------------------------------- | ------------------------------------------------------- |
| ✅ Useful for                            | Summarizing the **release** in a human-readable way.    |
| ✅ Audience                              | GitHub/GitLab release pages, `git show <tag>`, etc.     |
| ❌ Not standard for changelog generation | Tools don’t use them unless custom scripts are written. |

📝 Combined Strategy (Advanced teams):
| Element | Used For |
| ---------------------------------- | --------------------------------------------------------------------- |
| 🔹 Commit message | Primary source for changelog entries |
| 🔹 Tag message | Polished summary of the release (manual or templated) |
| 🔹 Changelog file (`CHANGELOG.md`) | Generated or curated using commits, with summaries from tag if needed |

🔧 Examples of tooling using commit messages:

-   Commitizen – generates changelog from commit history
-   semantic-release – uses commit messages to bump version + changelog
-   standard-version – commit-based changelog and versioning
-   Git-Cliff, Git-Chglog – commit-based but customizable
-   Conventional Changelog – formal spec that parses commits

🧠 Summary

| Source                 | Recommended Use                                                   |
| ---------------------- | ----------------------------------------------------------------- |
| ✅ **Commit Messages** | ✅ Primary and most common for changelog generation               |
| ⚠️ Tag Messages        | 📝 Optional, more for summaries and `git show`, not changelogs    |
| ❌ None / Manual       | ❌ Risk of inconsistency, not scalable                            |
| ✅ Custom Combination  | ✅ Best for advanced workflows: structured commits + curated tags |
