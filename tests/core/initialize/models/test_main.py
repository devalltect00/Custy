# tests/core/initialize/models/test_main.py

"""
tests/core/initialize/test_main.py

Unit tests for the initialization workflow coordinator.

These tests verify that InitMain orchestrates the initialization
workflow correctly by building configuration, generating an execution
plan, running scaffold generation, presenting results, and handling
runtime failures.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.cli.constants.enums import InitMode
from app.core.initialize import main
from app.core.initialize.main import InitMain
from app.core.initialize.models.init_spec import InitSpec
from app.core.initialize.models.initialization_result import (
    InitializationResult,
)


class DummyProgress:
    """Minimal context manager used to replace progress_spinner."""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class TestInitMain:
    """Tests for InitMain."""

    def _build_args(self):
        """Creates a reusable CLI argument object."""

        return SimpleNamespace(
            mode=InitMode.ALL,
            force_init=False,
            ask=False,
            dry_run=False,
            debug=False,
            log_level="INFO",
        )

    def test_execute_runs_initialization_pipeline(
        self,
        monkeypatch,
    ):
        """Runs the complete initialization workflow."""

        args = self._build_args()

        spec = InitSpec(
            name="all",
            templates=["template"],
            dirs=["directory"],
            template_dirs=["examples"],
            messages=["done"],
        )

        result = InitializationResult(
            mode="all",
        )

        builder = MagicMock()
        builder.return_value.build.return_value = spec

        generator = MagicMock()
        generator.return_value.run.return_value = result

        presenter = MagicMock()
        presenter.return_value.render.return_value = "TABLE"

        console_print = MagicMock()

        monkeypatch.setattr(
            main,
            "InitBuilder",
            builder,
        )

        monkeypatch.setattr(
            main,
            "ScaffoldGenerator",
            generator,
        )

        monkeypatch.setattr(
            main,
            "InitializationPresenter",
            presenter,
        )

        monkeypatch.setattr(
            main,
            "progress_spinner",
            lambda *_: DummyProgress(),
        )

        monkeypatch.setattr(
            main.console,
            "print",
            console_print,
        )

        monkeypatch.setattr(
            main,
            "success_summary_panel",
            lambda **_: "SUCCESS",
        )

        monkeypatch.setattr(
            main,
            "perf_counter",
            MagicMock(
                side_effect=[10.0, 12.5],
            ),
        )

        workflow = InitMain()

        workflow.execute(args)

        builder.assert_called_once()

        builder.return_value.build.assert_called_once()

        generator.assert_called_once_with(
            force=False,
            interactive=False,
            dry_run=False,
        )

        generator.return_value.run.assert_called_once_with(
            mode="all",
            templates=spec.templates,
            dirs=spec.dirs,
            template_dirs=spec.template_dirs,
        )

        presenter.return_value.render.assert_called_once_with(
            result,
        )

    def test_execute_prints_success_messages(
        self,
        monkeypatch,
    ):
        """Prints every success message from the specification."""

        args = self._build_args()

        spec = InitSpec(
            name="all",
            templates=[],
            dirs=[],
            template_dirs=None,
            messages=[
                "Message One",
                "Message Two",
            ],
        )

        result = InitializationResult(
            mode="all",
        )

        monkeypatch.setattr(
            main,
            "InitBuilder",
            MagicMock(
                return_value=MagicMock(
                    build=MagicMock(return_value=spec),
                )
            ),
        )

        monkeypatch.setattr(
            main,
            "ScaffoldGenerator",
            MagicMock(
                return_value=MagicMock(
                    run=MagicMock(return_value=result),
                )
            ),
        )

        monkeypatch.setattr(
            main,
            "InitializationPresenter",
            MagicMock(
                return_value=MagicMock(
                    render=MagicMock(return_value="TABLE"),
                )
            ),
        )

        printed = MagicMock()

        monkeypatch.setattr(
            main.console,
            "print",
            printed,
        )

        monkeypatch.setattr(
            main,
            "progress_spinner",
            lambda *_: DummyProgress(),
        )

        monkeypatch.setattr(
            main,
            "success_summary_panel",
            lambda **_: "SUCCESS",
        )

        monkeypatch.setattr(
            main,
            "perf_counter",
            MagicMock(
                side_effect=[0.0, 1.0],
            ),
        )

        InitMain().execute(args)

        output = "".join(str(call) for call in printed.call_args_list)

        assert "Message One" in output
        assert "Message Two" in output

    @pytest.mark.parametrize(
        "mode",
        [
            InitMode.ALL,
            InitMode.ALL_NO_EXAMPLES,
            InitMode.CONFIG,
        ],
    )
    def test_execute_prints_configuration_next_steps(
        self,
        monkeypatch,
        mode,
    ):
        """Config-generating modes explain required project-specific review."""

        args = self._build_args()
        args.mode = mode
        spec = InitSpec(
            name=mode.value,
            templates=[],
            dirs=[],
            template_dirs=None,
            messages=None,
        )

        monkeypatch.setattr(
            main,
            "InitBuilder",
            MagicMock(
                return_value=MagicMock(
                    build=MagicMock(return_value=spec),
                )
            ),
        )
        monkeypatch.setattr(
            main,
            "ScaffoldGenerator",
            MagicMock(
                return_value=MagicMock(
                    run=MagicMock(
                        return_value=InitializationResult(mode=mode.value),
                    ),
                )
            ),
        )
        monkeypatch.setattr(
            main,
            "InitializationPresenter",
            MagicMock(
                return_value=MagicMock(
                    render=MagicMock(return_value="TABLE"),
                )
            ),
        )
        printed = MagicMock()
        monkeypatch.setattr(main.console, "print", printed)
        monkeypatch.setattr(
            main,
            "progress_spinner",
            lambda *_: DummyProgress(),
        )
        monkeypatch.setattr(
            main,
            "success_summary_panel",
            lambda **_: "SUCCESS",
        )
        monkeypatch.setattr(
            main,
            "perf_counter",
            MagicMock(side_effect=[0.0, 1.0]),
        )

        InitMain().execute(args)

        output = "".join(str(call) for call in printed.call_args_list)

        assert ".config/custy/config.toml" in output
        assert "tool.custy.changelog.links.repository" in output
        assert "default_remote" in output
        assert "main_remotes" in output
        assert "backup_remotes" in output
        assert "git remote -v" in output
        assert "custy validate" in output

    def test_execute_passes_dry_run_to_scaffold_generator(
        self,
        monkeypatch,
    ):
        """Initialization preview state reaches the filesystem service."""

        args = self._build_args()
        args.dry_run = True
        spec = InitSpec(
            name="all",
            templates=[],
            dirs=[],
            template_dirs=None,
            messages=None,
        )
        generator = MagicMock()
        generator.return_value.run.return_value = InitializationResult(
            mode="all",
            dry_run=True,
        )

        monkeypatch.setattr(
            main,
            "InitBuilder",
            MagicMock(
                return_value=MagicMock(
                    build=MagicMock(return_value=spec),
                )
            ),
        )
        monkeypatch.setattr(main, "ScaffoldGenerator", generator)
        monkeypatch.setattr(
            main,
            "InitializationPresenter",
            MagicMock(
                return_value=MagicMock(
                    render=MagicMock(return_value="TABLE"),
                )
            ),
        )
        monkeypatch.setattr(main.console, "print", MagicMock())
        monkeypatch.setattr(
            main,
            "progress_spinner",
            lambda *_: DummyProgress(),
        )
        monkeypatch.setattr(
            main,
            "success_summary_panel",
            lambda **_: "SUCCESS",
        )
        monkeypatch.setattr(
            main,
            "perf_counter",
            MagicMock(side_effect=[0.0, 1.0]),
        )

        InitMain().execute(args)

        generator.assert_called_once_with(
            force=False,
            interactive=False,
            dry_run=True,
        )

    def test_execute_handles_empty_messages(
        self,
        monkeypatch,
    ):
        """Succeeds when no success messages are defined."""

        args = self._build_args()

        spec = InitSpec(
            name="all",
            templates=[],
            dirs=[],
            template_dirs=None,
            messages=None,
        )

        monkeypatch.setattr(
            main,
            "InitBuilder",
            MagicMock(
                return_value=MagicMock(
                    build=MagicMock(return_value=spec),
                )
            ),
        )

        monkeypatch.setattr(
            main,
            "ScaffoldGenerator",
            MagicMock(
                return_value=MagicMock(
                    run=MagicMock(
                        return_value=InitializationResult(
                            mode="all",
                        )
                    ),
                )
            ),
        )

        monkeypatch.setattr(
            main,
            "InitializationPresenter",
            MagicMock(
                return_value=MagicMock(
                    render=MagicMock(return_value="TABLE"),
                )
            ),
        )

        monkeypatch.setattr(
            main.console,
            "print",
            MagicMock(),
        )

        monkeypatch.setattr(
            main,
            "progress_spinner",
            lambda *_: DummyProgress(),
        )

        monkeypatch.setattr(
            main,
            "success_summary_panel",
            lambda **_: "SUCCESS",
        )

        monkeypatch.setattr(
            main,
            "perf_counter",
            MagicMock(
                side_effect=[0.0, 1.0],
            ),
        )

        InitMain().execute(args)

    @pytest.mark.parametrize(
        "exception",
        [
            RuntimeError("boom"),
            ValueError("invalid"),
        ],
    )
    def test_execute_propagates_errors_to_cli_boundary(
        self,
        monkeypatch,
        exception,
    ):
        """Propagates initialization failures for centralized presentation."""

        monkeypatch.setattr(
            main,
            "progress_spinner",
            lambda *_: DummyProgress(),
        )

        monkeypatch.setattr(
            main,
            "InitBuilder",
            MagicMock(
                side_effect=exception,
            ),
        )

        with pytest.raises(type(exception)):
            InitMain().execute(
                self._build_args(),
            )

    def test_execute_passes_elapsed_time_to_summary_panel(
        self,
        monkeypatch,
    ):
        """Passes the elapsed execution time to the success summary."""

        args = self._build_args()

        spec = InitSpec(
            name="all",
            templates=[],
            dirs=[],
            template_dirs=None,
            messages=None,
        )

        monkeypatch.setattr(
            main,
            "InitBuilder",
            MagicMock(
                return_value=MagicMock(
                    build=MagicMock(return_value=spec),
                )
            ),
        )

        monkeypatch.setattr(
            main,
            "ScaffoldGenerator",
            MagicMock(
                return_value=MagicMock(
                    run=MagicMock(
                        return_value=InitializationResult(
                            mode="all",
                        )
                    ),
                )
            ),
        )

        monkeypatch.setattr(
            main,
            "InitializationPresenter",
            MagicMock(
                return_value=MagicMock(
                    render=MagicMock(return_value="TABLE"),
                )
            ),
        )

        monkeypatch.setattr(
            main.console,
            "print",
            MagicMock(),
        )

        monkeypatch.setattr(
            main,
            "progress_spinner",
            lambda *_: DummyProgress(),
        )

        panel = MagicMock(
            return_value="SUCCESS",
        )

        monkeypatch.setattr(
            main,
            "success_summary_panel",
            panel,
        )

        monkeypatch.setattr(
            main,
            "perf_counter",
            MagicMock(
                side_effect=[100.0, 103.75],
            ),
        )

        InitMain().execute(args)

        _, kwargs = panel.call_args

        assert kwargs["elapsed_time"] == 3.75
