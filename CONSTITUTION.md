# FAIR-DM Shared Constitution

<!-- Changes go through a human-gated amendment, never in the middle of other work. -->

## Core articles

### Article I — Testing
A change to a reusable workflow is tested by running it on the example portal in `tests/portal`,
through the `Validate` workflow. A behaviour a workflow adds is exercised there: a new check runs
on the example portal, a new failure message is reached by something the example can do. The
example portal's own Python follows
[`docs/contributing/standards/testing.md`](docs/contributing/standards/testing.md).

### Article II — Simplicity
Start with the simplest workflow that serves the portals that exist. A new workflow, job, input
or third-party action each needs a stated reason in the pull request that adds it.

### Article III — Anti-Abstraction
No input, composite action or indirection for a portal that does not exist yet. A step repeated in
several workflows stays repeated while GitHub offers no way to share it within one tag of this
repository, and every copy changes in the same pull request.

### Article IV — Integration-First
The caller workflow is the contract. A change is designed from what a portal writes and sees: the
caller file, the secrets it passes, the check names its ruleset requires, and what it must
provide. It is verified the way a portal uses it, through a caller on the example portal.

### Article V — Security & data-safety
These workflows run in other organisations' repositories with their secrets, so this repository
is part of every portal's supply chain.
- Secrets are declared under `on.workflow_call.secrets` and passed by name. `secrets: inherit` is
  never relied on.
- Each workflow and job asks for the fewest permissions it needs. Checkouts set
  `persist-credentials: false` unless a later step pushes.
- Third-party actions are pinned to a release tag. A new third-party action needs a stated reason.
- A value read from a file or an event reaches a shell through an environment variable, never
  through `${{ }}` inside a `run` script, unless it has been checked against a strict pattern.
- Changes to tokens, permissions or secrets never take a shortened review path.

### Article VI — Documentation
Every reusable workflow, its inputs and secrets, the checks it reports and what it requires of a
portal are documented in the README, and recorded in `CHANGELOG.md`, in the same pull request that
changes them. Comments in workflow files say why, not what, following
[`docs/contributing/standards/code-documentation.md`](docs/contributing/standards/code-documentation.md).
The README follows [`docs/contributing/standards/documentation.md`](docs/contributing/standards/documentation.md)
where it applies to a single-page README.

### Article VII — Dependency discipline
The actions the workflows use are dependencies of every portal. Dependabot proposes their updates,
and an update merges only after the example portal has passed every workflow with it. The example
portal pins FairDM to a release or a commit on FairDM's default branch, and moves it on purpose.

## Project articles

### Article VIII — One kind of caller
Every workflow serves portals and nothing else, and does the same thing for every portal. No input
switches a workflow's behaviour for a particular portal. A repository that does not fit writes its
own workflow. The one input, `working-directory`, exists so the example portal can live in a
subdirectory; portals leave it unset.

### Article IX — The platform comes from FairDM
The base image version and PostGIS version a workflow uses are read from the
`[tool.fairdm.platform]` table of the FairDM the portal pins in `uv.lock`. A workflow never names
one itself and never takes one as an input. When it cannot read them it fails, saying why.

### Article X — Interface stability
The interface is: the reusable workflow file names, their inputs and secrets, the names of the
checks they report, the permissions a caller must grant, and what a portal must provide. Before
1.0 a minor release may break it, and the release says what a portal changes. From 1.0, breaking it
needs a major release.

### Article XI — Tag and release discipline
Portals pin a tag, never `main`. A tag is never moved or deleted once published. A change reaches a
portal only through a new tag and a pull request in that portal.

## Articles not adopted

This repository ships no Django application. The example portal is a few lines of configuration
with no models, strings or behaviour of its own. These articles have no subject here, and become
live if that changes:

- Internationalization
- Data-model conventions (Django)
- Cohesion (Python)

[`docs/contributing/standards/django.md`](docs/contributing/standards/django.md) is kept with the
other standards for the example portal's few Django files.

## Quality bar

Read at plan and review. Applies to every change.
- `Lint Workflows` passes: actionlint and the workflow schema are clean.
- Every reusable workflow passes on the example portal.
- A change to the interface (Article X) updates the README and `CHANGELOG.md` in the same pull
  request, and the README's caller examples still work as written.
- The `Platform` job is identical in every workflow that has one.

## Non-negotiables

- The validation checks pass before a change merges. Nobody overrides a red check.
- The default branch requires one approval, and the author of a change never approves it.
- Dependabot auto-merge is permitted only while the ruleset requires the example portal's checks.

---

**Version**: 1.0.0 | **Ratified**: 2026-10-19 | **Last Amended**: 2026-10-19
