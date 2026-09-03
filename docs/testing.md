<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# Testing

What is tested, how, and what a passing suite proves. The tests are organised
by the crate they exercise, and the most valuable of them are stated in the
specification documents themselves as required properties; this document
collects them and says how each is checked.

`cargo test` runs everything; CI runs it on every push and pull request, with
formatting and clippy beside it.

---

## 1. The model

**The invariant checker is exercised in both directions.** For each of the
seventeen invariants in the structural model, section 4, a test constructs a
record that violates exactly that invariant and asserts the checker names it;
and the worked instance of section 8 passes clean. The three refusals the
worked instance lists are tests.

**Every mutation is a property test.** Using a generator that builds random
legal domains (random workflows, projects nested properly, branches placed by
the model's own rules, some open, some returning, cursors and flags
scattered), each mutation is applied with random legal arguments and the
result must satisfy every invariant; applied with random illegal arguments it
must refuse with the documented code and leave its input untouched. The
generator is itself checked: everything it produces passes the checker.

**The catalogue's required properties** (command catalogue, section 10) are
property tests over the same generator: a command's subject is the only node
whose log changed; every moved node keeps its fields except the ones the
conversions change; no command creates a return; nothing is deleted for being
empty.

**Gap split and merge** are tested exhaustively on the three insertion
positions and on removal, against the structural model's section 2.4: which
gap keeps its id, which lists move where, and that nothing detaches.

**The id minter** is tested for width, prefix, lowercase, monotonicity under
a clock stepped backwards, and the counter's behaviour at the 1296th id in a
millisecond.

## 2. The store and the command layer

**The atomic write** is tested by interrupting it: a write whose rename step
is made to fail must leave the old file intact and readable, and a temporary
file left behind must be ignored by the next read.

**Tolerant read, canonical write** is tested by round-tripping the worked
instance through a hand-edited JSON5 form (comments, unquoted keys, trailing
commas) and asserting the canonical output is byte-identical to the fixture
in the persistence document, section 3.

**Path safety** is tested with traversal attempts: a domain path outside the
library root, a note filename with a separator, a sibling directory whose
name begins with the root's, each refused.

**The pipeline** is tested end to end on a temporary library: each refusal
code is provoked once; a refusal leaves the file byte-identical; a `stale`
revision is refused; the revision increments by one per successful write; a
command that writes a note file writes it before the record, verified by
failing the record write and finding the orphan.

**Undo** is tested for the slot's rules: filled by a `ui` command, not by an
`automation` one; cleared by an automation write, a domain switch, and a
delete; an undo restores the pre-image byte for byte including the log; and
an undo after another write is refused as stale.

## 3. The layout engine

**The required properties** (layout engine, section 11) are each a test over
the generator's domains, run on the layout's output: no unmarked proper
crossing; no lateral inside a card except as reported; every lateral segment
flat or at twelve degrees; the four clearances to the pixel; sibling start nodes
level; a tall branch stretching only above its return; lane order following
the side lists; determinism under permuted key order; monotonicity under an
added card.

**Golden masters.** A small set of hand-built domains (the worked instance;
one with a shared branch point carrying three siblings on each side; one with
an open branch outermost and a returning branch inside it; one with a folded
project) has its layout output snapshotted, so a change in geometry is a
visible diff in review rather than a surprise on screen.

**The fan.** For a junction with `n` siblings the flats are at `n` distinct
heights and no two siblings cross.

## 4. The mark geometry

**Golden paths.** Every silhouette's construction evaluated at its stated
`(w, h)` must reproduce the golden-master path data in the mark geometry to
two decimal places, and the inner transform likewise. The tilted openers are
checked to lie within their card boxes at their fixed tilts.

**The underpass** is tested on crossings at several angles: the cut's setback
follows the formula, the caps lie parallel to the crossed line, and a
near-parallel crossing is capped at `breakMax`.

## 5. The interface

**Drop-target enumeration** is tested against the command layer: for a
domain and a dragged object, the set of targets the interface offers equals
the set of commands the command layer accepts, computed independently by
trial application in the test. This is the property the interaction document
stakes everything on, and it is the test that must never be skipped.

**Gestures** are driven through the accessibility tree with `egui_kittest`:
a right-click opens the correct menu with the correct items for the node's
kind and position; a status glyph click cycles; a double-click flags; a drag
from a start node to a branch target issues `move_workflow`; Escape cancels.
Each asserts on the record afterwards, not on pixels.

**Dialog strings** are tested verbatim against the chrome's tables.

## 6. The automation server

**End to end**, with an MCP client in the test speaking to a server bound to
an ephemeral port on a temporary library: the tool list at each tier is
exactly the catalogue's table for that tier; a tool above the tier is absent,
not refused; every prompt names only tools present at its tier; a write
returns the new revision and outline; a stale revision is refused; a request
with a foreign `Host` or `Origin` is answered `403`; `GET /mcp` is answered
`405`; `/health` answers.

**The instructions text** is tested to name only tools that exist.

## 7. What is not tested by machine

Whether the drawing looks right. The fan rule, the tilt of the openers, and
the seam of a folded pair are derived rather than observed, and only a render
shows whether they read. Visual verification is a step in the implementation
plan, done by running the application and looking, and a change to any of
them is not claimed to work without a screenshot.
