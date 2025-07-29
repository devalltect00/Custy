# Sort tag based create date

```bash
git tag --sort=-creatordate
```

## output like:

```bash
1.3.3
1.3.2
1.3.1rc2
1.3.0rc1
v1.2.0
v1.1.5
v1.1.4
v1.1.3
v1.1.2
v0.0.1
```

# get all commit message for specific version

```bash
git log 1.3.1rc2..HEAD --pretty=format:%H%n%B%n---END---
```

example: git log 1.3.1rc2..HEAD --pretty=format:%H%n%B%n---END---#
output like:

```bash
b9841b2139269d2c39f72995e2215efe752d4409
docs(changelog): update changelog

---END---
7f3cd6a30ba490ea73fab47548abadbe8901bf25
docs(TODO.md): add or change todo

-   add or change todo

Changelog: handled separately

---END---
0e6e37864143a74c645a70f35cc507702d1b3034
docs(changelog): update changelog

---END---
03fcda08983d826388749eb6a341726dcdde5415
docs(TODO.md): add or change todo

-   add or change todo

Changelog: handled separately

---END---
5a2b9e5cfd23dcc0554f97d934370cdb5bb8c723
docs(changelog): update changelog

# ---END---
```

# show git log (oneline, graph):

```bash
git log --oneline --graph
```

## output like:

```bash
-   b9841b2 (HEAD -> main, origin/main) docs(changelog): update changelog
-   7f3cd6a (tag: 1.3.3) docs(TODO.md): add or change todo
-   0e6e378 docs(changelog): update changelog
-   03fcda0 (tag: 1.3.2) docs(TODO.md): add or change todo
-   5a2b9e5 docs(changelog): update changelog
-   0478049 (tag: 1.3.1rc2) chore(commit_msg): support 'release' as valid Conventional Commit type
-   26b3017 docs(changelog): update changelog
-   80e4d6b (tag: 1.3.0rc1) feat(versioning): Improve pre-release and full versioning support with PEP 440
-   23ac55e docs(changelog): update changelog
-   7b27356 (tag: v1.2.0) feat(git_commit_tagger): replace cz check with custom commit message checker
-   fdd7534 docs(changelog): update changelog
-   edd1e79 (tag: v1.1.5) fix(git_commit_tagger): add or change todo
-   dc737c5 docs(changelog): update changelog
-   4af9299 (tag: v1.1.4) docs(TODO.md): add or change todo
-   # c50c313 docs(changelog): update changelog
```

# show git tag log:

```bash
git log --no-walk --tags --pretty="format:%h %d %s"
```

## output like:

```bash
7f3cd6a (tag: 1.3.3) docs(TODO.md): add or change todo
03fcda0 (tag: 1.3.2) docs(TODO.md): add or change todo
0478049 (tag: 1.3.1rc2) chore(commit_msg): support 'release' as valid Conventional Commit type
80e4d6b (tag: 1.3.0rc1) feat(versioning): Improve pre-release and full versioning support with PEP 440
7b27356 (tag: v1.2.0) feat(git_commit_tagger): replace cz check with custom commit message checker
edd1e79 (tag: v1.1.5) fix(git_commit_tagger): add or change todo
4af9299 (tag: v1.1.4) docs(TODO.md): add or change todo
de4c3bb (tag: v1.1.3) fix(Makefile): correct commands
f054462 (tag: v1.1.2) chore(release): manually fix and update version to v1.1.2
9ef7b1f (tag: v0.0.1) fix(Makefile): correct commands and update documentation
```
