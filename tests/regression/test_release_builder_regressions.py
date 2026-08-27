# tests/regression/test_release_builder_regressions.py

"""
Regression tests for ReleaseNoteBuilder.
"""

from app.core.git_ops.versioning.builder.release_builder import (
    ReleaseNoteBuilder,
)
from app.core.git_ops.versioning.models.release_info import ReleaseInfo
from app.core.git_ops.versioning.models.version_type import VersionType


class TestReleaseNoteBuilderRegressions:
    """
    Regression tests for ReleaseNoteBuilder.
    """

    def _release_info(
        self,
        version="v1.2.3",
        version_type=VersionType.FINAL,
    ):
        return ReleaseInfo(
            version=version,
            version_type=version_type,
            app_name="Custy",
        )

    def test_builder_can_be_created(self):
        builder = ReleaseNoteBuilder(self._release_info())

        assert builder is not None

    def test_release_info_preserved(self):
        info = self._release_info()

        builder = ReleaseNoteBuilder(info)

        assert builder.info is info

    def test_build_commit_msg_returns_string(self):
        builder = ReleaseNoteBuilder(self._release_info())

        msg = builder.build_commit_msg()

        assert isinstance(msg, str)
        assert msg.strip()

    def test_build_tag_msg_returns_string(self):
        builder = ReleaseNoteBuilder(self._release_info())

        msg = builder.build_tag_msg()

        assert isinstance(msg, str)
        assert msg.strip()

    def test_commit_message_contains_version(self):
        builder = ReleaseNoteBuilder(self._release_info())

        msg = builder.build_commit_msg()

        assert "1.2.3" in msg

    def test_tag_message_contains_version(self):
        builder = ReleaseNoteBuilder(self._release_info())

        msg = builder.build_tag_msg()

        assert "1.2.3" in msg

    def test_final_release_message_mentions_stable(self):
        builder = ReleaseNoteBuilder(
            self._release_info(
                version_type=VersionType.FINAL,
            )
        )

        msg = builder.build_tag_msg()

        assert "stable" in msg.lower()

    def test_rc_release_message_mentions_candidate(self):
        builder = ReleaseNoteBuilder(
            self._release_info(
                version="v2.0.0rc1",
                version_type=VersionType.RC,
            )
        )

        msg = builder.build_tag_msg()

        assert "candidate" in msg.lower()

    def test_builder_is_deterministic(self):
        builder = ReleaseNoteBuilder(self._release_info())

        assert builder.build_commit_msg() == builder.build_commit_msg()

        assert builder.build_tag_msg() == builder.build_tag_msg()

    def test_multiple_builders_are_independent(self):
        first = ReleaseNoteBuilder(self._release_info())

        second = ReleaseNoteBuilder(self._release_info())

        assert first is not second
