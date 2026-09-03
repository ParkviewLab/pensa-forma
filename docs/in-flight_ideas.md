<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# In-flight ideas

*Candidates under consideration. Each is a question, not a commitment: to
research, weigh against the [northstar](northstar.md), and either promote to
a plan or drop. Nothing here is acted on silently. Settled matters are in the
[decisions record](decisions.md); the proposals awaiting a ruling are listed
there too, not here.*

## Design

### Fractional sort keys for the three orderings

Ordered arrays of ids (D10) are legible and simple; two writers inserting in
one list at once conflict at the revision check and one retries. If
concurrent reordering by a person and an agent proves painful, fractional
keys let both land, at the cost of readability and a rebalancing rule.

### Reflecting external edits live

The application reads the record afresh on every command, so a file edited
in a text editor is seen at the next command, but not before. A filesystem
watcher would re-render on the edit itself. It adds a dependency and a
reconciliation path for the note editor; worth it if hand-editing turns out
to be a habit.

### Notes as MCP resources

The automation server offers no resources (automation server, section 9). If
any earn a place it is notes: a note is genuinely a document with a filename,
and a stale copy of prose costs little. A second surface to keep in step with
the first, so deferred until a client needs it.

### Front matter in note files

A note file carries only the node's prose; its title lives on the node. Front
matter (the title, the node id, the kind) would let other tools read a note
in context, at the cost of the file no longer being "just markdown" and of a
second copy of the title that can drift. The automation server is the
intended channel for other tools; revisit if a file-level consumer appears.

### A per-install bearer token for the automation server

Deferred from the first version (automation server, section 4). Generated
once, kept in settings, shown in the pill, passed as a header; composes with
the loopback binding and the Host and Origin allowlist.

### A server mode over a LAN

One authoritative store on a LAN host serving several windows would fall out
of the single command interface (a remote-client adapter in place of the
file-backed one), but assumes a reachable host and a live-update channel.
Not built on speculation.

### A synchronisation capability over the files

Reusing an external synchroniser (a synced folder, a git remote) over the
library, with conflict copies rather than merging, keeps axiom 8 intact; a
sync of the application's own would be a separate, optional, off-by-default
capability. Not before the application is in daily use.

### The atmosphere burst

The mark geometry defines an optional four-plus-spoke starburst as a
background decoration and draws none. If a real theming pass wants
atmosphere, scatter them procedurally from the drawing's bounds, seeded by
the domain id so they stay put.

## Tooling

### Release packaging for a Rust desktop app

How per-OS installers get built and attached to the GitHub Release. The
candidates are `cargo-dist` (which generates the dmg, msi, and AppImage
targets and can drive the release itself) and a bespoke `release-rust.yml` in
the handbook's shape (gate, a three-OS build matrix, the changelog job) with
`cargo-packager` for the bundles and `apple-codesign` for macOS signing and
notarisation from any CI runner. The [architecture](architecture.md) assumes
the latter; whichever is chosen must slot into the tag → CI → GitHub Release
flow the handbook establishes for desktop apps. Also open: whether Windows
signing is wanted for the first releases.

### The dev-tools version helpers do not read `Cargo.toml`

`_sot.sh` in [dev-tools](https://github.com/ParkviewLab/dev-tools) detects
only `pyproject.toml`, `package.json`, and `VERSION.txt`, so `git bump` and
`git release` cannot drive this repo yet. A Cargo kind is needed: detect
`Cargo.toml`, read and write `[workspace.package].version` (and
`[package].version` for a single crate). That is a dev-tools change and its
own PR; the handbook's rule against hand-typing a version argues against a
one-off manual exception for the first release.

### A Rust profile in the handbook

This is the family's first Rust repo. The conventions it settles (the rustfmt
and clippy gates, the `rust-toolchain.toml` pin, the `test-rust.yml` shape,
the version guard's Cargo branch, the workspace layout) are recorded only here
for now. Once proven, propose a `rust-tooling.md` in the handbook, analogous
to `node-tooling.md`, so the next Rust repo starts from the same shape.

### Designed HTML for the northstar

The handbook's dual-track convention asks for a designed HTML companion to
the northstar. The two HTML siblings that matter most to an implementer, the
mark geometry's and the chrome's, come first; the northstar's follows.
