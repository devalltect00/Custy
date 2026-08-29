# app/core/project/__init__.py

"""Project layout and metadata detection."""

from .detector import (
    AUTO_VALUE,
    ProjectEcosystem,
    ProjectLayout,
    detect_project_layout,
    detect_project_name,
)

__all__ = [
    "AUTO_VALUE",
    "ProjectEcosystem",
    "ProjectLayout",
    "detect_project_name",
    "detect_project_layout",
]
