# Make Workflows

## Overview

Custy's root `Makefile` loads focused modules under `make/core/`. Run Make from
the Custy repository root and use the project help to discover targets:

```bash
make help
make help-remote
```

Bare `make` and `make help` display the project's formatted command list.
`make --help` displays GNU Make's own executable help and is not controlled by
this repository.

## Published Reflow Image

The `r-reflow-*` targets run the published Reflow image from GHCR against the
workspace selected by `REMOTE_WORKSPACE`. Registry management is separate from
runtime execution:

```bash
make r-reflow-info
make r-reflow-pull
make r-reflow-remove
```

`r-reflow-push` publishes a container image and therefore requires explicit
registry credentials and intent.

The runtime targets follow Reflow's current CLI command names:

| Reflow CLI workflow | Custy Make target | Preview target |
|---|---|---|
| `reflow init` | `r-reflow-init` | `r-reflow-init-dryrun` |
| `reflow releases recover` | `r-reflow-releases-recover` | `r-reflow-releases-recover-dryrun` |
| `reflow tags convert` | `r-reflow-tags-convert` | `r-reflow-tags-convert-dryrun` |
| `reflow dockerize` | `r-reflow-dockerize` | `r-reflow-dockerize-dryrun` |

The `r-reflow-tags-replay` targets are deprecated compatibility aliases. They
display a warning and delegate to `r-reflow-releases-recover`; they do not call
the deprecated CLI spelling directly.

## Repository Targets

For a local repository, mount the target as the remote workspace:

```bash
make r-reflow-tags-convert-dryrun \
  REMOTE_WORKSPACE="D:/project/testing_lab/testing_reflow"
```

The mounted directory becomes `/workspace` inside the container, so Reflow
uses it as the current repository unless another target is supplied.

For a GitHub or GitLab URL, pass the global Reflow option before the command:

```bash
make r-reflow-tags-convert-dryrun \
  REMOTE_REFLOW_GLOBAL_ARGS="--repository-url https://github.com/owner/repository.git"
```

For a live remote conversion, add `--push --yes` to the command-specific
arguments. Without `--push`, tags created in a temporary URL checkout disappear
when Reflow removes that checkout.

```bash
make r-reflow-tags-convert \
  REMOTE_REFLOW_GLOBAL_ARGS="--repository-url https://github.com/owner/repository.git" \
  REMOTE_REFLOW_TAGS_CONVERT_ARGS="--to semver --push --yes"
```

`reflow init` requires a local repository target and does not accept a
repository URL.

## Arguments

Use the variable matching the command layer:

| Variable | Purpose |
|---|---|
| `REMOTE_REFLOW_GLOBAL_ARGS` | Global options such as `--repository`, `--repository-url`, `--debug`, or `--no-banner` |
| `REMOTE_REFLOW_INIT_ARGS` | Options passed to `reflow init` |
| `REMOTE_REFLOW_RELEASES_RECOVER_ARGS` | Options passed to `reflow releases recover` |
| `REMOTE_REFLOW_TAGS_CONVERT_ARGS` | Options passed to `reflow tags convert` |
| `REMOTE_REFLOW_DOCKERIZE_ARGS` | Options passed to `reflow dockerize` |
| `REMOTE_REFLOW_EXTRA_ARGS` | Final escape hatch for additional command arguments |

Dry-run targets append the global `--dry-run` option. They preserve repository
selection and every other value already supplied through
`REMOTE_REFLOW_GLOBAL_ARGS`.

## Dockerize Access

Reflow's `dockerize` workflow invokes Docker from inside the Reflow container.
The Make target mounts `DOCKER_SOCKET`, which defaults to
`/var/run/docker.sock`, so the container can communicate with the host Docker
daemon.

```bash
make r-reflow-dockerize-dryrun \
  REMOTE_WORKSPACE="D:/project/testing_lab/testing_reflow"
```

Override `DOCKER_SOCKET` only when the host uses a different Docker endpoint.

## Safety and Credentials

Start with a `-dryrun` target. Reflow previews its own Git, release, and Docker
mutations, but registry management targets such as `r-reflow-push` and
`r-reflow-remove` are direct Docker operations and do not have Reflow dry-run
semantics.

Remote Git pushes, release recovery, and registry publication require the
corresponding credentials inside the container. Do not store tokens in the
Makefile or container image; provide credentials securely at runtime.

