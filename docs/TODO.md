# `TODO.md`

Personal notes, planning, and roadmap for **Custy**

---

## ✨ Feature

### ✅ Completed

-   [v] handle custy Full workflow
-   [v] handle custy "git add ."
-   [v] handle custy generate changelog
-   [v] handle custy as a tool
-   [v] handle custy command and put in makefile

---

### 🧩 In Progress

-   [ ] _(Nothing yet)_

---

### 🧠 Planning

-   [ ] for version use this format major.minor.patch-pre_release.pre_release_number
-   [ ] use 2 git remote, gitlab as `main`, and github as backup
-   [ ] use 2 branch; `main` and `dev`; `main` is stable one and `dev` is more experimental
-   [ ] Update the major, minor, and patch on `main` branch. But on `dev` branch `main`, I just update pre_release and pre_release
-   [ ] If there is a abandoned branch or experminet or deprecated branch version and want to go back to `main` branch. I choose to rename branch use format like archive/{feature}-{date} or experiment/{feature}-{date}. If I just don't care about archieving the branch I can use option to reset `dev` back to `main`
-   [ ] remote on gitlab push `main` and `dev`. but on github just push `main`
-   [ ] Use .git/config (Local/Repo-specific)
-   [ ] change the pre-release format
-   [ ] need to check what type of project before making the versioning. for now just stick with python

---

### 🗑️ Cancelled / Dropped

-   [ ] _(Nothing yet)_

---

## ⚖️ considerations

-   [ ] allow to and stages, commit, and push TODO.md on gitlab but not on github

---

## 💡Ideas

-   [ ] Automatically set template commit-msg.txt based on stages which one is added and modified.
-   [ ] Automatically create and delete commit-msg.txt when needed if we set argument on CLI or by default like that.
-   [ ] Backup before delete the commit-msg.txt
-   [ ] Backup just 3 maxiumum. 3 lastest/newest backup or we can set on CLI. by default 3

---

## 🧾 Notes

### Branch Stratgies

If I have 2 branch
**case 1**: abandon current `dev` branch
solution1: rename and archieving branch. Go back to `main` branch (prefered)
solution2: Reset back `dev` to `main`
**case 2**: finalize and release the code on `dev` branch on `main`
solution1: go back to `main` branch. merge them. tagging and push the `main`. Update the `dev` to start the next experiment cycle. use new version for `dev` and push the `dev`
**case 3**: Let's say there is a scenario I want to just see if the pipline job in gitlab is working let's say I havemore than 5 stages let's say 7 stages on gilab pipline. of course I will commit and push to gitlab. many commit and pushes with many failed pipline jobs. I try after one of commits and push one is success for 7 stages. It kinda messy you know. What should I do. my CHANGELOG.md will become messy with many commits that unused where many failed pipline jobs.
✅ **Solutions**:

1. Use a Temporary Pipeline Test Branch
2. Squash Commits Before Merging into dev or main
3. Use [skip ci] or [ci skip] in Commit Messages like `git commit -m "ci: testing YAML [skip ci]"` or `git commit -m "docs: update README [ci skip]"`
4. Cleanup Before Tagging/Changelog
