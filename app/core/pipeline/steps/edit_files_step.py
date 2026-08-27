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

    @log_step(label="edit-files")
    def execute(self, ctx):
        ctx.engine.edit_release_files()
