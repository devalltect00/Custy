# app/core/initialize/models/template_dir.py

from dataclasses import dataclass


@dataclass
class TemplateDir:
    target: str
    source: str
