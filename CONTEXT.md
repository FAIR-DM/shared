# CONTEXT.md — Domain glossary

The vocabulary of this repository. Issues, reviews and documentation use these terms and avoid the
listed synonyms.

- **Portal** — a Django application built on FairDM, locked with uv and deployed as a container
  image built on FairDM's base images. The only kind of repository these workflows serve.
  *(Avoid: "project", "app", "downstream repo".)*
- **Reusable workflow** — a `workflow_call` workflow under `.github/workflows/` that a portal
  calls: `tests.yml`, `browser-tests.yml`, `build-checks.yml`, `image.yml`, `prepare-release.yml`
  and `tag-release.yml`.
- **Caller workflow** — the short file in a portal's `.github/workflows/` that calls a reusable
  workflow and passes its secrets by name. Its job name prefixes the check names a portal's ruleset
  requires, as in `call-tests / Tests`.
- **Platform** — the base image version and the PostGIS version a FairDM release or commit
  declares under `[tool.fairdm.platform]` in its `pyproject.toml`. A portal runs on the platform of
  the FairDM it pins. Also the name of the job in each reusable workflow that reads it.
  *(Avoid: "stack", "environment".)*
- **Base images** — the FairDM runtime image `ghcr.io/fair-dm/fairdm:<version>` and development
  image `ghcr.io/fair-dm/fairdm:<version>-dev`, versioned separately from FairDM. Portal tests and
  checks run in the development image. A portal's production image is built on both.
- **Portal image** — a portal's own production image, built from the `Dockerfile` at its root and
  published to `ghcr.io/<owner>/<repository>` on a release.
- **Example portal** — the minimal portal in `tests/portal` that `Validate` runs through every
  reusable workflow. Not a template for real portals.
- **Calendar version** — a portal's version, `<year>.<month>.<release>`, worked out by
  `prepare-release.yml` from the date and existing tags.
- **Pin tag** — a `v<major>.<minor>.<patch>` tag of this repository that a portal's caller
  workflows reference. This repository's own versions are semantic, unlike a portal's.
  *(Avoid: pinning `main`.)*
- **Release pull request** — the pull request `prepare-release.yml` (or, for this repository,
  `prepare-shared-release.yml`) opens. Merging it is the release decision.
