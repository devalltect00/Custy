# tests/cli/commands/validate/test_command_validate.py

"""
tests/cli/commands/validate/test_command.py

Tests for the validate command execution flow.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

from app.cli.commands.validate import command


class DummyAppContext:
    def __init__(self):
        self.dry_run = True
        self.debug = False
        self.log_level = "info"


class TestValidateCommand:
    def test_validate_executes_pipeline(self, monkeypatch):
        cfg = MagicMock()
        args = MagicMock()

        get_config = MagicMock(return_value=cfg)
        get_context = MagicMock(return_value=DummyAppContext())
        resolve = MagicMock(return_value=args)

        register = MagicMock()

        resolver_instance = MagicMock()
        resolver_instance.resolve.return_value = ["validate"]

        resolver_cls = MagicMock(return_value=resolver_instance)

        engine_builder = MagicMock()
        engine_builder.from_cli_args.return_value = engine_builder
        engine_builder.build.return_value = MagicMock()

        engine_cls = MagicMock(return_value=engine_builder)

        pipeline = MagicMock()
        pipeline_builder = MagicMock()
        pipeline_builder.build.return_value = pipeline
        pipeline_cls = MagicMock(return_value=pipeline_builder)

        monkeypatch.setattr(command, "get_config", get_config)
        monkeypatch.setattr(command, "get_context", get_context)
        monkeypatch.setattr(command, "resolve_validate_args", resolve)
        monkeypatch.setattr(command, "register_all_steps", register)
        monkeypatch.setattr(command, "CommandResolver", resolver_cls)
        monkeypatch.setattr(command, "WorkflowEngineBuilder", engine_cls)
        monkeypatch.setattr(command, "PipelineBuilder", pipeline_cls)

        command.validate(
            ctx=MagicMock(),
            commit_message_file=None,
            tag_message_file=None,
            version_file=None,
            auto_stage=None,
            stage_mode=None,
            check_cz=None,
        )

        get_config.assert_called_once()
        get_context.assert_called_once()
        resolve.assert_called_once()
        register.assert_called_once()
        resolver_instance.resolve.assert_called_once_with(["validate"])
        engine_builder.from_cli_args.assert_called_once()
        pipeline_builder.build.assert_called_once_with(["validate"])
        pipeline.run.assert_called_once()

    def test_combined_args_contains_global_flags(self, monkeypatch):
        app_ctx = DummyAppContext()
        monkeypatch.setattr(command, "get_context", MagicMock(return_value=app_ctx))
        monkeypatch.setattr(command, "get_config", MagicMock(return_value=MagicMock()))
        monkeypatch.setattr(
            command, "resolve_validate_args", MagicMock(return_value=SimpleNamespace())
        )
        monkeypatch.setattr(command, "register_all_steps", MagicMock())

        resolver = MagicMock()
        resolver.resolve.return_value = []
        monkeypatch.setattr(
            command, "CommandResolver", MagicMock(return_value=resolver)
        )

        wb = MagicMock()
        wb.from_cli_args.return_value = wb
        wb.build.return_value = MagicMock()
        monkeypatch.setattr(
            command, "WorkflowEngineBuilder", MagicMock(return_value=wb)
        )

        pb = MagicMock()
        pb.build.return_value = MagicMock(run=MagicMock())
        monkeypatch.setattr(command, "PipelineBuilder", MagicMock(return_value=pb))

        command.validate(MagicMock())

        passed = wb.from_cli_args.call_args.args[0]
        assert passed.dry_run is True
        assert passed.debug is False
        assert passed.log_level == "info"
