# app/core/pipeline/steps/edit_files_step.py

from app.core.pipeline.decorators.log_step import log_step

from .base_step import BaseStep


class EditFilesStep(BaseStep):
    """
    Step 5: Edit Release Files

    Opens editor for user to modify:
    - commit message
    - tag message

    Blocking step until user finishes editing.
    """

    requires_exclusive_terminal: bool = True

    def __init__(self, *, include_tag: bool = True) -> None:
        """Configure whether the tag-message editor participates in this step.

        Args:
            include_tag: Open the tag-message file after the commit-message file.
                Development-only commit workflows disable this behavior.
        """

        self.include_tag = include_tag

    @log_step(label="edit-files")
    def execute(self, ctx):
        ctx.engine.edit_release_files(include_tag=self.include_tag)
