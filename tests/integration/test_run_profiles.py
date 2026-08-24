# tests/integration/test_run_profiles.py

"""
tests/integration/test_run_profiles.py

Integration tests for profile resolution and pipeline execution.
"""

from unittest.mock import MagicMock

from app.core.pipeline.command_resolver import CommandResolver
from app.core.pipeline.builder import PipelineBuilder


class TestRunProfiles:
    """
    Integration tests for pipeline profiles.
    """

    def test_validate_profile(self):
        ctx = MagicMock()

        resolver = CommandResolver()
        builder = PipelineBuilder(isVisible=False)

        pipeline = builder.build(
            resolver.resolve(["validate"])
        )

        pipeline.run(ctx)

        ctx.engine.ensure_git_repo.assert_called_once()
        ctx.engine.ensure_remote_exists.assert_called_once()
        ctx.engine.ensure_version_file.assert_called_once()

    def test_release_profile(self):
        ctx = MagicMock()

        resolver = CommandResolver()
        builder = PipelineBuilder(isVisible=False)

        pipeline = builder.build(
            resolver.resolve(["release"])
        )

        pipeline.run(ctx)

        ctx.engine.prepare_version_tag.assert_called_once()
        ctx.engine.execute_commit_phase.assert_called_once()
        ctx.engine.create_tag.assert_called_once()
        ctx.engine.push_changes.assert_called_once()

    def test_dev_profile(self):
        ctx = MagicMock()

        resolver = CommandResolver()
        builder = PipelineBuilder(isVisible=False)

        pipeline = builder.build(
            resolver.resolve(["dev"])
        )

        pipeline.run(ctx)

        ctx.engine.execute_commit_phase.assert_called_once()

    def test_multiple_profiles(self):
        ctx = MagicMock()

        resolver = CommandResolver()
        builder = PipelineBuilder(isVisible=False)

        pipeline = builder.build(
            resolver.resolve(
                [
                    "validate",
                    "release",
                ]
            )
        )

        pipeline.run(ctx)

        ctx.engine.ensure_git_repo.assert_called_once()
        ctx.engine.prepare_version_tag.assert_called_once()
        ctx.engine.execute_commit_phase.assert_called_once()

    def test_profile_without_duplicates(self):
        resolver = CommandResolver()

        steps = resolver.resolve(
            [
                "validate",
                "release",
            ]
        )

        names = [step["name"] for step in steps]

        assert len(names) == len(set(names))
