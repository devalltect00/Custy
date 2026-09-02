# Private GitLab Python package registry

Custy's GitLab pipeline publishes reviewed releases to the project's private
PyPI-compatible package registry. Git tags remain readable release identifiers;
wheel and source-distribution metadata always use canonical PEP 440 versions.

## Release flow

Tag pipelines run in this order:

```text
test -> package -> docker -> publish -> release
```

The package gate accepts any annotated tag with a non-empty message. It
normalizes the tag, builds one wheel and one source distribution, runs
`twine check`, verifies filenames and embedded metadata, installs the wheel in
a clean virtual environment, and starts `custy --help`.

For an unprotected tag, the pipeline ends successfully after this validation
and retains the build artifacts for inspection. Only a protected tag may
continue to the production image, private package upload, and GitLab release.
The production image uses the same normalized package version.

## Version mapping

| Release tag | Published package version |
| --- | --- |
| `v2.1.0` | `2.1.0` |
| `v2.2.0-alpha.1` | `2.2.0a1` |
| `v2.2.0-beta.1` | `2.2.0b1` |
| `v2.2.0-rc.1` | `2.2.0rc1` |
| `v2.2.0-dev.1` | `2.2.0.dev1` |
| `v2.1.0.post1` | `2.1.0.post1` |

Canonical PEP 440 tags such as `v2.2.0rc1` are also accepted. Unknown labels,
missing numeric identifiers, local build metadata, and ambiguous forms such as
`v2.1.0-post.1` fail before publication. Use the canonical PEP 440 tag
`v2.1.0.post1` for a post-release.

## Installation

Use a deploy token with `read_package_registry` permission:

```bash
python -m pip install \
  --index-url "https://<deploy-token-user>:<deploy-token>@gitlab.com/api/v4/projects/<project-id>/packages/pypi/simple" \
  "custy==2.1.0"
```

Inside an authorized GitLab pipeline, use `gitlab-ci-token` and
`CI_JOB_TOKEN`. Do not commit tokens or credential-bearing URLs.

For strictly private resolution, disable PyPI package forwarding in the GitLab
group settings. Avoid `--extra-index-url` for private packages because multiple
indexes can introduce dependency-confusion risk.

## Immutability and retries

GitLab does not accept a second upload with the same distribution name and
version. The workflow deliberately does not use `--skip-existing`: a duplicate
fails visibly and requires a new release version. Never delete an existing
package merely to reuse its version.
