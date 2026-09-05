# tests/regression/test_python_package_workflow.py

"""Structural regression tests for private GitLab package publication."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _read(relative_path: str) -> str:
    """Read a repository workflow file as UTF-8 text."""

    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


def test_pipeline_orders_package_publication_before_release_creation() -> None:
    """Validated artifacts and images should precede external publication."""

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
