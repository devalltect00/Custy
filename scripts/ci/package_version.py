# scripts/ci/package_version.py

"""Validate release tags and Python distribution metadata for GitLab CI.

The repository uses readable Semantic Versioning tags while Python package
artifacts must use canonical PEP 440 versions. This module implements the
small, explicit mapping supported by the release pipeline and rejects formats
whose ordering would be ambiguous after conversion.
"""

from __future__ import annotations

import argparse
import email
import re
import tarfile
import zipfile
from pathlib import Path, PurePosixPath
from typing import NoReturn

from packaging.utils import (
    InvalidSdistFilename,
    InvalidWheelFilename,
    canonicalize_name,
    parse_sdist_filename,
    parse_wheel_filename,
)
from packaging.version import InvalidVersion, Version

_NUMBER = r"(?:0|[1-9][0-9]*)"
_RELEASE = rf"(?P<major>{_NUMBER})\.(?P<minor>{_NUMBER})\.(?P<patch>{_NUMBER})"
_SEMVER_TAG = re.compile(
    rf"^v{_RELEASE}(?:-(?P<label>alpha|beta|rc|dev)\.(?P<number>{_NUMBER}))?$"
)
_PEP440_TAG = re.compile(
    rf"^v{_RELEASE}(?:(?P<pre>a|b|rc)(?P<pre_number>{_NUMBER})"
    rf"|\.dev(?P<dev_number>{_NUMBER})|\.post(?P<post_number>{_NUMBER}))?$"
)
_ACCEPTED_FORMATS = (
    "vMAJOR.MINOR.PATCH, vMAJOR.MINOR.PATCH-alpha.N, "
    "vMAJOR.MINOR.PATCH-beta.N, vMAJOR.MINOR.PATCH-rc.N, "
    "vMAJOR.MINOR.PATCH-dev.N, or canonical PEP 440 tags such as "
    "vMAJOR.MINOR.PATCHrcN and vMAJOR.MINOR.PATCH.postN"
)


class PackageVersionError(ValueError):
    """Raised when a release tag or built distribution violates policy."""


def normalize_release_tag(tag: str) -> str:
    """Return the canonical PEP 440 package version for a release tag.

    Args:
        tag: Annotated Git release tag, including its leading ``v``.

    Returns:
        Canonical PEP 440 version without the Git tag's leading ``v``.

    Raises:
        PackageVersionError: If the tag is unsupported or ambiguous.

    Notes:
        Arbitrary SemVer prerelease labels, SemVer build metadata, and
        ``-post.N`` are intentionally rejected. In particular, ``-post.N`` is
        ordered before a stable release by SemVer but ``.postN`` is ordered
        after it by PEP 440.
    """

    semver_match = _SEMVER_TAG.fullmatch(tag)
    pep440_match = _PEP440_TAG.fullmatch(tag)
    match = semver_match or pep440_match
    if match is None:
        raise PackageVersionError(
            f"Unsupported release tag {tag!r}. Accepted formats: {_ACCEPTED_FORMATS}."
        )

    base = ".".join(match.group(name) for name in ("major", "minor", "patch"))
    candidate = base

    if semver_match is not None:
        label = semver_match.group("label")
        number = semver_match.group("number")
        if label == "alpha":
            candidate = f"{base}a{number}"
        elif label == "beta":
            candidate = f"{base}b{number}"
        elif label == "rc":
            candidate = f"{base}rc{number}"
        elif label == "dev":
            candidate = f"{base}.dev{number}"
    else:
        pre = match.group("pre")
        if pre is not None:
            candidate = f"{base}{pre}{match.group('pre_number')}"
        elif match.group("dev_number") is not None:
            candidate = f"{base}.dev{match.group('dev_number')}"
        elif match.group("post_number") is not None:
            candidate = f"{base}.post{match.group('post_number')}"

    try:
        return str(Version(candidate))
    except InvalidVersion as exc:
        raise PackageVersionError(
            f"Release tag {tag!r} could not be normalized to PEP 440."
        ) from exc


def _metadata_from_wheel(path: Path) -> tuple[str, str]:
    """Return the Name and Version metadata from one wheel archive."""

    with zipfile.ZipFile(path) as archive:
        metadata_files = [
            name for name in archive.namelist() if name.endswith(".dist-info/METADATA")
        ]
        if len(metadata_files) != 1:
            raise PackageVersionError(
                f"Wheel {path.name!r} must contain exactly one METADATA file."
            )
        message = email.message_from_bytes(archive.read(metadata_files[0]))
    return message.get("Name", ""), message.get("Version", "")


def _metadata_from_sdist(path: Path) -> tuple[str, str]:
    """Return the Name and Version metadata from one source distribution."""

    with tarfile.open(path, mode="r:gz") as archive:
        metadata_files = []
        for member in archive.getmembers():
            member_path = PurePosixPath(member.name)
            if (
                member.isfile()
                and member_path.name == "PKG-INFO"
                and len(member_path.parts) == 2
            ):
                metadata_files.append(member)
        if len(metadata_files) != 1:
            raise PackageVersionError(
                f"Source distribution {path.name!r} must contain one PKG-INFO file."
            )
        extracted = archive.extractfile(metadata_files[0])
        if extracted is None:
            raise PackageVersionError(
                f"Could not read PKG-INFO from source distribution {path.name!r}."
            )
        message = email.message_from_binary_file(extracted)
    return message.get("Name", ""), message.get("Version", "")


def _validate_identity(
    *,
    artifact: Path,
    actual_name: str,
    actual_version: str,
    expected_name: str,
    expected_version: str,
) -> None:
    """Validate an artifact's normalized distribution name and version."""

    if canonicalize_name(actual_name) != canonicalize_name(expected_name):
        raise PackageVersionError(
            f"{artifact.name!r} contains distribution {actual_name!r}; "
            f"expected {expected_name!r}."
        )
    try:
        normalized_version = str(Version(actual_version))
    except InvalidVersion as exc:
        raise PackageVersionError(
            f"{artifact.name!r} contains invalid version {actual_version!r}."
        ) from exc
    if normalized_version != expected_version or actual_version != expected_version:
        raise PackageVersionError(
            f"{artifact.name!r} contains version {actual_version!r}; "
            f"expected canonical PEP 440 version {expected_version!r}."
        )


def verify_distributions(tag: str, distribution: str, dist_dir: Path) -> str:
    """Verify wheel and sdist filenames and embedded package metadata."""

    expected_version = normalize_release_tag(tag)
    wheels = sorted(dist_dir.glob("*.whl"))
    sdists = sorted(dist_dir.glob("*.tar.gz"))
    if len(wheels) != 1 or len(sdists) != 1:
        raise PackageVersionError(
            f"Expected exactly one wheel and one sdist in {dist_dir}; found "
            f"{len(wheels)} wheel(s) and {len(sdists)} sdist(s)."
        )

    wheel = wheels[0]
    sdist = sdists[0]
    try:
        wheel_name, wheel_version, _, _ = parse_wheel_filename(wheel.name)
        sdist_name, sdist_version = parse_sdist_filename(sdist.name)
    except (InvalidWheelFilename, InvalidSdistFilename) as exc:
        raise PackageVersionError(f"Invalid distribution filename: {exc}") from exc

    _validate_identity(
        artifact=wheel,
        actual_name=str(wheel_name),
        actual_version=str(wheel_version),
        expected_name=distribution,
        expected_version=expected_version,
    )
    _validate_identity(
        artifact=sdist,
        actual_name=str(sdist_name),
        actual_version=str(sdist_version),
        expected_name=distribution,
        expected_version=expected_version,
    )
    for artifact, metadata_reader in (
        (wheel, _metadata_from_wheel),
        (sdist, _metadata_from_sdist),
    ):
        metadata_name, metadata_version = metadata_reader(artifact)
        _validate_identity(
            artifact=artifact,
            actual_name=metadata_name,
            actual_version=metadata_version,
            expected_name=distribution,
            expected_version=expected_version,
        )

    return expected_version


def _exit_with_error(parser: argparse.ArgumentParser, error: Exception) -> NoReturn:
    """Exit an argument parser with a concise CI-friendly validation error."""

    parser.exit(status=2, message=f"Package version error: {error}\n")


def main() -> None:
    """Run release-tag normalization or distribution verification."""

    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    normalize_parser = subparsers.add_parser(
        "normalize", help="convert a supported release tag to canonical PEP 440"
    )
    normalize_parser.add_argument("tag")
    verify_parser = subparsers.add_parser(
        "verify-dist", help="verify wheel and sdist identity against a release tag"
    )
    verify_parser.add_argument("tag")
    verify_parser.add_argument("distribution")
    verify_parser.add_argument("dist_dir", type=Path)

    args = parser.parse_args()
    try:
        if args.command == "normalize":
            print(normalize_release_tag(args.tag))
            return
        print(verify_distributions(args.tag, args.distribution, args.dist_dir))
    except PackageVersionError as exc:
        _exit_with_error(parser, exc)


if __name__ == "__main__":
    main()
