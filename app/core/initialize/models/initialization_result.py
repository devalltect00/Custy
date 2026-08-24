# app/core/initialize/models/initialization_result.py

"""
Initialization result models.

This module contains execution results produced by
the initialization workflow.

These models are intended for:

- UI presentation
- Logging
- Reporting
- Testing

The result object allows execution services to
return structured information instead of printing
directly to the console.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class InitializationResult:
    """
    Initialization execution summary.

    Attributes
    ----------
    mode:
        Initialization mode that was executed.

    created_files:
        Number of newly created files.

    copied_files:
        Number of copied template files.

    skipped_files:
        Number of skipped files.

    created_directories:
        Number of created directories.

    dry_run:
        Whether the counts describe planned rather than applied changes.
    """

    mode: str

    created_files: int = 0

    copied_files: int = 0

    skipped_files: int = 0

    created_directories: int = 0

    dry_run: bool = False
