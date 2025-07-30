from typing import List, Optional

from pydantic import BaseModel, Field, validator

from .version_type import VersionType


# -----------------------------
# 📦 Release Info Model
# -----------------------------
class ReleaseInfo(BaseModel):
    """
    Pydantic model containing structured metadata for a release.

    Attributes:
        version (str): The version being released.
        version_type (VersionType): Enum type indicating the stage of release.
        app_name (str): The name of the application.
        prerelease_tags (List[str]): Tags of pre-release versions leading up to this one.
        latest_prerelease (Optional[str]): The latest prerelease tag, if any.
        has_changes_since_rc (bool): Whether this release has changes after the last RC.
    """
    version: str
    version_type: VersionType = Field(default=VersionType.FINAL)
    app_name: str = "Custy"
    prerelease_tags: List[str] = []
    latest_prerelease: Optional[str] = None
    has_changes_since_rc: bool = True

    @validator("version_type", pre=True, always=True)
    def infer_version_type(cls, v, values):
        if not v and "version" in values:
            return VersionType.detect(values["version"])
        return v
