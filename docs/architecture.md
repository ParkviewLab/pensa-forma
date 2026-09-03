<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# Architecture

The authority for how the application is put together as software: the
Cargo workspace and its crates, what each depends on, the threading model
between the interface and the automation server, the rendering pipeline, the
text and note pipeline, packaging and signing, and the crate inventory with
licences. The behaviour each part implements is specified elsewhere; this
document says where that behaviour lives and how the parts meet.

---

## 1. One language, one process, one authority

The application is a single Rust binary. The interface is an immediate-mode
GUI on egui hosted by eframe (D25); the automation server is an MCP endpoint
in the same process; the model, the store, and the command layer are shared
crates that both the interface and the server call. There is no second
process, no bridge, and no serialisation of task operations between layers:
the model has exactly one home.

## 2. The workspace

Six crates (P6), each with one job, arranged so that dependencies point one
way:

```
crates/
  model/      the record types, ids, the invariant checker, and every mutation
  store/      the filesystem: locations, path safety, atomic writes, settings, view state
  command/    the command layer: the pipeline, the catalogue, undo, notification, reads
  layout/     heights, lanes, junctions, underpasses, folding: record in, geometry out
  server/     the MCP server: transport, hardening, tools, prompts, scope tiers
  app/        the eframe application: chrome, canvas, marks, interaction, note editor, dialogs
```

| Crate | Depends on | Knows nothing of |
| --- | --- | --- |
| `model` | `serde`, `thiserror` | files, drawing, the protocol |
| `store` | `tempfile`, `directories`, `serde_json`, `json5` | node kinds, invariants |
| `command` | `model`, `store` | drawing, the protocol |
| `layout` | `model` | files, drawing APIs, the protocol |
| `server` | `command`, `rmcp`, `axum`, `tokio` | drawing |
| `app` | every crate above, `eframe`, `egui` | the protocol's wire format |

`model` is pure: no I/O, no clock beyond the id minter's, no toolkit types,
which is what makes its invariants and mutations testable headless and lets
the interface's trial applications (interaction, section 5) run thousands of
times a second. `store` is the only crate that touches the filesystem, and it
knows nothing about what it stores beyond "a record's text" and "a note's
text". `command` is the only crate that both understands the model and
writes files, which is the one write path. `layout` is pure too: a validated
record and a map of card sizes in, positions out. `server` and `app` are the
two callers of `command` and never call each other.

The binary is `crates/app`'s target, named `pensa-forma`. The version is
`[workspace.package].version` in the root `Cargo.toml`, inherited by every
member with `version.workspace = true`, and the application reads it at
runtime from `env!("CARGO_PKG_VERSION")`; it is never written anywhere else.

The workspace pins its toolchain in `rust-toolchain.toml` and uses edition
2024. `cargo fmt`, `cargo clippy --all-targets -- -D warnings`, and `cargo
test` are the gates, run locally and in CI.

## 3. Threads and the lock

Two threads matter.

The **frame thread** is eframe's: it runs the event loop, paints each frame,
and executes every command the interface issues, synchronously, inside the
frame in which the gesture completed. A command costs one read, one apply,
one validate, and one atomic write, a millisecond or so, so it is run inline
rather than deferred; the map re-renders on the next frame from the returned
record.

The **server thread** hosts a tokio runtime on which the HTTP listener and
the MCP handler run. Every tool call ends in a call into the command layer.

The command layer holds one mutex around the whole pipeline (command layer,
section 4), and both threads take it. The frame thread holds it for one
command; the server thread holds it for one tool call. Neither holds it
across a frame or across a request. That is the whole of the concurrency
design: no channel, no actor, no transactional state, because there is
nothing to coordinate but "one at a time".

Two channels cross between the threads. The server sends a `DomainChanged
{ id, revision }` notification to the frame thread after a successful
automation write, through a channel the frame thread drains at the start of
each frame; on receipt it schedules a re-render and requests a repaint. The
frame thread sends the server `Start`, `Stop`, and `SetScope` control
messages from the automation pill, and reads the server's status from a
shared atomic state for the pill's dot and tooltip.

The frame loop is otherwise idle when nothing changes: eframe repaints on
input, on a repaint request, and otherwise not, so an idle application costs
nothing.

## 4. The rendering pipeline

Each frame in which the record or the view has changed runs, in order:

1. **Read.** The record for the open domain, as returned by the last command
   or notification. The interface holds this record between frames as the
   thing it draws; it is not a cache the command layer consults.
2. **Measure.** Every card's height from the text engine: the label's line
   count under the card's inner width with soft-hyphen break opportunities,
   plus the fixed metrics of the mark geometry. Measurement is a pure
   function of the fonts and the text, so it is memoised by (kind, title,
   status, here, flagged) and recomputed only for cards whose inputs changed.
3. **Layout.** The `layout` crate, given the record, the fold set, and the
   measured sizes, returns anchors, tracks, junctions, underpasses, bounds,
   and conflicts.
4. **Paint.** The marks, in the mark geometry's paint order, transformed by
   the camera into screen coordinates before flattening, so that curves are
   subdivided at model scale and text is laid out at its screen size. Each
   silhouette is flattened to a point list and filled through one helper that
   routes concave shapes through a tessellator and convex ones through the
   painter's own fill (mark geometry, implementation notes).
5. **Interact.** Each card allocates a rectangle and asks the toolkit for its
   response (hover, click, double-click, drag start, drag, drag stop); each
   junction halo and each drop target is a hit region tested against the
   pointer. Hover and drag looks are chosen per frame from that state, since
   an immediate-mode toolkit retains no styling to toggle.

Steps 2 and 3 run only when the record, the fold set, or the fonts change;
steps 4 and 5 run every painted frame. The camera transform is applied by
mapping coordinates, not by a layer transform, so vector marks stay crisp and
text is rasterised at its true size at every zoom.

Fonts are bundled as bytes and installed into the toolkit's font definitions
at start: the UI face, the display face, and the platform's monospace face by
name, per the chrome's appendix. Card labels are soft-hyphenated by a
Knuth-Liang hyphenator at measure time; where the text engine does not treat
the soft hyphen as a break opportunity, the measure step chooses the wrap
points itself and lays out the label line by line.

## 5. The note pipeline

The note editor is a native text-editing widget over a rope buffer, with the
toolkit's own undo and input-method support, and the preview is a markdown
renderer to native widgets. Markdown is parsed by a CommonMark parser with the
table, strikethrough, and task-list extensions. Math is a preview concern
only: the source pane holds plain text, and the preview recognises `$…$` and
`$$…$$` runs, typesets each to a vector image through a native TeX layout
engine, caches the result keyed by source, size, and colour, and shows a
malformed formula as visible error text. The editor's autosave, debounce,
reconciliation, and dialogs are the chrome's.

The math typesetter's crates are vendored into the tree, so the build does
not depend on a network registry serving them, with their own licence
headers intact and their bundled fonts under the fonts' own licence.

## 6. The automation server

The `server` crate builds the tool surface from the catalogue at the
configured tier when a session initialises, hosts the Streamable HTTP
transport on an axum listener bound to loopback, applies the Host and Origin
allowlist to every request, and answers `/health`. Tool parameters are typed
Rust structures deriving their JSON schemas, so the schema an agent sees and
the value the code receives cannot disagree.

## 7. Packaging and signing

A release builds the binary for macOS, Windows, and Linux and packages each
into an installer: a `.dmg` for macOS, an NSIS installer for Windows, an
AppImage and a `.deb` for Linux, produced by `cargo-packager` from one
configuration. The macOS build is signed with a Developer ID Application
certificate and notarised through an App Store Connect API key, using a pure
Rust signing tool that runs on any CI platform; Windows and Linux ship
unsigned in the first releases. The application icon is authored once at
1024×1024 and the packager derives the platform formats. Bundled fonts and the
generated third-party licence notices travel in the bundle's resources, and
the Open Source Licenses window reads them from there.

The release flow itself (tag-driven, a gate, a build matrix, the changelog
job, the back-merge) follows the ParkviewLab handbook; the workflow files land
with the first release.

## 8. The crate inventory

Every runtime dependency is MIT and/or Apache-2.0 licensed, which is
compatible with distributing an AGPL-3.0-or-later binary; the two exceptions
are noted. Versions are those current when this document was written and are
pinned in `Cargo.lock`; bump deliberately.

| Crate | Role | Licence |
| --- | --- | --- |
| `eframe`, `egui`, `epaint` | the application shell, the immediate-mode GUI, and its painter | MIT OR Apache-2.0 |
| `egui_commonmark` | the note preview's markdown widget | MIT OR Apache-2.0 |
| `pulldown-cmark` | the markdown parser beneath it | MIT |
| `lyon_tessellation` | filling the concave silhouettes | MIT OR Apache-2.0 |
| `hyphenation` | Knuth-Liang soft-hyphen points for card labels | MIT OR Apache-2.0 |
| `ratex-layout`, `ratex-svg` (vendored) | in-note math, TeX source to vector | MIT, with OFL-1.1 fonts |
| `serde`, `serde_json` | the record's serialisation and canonical write | MIT OR Apache-2.0 |
| `json5` | the tolerant read | MIT |
| `tempfile` | the atomic write-to-temporary-then-rename | MIT OR Apache-2.0 |
| `directories` | the platform data directory | MIT OR Apache-2.0 |
| `thiserror`, `anyhow` | typed errors in the crates, plumbing at the edge | MIT OR Apache-2.0 |
| `rmcp` | the MCP server SDK | Apache-2.0 |
| `axum`, `tokio` | the loopback HTTP listener and the server's runtime | MIT |
| `ureq` | the About window's release check, blocking, with a timeout | MIT OR Apache-2.0 |
| `rfd` | native file and folder dialogs | MIT |
| `open` | opening external links in the system browser | MIT |
| `arboard` | the system clipboard | MIT OR Apache-2.0 |
| `log`, `env_logger` | logging | MIT OR Apache-2.0 |
| `egui_kittest` (dev) | interface tests through the accessibility tree | MIT OR Apache-2.0 |
| `insta` (dev) | snapshot tests for layout and geometry | Apache-2.0 |
| `proptest` (dev) | property tests over the invariants | MIT OR Apache-2.0 |
| `cargo-packager` (tool) | the installers | Apache-2.0 OR MIT |
| `apple-codesign` (tool) | macOS signing and notarisation from any CI platform | MPL-2.0 |

The two exceptions: `apple-codesign` is a build-time tool, not linked into
the binary, so its licence does not touch the application's; and the
vendored math crates bundle fonts under the SIL Open Font License 1.1, the
same class as the interface's own bundled faces, which keep their upstream
licence and are never relabelled.

An optional filesystem watcher, for reflecting external edits live, would
add `notify` (CC0-1.0); it is an in-flight idea, not a dependency.
