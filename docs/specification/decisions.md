<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# Decisions record

Settled design decisions for PensaForma, with the reasoning that produced them, so that neither a later session nor a later reader re-litigates a question that has already been answered. A decision listed under "Settled" is closed. A proposal listed under "Proposed" has been written into the specification as if it held, so that the documents read whole, but awaits the author's ruling; each names the document that depends on it. Open questions are listed last and are neither.

Dates are the date of settlement.

---

## Settled

### D1. Document precedence

*2026-08-30.*

Where documents in this set disagree, the northstar is the authority for intent and the structural model is the authority for structure; the interaction, layout, geometry, and chrome documents are rewritten toward them rather than the reverse. The glossary fixes the vocabulary every document speaks.

### D2. Five node kinds

*2026-08-30.*

The model has five node kinds: `start` and `finish`, which bound a workflow; `begin` and `end`, which bound a project; and `task`.

The alternative considered was three kinds, unifying the workflow boundary with the project boundary, on the evidence that the drag-and-drop rules convert one into the other while preserving identity. That unification was rejected: a workflow and a project are different things in this model, and collapsing them would lose the distinction that lets a branch be a workflow rather than a displaced project.

**Consequence.** The mark geometry draws a silhouette for each of the two workflow boundaries (D7) as well as for the project boundaries and the task.

### D3. An open branch is legal

*2026-08-30.*

A branch workflow need not return to its parent. A branch with a departure and no return is a legal, persisted state, not merely a transient one during a gesture.

**Consequence.** Every validity rule needs an open-branch case, the layout must render a branch that terminates in air, and no operation may refuse merely because it would leave a branch open. It also means the branch relation, not the return, is what carries acyclicity.

### D4. The model stores each branch's side and its order on that side

*2026-08-30.*

A branch point and a return point each have two sides, left and right. Each side holds an explicit inner-to-outer ordering of the branch workflows connected on it, and that ordering is model state, not a layout decision.

The alternative was to record only that a branch departs at one point and returns at another, leaving side and order to a layout engine minimising crossings. That was rejected because a branch's position would then move when an unrelated edit changed the layout, and the user could not place a branch deliberately.

**Consequence.** The drop-target inventory doubles (both sides of every point), and the layout engine obeys the stored order rather than choosing one.

### D5. The "here" cursor is scoped one per workflow

*2026-08-30.*

Each workflow, main or branch, carries at most one "here" cursor, which marks the current task within it. A parent and its branch each hold their own, so parallel threads of work each have a position. Only a task may carry it.

### D6. The activity log is editable, and is therefore a worklog

*2026-08-30.*

Every opener and task carries a time-stamped activity log (a closer none, D11 as amended). The chrome provides both a viewer and an editor for it, and both users and AI agents may add entries and modify existing ones, for any reason.

**Consequence, stated plainly because it is easy to lose.** An editable log cannot answer "what actually happened"; it answers "what has been recorded". It is a worklog, not an audit trail. If an audit trail is ever wanted, it is a second and immutable record, not a mode of this one. The entry schema must therefore carry an author, a distinction between system-written and hand-written entries, and a marker for a later revision, or a revised entry becomes indistinguishable from an original.

### D7. Start and finish nodes wear mid-century shapes of their own

*2026-08-30; the tilt and the glyph placements amended 2026-09-02.*

The start node wears a jaunty ellipse; the finish node wears a narrow keystone (amended from a circle, below) and carries no label. Both follow three rules of the style, stated in full in the mark geometry: no outline is a constant-width stroke, every line being a variable-width filled ribbon whose weight pools along one nominated side; every such mark is rotated to a slight, jaunty angle; and shapes are authored splayed, with no parallel edges.

**Amendment, 2026-09-02.** Renders at nine, minus five, and minus three degrees were compared, and the slight tilt was chosen: the range is two to six degrees either way, and the worked instance is minus three. At that tilt the ellipse all but fills its box and the lean reads as a hand-set card rather than a tilted one. The note glyph's placement was ruled at the same time, because a card's corner is empty on a conic: on the start ellipse the glyph anchors to the inner ellipse's inscribed corner and rotates with the mark; on the finish circle it sits beside the mark, to its right, centred. The mark geometry carries the constructions.

**Third amendment, 2026-09-02.** The start ellipse's major axis is held to seven tenths of the width its box allows, after renders at 100, 90, 80, and 70 percent; the minor axis keeps the full fitted height. The opener then reads as a compact medallion rather than a bar across the card. The cost was accepted knowingly: a start title wraps to the inner ellipse's inscribed width, about 85 pixels, so long workflow titles make tall medallions.

**Second amendment, 2026-09-02.** The finish node's circle was replaced by a narrow keystone, 92 by 44, centred in the card box at an offset of 48 and tilted with the card, after renders of the circle beside keystones of 56, 72, and 92. A circle is the most generic mark on the map, the same figure as the station dots and the status glyphs only larger, so an unlabelled circle at the top of a line could be mistaken for a heavy dot; the keystone is a shape nothing else wears, and its asymmetry, wider at the top than at its base, reads as a cap set on the line. The note glyph is centred on the keystone's inner shape, the cap carrying no label. The keystone is therefore no longer held in reserve. An even width was chosen so that the mark centres on the even card box with its edges on whole pixels.

**Fourth amendment, 2026-09-02.** The cap's size, shape, and tilt were settled after renders of five sizes beside a task card and the opener, four tilts, and three readings of a lifted corner: the keystone is built at 100 by 50 with its box grown 2 at the top and the top-right corner at the new top, so that the top edge still climbs to the right once tilted; the box is 100 by 52, centred at an offset of 44; and the tilt is fixed at +2 on every finish card, since the cap's own lean is cancelled by a negative tilt and exaggerated by a larger one. Only the start node's tilt varies with the id. The finish card is 52 high, between the opener's 54 and a task's 56.

**Fifth amendment, 2026-09-02.** The start node's tilt is fixed at −3 on every card, and the per-id variation is withdrawn. A rendered domain with three openers at three angles showed that the variation reads as inconsistency rather than as hand placement once the shapes are this restrained, and a uniform opener is recognised faster. Both workflow boundaries are now constant marks: the ellipse at −3, the keystone at +2.

**Sixth amendment, 2026-09-02.** The start ellipse is scaled to 0.85 on both axes, after a rendered domain showed it outweighing the finish keystone at the other end of the line; at seven tenths of the width and 0.85 of the fit it is 54.3 by 23.1 in the 188 by 58 card. Its band is now inset on the ellipse's own box rather than the card's, so the outline keeps its stated thickness at any size. The label's wrap width falls with the mark, to about 68 pixels, roughly ten characters a line, which was accepted.

Two notes carried forward to the geometry work.

The variable-width outline needs no new machinery. The geometry already draws every outline as two fills, an outer path and an affinely inset inner one, rather than as a stroke. Applied to an ellipse or a circle, that inset yields a band varying smoothly around the perimeter, heavy on one side and fine on the other, which is exactly the calligraphic weight the style asks for. The alternative, a second outline technique with per-vertex control, buys that control at the cost of two ways to draw one thing.

The tilt is genuinely new, since every other mark is axis-aligned, and it touches hit-testing, the station anchor, layout bounding boxes, and label placement. Each node's tilt is derived deterministically from its id, so the map is varied but a given card never changes shape when it is reordered; a tilt drawn from a running index would suit a static grid of decorative icons, not a diagram the user rearranges.

**Sixth amendment, 2026-09-03.** The finish node carries no note (D11 as amended), so the glyph placement on the keystone recorded above is withdrawn; only the start ellipse's placement stands.

### D8. A gap is the stored record; its two points are addressed within it

*2026-08-30.*

Branch points and return points have stored identity rather than being derived from the node below them. The stored record, however, is the *gap*: one record sitting between two consecutive nodes, owning both its branch point and its return point, which are addressed as `(gap id, branch|return)`.

Stored identity was chosen because it makes every attachment a single reference rather than a compound key of host node, which point, side, and index; because undo becomes a record swap rather than a recomputation against a since-mutated sequence, which is where undo faults live; and because an agent can hold a reference across calls, whereas "the branch point above node X" changes meaning the instant anything is inserted above X.

Two pieces of work are *not* simplified by it, and were excluded from the case: the repair rules, since both schemes must rewrite the attachments on whichever point disappears when two gaps merge; and insertion, since both must decide which resulting point inherits the existing branches, and that decision is the outgoing/middle/incoming distinction needed regardless.

The gap, rather than the point, is the record because it halves the record count and yields an invariant a validator states in one line: the node list and the gap list interleave exactly, n nodes to n−1 gaps. That makes an orphaned point unrepresentable rather than merely detectable. The choice rests on one assumption: that a branch point and its paired return point always share a lifetime, which holds throughout the model as written.

### D9. Undo reverses the last human operation only

*2026-08-30.*

One slot, not a stack. It holds the most recent structural or state operation originating from the local user interface, and reversing it also removes the activity-log entry that operation created. There is no redo.

An operation arriving from the automation server never fills the slot and is never undone. Such a write *invalidates* the pending slot rather than being reversed through, because reversing across another writer's change is how one silently destroys their work, and the check costs a revision comparison. Switching or deleting the domain also clears it, as does quitting.

Note text is out of scope: the note editor keeps its own text undo.

### D10. Orderings are ordered arrays of ids on the parent

*2026-08-30.*

The three explicit orderings (main workflows within a domain, branch workflows on each side of a branch point, branch workflows on each side of a return point) are stored as ordered arrays of ids on the containing record.

Fractional sort keys were considered, since they let two writers insert in different places without conflicting, which matters given an automation server writing alongside a user. They were rejected for the first version as harder to read off the stored record and as requiring a rebalancing rule. If concurrent reordering proves painful in practice, the migration is understood.

### D11. Titles on openers; status on tasks only

*2026-08-30; the closers amended 2026-09-03.*

A `start` node and a `begin` node carry a title. A `finish` node and an `end` node carry none, so a boundary pair is named by the node that opens it. Only a task carries a status and only a task may hold the "here" cursor. Any node may be flagged, and every node has a note reference and an activity log.

The rejected alternatives were a rolled-up status on boundaries, showing aggregate progress on a collapsed project, and an independently settable status on every node. The latter is the one arrangement in which the map can display a contradiction, a project marked done above unfinished contents.

**Amended 2026-09-03.** A `finish` node and an `end` node carry no note, no flag, and no log either: a closer is its id and its kind, an end node its `pair` besides, and everything a pair records lives on its opener. The log entries that `attach_return` and `detach_return` wrote to a branch's finish node go to its start node, which holds the workflow's log; the finish node remains the handle for the return and the home of `Detach return` (D18).

### D12. A node's prose is its note; there is one field, not two

*2026-08-30.*

A node has one field of prose, and its name is **note**. "Description" is not in the vocabulary, so that no reader infers a second field.

The note is a markdown file in the domain's `notes/` directory; the node record holds only the filename. That the prose lives outside the node record has four consequences, set out in the structural model: the reference alone answers whether a node has prose, so the canvas need not open files to decide whether to draw a note glyph; a note write is not part of a domain operation and does not pass through the domain's atomicity, the sole crossing point being the first save of a new note, which must be ordered file first; an unreferenced note file is a legal orphan rather than an integrity fault; and a reference to an empty file is legal, since emptying a note is not deleting it.

### D13. Sibling branches fan from the junction; they do not chain

*2026-08-30.*

Where several branches share one branch point, each connects directly to the junction, and where several returns share one return point, each connects directly to that junction. One clearance rule serves every lateral, a branch's connector is independent of its siblings, so reordering one does not redraw another, and the height constraints need no second case.

**This supersedes the chain first proposed for the branch and return edges**, under which the junction reached only the innermost branch and each further branch connected to the previous branch's boundary node. That form is withdrawn and must not be carried into any document.

The cost is accepted knowingly: an outer branch's lateral crosses the inner branches on its side, and each crossing is drawn as an underpass. The underpass construction exists in the mark geometry, and crossings are unavoidable in this model regardless (D14's note on spans).

### D14. Every node occupies the same fixed 188-wide box

*2026-08-30.*

The ellipse and keystone of D7 are drawn within the standard card box, centred, so that only height varies between nodes and the keystone simply does not fill its box.

The reason is the packer. Because card width is fixed, a subtree's contour reduces from a real outline to an integer count of lanes, and placing a sibling reduces to pushing a whole subtree out by a whole number of lanes. Variable widths would require the full non-layered contour form, which is a known and documented replacement rather than a gamble, but it is a replacement bought for nothing here: no node needs its own width.

The lane step is the card width plus a horizontal gutter.

### D15. Folding applies to projects only

*2026-08-30; extended to workflows 2026-09-03.*

A `begin`/`end` pair can be collapsed onto one card, the seam drawn as the two hull silhouettes crossing into a lens. A workflow's `start`/`finish` pair never folds, and a branch is hidden only by folding a project that contains it.

Folding a branch workflow was considered as the natural way to quieten a busy map. It was deferred because it needs a second seam construction for the ellipse-and-keystone pair and a rule for where a folded branch's return lateral arrives, which it must still do. Recorded here as a candidate rather than dismissed.

Fold state is client-local view state keyed by the `begin` node's id, never a field of the stored record.

**Amended 2026-09-03.** Folding applies to workflows as well, any workflow, main or branch. The two reasons for deferring it are answered: the pair is drawn shut by the construction in the mark geometry's 3.12, the start ellipse painted over the finish keystone at a seam of 35, and a folded branch's laterals arrive and leave exactly as they do when it is open, `L` beneath the start card's silhouette and `L` above the finish card's, the riser running behind the pair. A folded branch keeps its lane; a folded main workflow is one card in the row of mains. Fold state keys on the opener's id, `start` or `begin`. The candidate once recorded in the in-flight ideas is thereby settled.

### D16. On a cursor collision, the receiving workflow's cursor survives

*2026-08-30.*

Two edits can bring two "here" cursors into one workflow: a branch becoming a project inside its parent, and a task carrying the cursor moving into a workflow that already has one. In both, the cursor already in the receiving workflow stays and the incoming one is cleared. A structural edit never moves where the author was working on the line they dropped into.

### D17. An emptied scope and an emptied workflow both persist

*2026-08-30.*

Nothing is deleted automatically for being empty. A project left with only its begin and end nodes stays; so does a workflow left with only its start and finish nodes, whether or not branches remain attached to it. The author removes either through the ordinary delete flow, which confirms first.

This removes two rules, including the special case for an emptied workflow that still has branches, and one class of silent loss: a start node carries a title, possibly a note, and an activity log, and automatic deletion would destroy all three without a dialog.

### D18. `Detach return` lives on the finish node's menu

*2026-08-30.*

A menu item detaches a branch's return in place, leaving the branch open. It sits on the finish node's menu and appears only when the branch returns.

The placement mirrors the drag handles exactly: the finish node owns the return in both gestures and menu, whilst the start node owns attachment, side, and order. Keeping the two handles disjoint everywhere is what makes either predictable. It also closes an asymmetry, the menus otherwise being able to attach a return but never to detach one.

### D19. The note glyph means a note exists, not that it has text

*2026-08-30.*

Emptying a note in the editor is not deleting it: the file and the node's reference both remain, and only the explicit delete flow removes them. A card can therefore show the note glyph and open to nothing.

The reason is not tidiness but drawing cost. The glyph is a function of the node's reference alone, which is what lets the canvas decide whether to draw it across several hundred cards without opening a single file. Making it track content would need either a read per card at draw time or a has-text flag in the record, and derived data in the record is data that can disagree with itself.

### D20. The id scheme

*2026-08-30.*

Twelve characters, fixed width: a two-character kind prefix, a base-36 millisecond timestamp of exactly eight characters, and a two-character base-36 counter that resets each millisecond. So `n_mrtwgppt01`. Prefixes are `d_`, `w_`, `n_`, and `g_`, and the counter is shared across all four.

Entirely lowercase, because an id is part of a note's filename and a case-normalising filesystem must not conflate two. Fixed width, so a column of ids lines up in a diff. A counter rather than a random suffix, because randomness only lowers the chance of a collision whilst a counter removes it, and pasting two hundred nodes inside one millisecond is exactly the case a short random suffix does not cover. Monotonic against a clock that steps backwards. Opaque and never parsed, which is also the upgrade path: ids are unique by construction within an installation, and a device discriminator can be added to newly minted ids on the day a second writer exists without touching a single old one.

### D21. The standard trunk-edge length, and the middle-edge quantisation

*2026-08-30.*

One length, `L`, serves as the outgoing edge, the incoming edge, and the least separation of two junction diamonds sharing a gap; a departure clearance, an arrival clearance, and a junction gap held as three numbers would collapse into it. A middle edge is either zero or at least `L`, never between.

*Amended 2026-09-03.* `L` is 24, measured from the silhouette's edge where the line passes through it (the mark geometry tabulates each shape's insets), and is sized so that the two fixed edges do all the clearing: a lateral climbs about twenty pixels across a card's half-width, and with a four-pixel margin that is 24, so a gap with departures only or arrivals only stays shut with its one diamond in the middle, and only a gap using both points, or a gap the height solve stretches, opens its middle edge. The first worked example had `L` at 12 with a clearance rule that opened the middle edge by 12 in every gap with departures, which put an invisible return point above every drawn branch point; that rule is withdrawn.

The rule exists to make drop targets hittable by construction rather than by tolerance. Every position within a gap is then at least `L` tall: an unoccupied gap is one zone of `2L`, a gap occupied at one point splits into `L` and at least `L`, and a gap occupied at both splits into three, each at least `L`. No screen-pixel floor, no apportioning, no proportional fallback.

The cost is a quantisation confined to the open band between `2L` and `3L`; above `3L` the air is continuous, so a gap that needs more takes exactly what it needs. With the constants in the layout document the raised airs already land at or near `3L`, which is some evidence the length is right rather than imposed.

### D26. No station dots; the anchor is a measurement point

*2026-09-02.*

The line carries no mark where a card attaches to it. The card is the station, and the only marks on a track are the junction diamonds, so every mark on a line means a junction. The anchor gap that once held the dot is gone with it: gaps are measured between the silhouettes where the line passes through them, so that two cards a shut gap apart look the same distance apart whatever shapes they wear, and each junction stands `L` clear of the silhouette on its side, at either end of a gap alike. A riser is drawn from card centre to card centre, behind the cards, so that it meets an ellipse or a keystone that does not fill its box. (The first renderings of the worked example measured the return point from the card's edge but the branch point from an anchor above the card, and stopped risers at the box edges, which put the arrival diamond nearly against its card and left the openers floating clear of their lines; both are corrected here.) The air rule's arrival case loses its dot-radius term, and a riser is drawn from card to card, an open branch's ending at its finish keystone. Decided on the northstar's tenth axiom: the dot clarified nothing the card and the diamonds do not. With the dot gone the diamond is the only mark on a line, and it grows from 8 to 12 pixels on a side, chosen from renders at 8, 10, 12, and 14: at 12 it reads as a junction at the ordinary zoom without reading as a node.

*Amended 2026-09-03.* Every branch point and return point is drawn, whether or not a branch attaches there, after a render of the worked example with every point drawn was set beside one with occupied points only. Where the station dots had put a decorative mark in every gap, the point diamonds put a meaningful one there: each is a place a branch may depart or arrive, the drop positions are visible at rest, and a shut gap's single diamond at its midpoint reads as the gap's own mark. One diamond where a gap's two points coincide, two where its middle edge has opened.

### D22. A new application, in Rust, in its own repository

*2026-09-02.*

PensaForma is built from the ground up, in Rust, in the public repository `ParkviewLab/pensa-forma`, following the ParkviewLab handbook's conventions. The product is named PensaForma (pensa, tasks; forma, shape), styled with the seam between its roots shown; the repository, binary, and bundle identifier use `pensa-forma`, the crate `pensa_forma`. The name was settled before any identifier reached disk or a registration, which is the moment a name becomes expensive to change; a working name used during the specification's drafting was retired at the same time.

### D23. The specification stands alone

*2026-09-02.*

No document in this set names, cites, compares with, or alludes to any other application. Every rule is stated positively with its own reasoning, so that an implementer who has read nothing but this set and the ParkviewLab handbook can build the application. Scholarship (the tidy-tree literature, the protocol specifications) is cited; software is not.

### D24. No import from other file formats

*2026-09-02.*

The application reads and writes its own domain format and nothing else. It has no import path for other applications' files, and its data directory and domain-directory prefix are its own, so it never opens a library it does not own.

### D25. The toolkit is egui with eframe

*2026-09-02.*

The user interface is an immediate-mode Rust GUI built on egui, hosted by eframe. The application's interface is not document layout but a bespoke vector scene with pan, zoom, custom silhouettes, and per-frame interaction state, which is what an immediate-mode painter under a camera transform is built for; the toolkit also supplies pan and zoom, a text editor with undo, accessibility through AccessKit, and a markdown preview widget without further dependencies. The two places its painter needs help, filling concave silhouettes and cutting the underpass, are answered by a tessellator and by drawing the lateral as an explicit ribbon; both are recorded in the mark geometry's implementation notes.

---

### D27. Workflows stay; the unification of workflows and projects is declined

*2026-09-03.*

One record kind for every bounded run, with main, branch, and nested as its three placements, was considered on the evidence that a workflow and a project have the same shape and that the drag rules convert one into the other while preserving identity. Three drawings of one small domain were compared: the five kinds as written; one kind wearing the hulls everywhere and called a project in every placement; and one kind with the ellipse and keystone kept for main and branch runs by placement. The unified record shortens a line that is a single project by two cards and two gaps, and it makes the conversions plain moves.

It was declined. The five-kind drawing is at a glance the clearer and the more specific, a start and a finish being unmistakable where a line begins and ends; and calling every run a project would put that name on runs that are not projects. Two costs are accepted knowingly: a line that holds one project carries its own start and finish around it, and a project becomes a branch, or a branch a project, by a conversion of kind rather than by a move.

**Consequence.** D2 stands. The two properties the unification would have brought with it are taken on their own terms instead: a workflow folds (D15 as amended), and a closer carries no note, flag, or log (D11 as amended).

### D28. "Plan" leaves the vocabulary; the domain orders its main workflows in `mains`

*Proposed 2026-09-02; settled 2026-09-03.*

A domain holds workflows, some main and some branch. The ordered list of main workflows is the domain's `mains` field, and the menus say "workflow" where a person creates or pastes one. No second noun stands for a main workflow.

### D29. The automation server's port is 35899

*Proposed 2026-09-02 as 35901; settled 2026-09-03 at 35899.*

Loopback only, fixed, and never roaming; it sits below the ephemeral ranges of macOS and Windows. If the port is taken the server does not start and the pill says so; it never picks another port on its own.

### D30. Status values, labels, and `completedAt`

*Proposed 2026-09-02; settled 2026-09-03 with different values.*

Stored values `todo`, `in-progress`, `completed`, `cancelled`. The tag under a task card reads to do, in progress, done, cancelled; the status submenu reads To do, In progress, Completed, Cancelled; the glyph click cycles the stored values in that order. A task entering `completed` is stamped with `completedAt`, the time of the change, and leaving `completed` clears it (I18). The stored value `todo` never appears on screen.

The proposal's `doing` and `done`, shown as Doing and Done, were rejected: these are the author's established words, and the specification is not to coin alternatives where an established vocabulary exists.

### D31. The activity log's automatic entries

*Proposed 2026-09-02; settled 2026-09-03 with status changes added.*

The application writes one `system` entry to exactly one node per command, the node the command names as its subject, for a structural change and for a status change: creating a node, moving a node or an extent, converting a project to a branch or a branch to a project, attaching or detaching a departure or a return, reordering a branch or a main workflow, and setting or cycling a task's status (event `status`, naming the new status). A rename, a flag or cursor change, and a note edit write none; they are state that the record itself shows. Deletion writes nothing, the deleted node's log dying with it. An entry holds frozen prose in `text` and a machine-readable `event` code, so it reads at a glance and filters by kind. A `system` entry is editable on the same terms as any other and carries `editedAt` and `editedBy` once edited. The log is unbounded; the viewer shows the newest entries first and pages.

### D32. Bookmarks hold a node set, not a camera

*Proposed 2026-09-02; settled 2026-09-03.*

A bookmark is `{name, folded, nodes}`: the folded opener ids, start or begin, and the ids of every node drawn wholly inside the viewport when it was saved. A client frames those nodes under its own maximum scale and minimum padding, so a bookmark survives a layout change and another window size by construction and degrades only when every node it names is gone.

### D33. The Cargo workspace

*Proposed 2026-09-02; settled 2026-09-03.*

Six crates: `model`, `store`, `command`, `layout`, `server`, and `app`, with the binary in `app`. The version is `[workspace.package].version`, inherited by every member.

### D34. Data locations

*Proposed 2026-09-02; settled 2026-09-03.*

The application's data directory is the platform's per-user application-data directory for `ai.parkviewlab.pensa-forma`; the default library is its `domains/` subdirectory; a domain directory is named `pensaforma_domain_<slug>_<id>`.

### D35. One drop indicator

*Proposed 2026-09-02 as two; settled 2026-09-03 as one.*

The chevron pair, in the `--cursor` token, marks every legal target, a main-workflow target included, where it sits at the centre of the gutter or margin the drop would occupy at the pointer's height. The vertical bar proposed for main-workflow targets is withdrawn: one mark that says "here" serves every target, and its place in a gutter rather than on a line already says what the drop will do.

### D36. The domain directory describes itself

*2026-09-08.*

The record is plain JSON, read tolerantly (JSON5 accepted) and written canonically. A reader with only the directory should not have to divine what the fields mean, and comments in the record cannot supply the description: the application rewrites the whole record on every save from its data model, so anything the text carried beyond the data would survive only until the next save. A format that invites annotation and then discards it is worse than one that says what it is.

The description therefore travels beside the data, as two files the application writes into every domain directory: `domain.schema.json`, a JSON Schema with a description on every property, which the record names in a `$schema` field so that editors explain the fields and validators check them without the application; and `README.md`, the same description as a page for a person. Both are generated from the schema's descriptions, authored once beside the `store` crate and checked against the structural model by test, so the description cannot drift from the record; both are rewritten when the schema version changes and never read for data.

**Consequence.** `$schema` is the record's first field; the persistence document's section 3.1 specifies the two files; the store writes them on `create_domain` and on migration; the tests validate the fixture against the schema and assert that every field in the structural model's tables carries a description.

## Proposed

None at present.

---

## Open questions

None outstanding.
