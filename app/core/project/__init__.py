# app/core/project/__init__.py

"""Project layout and metadata detection."""

from .detector import (
    AUTO_VALUE,
    ProjectEcosystem,
    ProjectLayout,
    detect_project_layout,
)

__all__ = [
    "AUTO_VALUE",
    "ProjectEcosystem",
    "ProjectLayout",
    "detect_project_layout",
]
