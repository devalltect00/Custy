# tests/constants/test_git_workflow_rules.py

"""
tests/constants/test_git_workflow_rules.py

Unit tests for Git workflow rule constants.
"""

from app.constants.git_workflow_rules import (
    ALLOWED_COMMIT_TYPES,
    NON_CRITICAL_BRANCHES,
)


class TestGitWorkflowRules:

    def test_allowed_commit_types_contains_expected_values(self):
        expected = {
            "feat",
            "fix",
            "docs",
            "style",
            "refactor",
            "perf",
            "test",
            "chore",
            "ci",
            "build",
            "release",
        }

        assert expected.issubset(ALLOWED_COMMIT_TYPES)

    def test_allowed_commit_types_unique(self):
        assert len(ALLOWED_COMMIT_TYPES) == len(set(ALLOWED_COMMIT_TYPES))

    def test_non_critical_branches(self):
        assert NON_CRITICAL_BRANCHES == (
            "feature/",
            "ci/",
            "sandbox/",
        )

    def test_branch_prefixes_end_with_slash(self):
        for prefix in NON_CRITICAL_BRANCHES:
            assert prefix.endswith("/")

    def test_commit_types_are_strings(self):
        assert all(isinstance(item, str) for item in ALLOWED_COMMIT_TYPES)
