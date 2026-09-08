# tests/regression/test_python_package_workflow.py

"""Structural regression tests for private GitLab package publication."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _read(relative_path: str) -> str:
    """Read a repository workflow file as UTF-8 text."""

    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


def test_pipeline_orders_package_publication_before_release_creation() -> None:
    """Validated artifacts and images should precede external publication."""

    github_release = _read(".github/workflows/release.yml")
    pipeline = _read(".gitlab-ci.yml")
    package = _read(".gitlab/python-package.yml")
    production = _read(".gitlab/docker-prod.yml")
    release = _read(".gitlab/release.yml")

    for stage in ("test", "package", "docker", "publish", "release"):
        assert f"    - {stage}" in pipeline
    assert 'local: ".gitlab/python-package.yml"' in pipeline
    assert "annotated Git tag" in package
    assert "CI_COMMIT_REF_PROTECTED" in package
    assert "CI_JOB_TOKEN" in package
    assert "SETUPTOOLS_SCM_PRETEND_VERSION" in package
    assert "python -m twine check dist/*" in package
    assert "--skip-existing" not in package
    assert "Unprotected tag detected; validating package artifacts only" in package
    assert "publication requires a protected release tag" not in package
    assert "job: package:build" in production
    assert "job: package:publish" in release
    assert "job: docker:prod" in release
    for protected_workflow in (package, production, release):
        assert 'CI_COMMIT_REF_PROTECTED == "true"' in protected_workflow
    assert "\\`$PACKAGE_VERSION\\`" in release
    assert "      ```bash" not in release

    # Markdown backticks inside an unquoted heredoc are Bash command
    # substitutions. GitHub release notes must keep Docker examples literal.
    assert "          cat <<EOF >> RELEASE_NOTES.md" not in github_release
    assert "printf '```bash\\n'" in github_release
    assert "docker pull ghcr.io/%s:%s\\n" in github_release
    assert "docker run --rm ghcr.io/%s:%s --help\\n" in github_release
    assert '"$IMAGE_NAME" "$TAG"' in github_release
    assert "- Version: `%s`\\n" in github_release
    assert "- Release Type: `%s`\\n" in github_release
    assert '"$GITHUB_REPOSITORY"' in github_release
    assert '"$GITHUB_WORKFLOW"' in github_release


def test_production_images_publish_stable_version_aliases_only() -> None:
    """Stable releases should move aliases without promoting prereleases."""

    github = _read(".github/workflows/docker-prod.yml")
    gitlab = _read(".gitlab/docker-prod.yml")

    assert 'echo "major=$MAJOR" >> "$GITHUB_OUTPUT"' in github
    assert 'echo "minor=$MINOR" >> "$GITHUB_OUTPUT"' in github
    assert 'echo "publish_aliases=$PUBLISH_ALIASES" >> "$GITHUB_OUTPUT"' in github
    assert (
        "type=raw,value=v${{ steps.version.outputs.major }}."
        "${{ steps.version.outputs.minor }},"
        "enable=${{ steps.version.outputs.publish_aliases }}"
    ) in github
    assert (
        "type=raw,value=v${{ steps.version.outputs.major }},"
        "enable=${{ steps.version.outputs.publish_aliases }}"
    ) in github
    assert (
        "type=raw,value=latest," "enable=${{ steps.version.outputs.publish_latest }}"
    ) in github

    stable_condition = 'if printf \'%s\' "$TAG" | grep -Eq "$STABLE_TAG_REGEX"; then'
    stable_block = gitlab[gitlab.index(stable_condition) :]
    for alias in (
        '"$CI_REGISTRY_IMAGE:v$MAJOR.$MINOR"',
        '"$CI_REGISTRY_IMAGE:v$MAJOR"',
        '"$CI_REGISTRY_IMAGE:latest"',
    ):
        assert f'docker tag "$CI_REGISTRY_IMAGE:$IMAGE_TAG" {alias}' in stable_block
        assert f"docker push {alias}" in stable_block
    assert "Prerelease tag detected; stable aliases will not be updated." in gitlab
