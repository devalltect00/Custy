# tests/core/pipeline/test_profiles.py

"""
tests/workflow/test_profiles.py

Unit tests for pipeline profiles.
"""

from app.core.pipeline.profiles import (
    PIPELINE_PROFILES,
    STEP_ORDER,
)


class TestPipelineProfiles:

    def test_required_profiles_exist(self):
        expected = {
            "validate",
            "commit",
            "tag",
            "push",
            "dev",
            "release",
            "full",
            "init",
            "apply_version",
            "changelog",
        }

        assert expected.issubset(PIPELINE_PROFILES)

    def test_every_profile_is_non_empty(self):
        for name, profile in PIPELINE_PROFILES.items():
            assert isinstance(profile, list)
            assert len(profile) > 0

    def test_every_step_contains_name(self):
        for profile in PIPELINE_PROFILES.values():
            for step in profile:
                assert "name" in step

    def test_release_contains_expected_steps(self):
        release = PIPELINE_PROFILES["release"]

        names = [step["name"] for step in release]

        assert "prepare_version_step" in names
        assert "workflow_init_step" in names
        assert "commit_step" in names
        assert "tag_step" in names
        assert "push_step" in names

    def test_full_finishes_with_finalize(self):
        full = PIPELINE_PROFILES["full"]

        assert full[-1]["name"] == "finalize_step"

    def test_step_order_unique(self):
        values = list(STEP_ORDER.values())

        assert len(values) == len(set(values))

    def test_step_order_contains_core_steps(self):
        expected = {
            "ensure_git_repo_step",
            "prepare_version_step",
            "commit_step",
            "tag_step",
            "push_step",
            "finalize_step",
        }

        assert expected.issubset(STEP_ORDER.keys())

    def test_step_order_sorted_values(self):
        values = list(STEP_ORDER.values())

        assert values == sorted(values)
