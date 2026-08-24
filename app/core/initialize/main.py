# app/core/initialize/main.py

"""
Initialization workflow entry point.

Responsibilities
----------------

- Build initialization configuration
- Build initialization plan
- Execute scaffold generation
- Display progress information
- Display execution summaries
- Handle runtime errors
"""

from time import perf_counter

from app.core.initialize.builder.init_builder import (
    InitBuilder,
)
from app.core.initialize.models.init_config import (
    InitConfig,
)
from app.core.initialize.presenters.initialization_presenter import (
    InitializationPresenter,
)
from app.core.initialize.services.scaffold_generator import (
    ScaffoldGenerator,
)
from app.ui.console import console
from app.ui.exceptions import show_error
from app.ui.panels import success_summary_panel
from app.ui.progress import progress_spinner
from app.cli.constants import (
  InitMode,
)

class InitMain:
    """
    Initialization workflow coordinator.
    """

    def execute(
        self,
        args,
    ) -> None:
        """
        Execute initialization workflow.

        Parameters
        ----------
        args:
            Resolved initialization arguments.
        """

        start_time = perf_counter()

        try:
            # =====================================================
            # 1. Build configuration
            # =====================================================

            with progress_spinner("Preparing configuration"):
                config = InitConfig(
                    mode=args.mode,
                    force_init=args.force_init,
                    ask=args.ask,
                    dry_run=args.dry_run,
                    no_debug=not args.debug,
                    log_level=args.log_level,
                )

            # =====================================================
            # 2. Build execution plan
            # =====================================================
            with progress_spinner("Building initialization plan"):
                spec = InitBuilder(
                    config,
                ).build()

            # =====================================================
            # 3. Execute initialization
            # =====================================================
            with progress_spinner("Initializing project"):
                generator = ScaffoldGenerator(
                    force=config.force_init,
                    interactive=config.ask,
                    dry_run=config.dry_run,
                )

                console.print("\n")

                result = generator.run(
                    mode=config.mode.value,
                    templates=spec.templates,
                    dirs=spec.dirs,
                    template_dirs=spec.template_dirs,
                )

            console.print()

            # =====================================================
            # 4. Summary Table
            # =====================================================
            console.print(InitializationPresenter().render(result))

            console.print()

            # =====================================================
            # 5. Messages
            # =====================================================
            if config.dry_run:
                console.print(
                    "[dry_run](dry-run)[/dry_run] "
                    "No initialization files or directories were changed."
                )
            elif spec.messages:
                for message in spec.messages:
                    console.print(f"[green]{message}[/green]")

            # =====================================================
            # 6. Success
            # =====================================================
            elapsed_time = perf_counter() - start_time

            console.print()

            console.print(
                success_summary_panel(
                    message=(
                        "[bold green]✅ "
                        + (
                            "Initialization preview completed."
                            if config.dry_run
                            else "Initialization completed successfully."
                        )
                        + "[/bold green]\n\n"
                        f"[dim]Mode: {config.mode.value}[/dim]"
                    ),
                    elapsed_time=elapsed_time,
                )
            )

            console.print("\n[bold yellow]💡 Next Steps[/bold yellow]")

            if config.dry_run:
                console.print("  [cyan]custy init[/cyan]")
            else:
                console.print("  [cyan]custy commit[/cyan]")

        except Exception as exc:
            show_error(f"Initialization failed.\n\n{exc}")

            raise
