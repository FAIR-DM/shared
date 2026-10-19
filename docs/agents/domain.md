# Domain docs layout

Single-context layout:

- **`CONTEXT.md`** at the root is the glossary: portal, platform, base images, caller workflow,
  example portal, pin tag and the rest. Issues and reviews use its terms.
- **`docs/adr/`** holds one file per standing decision, once there is one. A decision is changed by
  superseding its record, never by contradicting it quietly.
- **`README.md`** is for portal maintainers: what each workflow does, what a portal must provide,
  and the caller files to copy.

FairDM's side of the contract, the `[tool.fairdm.platform]` table and the base images, is
documented in FairDM itself.
