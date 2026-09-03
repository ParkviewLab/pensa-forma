<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# Implementation plan

The order in which to build the application from this specification, as
milestones with what each delivers and what proves it. Each milestone is a
sequence of pull requests into `develop`, and each ends with the tests the
[testing](testing.md) document names for its crates passing. The plan is an
order, not a schedule.

## 0. The workspace

Create the Cargo workspace of the [architecture](architecture.md): the six
crates, empty, with `[workspace.package].version` at `0.1.0-dev0`, the
toolchain pin, and `test-rust.yml` in CI running format, clippy, and tests.
Add the `checks` job to the required status checks on `develop`.

Proves: CI green on an empty workspace.

## 1. The model

`model`: the record types with serde derivations, the id minter, the
seventeen invariants as one checker, the reverse index built at load, and
every mutation the [catalogue](command-catalogue.md) names, each with its
precondition and refusal text. The worked instance as a fixture. The
property-test generator of legal domains.

Proves: every invariant test in both directions; every mutation as a
property test; the catalogue's required properties; gap split and merge
exhaustively.

## 2. The store and the command layer

`store`: the data directory, the library, domain directories and their
labels, note files, bookmarks, settings, view state, the atomic write, path
safety. `command`: the pipeline with its lock, the closed set of refusals,
the revision check, the undo slot, notification, the reads, and the outline
renderer.

Proves: the store and command-layer tests, on a temporary library; the
canonical fixture round-trips byte for byte.

## 3. The layout engine

`layout`: heights by longest path, the air rule, lanes by the band packer,
the laterals with the fan split, junctions, underpass detection, folding, the
repair pass, and the output structure.

Proves: the required properties over generated domains; the golden masters
snapshotted, the [worked example](worked-example.md)'s numbers reproduced to
the pixel.

## 4. The canvas

`app`, first half: the eframe shell with the header bar, the domain switcher,
the theme toggle, and the zoom cluster; the canvas painting every mark of the
[mark geometry](mark-geometry.md) from the layout's output; measurement
through the text engine with soft hyphens; the camera; the flagged-only mode;
the sample domains seeded on an empty library.

Proves: the golden-path tests for the silhouettes; a screenshot of each
sample domain in both themes, reviewed by eye against the geometry and the
layout documents. This is the first milestone with something to look at, and
looking is part of the acceptance.

## 5. Interaction

`app`, second half: hit regions, the context menus with their inventories,
the dialogs with their exact strings, the glyph clicks, the flag double-click,
and drag-and-drop with trial-application legality, the two indicators, the
ghost, auto-pan, and the stale-drop dialog. Undo through the Edit menu.

Proves: the drop-target enumeration test against the command layer; the
gesture tests through the accessibility tree; the dialog strings verbatim.

## 6. Notes and the log

The note editor with its source pane, toolbar, preview, math, divider,
autosave, and reconciliation; the activity log panel with add, edit, and
delete.

Proves: the editor's reconciliation cases; the log commands' undo behaviour.

## 7. The automation server

`server`: the loopback listener, the stateless Streamable HTTP endpoint, the
Host and Origin allowlist, `/health`, the scope tiers by non-registration,
every tool over the catalogue, the two prompts, the instructions text, the
live-view notification, the pill, and the single-instance lock.

Proves: the end-to-end tests with an MCP client on an ephemeral port.

## 8. About, licences, export, bookmarks

The About window with its release check, the Open Source Licenses window
reading the generated inventory, markdown export, bookmarks with the node-set
framing.

Proves: the remaining chrome tests; a full pass through every menu item on a
sample domain.

## 9. Packaging and the first release

`cargo-packager` configuration for the three platforms, the application
icon, macOS signing and notarisation in CI, the generated licence notices,
the release workflow in the handbook's shape, and the dev-tools Cargo kind so
that `git bump` and `git release` drive the repo. Then the first release.

Proves: installers for three platforms from a tag, the About window reporting
the version, and the handbook's release gate passing.

## After

Daily use. The in-flight ideas are weighed against what daily use shows,
and the proposals in the decisions record are ruled on as they come up.
