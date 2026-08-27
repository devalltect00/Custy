# tests/cli/commands/workflow/test_command_workflow.py

"""
tests/cli/commands/workflow/test_command.py

Tests for the workflow branch command execution flow.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

from app.cli.commands.workflow import command


class DummyAppContext:
    def __init__(self):
        self.dry_run = False
        self.debug = False
        self.log_level = "info"

    def update_from_args(self, args, debug_flag=None):
        self.updated_args = args
        self.updated_debug = debug_flag


class TestWorkflowCommand:
    def test_branch_executes_pipeline(self, monkeypatch):
        cfg = MagicMock()
        app_ctx = DummyAppContext()
        resolved_args = SimpleNamespace()

        monkeypatch.setattr(command, "get_config", MagicMock(return_value=cfg))
        monkeypatch.setattr(command, "get_context", MagicMock(return_value=app_ctx))
        monkeypatch.setattr(
            command,
            "resolve_workflow_args",
            MagicMock(return_value=resolved_args),
        )
        monkeypatch.setattr(command, "register_all_steps", MagicMock())

        engine_builder = MagicMock()
        engine_builder.from_cli_args.return_value = engine_builder
        engine_builder.build.return_value = MagicMock()
        monkeypatch.setattr(
            command,
            "WorkflowEngineBuilder",
            MagicMock(return_value=engine_builder),
        )

        git_context = MagicMock()
        monkeypatch.setattr(
            command,
            "GitContext",
            MagicMock(return_value=git_context),
        )

        pipeline = MagicMock()
        pipeline_builder = MagicMock()
        pipeline_builder.build.return_value = pipeline
        monkeypatch.setattr(
            command,
            "PipelineBuilder",
            MagicMock(return_value=pipeline_builder),
        )

        command.branch(ctx=MagicMock())

        assert app_ctx.updated_args is resolved_args
        engine_builder.from_cli_args.assert_called_once_with(app_ctx)
        pipeline_builder.build.assert_called_once_with([{"name": "finalize"}])
        pipeline.run.assert_called_once_with(git_context)

    def test_debug_flag_forwarded_to_context(self, monkeypatch):
        app_ctx = DummyAppContext()

        monkeypatch.setattr(command, "get_config", MagicMock(return_value=MagicMock()))
        monkeypatch.setattr(command, "get_context", MagicMock(return_value=app_ctx))
        monkeypatch.setattr(
            command,
            "resolve_workflow_args",
            MagicMock(return_value=SimpleNamespace()),
        )
        monkeypatch.setattr(command, "register_all_steps", MagicMock())

        builder = MagicMock()
        builder.from_cli_args.return_value = builder
        builder.build.return_value = MagicMock()

        monkeypatch.setattr(
            command,
            "WorkflowEngineBuilder",
            MagicMock(return_value=builder),
        )
        monkeypatch.setattr(command, "GitContext", MagicMock())

        pipeline = MagicMock(run=MagicMock())
        pb = MagicMock()
        pb.build.return_value = pipeline
        monkeypatch.setattr(command, "PipelineBuilder", MagicMock(return_value=pb))

        command.branch(ctx=MagicMock(), debug=True)

        assert app_ctx.updated_debug is True
