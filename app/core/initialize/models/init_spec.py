# app/core/initialize/models/init_spec.py

from dataclasses import dataclass
from typing import Optional


@dataclass
class InitSpec:
    """
    Initialization Plan

    Represents a fully prepared initialization configuration.

    This is a pure data object used by InitService to execute
    scaffold generation without knowing how the plan was built.

    Execution-ready definition of initialization.

    This is NOT logic.
    This is NOT input.

    This is WHAT will be executed.

    Attributes:
        name (str):
            Human-readable mode name (for logging)

        templates (List):
            List of template files to generate

        dirs (List):
            List of directories to create

        template_dirs (Optional[List]):
            Optional template directories (used for examples)

        messages (List[str]):
            Success messages to display after execution
    """

    name: str
    templates: list
    dirs: list
    template_dirs: Optional[list] = None
    messages: Optional[list[str]] = None
