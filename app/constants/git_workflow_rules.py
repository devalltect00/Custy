# app/constants/git_workflow_rules.py

ALLOWED_COMMIT_TYPES = {
    "feat", "fix", "docs", "style", "refactor",
    "perf", "test", "chore", "ci", "build", "release",
}

NON_CRITICAL_BRANCHES = ("feature/", "ci/", "sandbox/")
