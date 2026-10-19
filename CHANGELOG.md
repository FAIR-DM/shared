# Changelog

All notable changes to this repository are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Reusable workflows for FairDM portals: `tests.yml`, `browser-tests.yml`, `build-checks.yml`,
  `image.yml`, `prepare-release.yml` and `tag-release.yml`. Each runs a portal on the base image and
  PostGIS versions declared by the FairDM it pins in `uv.lock`.
- An example portal in `tests/portal` that the `Validate` workflow runs through every portal
  workflow.
