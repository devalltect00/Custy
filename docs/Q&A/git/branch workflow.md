# Questions

```text
Now I'm in v1.4.0a1 with git tag on branch main. Now I want to move to beta version with branch dev. when ready go to rc version and release version

I'm using these Git Branching Strategy & Workflow Lifecycle Summary
=====
## 🌿 Git Branching Strategy

| Branch         | Purpose                                   | Keep Permanent? | Tag Version Examples      |
| -------------- | ----------------------------------------- | --------------- | ------------------------- |
| main         | Production/stable releases                | ✅ Yes          | 1.2.0, 1.2.1, 2.0.0 |
| develop      | Development and pre-releases              | ✅ Yes          | 1.3.0a1, 1.3.0.dev2   |
| release/x.y  | Prepare for release and RCs               | ❌ No           | 1.3.0rc1, 1.3.0       |
| hotfix/x.y.z | Patch urgent production issues            | ❌ No           | 1.3.0.post1             |
| feature/*    | Isolated feature development              | ❌ No           | Not tagged directly       |
| ci/*         | Pipeline and CI/CD job testing            | ❌ No           | Not tagged                |
| sandbox/*    | Debug, experimental or throwaway branches | ❌ No           | Not tagged                |

---

## 🔁 Workflow Lifecycle Summary

1. Work on develop using dev, a, or b versions
2. Create release/x.y to prep release, tag rc versions
3. Merge release/x.y to main and tag stable release (e.g., v1.3.0)
4. Create hotfix/x.y.z if production bug is found after release
5. Test pipelines on ci/test-* branch
6. All other branches (release, hotfix, feature, ci) are deleted after merge
=====

Give step by step to do that
```

# Answers

## ✅ CASE 1: Start Dev, Alpha, Beta Development on `develop`

1. Checkout develop branch (or create if missing):

```bash
git checkout develop
git pull origin develop  # optional if already exists remotely
```

2. Bump version to Dev, Alpha, Beta (e.g., vx.y.zbn):

Assuming I have a script/CLI tool that supports version bump with pre-release flag.

```bash
python -m app all --bump patch templates/commit-msg.txt --pre-release beta
# This should generate vx.y.zbn, preserving x.y.z base
```

3. **Develop and commit** as usual in develop:

```bash
git add .
git commit -m ""
git tag -a vx.y.zbn -m ""
git push --follow-tags origin develop
```

## ✅ CASE 2: Move to RC with release/x.y

Once I'm confident the alpha/beta/dev features are stable:

1. Create release branch:

```bash
git checkout -b release/x.y
```

2. Bump to RC version:

```bash
python -m app all --bump patch templates/commit-msg.txt --pre-release rc
# This should produce vx.y.zrcn
```

3. Test, fix minor things, tag RCs:

```bash
git add .
git commit -m ""
git tag -a vx.y.zrcn -m ""
git push --follow-tags origin release/x.y
```

Repeat RCs (e.g., vx.y.zrc2) as needed.

## ✅ CASE 3: Final Release on main

When I'm ready to release to production:

1. Merge release/x.y → main:

```bash
git checkout main
git pull origin main
git merge release/x.y
```

2. Bump to stable release:

```bash
python -m app all --bump final templates/commit-msg.txt
# Should result in vx.y.z
```

3. Push and tag:

```bash
git tag -a v1.4.0 -m "🚀 Stable Release vx.y.z"
git push --follow-tags origin main
```

## ✅ CASE 4: Cleanup

1. Delete release branch (optional, by strategy):

```bash
git branch -d release/x.y
git push origin --delete release/x.y
```

2. Start next cycle on develop, e.g., v1.5.0.dev1:

```bash
git checkout develop
python -m app all --bump minor templates/commit-msg.txt --pre-release dev
git push --follow-tags origin develop
```

## ✅ CASE 5: Use the hotfix/x.y.z branch

According to my branching strategy:

Branch Purpose Example
hotfix/x.y.z For patching production issues hotfix/1.4.0

This branch forks from main, not release/x.y.

🪄 Step-by-Step: Create a Post-release
Assume:

Last final release is v1.4.0

I'm fixing a bug to create v1.4.0.post1

✅ 1. Checkout main

```bash
git checkout main
git pull origin main
```

✅ 2. Create hotfix branch

```bash
git checkout -b hotfix/1.4.0
```

✅ 3. Fix the bug or doc or anything

```
# Edit file(s)
git add .
git commit -m "fix(ui): resolve production bug in login form"
```

✅ 4. Bump to post-release
Use my versioning tool (I'm using PEP 440):

```bash
python -m app all --bump patch templates/commit-msg.txt --post-release
# Should generate version: 1.4.0.post1
```

If I want to skip bumping patch and just append .post1, use a custom flag if supported (or override manually).

✅ 5. Push and tag

```bash
git push --follow-tags origin hotfix/1.4.0
```

✅ 6. Merge to main
After testing and review:

```bash
git checkout main
git merge hotfix/1.4.0
git push origin main
```

✅ 7. Delete hotfix branch

```bash
git branch -d hotfix/1.4.0
git push origin --delete hotfix/1.4.0
```

## ✅ CASE 6: feature/\* – Isolated Feature Development

This is where I work on a single, focused unit of functionality (feature, improvement, etc.) without affecting the main flow.

🔁 Lifecycle for feature/\*
Step-by-step:

1. ✅ Start from develop

```
git checkout develop
git pull origin develop
git checkout -b feature/new-login-page
```

Always branch off from develop, not main.

2. 💻 Work on your feature
   Make changes, commit, test.

```
git add .
git commit -m "feat(auth): add new login UI with validation"
```

3. ✅ Rebase regularly to avoid conflicts

```
git fetch origin
git rebase origin/develop
```

4. 🧪 Push to remote for review or CI/CD

```
git push origin feature/new-login-page
```

5. 🔀 Merge to develop when done
   After review (or MR/PR approved):

```
git checkout develop
git merge feature/new-login-page
git push origin develop
```

6. 🧹 Delete the branch

```
git branch -d feature/new-login-page
git push origin --delete feature/new-login-page
```

## ✅ CASE 7: ci/\* – Pipeline and CI/CD Job Testing

This branch is not for features or releases, but specifically for testing GitLab/GitHub Actions/CI pipelines.

🔁 Lifecycle for ci/\*
Step-by-step:

1. ✅ Create the test branch (usually from develop or main)

```bash
git checkout -b ci/test-auto-versioning
```

2. ⚙️ Make your CI/CD pipeline/test config changes

-   .gitlab-ci.yml
-   .github/workflows/test.yml

3. ✅ Commit

```bash
git add .github/workflows/test.yml
git commit -m "ci: test automatic changelog generation"
```

4. 🚀 Push to trigger pipeline

```bash
git push origin ci/test-auto-versioning
```

5. 🧪 Observe pipeline results

-   Fix errors.
-   Repeat push.

6. 🔀 If successful, merge into develop or main

```bash
git checkout develop
git merge ci/test-auto-versioning
git push origin develop
```

7. 🧹 Delete CI branch

```bash
git branch -d ci/test-auto-versioning
git push origin --delete ci/test-auto-versioning
```

CASE 8: Add archive/ prefix cleanup
For deprecated feature branches

Based on 8 case:
CASE 1: Start Dev, Alpha, Beta Development on develop
CASE 2: Move to RC with release/x.y
CASE 3: Final Release on main
CASE 4: Cleanup
CASE 5: Use the hotfix/x.y.z branch
CASE 6: feature/\* – Isolated Feature Development
CASE 7: ci/\* – Pipeline and CI/CD Job Testing
CASE 8: Add archive/ prefix cleanup

Case 1, used when (`release` version with `main` branch) switch into (`Dev`, `Alpha`, `Beta` version with `develop` branch)
Case 2, used when (`Dev`, `Alpha`, `Beta` version with `develop` branch) switch into (`rc` version with `release/x.y` branch)
Case 3, used when (`rc` version with `release/x.y` branch) switch into (`release` version with `main` branch)
Case 4, used when (`release` version with `main` branch) switch into (`Dev`, `Alpha`, `Beta` version with `develop` branch)
Case 5 used when (`release` version with `main` branch) switch into (`post` version with `hotfix/x.y.z` branch) and switch back into (`release` version with `main` branch)
etc...
