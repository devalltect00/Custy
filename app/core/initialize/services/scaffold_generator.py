# app/core/initialize/services/scaffold_generator.py

"""
Project scaffold generation.

Responsibilities
----------------

- Create directories
- Generate template files
- Copy template directories
- Track execution statistics
- Return structured execution results

This module intentionally contains no presentation logic.
UI rendering is handled by presenters.
"""

from importlib.resources import files
from importlib.resources.abc import Traversable
from pathlib import Path

from app.constants.path import (
    THIS_PROJECT_SOURCE,
)
from app.core.initialize.models.initialization_result import (
    InitializationResult,
)
from app.ui.console import console


class ScaffoldGenerator:
    """
    Execute project initialization.

    Creates files and directories according to the
    initialization specification.
    """

    def __init__(
        self,
        *,
        force: bool = False,
        interactive: bool = False,
        dry_run: bool = False,
    ) -> None:
        """Initialize scaffold generation behavior.

        Args:
            force:
                Allow existing targets to be overwritten.

            interactive:
                Ask before overwriting existing targets.

            dry_run:
                Report planned filesystem changes without applying them.
        """

        self.force = force
        self.interactive = interactive
        self.dry_run = dry_run

        self.created_files = 0
        self.copied_files = 0
        self.skipped_files = 0
        self.created_directories = 0

    def _showed_skip(
        self,
        path: Path,
        reason: str,
    ) -> None:
        console.print(
            f"[yellow]Skipped[/yellow] "
            f"[cyan]{path}[/cyan] "
            f"[dim]({reason})[/dim]"
        )

    def create_directories(
        self,
        directories: list[str],
    ) -> None:
        """
        Create directories.
        """

        for directory in directories:
            path = Path(directory)

            if path.exists():
                continue

            if self.dry_run:
                console.print(f"[dry_run](dry-run)[/dry_run] Would create {path}")
            else:
                path.mkdir(
                    parents=True,
                    exist_ok=True,
                )

            self.created_directories += 1

    def should_write(
        self,
        path: Path,
    ) -> bool:
        """
        Determine whether a file should be written.
        """

        if not path.exists():
            return True

        if self.force:
            return True

        if self.interactive:
            if self.dry_run:
                return False

            answer = input(f"{path} exists. Overwrite? (y/N): ")

            return answer.lower() == "y"

        return False

    def write_file(
        self,
        template,
    ) -> None:
        """
        Generate a template file.
        """

        path = Path(template.target_path)

        if not self.should_write(path):
            self.skipped_files += 1

            self._showed_skip(
                path,
                "already exists",
            )

            return

        content = template.render()

        if self.dry_run:
            action = "overwrite" if path.exists() else "create"
            console.print(
                "[dry_run](dry-run)[/dry_run] "
                f"Would {action} {path}"
            )
            self.created_files += 1
            return

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            content,
            encoding="utf-8",
        )

        self.created_files += 1

        console.print(f"[green]Created[/green] {path}")

    def copy_package_dir(
        self,
        package_path: str,
        target_path: str,
        *,
        force: bool = False,
    ) -> None:
        """Copy a packaged template directory into a project.

        Existing destination directories are merged with the packaged
        resources. Existing files are preserved unless force is enabled,
        while missing files and nested directories are always copied.

        Args:
            package_path:
                Directory path relative to app.templates.

            target_path:
                Project directory that receives the packaged resources.

            force:
                Overwrite existing files when enabled.
        """

        src_root = files(f"{THIS_PROJECT_SOURCE}.templates").joinpath(package_path)

        dst_root = Path(target_path)

        self._copy_package_tree(
            src_root,
            dst_root,
            force=force,
        )

    def _copy_package_tree(
        self,
        source: Traversable,
        destination: Path,
        *,
        force: bool,
    ) -> None:
        """Recursively copy package resources using the Traversable API.

        importlib.resources may expose resources from a filesystem, archive,
        or another package loader. Recursing with iterdir keeps initialization
        compatible with each supported resource backend.

        Args:
            source:
                Traversable packaged directory to copy.

            destination:
                Filesystem directory that receives the current resource tree.

            force:
                Overwrite existing files when enabled.
        """

        for item in source.iterdir():
            target = destination / item.name

            if item.is_dir():
                if not self.dry_run:
                    target.mkdir(
                        parents=True,
                        exist_ok=True,
                    )

                self._copy_package_tree(
                    item,
                    target,
                    force=force,
                )

                continue

            if target.exists() and not force:
                self.skipped_files += 1

                self._showed_skip(
                    target,
                    "already exists",
                )

                continue

            if self.dry_run:
                console.print(
                    "[dry_run](dry-run)[/dry_run] "
                    f"Would copy {target}"
                )
            else:
                target.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                target.write_text(
                    item.read_text(
                        encoding="utf-8",
                    ),
                    encoding="utf-8",
                )

            self.copied_files += 1

            if not self.dry_run:
                console.print(f"[cyan]Copied[/cyan] {target}")

    def run(
        self,
        *,
        mode: str,
        templates=None,
        dirs=None,
        template_dirs=None,
    ) -> InitializationResult:
        """
        Execute initialization workflow.

        Returns
        -------
        InitializationResult
        """

        if dirs:
            self.create_directories(dirs)

        if templates:
            for template in templates:
                self.write_file(template)

        if template_dirs:
            for template_dir in template_dirs:
                self.copy_package_dir(
                    template_dir.source,
                    template_dir.target,
                    force=self.force,
                )

        return InitializationResult(
            mode=mode,
            created_files=self.created_files,
            copied_files=self.copied_files,
            skipped_files=self.skipped_files,
            created_directories=self.created_directories,
            dry_run=self.dry_run,
        )
