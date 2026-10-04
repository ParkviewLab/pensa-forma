<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# Testing

What is tested, how, and what a passing suite proves. The tests are organised by the crate they exercise, and the most valuable of them are stated in the specification documents themselves as required properties; this document collects them and says how each is checked.

`cargo test` runs everything; CI runs it on every push and pull request, with formatting and clippy beside it.

---

## 1. The model

**The invariant checker is exercised in both directions.** For each of the nineteen invariants in the structural model, section 4, a test constructs a record that violates exactly that invariant and asserts the checker names it; and the worked instance of section 8 passes clean. The three refusals the worked instance lists are tests.

**Every mutation is a property test.** Using a generator that builds random legal domains (random workflows, projects nested properly, branches placed by the model's own rules, some open, some returning, here marks and flags scattered, every non-empty title distinct), each mutation is applied with random legal arguments and the result must satisfy every invariant; applied with random illegal arguments it must refuse with the documented code and leave its input untouched. The generator is itself checked: everything it produces passes the checker.

**The catalogue's required properties** (command catalogue, section 10) are property tests over the same generator: a command's subject is the only node whose log changed; every moved node keeps its fields except the ones the conversions change; no command creates a return; nothing is deleted for being empty.

**Gap split and merge** are tested exhaustively on the three insertion positions and on removal, against the structural model's section 2.4: which gap keeps its id, which lists move where, and that nothing detaches.

**The id minter** is tested for width, prefix, lowercase, monotonicity under a clock stepped backwards, and the counter's behaviour at the 1296th id in a millisecond.

**Titles** are tested four ways: the helper that keeps them unique yields `base-1` on a first collision and `base-2` on the next, and renumbers from the stripped base when a `-N` title collides; every title-setting mutation (`create_workflow`, `insert_task`, `wrap_run`, `open_branch`, `set_title`, `paste`), applied with a taken title, leaves every non-empty title in the domain distinct and reports the final title; a blank title yields `New task` or `New project` for a task or a project and stays empty for a workflow; and a paste of a clip into the domain it came from yields suffixed copies.

**Paste** is tested for exactness: a main workflow copied and pasted into an empty domain equals the original once ids are mapped, field for field (statuses, completion dates, here marks, flags, branch sides and orders, logs, and note texts), but for the one "Pasted." entry on its start node, and shares no id with it.

## 2. The store and the command layer

**The atomic write** is tested by interrupting it: a write whose rename step is made to fail must leave the old file intact and readable, and a temporary file left behind must be ignored by the next read.

**Tolerant read, canonical write** is tested by round-tripping the worked instance through a hand-edited JSON5 form (comments, unquoted keys, trailing commas) and asserting that the canonical output parses to the same data as the fixture in the persistence document, section 3, and that a second write of it is byte-identical to the first.

**The self-describing directory** is tested two ways: the persistence fixture validates against `domain.schema.json`, and every field in the structural model's tables is asserted to carry a `description` in the schema, so that a field added to the model without a description fails the build. Creating a domain on a temporary library is asserted to write the schema and the README beside the record, and a migration to rewrite them.

**Path safety** is tested with traversal attempts: a domain path outside the library root, a note filename with a separator, a sibling directory whose name begins with the root's, each refused.

**The pipeline** is tested end to end on a temporary library: each refusal code is provoked once; a refusal leaves the file byte-identical; a `stale` revision is refused; the revision increments by one per successful write; a command that writes a note file writes it before the record, verified by failing the record write and finding the orphan.

**Validation on load** is tested with a hand-edited record carrying two nodes with one title: opening it is refused with I19 and both ids named, and the file is byte-identical afterwards; the same test is run for one other invariant, to prove that the check on load is general.

**Undo** is tested for the slot's rules: filled by a `ui` command, not by an `automation` one; cleared by an automation write, by a window write that is not undoable (the first save of a note), by a domain switch, and by a delete; an undo restores the pre-image, its revision aside, including the log, and writes the stored revision plus one, so a change from 7 to 8 undone leaves 9; a second undo in a row does nothing; and an undo after another write is refused as stale.

## 3. The layout engine

**The required properties** (layout engine, section 11) are each a test over the generator's domains, run on the layout's output: no unmarked proper crossing; no lateral inside a card except as reported; every lateral within the rectangle its ends span, in every style's route; in Googie's route every segment flat or at the ramp angle; the two fixed edges to the pixel; sibling start nodes level; a tall branch stretching only above its return; lane order following the side lists; determinism under permuted key order; monotonicity under an added card.

**Golden masters.** A small set of hand-built domains (the [worked example](worked-example.md), whose record, positions, and lateral point lists are the first fixture; the structural model's worked instance; one with a shared branch point carrying three siblings on each side; one with an open branch outermost and a returning branch inside it; one with a folded project, and one with a folded branch workflow) has its layout output snapshotted, so a change in geometry is a visible diff in review rather than a surprise on screen.

**The fan.** For a junction with `n` siblings no two siblings cross, in every style's route; in Googie's the flats are at `n` distinct heights.

**Fixtures.** The worked example's domain is the first fixture; the design page's Large domain, the worked example's domain with eighteen tasks added, is the second, for density.

## 4. The styles

**Golden paths.** In every style, every silhouette and mark evaluated at its stated box must reproduce the golden-master path data of [styles-masters.json](styles-masters.json) to two decimal places, and Googie's inner transforms likewise. Googie's tilted start ellipse and finish keystone are checked to lie within their card boxes at their fixed tilts. `scripts/style_masters.py --check` confirms that the masters file matches the design page and that the style documents carry it.

**The contract.** Every item of the style contract's checklist is defined for every style: each style supplies every required token in both themes, its three faces, six silhouettes with their insets, both folds, label geometry for every kind, a glyph envelope, a here mark, a flag on a task, a begin node, and a start node, a route, a junction, and its tint participation. The four glyphs are the same shapes in every style. Toggling a flag or a here mark changes no position in the layout's output, in any style.

**Tint.** In a style that tints, a body's fill at 72 % and above is `--panel`, at 45 % and below its tint token, and at 60 % the mix the curve gives (`k = 1 − (1 − t)²`, `t = 4/9`, so `k ≈ 0.69`); in a style that does not, the fill is the same at every zoom.

**Settings.** A `theme` other than `light` or `dark`, or an unreadable settings file, gives light; a `style` the application does not ship, or none, gives Googie. The first paint uses the stored style's ground for the stored theme, and Googie's light ground when nothing can be read.

**Screenshots.** Each sample domain is rendered in every style and both themes, and reviewed by eye against the style documents and the design page.

**The underpass** is tested on crossings at several angles: the cut's setback follows the formula, the caps lie parallel to the crossed line, and a near-parallel crossing is capped at `breakMax`.

## 5. The interface

**Drop-target enumeration** is tested against the command layer: for a domain and a dragged object, the set of targets the interface offers equals the set of commands the command layer accepts, computed independently by trial application in the test. This is the property the interaction document stakes everything on, and it is the test that must never be skipped.

**Gestures** are driven through the accessibility tree with `egui_kittest`: a right-click opens the correct menu with the correct items for the node's kind and position; a status glyph click cycles; a double-click flags; a drag from a start node to a branch target issues `move_workflow`; Escape cancels. Each asserts on the record afterwards, not on pixels.

**Dialog strings** are tested verbatim against the chrome's tables.

## 6. The automation server

**End to end**, with an MCP client in the test speaking to a server bound to an ephemeral port on a temporary library: the tool list at each tier is exactly the catalogue's table for that tier; a tool above the tier is absent, not refused; every prompt names only tools present at its tier; a write returns the new revision, the final title, and the outline; a read addressed by title resolves, and one addressed by an empty or unknown title is refused `not_found`; a write addressed by title is refused `bad_arguments`; a stale revision is refused; a request with a foreign `Host` or `Origin` is answered `403`; `GET /mcp` is answered `405`; `/health` answers.

**The instructions text** is tested to name only tools that exist.

## 7. What is not tested by machine

Whether the drawing looks right. The fan rule, Googie's tilts, each style's folds, and each style's reading at 60 % are derived rather than observed, and only a render shows whether they read. Visual verification is a step in the implementation plan, done by running the application and looking, and a change to any of them is not claimed to work without a screenshot.
