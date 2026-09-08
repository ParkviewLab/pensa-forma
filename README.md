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

## The documents

Everything of substance is in [`docs/`](docs/README.md): the
[northstar](docs/northstar.md), the statement of what the application is for,
which everything else is downstream of; the in-flight ideas; the contributing
guide; and the specification itself in
[`docs/specification/`](docs/specification/README.md), whose own index gives
the reading order. Each directory carries its own index, and each index lists
only what that directory holds.

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
