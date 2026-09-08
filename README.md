<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# PensaForma

A desktop application for planning and tracking work as a graph of workflows,
for humans and AI agents alike. A workflow orders tasks; a project groups a run
of them; a branch runs in parallel beside its workflow and may rejoin it. The
graph is drawn as a mid-century retrofuturist systems diagram, a
Googie-inspired Atomic Age flowchart laid out like a retro transit map; it is
kept as plain files on your own disk, and is open to AI agents through a local
Model Context Protocol (MCP) automation server while the application runs.

## Status

Specification stage. The repository holds the specification before it holds
the code: the documents in [`docs/specification/`](docs/specification/) are written to be complete enough
that an implementation can be built from them alone. The application is
written in Rust; the Cargo workspace lands with the first implementation
milestone.

## What is in this repository

| Entry | What it holds |
|---|---|
| [`docs/`](docs/README.md) | Everything of substance: `docs/northstar.md` (the intent), `docs/in-flight_ideas.md` (the open questions), `docs/CONTRIBUTING.md` (how to work here), and the `specification/` directory |
| [`docs/specification/`](docs/specification/README.md) | The specification: the documents an implementation is built from, their HTML twins, and the worked example |
| [`scripts/`](scripts/) | `worked_example.py`, which generates the worked example from the specification's rules; `generate_changelog.py`, which the release flow uses |
| [`.github/workflows/`](.github/workflows/) | Continuous integration: the REUSE licensing check and the version guard |
| [`LICENSING.md`](LICENSING.md), [`LICENSE`](LICENSE), [`LICENSES/`](LICENSES/), [`REUSE.toml`](REUSE.toml) | The licensing terms, the license texts, and the per-path license map |
| [`CHANGELOG.md`](CHANGELOG.md), [`cliff.toml`](cliff.toml) | The changelog and the configuration that generates it from pull-request titles |
| [`AGENTS.md`](AGENTS.md), [`CLAUDE.md`](CLAUDE.md) | The conventions an AI collaborator follows here, pointing at the ParkviewLab handbook |

The Cargo workspace is not here yet; it lands with the first implementation
milestone (see the [implementation plan](docs/specification/implementation-plan.md)).

## The documents

Start with [`docs/northstar.md`](docs/northstar.md), the statement of what
the application is for; everything else is downstream of it. Each directory
below also carries an index of its own.

### In `docs/`

The intent, the open questions, and how to work in this repository.

| Document | What it is |
|---|---|
| [docs/northstar.md](docs/northstar.md) | Intent: four intents, their tensions, twelve axioms; the authority where intent and structure seem to disagree |
| [docs/in-flight_ideas.md](docs/in-flight_ideas.md) | Questions under consideration, each a candidate to weigh against the northstar and promote or drop |
| [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) | How to work in this repository: branches, pull requests, releases |

### In `docs/specification/`

The specification: complete enough that an implementation can be built from
these documents alone. Its [index](docs/specification/README.md) gives the
reading order.

| Document | What it is the authority for |
|---|---|
| [glossary.md](docs/specification/glossary.md) | The vocabulary every document, menu, and tool speaks |
| [decisions.md](docs/specification/decisions.md) | Every settled decision with its reasoning, by number |
| [structural-model.md](docs/specification/structural-model.md) | What exists, identity, the record, the eighteen invariants, the worked instance |
| [command-layer.md](docs/specification/command-layer.md) | The one write path: the pipeline, validation, undo, refusals |
| [command-catalogue.md](docs/specification/command-catalogue.md) | Every command: arguments, tier, effect, refusal text, log entry |
| [interaction.md](docs/specification/interaction.md) | Drag-and-drop: handles, targets, legality by trial application |
| [layout-engine.md](docs/specification/layout-engine.md) | Where every mark goes: heights, lanes, laterals, junctions, folding |
| [mark-geometry.md](docs/specification/mark-geometry.md) · [.html](docs/specification/mark-geometry.html) | How every mark is drawn, with golden masters, and the drawn twin |
| [ui-chrome.md](docs/specification/ui-chrome.md) · [.html](docs/specification/ui-chrome.html) | The shell: window, header, menus, dialogs, note editor, log panel, and the drawn twin |
| [persistence.md](docs/specification/persistence.md) | Locations, the on-disk record, notes, bookmarks, settings, atomic writes |
| [automation-server.md](docs/specification/automation-server.md) | The MCP automation server: binding, hardening, tiers, tools, prompts, live view |
| [architecture.md](docs/specification/architecture.md) | The workspace, threads, rendering, packaging, the crate inventory |
| [worked-example.md](docs/specification/worked-example.md) · [.html](docs/specification/worked-example.html) | One domain carried through record, layout, and drawing: the fixture to build against |
| [testing.md](docs/specification/testing.md) | What is tested and how |
| [implementation-plan.md](docs/specification/implementation-plan.md) | The milestones, in order |

The mark geometry and the UI chrome each have a designed HTML sibling beside
them, rendering the marks and the widgets from the same data, so the target
can be seen as well as read; the worked example's sibling is generated from
the rules by `scripts/worked_example.py`. Markdown is canonical; if the two
drift, the Markdown wins.

## Building and testing

Not yet applicable. The build and test instructions arrive with the code.

## Releasing

Tag-driven, per the
[ParkviewLab handbook](https://github.com/ParkviewLab/handbook/blob/main/docs/releases.md):
`git bump` then `git release` from `main`; per-OS installers attach to the
GitHub Release. The release workflow lands with the first release.

## License

PensaForma is dual-licensed: the code is free software under
**AGPL-3.0-or-later** by default, with a **commercial license** available as an
alternative for closed-source use without the AGPL's obligations.
Documentation is **CC-BY-4.0**.

See [LICENSING.md](LICENSING.md) for the full picture and the commercial-license
contact. Canonical per-license texts live in [`LICENSES/`](LICENSES/)
([REUSE](https://reuse.software)-compliant).

---
<sub>© 2026 Gary Frattarola · Code under [AGPL-3.0-or-later](LICENSE), docs under [CC-BY-4.0](LICENSES/CC-BY-4.0.txt)</sub>
