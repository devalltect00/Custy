"""Tests for the GitLab Python-package version policy."""

from __future__ import annotations

import io
import tarfile
import zipfile
from pathlib import Path

import pytest

from scripts.ci.package_version import (
    PackageVersionError,
    normalize_release_tag,
    verify_distributions,
)


@pytest.mark.parametrize(
    ("tag", "expected"),
    [
        ("v1.2.3", "1.2.3"),
        ("v1.2.3-alpha.1", "1.2.3a1"),
        ("v1.2.3-beta.2", "1.2.3b2"),
        ("v1.2.3-rc.3", "1.2.3rc3"),
        ("v1.2.3-dev.4", "1.2.3.dev4"),
        ("v1.2.3a1", "1.2.3a1"),
        ("v1.2.3b2", "1.2.3b2"),
        ("v1.2.3rc3", "1.2.3rc3"),
        ("v1.2.3.dev4", "1.2.3.dev4"),
        ("v1.2.3.post5", "1.2.3.post5"),
    ],
)
def test_normalize_release_tag_supports_explicit_release_formats(
    tag: str, expected: str
) -> None:
    """Supported repository tags should produce canonical PEP 440 versions."""

    assert normalize_release_tag(tag) == expected


@pytest.mark.parametrize(
    "tag",
    [
        "1.2.3",
        "v1.2",
        "release-1.2.3",
        "v1.2.3-preview.1",
        "v1.2.3-custom.1",
        "v1.2.3-rc",
        "v1.2.3-post.1",
        "v1.2.3+build.1",
        "v01.2.3",
    ],
)
def test_normalize_release_tag_rejects_ambiguous_or_unexpected_formats(
    tag: str,
) -> None:
    """The publisher must fail closed instead of guessing version semantics."""

    with pytest.raises(PackageVersionError, match="Unsupported release tag"):
        normalize_release_tag(tag)


def _write_distributions(
    dist_dir: Path,
    *,
    version: str = "1.2.3rc1",
    metadata_version: str | None = None,
) -> None:
    """Create minimal wheel and sdist archives for metadata verification."""

    embedded_version = metadata_version or version
    metadata = (
        "Metadata-Version: 2.1\n" "Name: custy\n" f"Version: {embedded_version}\n" "\n"
    ).encode()
    wheel = dist_dir / f"custy-{version}-py3-none-any.whl"
    with zipfile.ZipFile(wheel, mode="w") as archive:
        archive.writestr(f"custy-{version}.dist-info/METADATA", metadata)
    sdist = dist_dir / f"custy-{version}.tar.gz"
    with tarfile.open(sdist, mode="w:gz") as archive:
        info = tarfile.TarInfo(f"custy-{version}/PKG-INFO")
        info.size = len(metadata)
        archive.addfile(info, io.BytesIO(metadata))
        egg_info = tarfile.TarInfo(f"custy-{version}/custy.egg-info/PKG-INFO")
        egg_info.size = len(metadata)
        archive.addfile(egg_info, io.BytesIO(metadata))


def test_verify_distributions_checks_filenames_and_embedded_metadata(
    tmp_path: Path,
) -> None:
    """Both artifacts should agree with the normalized release tag."""

    _write_distributions(tmp_path)
    assert verify_distributions("v1.2.3-rc.1", "custy", tmp_path) == "1.2.3rc1"


def test_verify_distributions_rejects_noncanonical_embedded_version(
    tmp_path: Path,
) -> None:
    """A filename must not hide noncanonical package metadata."""

    _write_distributions(tmp_path, metadata_version="1.2.3-rc.1")
    with pytest.raises(PackageVersionError, match="expected canonical PEP 440"):
        verify_distributions("v1.2.3-rc.1", "custy", tmp_path)
