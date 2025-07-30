# `TODO.md`

Personal notes, planning, and roadmap for **Custy**

---

## ✨ Feature

### ✅ Completed

-   [x] handle custy Full workflow
-   [x] handle custy "git add ."
-   [x] handle custy generate changelog
-   [x] handle custy as a tool
-   [x] handle custy command and put in makefile
-   [x] Fix issue where added to stage and commit after change version on `.cz.toml` and `app/__version__.py` files
-   [x] Make own feature like/inspired by/like command `cz check`
-   [x] fixing pre-release version format using pep440 for python
-   [x] Use format [Epoch!]MAJOR.MINOR.PATCH[Pre-release][Post-release][Development][+Local] the pep440 for python
-   [x] support Post-release, development, local identifiers, and epoch segment
-   [x] support 'release' on commit type
-   [x] if the current version is pre-release or post or dev and so on. If we want to increment. let's say from rc, next version is rc, the major, minor, and patch won't change. same as from alpha to beta. but not beta to alpha because beta 1 higher level than alpha. for example from v.1.2.3rc1 to v.1.2.3rc2 instead of v.1.2.3rc1 to v.1.2.4rc2; another example from v.1.2.3b1 to v.1.2.3b2 instead of v.1.2.3b1 to v.1.2.4b2;
-   [x] generate changelog when on release version. So check if the version is major.minor.patch. So allowed to generate changelog and push the changelog
-   [x] Check if the commit type not [feat, fix, perf, docs, refactor] don't bump or use tagging. Id use types [feat, fix, perf, docs, refactor] we need to use specific parameter if we want to force bump or tagging; or maybe there are better suggestion.
    -   Option 1: keep/still bumping and tagging but give warning;
    -   Option 2: prevent bumping and tagging;
    -   Option 3: must use additional specific parameter if want to use bumping or tagging;
    -   Option 4: must use additional specific CLI parameter if want to use bumping or tagging;
    -   or other better options
-   [x] need to check what type of project before making the versioning. We already have versioning custom format configuration for python. at least we have python and javascript whether for electron js, react js, next js, and so on
-   [x] when tagging. instead of put message on CLI args. it's better to open files as tagging message same like we already have for commit-msg. If we also specify specific parameter that tells use default tagging message. maybe there are a better solutions
-   [x] for release version, check all pre-lease, develop (and so on that needed) version commit message combine the all the commit body, description (etc that needed) into 1 as template for release version when for example from pre-release to release and put to external txt file (commit-msg.txt)
-   [x] from pre-release or dev, etc to release. No need to change the major.minor.patch. for example from v.1.2.3rc1 to v.1.2.3 instead of v.1.2.3rc1 to v.1.2.4
    -   Option 1. level the tag message be like that (no changes)
    -   Option 2. the tag message based on commit message
    -   Option 3. manually every time commit the tag
    -   Option 4. maybe there are some better and best options and solutions
-   [x] Backup just 10 maxiumum. 10 lastest/newest backup or we can set on CLI. by default 10
-   [x] Fix issue where to put backups, templates folders/directory. also with commit-msg.txt if needed
-   [x] handle cleanup backups CLI
-   [x] Bug fix and Make commit-msg.txt and tag-msg.txt with some automation if possible. Ref: docs\git\commit_message.md
-   [x] Make sure backup and add all of them to stages before commit and push
-   [x] add feature to force commit even no staged changes detected

---

### 🧩 In Progress

-   _(Nothing yet)_

---

### 🧠 Planning

-   [ ] use 2 git remote, gitlab as main, and github as backup
-   [ ] use 2 branch; `main` and `dev`; `main` is stable one and `dev` is more experimental
-   [ ] Update the major, minor, and patch on `main` branch. But on `dev` branch `main`, I just update pre_release and pre_release
-   [ ] If there is a abandoned branch or experminet or deprecated branch version and want to go back to `main` branch. I choose to rename branch use format like archive/{feature}-{date} or experiment/{feature}-{date}. If I just don't care about archieving the branch I can use option to reset `dev` back to `main`
-   [ ] remote on gitlab push `main` and `dev`. but on github just push `main`
-   [ ] Use .git/config (Local/Repo-specific)
-   [ ] if when running custy is failed prevent or handle the backup files that just created
-   [ ] Give template commit message git-msg.txt
-   [ ] on CLI parameters, on --bump, add option `final`. So the bump from v1.4.0rc[n] to -> v1.4.0
-   [ ] bug fixes or improvements, if switch to `release/x/y` or `rc` version tag get all message from `dev` branch like `alpha`, `beta`, `rc`, `dev`, etc
-   [ ] if post release the commit message header initial commit type is `docs` or maybe `<docs>`
-   [ ] make `how to use` documentation. We can use the formal or friendly language style
-   [ ] bug fix when switch from release to post-release use the same version as release but use the post-release format so for example: from 1.5.0 → 1.5.0.post1 instead of from 1.5.0 → 1.6.0.post1

---

### 🗑️ Cancelled / Dropped

-   for version use this format major.minor.patch-pre_release.pre_release_number
-   change the pre-release format

---

## ⚖️ considerations

-   allow to and stages, commit, and push TODO.md on gitlab but not on github

---

## 💡Ideas

-   Automatically set template commit-msg.txt based on stages which one is added and modified.
-   Automatically create and delete commit-msg.txt when needed if we set argument on CLI or by default like that.
-   Backup before delete the commit-msg.txt
-   optionally, we can just see what would the next version by include additional CLI parameters or another ideas or just use --dry-run

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

### Usage

if the commit type not [feat, fix, perf, docs, refactor] the version will not bump. 💡Hint: use --dry-run before run the actual to see what the next version would be
