# app/core/editor/__init__.py

"""Cross-platform editor configuration, discovery, and launch services."""

from .service import EditorCandidate, EditorService
from .settings import EditorIdentifier, EditorSettings

__all__ = [
    "EditorCandidate",
    "EditorIdentifier",
    "EditorService",
    "EditorSettings",
]
