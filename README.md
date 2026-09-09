<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# PensaForma

A desktop application for planning and tracking work as a graph of workflows, for humans and AI agents alike. A workflow orders tasks; a project groups a run of them; a branch runs in parallel beside its workflow and may rejoin it. The graph is drawn as a mid-century retrofuturist flowchart; it is kept as plain files on your own disk, and is open to AI agents through a local Model Context Protocol (MCP) automation server while the application runs.

## Status

Specification stage. The repository holds the specification before it holds the code: the documents in [`docs/specification/`](docs/specification/) are written to be complete enough that an implementation can be built from them alone. The application is written in Rust; the Cargo workspace lands with the first implementation milestone.

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

The Cargo workspace is not here yet; it lands with the first implementation milestone (see the [implementation plan](docs/specification/implementation-plan.md)).

## The documents

Start with [`docs/northstar.md`](docs/northstar.md), the statement of what the application is for; everything else is downstream of it. The documents are indexed in [`docs/README.md`](docs/README.md), and the specification's reading order in [`docs/specification/README.md`](docs/specification/README.md).

## Building and testing

Not yet applicable. The build and test instructions arrive with the code.

## Releasing

Tag-driven, per the [ParkviewLab handbook](https://github.com/ParkviewLab/handbook/blob/main/docs/releases.md): `git bump` then `git release` from `main`; per-OS installers attach to the GitHub Release. The release workflow lands with the first release.

## License

PensaForma is dual-licensed: the code is free software under **AGPL-3.0-or-later** by default, with a **commercial license** available as an alternative for closed-source use without the AGPL's obligations. Documentation is **CC-BY-4.0**.

See [LICENSING.md](LICENSING.md) for the full picture and the commercial-license contact. Canonical per-license texts live in [`LICENSES/`](LICENSES/) ([REUSE](https://reuse.software)-compliant).

---
<sub>© 2026 Gary Frattarola · Code under [AGPL-3.0-or-later](LICENSE), docs under [CC-BY-4.0](LICENSES/CC-BY-4.0.txt)</sub>
