# 🌐 Dual Remote Git Strategy: GitLab (origin) + GitHub (backup)

This document provides a clear guide for managing two Git remotes: `origin` (GitLab) and `backup` (GitHub). GitLab is used as the **primary** repository for development and CI/CD, while GitHub is used as a **mirror backup** for critical branches.

---

## 🔁 Remote Naming Convention

| Remote Name | Platform | Purpose             |
| ----------- | -------- | ------------------- |
| `origin`    | GitLab   | Primary (main repo) |
| `backup`    | GitHub   | Mirror/backup only  |

To configure remotes:

```bash
git remote add origin git@gitlab.com:your-org/your-repo.git
git remote add backup git@github.com:your-username/your-repo.git
```

---

## 🚀 What to Push to Each Remote

| Branch Type    | Push to `origin` (GitLab)? | Push to `backup` (GitHub)? | Notes                                     |
| -------------- | -------------------------- | -------------------------- | ----------------------------------------- |
| `main`         | ✅ Always                  | ✅ Always                  | Final releases — must be backed up        |
| `develop`      | ✅ Always                  | ✅ Always                  | Active dev — good to mirror               |
| `release/x.y`  | ✅ Always                  | 🔄 Optional                | RC testing — backup if needed             |
| `hotfix/x.y.z` | ✅ Always                  | ✅ Always                  | Production fixes — critical to mirror     |
| `feature/*`    | 🔄 Optional                | ❌ No                      | Push to GitLab only if needed             |
| `ci/*`         | ✅ Only                    | ❌ No                      | Pipeline/testing — skip backup            |
| `sandbox/*`    | 🔄 Optional                | ❌ No                      | Local/test branches — not needed remotely |

---

## 🧠 Suggested Push Commands

### Push to GitLab (origin):

```bash
git push origin --all
git push origin --tags
```

### Push to GitHub (backup):

```bash
git push backup main
git push backup develop
git push backup --tags
```

> You can also script this with a shell alias or Git hook.

---

## 🧹 Cleanup Recommendations

| Branch            | Delete After Merge? |
| ----------------- | ------------------- |
| `release/x.y`     | ✅ Yes              |
| `hotfix/x.y.z`    | ✅ Yes              |
| `feature/*`       | ✅ Yes              |
| `ci/*`            | ✅ Yes              |
| `sandbox/*`       | ✅ Yes              |
| `main`, `develop` | ❌ No               |

---

## 📚 References

- [Git Remote Docs](https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes)
- [GitLab CI/CD Pipelines](https://docs.gitlab.com/ee/ci/)
- [GitHub Repository Mirroring](https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repository-mirroring)
