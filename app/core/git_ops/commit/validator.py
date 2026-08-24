# app/core/git_ops/commit/validator.py

import re
from pathlib import Path
from typing import Optional

from app.constants.git_workflow_rules import ALLOWED_COMMIT_TYPES
from app.core.exceptions.validation_error import ValidationError

HEADER_REGEX = re.compile(
    r"(?P<type>\w+)(\((?P<scope>[^\)]+)\))?!?: (?P<summary>.+)$"
)

def validate_commit_message_format(file_path: Path) -> str:
    """
    Validate commit message format and return detected commit type.

    Returns:
        str: commit type

    Raises:
        ValidationError
    """

    if not file_path.exists():
        raise ValidationError(
            message=f"Commit message file not found: {file_path}",
            hint="Run `custy init templates`",
            code="COMMIT_MSG_FILE_NOT_FOUND",
        )

    content = file_path.read_text(encoding="utf-8").strip()

    if not content:
        raise ValidationError(
            message="Commit message is empty.",
            hint="Write a valid commit message.",
            code="EMPTY_COMMIT_MSG",
        )

    first_line = content.splitlines()[0].strip()

    match = HEADER_REGEX.match(first_line)
    if not match:
        raise ValidationError(
            message="Invalid commit format.",
            hint="Expected: type(scope?): description",
            code="INVALID_COMMIT_FORMAT",
        )

    commit_type = match.group("type")

    if commit_type not in ALLOWED_COMMIT_TYPES:
        raise ValidationError(
            message=f"Invalid commit type '{commit_type}'",
            hint=f"Allowed: {sorted(ALLOWED_COMMIT_TYPES)}",
            code="INVALID_COMMIT_TYPE",
        )
    
    summary = match.group("summary").strip()
    if not summary:
        raise ValidationError(
            message=f"❌ Summary is empty.",
            code="SUMMARY IS EMPTY",
        )
    
    import logging

    logger = logging.getLogger(__name__)

    # Optional: check body exists and is not blank if present
    if len(content.splitlines()) > 1:
        body_lines = content.splitlines()[1:]
        if all(not line.strip() for line in body_lines):
            logger.debug("⚠️ Warning: Commit body exists but is empty.")
        else:
            logger.debug("✅ Body and/or footer detected.")

    logger.debug("✅ Commit message is valid.")

    return commit_type
