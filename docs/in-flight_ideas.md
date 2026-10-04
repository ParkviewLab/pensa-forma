<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# In-flight ideas

*Candidates under consideration. Each is a question, not a commitment: to research, weigh against the [northstar](northstar.md), and either promote to a plan or drop. Nothing here is acted on silently. Settled matters are in the [decisions record](specification/decisions.md); the proposals awaiting a ruling are listed there too, not here.*

## Design

### Fractional sort keys for the three orderings

Ordered arrays of ids (D10) are legible and simple; two writers inserting in one list at once conflict at the revision check and one retries. If concurrent reordering by a person and an agent proves painful, fractional keys let both land, at the cost of readability and a rebalancing rule.

### Reflecting external edits live

The application reads the record afresh on every command, so a file edited in a text editor is seen at the next command, but not before. A filesystem watcher would re-render on the edit itself. It adds a dependency and a reconciliation path for the note editor; worth it if hand-editing turns out to be a habit.

### Notes as MCP resources

The automation server offers no resources (automation server, section 9). If any earn a place it is notes: a note is genuinely a document with a filename, and a stale copy of prose costs little. A second surface to keep in step with the first, so deferred until a client needs it.

### Front matter in note files

A note file carries only the node's prose; its title lives on the node. Front matter (the title, the node id, the kind) would let other tools read a note in context, at the cost of the file no longer being "just markdown" and of a second copy of the title that can drift. The automation server is the intended channel for other tools; revisit if a file-level consumer appears.

### A per-install bearer token for the automation server

Deferred from the first version (automation server, section 4). Generated once, kept in settings, shown in the pill, passed as a header; composes with the loopback binding and the Host and Origin allowlist. It would close the one gap those leave: any process on the same machine can reach the port.

Its standing in the protocol, checked against the specification's 2026-07-28 revision: authorization is optional in MCP, and where an HTTP server requires it the specification's framework is OAuth 2.1, in which the token travels as `Authorization: Bearer <token>` but is issued by an authorization server the MCP server advertises, obtained through a browser flow, and bound to the server as its audience; a client must not send a token from anywhere else. A static per-install secret uses the same header and sits outside that framework. It works with clients that let a person configure a fixed header when registering a server, which is a client feature rather than conformance. The conformant alternative is for the application to act as its own authorization server, which the specification permits, at the cost of implementing the browser flow; the draft client-credentials extension is the nearest thing to a pre-shared secret and may be the fit if it stabilises. The choice, when it is made, is between the pragmatic header and the conformant flow.

### A server mode over a LAN

One authoritative store on a LAN host serving several windows would fall out of the single command interface (a remote-client adapter in place of the file-backed one), but assumes a reachable host and a live-update channel. Not built on speculation.

### A synchronisation capability over the files

Reusing an external synchroniser (a synced folder, a git remote) over the library, with conflict copies rather than merging, keeps axiom 8 intact; a sync of the application's own would be a separate, optional, off-by-default capability. Not before the application is in daily use.

### The atmosphere burst

Googie's style document defines an optional four-plus-spoke starburst as a background decoration and draws none; it is Googie's alone. If a real theming pass wants atmosphere, scatter them procedurally from the drawing's bounds, seeded by the domain id so they stay put.

### Render parameters as settings

A few sliders in a settings dialog for the values that most govern the look of a drawing: the card width, the standard trunk-edge length, the angle of the laterals' ramps, perhaps the gutter. The layout is already a function of these constants (layout engine, section 12), and they are view state, so they would live in `settings.json` and never reach the record or an agent. The three are coupled: the incoming and outgoing edges must clear a card's near corner, so `L` is derived from the card's half-width, the angle, and the junction margin, and a dialog would derive or clamp rather than offer three free sliders; `L` also has a floor from the interaction document, where every drop zone is at least `L` tall. The angle would be offered within a limited range; it governs Googie's route, from which `L` is derived, and every other style's route must still clear the cards at the `L` it gives. Every style's silhouettes are specified in a 188-wide box, so a width slider needs them parametric in all five, with the golden masters kept at the defaults and property tests across the ranges. Not before the drawing is in daily use at the defaults.

### Characters no bundled face holds

The application ships every face it uses and falls back to no platform font, so a character none of its faces holds (Chinese or other CJK text in a note, an emoji, a symbol such as ⌘) shows as an empty box. The first release accepts that. Two remedies are open. One is to ship a face of wide coverage, such as Noto Sans, at a cost in size that full CJK coverage puts at tens of megabytes (unmeasured). The other is to use the platform's fonts for those characters alone, so that every character the bundled faces hold is still set in them; egui ships a helper for this (`egui_system_fonts`, built on `fontique`), which finds an installed face for a missing character through the operating system's own fallback.

### Fröbel's density on a large domain, and its to-do colour

On the design page's Large domain at 60 % and below, Fröbel's white cards with thin outlines read as busier than the other styles, and its cadmium yellow for to do is the weakest of its three state colours on white. Whether a heavier outline at low zoom, an earlier tint, or a deeper yellow would serve better is open; the specification carries the design page's values until a comparison is made.

### Suuronen's dark palette

Suuronen's dark palette was derived from its light palette rather than tuned by eye, as the other styles' were. It is to be compared in use and tuned if it reads poorly; the derivation is recorded in its style document as the constraint any retuning keeps.

### Suuronen's adjacent flagged pieces

Suuronen draws a flag as two frames standing off the node. Where two flagged nodes stand a shut gap apart, their frames come close to each other and may read as one. How such neighbours should be drawn is open.

### Fröbel's flag in the dark at fit

In Fröbel's dark theme, zoomed out to fit, the flag circle's panel fill under its ink edge may read too faintly against the tinted bodies. Whether it needs a different treatment at low zoom in the dark is open.

## Tooling

What this repository settles as the family's first in Rust is fed back to the handbook and to dev-tools, in this order: the dev-tools change before the first release, which cannot be cut without it; the packaging choice at that release; and the handbook's Rust profile after it, once the conventions have carried a release.

### Release packaging for a Rust desktop app

How per-OS installers get built and attached to the GitHub Release. The candidates are `cargo-dist` (which generates the dmg, msi, and AppImage targets and can drive the release itself) and a bespoke `release-rust.yml` in the handbook's shape (gate, a three-OS build matrix, the changelog job) with `cargo-packager` for the bundles and `apple-codesign` for macOS signing and notarisation from any CI runner. The [architecture](specification/architecture.md) assumes the latter; whichever is chosen must slot into the tag → CI → GitHub Release flow the handbook establishes for desktop apps. Also open: whether Windows signing is wanted for the first releases.

### The dev-tools version helpers do not read `Cargo.toml`

`_sot.sh` in [dev-tools](https://github.com/ParkviewLab/dev-tools) detects only `pyproject.toml`, `package.json`, and `VERSION.txt`, so `git bump` and `git release` cannot drive this repo yet. A Cargo kind is needed: detect `Cargo.toml`, read and write `[workspace.package].version` (and `[package].version` for a single crate). That is a dev-tools change and its own PR; the handbook's rule against hand-typing a version argues against a one-off manual exception for the first release.

### A Rust profile in the handbook

This is the family's first Rust repo. The conventions it settles (the rustfmt and clippy gates, the `rust-toolchain.toml` pin, the `test-rust.yml` shape, the version guard's Cargo branch, the workspace layout) are recorded only here for now. Once proven, propose a `rust-tooling.md` in the handbook, analogous to `node-tooling.md`, so the next Rust repo starts from the same shape.
