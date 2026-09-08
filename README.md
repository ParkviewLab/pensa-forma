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
automation server while the application runs.

## Status

Specification stage. The repository holds the specification before it holds
the code: the documents in [`docs/`](docs/) are written to be complete enough
that an implementation can be built from them alone. The application is
written in Rust; the Cargo workspace lands with the first implementation
milestone.

## The documents

Start with [`docs/northstar.md`](docs/northstar.md), the statement of what
the application is for; everything else is downstream of it.

| Document | What it is the authority for |
|---|---|
| [glossary.md](docs/glossary.md) | The vocabulary every document, menu, and tool speaks |
| [northstar.md](docs/northstar.md) | Intent: four intents, their tensions, twelve axioms |
| [decisions.md](docs/decisions.md) | Settled decisions with their reasoning; proposals awaiting a ruling |
| [structural-model.md](docs/structural-model.md) | What exists, identity, the record, the seventeen invariants, the worked instance |
| [command-layer.md](docs/command-layer.md) | The one write path: the pipeline, validation, undo, refusals |
| [command-catalogue.md](docs/command-catalogue.md) | Every command: arguments, tier, effect, refusal text, log entry |
| [interaction.md](docs/interaction.md) | Drag-and-drop: handles, targets, legality by trial application |
| [layout-engine.md](docs/layout-engine.md) | Where every mark goes: heights, lanes, laterals, junctions, folding |
| [mark-geometry.md](docs/mark-geometry.md) | How every mark is drawn, with golden masters |
| [ui-chrome.md](docs/ui-chrome.md) | The shell: window, header, menus, dialogs, note editor, log panel |
| [persistence.md](docs/persistence.md) | Locations, the on-disk record, notes, bookmarks, settings, atomic writes |
| [automation-server.md](docs/automation-server.md) | The MCP server: binding, hardening, tiers, tools, prompts, live view |
| [architecture.md](docs/architecture.md) | The workspace, threads, rendering, packaging, the crate inventory |
| [worked-example.md](docs/worked-example.md) · [.html](docs/worked-example.html) | One domain carried through record, layout, and drawing: the fixture to build against |
| [testing.md](docs/testing.md) | What is tested and how |
| [implementation-plan.md](docs/implementation-plan.md) | The milestones, in order |
| [in-flight_ideas.md](docs/in-flight_ideas.md) | Questions under consideration |

The mark geometry and the UI chrome each have a designed HTML sibling beside
them, rendering the marks and the widgets from the same data, so the target
can be seen as well as read. Markdown is canonical; if the two drift, the
Markdown wins.

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
