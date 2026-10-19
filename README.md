# FAIR-DM Shared

[![Validate](https://github.com/FAIR-DM/shared/actions/workflows/validate.yml/badge.svg)](https://github.com/FAIR-DM/shared/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/FAIR-DM/shared/blob/main/LICENSE)

Reusable GitHub Actions workflows for research data portals built on
[FairDM](https://github.com/FAIR-DM/fairdm). A portal calls them from a few short workflow files of
its own instead of writing its CI, image build and release from scratch.

The workflows run a portal on what its FairDM declares. FairDM records the version of its base
image and the PostGIS version it is tested on under `[tool.fairdm.platform]` in its
`pyproject.toml`. Each workflow reads which FairDM the portal pins from `uv.lock` and uses those
versions for the tests, the checks and the production image. When a portal moves its FairDM pin,
its CI and its image move with it.

## Scope & philosophy

This repository holds the CI, image and release workflows for FairDM portals: Django
applications built on FairDM, locked with uv and deployed as a container image built on FairDM's
base image.

It is not for packages. FairDM itself and its add-on packages keep their own workflows. It has no
options that change what a workflow does for a particular portal: a portal that does not fit
writes its own workflow rather than adding a switch here.

When choices collide: a portal runs on exactly what its FairDM was tested on, callers pin a tag and
never `main`, and every workflow is proven on the example portal before it is released.

## Contents

- [What a portal needs](#what-a-portal-needs)
- [The workflows](#the-workflows)
- [Calling them](#calling-them)
- [Releasing a portal](#releasing-a-portal)
- [Versions of this repository](#versions-of-this-repository)
- [Contributing](#contributing)
- [License](#license)

## What a portal needs

- A `pyproject.toml` with standard `[project]` metadata and a committed `uv.lock` that pins
  `fairdm`, from PyPI or from a GitHub commit. That FairDM must declare
  `[tool.fairdm.platform]`.
- A `Dockerfile` at the repository root that builds `FROM` the FairDM base images and takes the
  image version as the `FAIRDM_IMAGE_VERSION` build argument. FairDM's
  [`docker/portal.Dockerfile`](https://github.com/FAIR-DM/fairdm/blob/main/docker/portal.Dockerfile)
  is the starting point.
- Settings that read the database from `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_USER`,
  `POSTGRES_PASSWORD` and `POSTGRES_DB`, as `fairdm.setup()` does.
- A `.pre-commit-config.yaml`, with `pre-commit` in the portal's development dependencies.
- `pytest`, `pytest-django` and `pytest-cov` in its development dependencies. Browser tests carry
  the `e2e` marker and need `pytest-playwright`.
- A `CHANGELOG.md` with an `## [Unreleased]` section, for the release workflows.

## The workflows

| Workflow | Checks it reports | What it does |
| --- | --- | --- |
| `tests.yml` | `Platform`, `Tests` | Runs `pytest -m "not e2e"` with coverage in the FairDM development image against a PostGIS service, and uploads the coverage to Codecov |
| `browser-tests.yml` | `Platform`, `Browser tests` | Installs Chromium in the same image and runs `pytest -m e2e` |
| `build-checks.yml` | `Platform`, `Code Quality`, `Security Scan` | Runs `pre-commit run --all-files` in the development image. Runs bandit and pip-audit there and uploads their reports, failing only when a report is missing |
| `image.yml` | `Platform`, `Build image` | Builds the root `Dockerfile` on the declared base image, starts it against PostGIS and Redis, and waits for a 200. On a release event it pushes the image to `ghcr.io/<owner>/<repository>` as the version and `latest` |
| `prepare-release.yml` | | Opens the release pull request for the next calendar version |
| `tag-release.yml` | | Creates the tag and GitHub Release once a release pull request merges |

`Platform` is the short job that reads the versions from the portal's FairDM. It fails with a
message naming the problem when `uv.lock` pins no FairDM, or when the pinned FairDM declares no
platform.

## Calling them

Each file below goes in the portal's `.github/workflows/`. Secrets are passed by name, because
`secrets: inherit` does not cross GitHub organisations. Replace `v0.1.0` with the newest tag.

`tests.yml`:

```yaml
name: Tests

on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

jobs:
  call-tests:
    uses: FAIR-DM/shared/.github/workflows/tests.yml@v0.1.0
    secrets:
      CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}

  # Only in a portal that has browser tests.
  call-browser-tests:
    uses: FAIR-DM/shared/.github/workflows/browser-tests.yml@v0.1.0
    secrets:
      CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
```

`build.yml`:

```yaml
name: Build

on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

jobs:
  call-build:
    uses: FAIR-DM/shared/.github/workflows/build-checks.yml@v0.1.0
```

`image.yml`. The image workflow asks for `packages: write` to push on a release, and a called
workflow cannot ask for more than its caller grants, so the caller grants it on every event:

```yaml
name: Image

on:
  pull_request:
  release:
    types: [published]
  workflow_dispatch:

permissions:
  contents: read
  packages: write

jobs:
  call-image:
    uses: FAIR-DM/shared/.github/workflows/image.yml@v0.1.0
```

Leave out `paths` filters on `pull_request` for any check a ruleset requires. A check that does
not run never reports, and the pull request cannot merge.

## Releasing a portal

Portals version by calendar: `<year>.<month>.<release>`, so the first release of October 2026 is
`2026.10.1` and the next one that month is `2026.10.2`. A release takes three steps:

1. Run **Prepare Release** from the Actions tab. It sets the version in `pyproject.toml` and
   `uv.lock`, turns `## [Unreleased]` into the version's section of `CHANGELOG.md`, and opens a
   pull request. Give it a version only to override the computed one.
2. Merge that pull request. That is the release decision. **Tag Release** sees the new version and
   creates the `v<version>` tag and GitHub Release.
3. The release event runs the image workflow, which pushes `ghcr.io/<owner>/<repository>:<version>`
   and `:latest`.

Both release workflows need a `RELEASE_TOKEN` secret holding a token with read and write access to
the repository's contents and pull requests. A pull request opened with the default
`GITHUB_TOKEN` runs no checks, and a release it creates fires no release event.

`prepare-release.yml`:

```yaml
name: Prepare Release

on:
  workflow_dispatch:
    inputs:
      version:
        description: Override the computed <year>.<month>.<release> (leave empty)
        type: string
        default: ""

permissions:
  contents: read

jobs:
  call-prepare-release:
    uses: FAIR-DM/shared/.github/workflows/prepare-release.yml@v0.1.0
    with:
      version: ${{ inputs.version }}
    secrets:
      RELEASE_TOKEN: ${{ secrets.RELEASE_TOKEN }}
```

`tag-release.yml`:

```yaml
name: Tag Release

on:
  push:
    branches: [main]
    paths: [pyproject.toml]

permissions:
  contents: read

jobs:
  call-tag-release:
    uses: FAIR-DM/shared/.github/workflows/tag-release.yml@v0.1.0
    secrets:
      RELEASE_TOKEN: ${{ secrets.RELEASE_TOKEN }}
```

## Versions of this repository

This repository is released with semantic versions, `v<major>.<minor>.<patch>`, and a portal pins
a tag. Never pin `main`: a portal's checks would change under it with no change of its own.

- A **major** version changes something a portal has to act on, such as what it must provide or the
  name of a check its ruleset requires.
- A **minor** version adds something, such as a new workflow.
- A **patch** version changes nothing a portal relies on.

The changes in each version are in [CHANGELOG.md](CHANGELOG.md).

## Contributing

Every workflow is checked by the `Validate` workflow. It runs actionlint and the workflow schema
over every file, then calls each portal workflow on the example portal in
[`tests/portal`](tests/portal), so a change has to work on a real portal before it is released.
The `working-directory` input exists only so the example portal can live in a subdirectory.
Portals leave it unset.

The `Platform` job is the same in each workflow that has one, because a called workflow cannot
share a step with another called workflow from the same repository at the same version. Change
all four copies together.

To check a workflow file locally:

```sh
uvx --from actionlint-py actionlint
uvx --from check-jsonschema check-jsonschema --builtin-schema vendor.github-workflows .github/workflows/*.yml
```

To release this repository, run **Prepare Shared Release** from the Actions tab with a bump and
merge the pull request it opens. **Tag Shared Release** then creates the tag.

## License

[MIT](LICENSE)
