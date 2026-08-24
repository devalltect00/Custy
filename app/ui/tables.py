# app/ui/tables.py

"""
Reusable Rich tables.

This module contains presentation helpers used
to display structured information to users.

Current tables
--------------

configuration_table()
    Display configuration summaries.

branch_cleanup_table()
    Display the result of a branch cleanup operation.
"""

from pathlib import Path

from rich.table import Table

from app.core.cleanup.branch.models import BranchCleanupResult


def configuration_table(
    *,
    target_directory: Path,
    profile: str,
    smart_mode: bool,
    max_depth: int,
    show_files: bool,
    collapse_dirs: set[str],
    project_type: str | None,
) -> Table:
    """
    Create configuration summary table.

    Parameters
    ----------
    target_directory:
        Repository root directory.

    profile:
        Active profile.

    smart_mode:
        Smart mode status.

    max_depth:
        Maximum traversal depth.

    show_files:
        Include files in tree output.

    collapse_dirs:
        Collapsed directories.

    project_type:
        Forced project type if provided.

    Returns
    -------
    Table
    """

    table = Table(
        title="Configuration",
    )

    table.add_column(
        "Setting",
        style="cyan",
    )

    table.add_column(
        "Value",
    )

    table.add_row(
        "Target Directory",
        str(target_directory),
    )

    table.add_row(
        "Profile",
        str(profile),
    )

    table.add_row(
        "Smart Mode",
        str(smart_mode),
    )

    table.add_row(
        "Max Depth",
        str(max_depth),
    )

    table.add_row(
        "Show Files",
        str(show_files),
    )

    table.add_row(
        "Project Type",
        str(project_type),
    )

    table.add_row(
        "Collapse Directories",
        ", ".join(sorted(collapse_dirs)) if collapse_dirs else "-",
    )

    return table

def branch_cleanup_table(
    result: BranchCleanupResult,
) -> Table:
    """
    Create a branch cleanup summary table.

    Parameters
    ----------
    result:
        Completed branch cleanup result.

    Returns
    -------
    Table
        Rich summary table.
    """

    table = Table(
        title=(
            "Branch Cleanup Preview"
            if result.dry_run
            else "Branch Cleanup Summary"
        ),
    )

    table.add_column(
        "Metric",
        style="cyan",
    )

    table.add_column(
        "Value",
    )

    table.add_row(
        "Scanned",
        str(result.scanned),
    )

    table.add_row(
        "Would Delete (Local)" if result.dry_run else "Deleted (Local)",
        str(result.deleted_count),
    )

    table.add_row(
        "Would Delete (Remote)" if result.dry_run else "Deleted (Remote)",
        str(len(result.deleted_remote)),
    )

    table.add_row(
        "Skipped",
        str(result.skipped_count),
    )

    table.add_row(
        "Failed",
        str(result.failed_count),
    )

    table.add_row(
        "Dry Run",
        "Yes" if result.dry_run else "No",
    )

    return table
