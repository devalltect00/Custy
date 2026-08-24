# app/core/initialize/models/template_file.py

from collections.abc import Callable
from dataclasses import dataclass
from typing import Optional


@dataclass
class TemplateFile:
    target_path: str
    source_path: Optional[str] = None
    content: Optional[Callable[[], str]] = None
    optional: bool = False

    def render(self) -> str:
        if callable(self.content):
            return self.content()
        return self.content or ""
