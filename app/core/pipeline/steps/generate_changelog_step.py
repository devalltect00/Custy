# app/core/pipeline/steps/generate_changelog_step.py

from .base_step import BaseStep
from app.core.pipeline.decorators.log_step import log_step


class GenerateChangelogStep(BaseStep):
    """
    Step 7.2: Generate Changelog

    Generates project changelog based on commits and versioning strategy.

    Responsibilities:
    - Collect commits (via Git / Commitizen)
    - Group commits (feat, fix, etc.)
    - Build structured changelog content
    - Write/update CHANGELOG.md

    This step is separated from version application to:
    - Improve modularity
    - Allow flexible workflow composition
    - Support optional changelog generation

    Typically executed after:
    - version is resolved
    - commit messages are validated

    Prepares release documentation before commit/tag.
    """

    @log_step(label="generate-changelog")
    def execute(self, ctx):
        ctx.engine.generate_changelog_if_needed()
