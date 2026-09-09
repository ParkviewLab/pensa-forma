<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# Interaction and drag-and-drop

The authority for how the graph is restructured by the pointer: what can be dragged, where it can be dropped, how a drop is judged legal, and which command a drop issues. It depends on the [structural model](structural-model.md), the [layout engine](layout-engine.md) for the geometry of its targets, the [command layer](command-layer.md) for the write path, and the [command catalogue](command-catalogue.md) for the commands it names. The context menus, which reach many of the same commands by another route, are in the [UI chrome](ui-chrome.md).

---

## 1. What the model guarantees, and what this document relies on

Drag-and-drop is not a convenience layered over the model; the model has the shape it has so that every ordinary rearrangement is a single gesture whose meaning is exact. Six properties of the structural model do the work here, and each rule below can be traced to one of them.

**A branch may be open**, so an edit that would invalidate a return has a fourth move beyond refusing, relocating, or guessing: the return is detached, the branch is visibly open, and the author says where it goes next. Nothing is rewritten behind the author's back.

**A branch is a workflow with its own finish node**, so its return is a fact about that node's membership of a return list, not a field carried on whichever node happens to be topmost. There is nothing to carry up when a node is added above, nothing to recover when a node is removed, and nothing to default when a branch is grafted in.

**A branch hangs on a gap, and gaps merge when a node between them is removed**, so removing a node never moves a branch; its gap merely gets longer. Every attachment at either gap survives on the merged gap.

**Side and order are stored**, so a drag can set them and nothing else ever changes them.

**A gap has three positions**, so an insertion beside a departure or an arrival can say which it means: below the departures, between departures and arrivals, or above the arrivals. Nothing needs repairing afterwards because nothing was ambiguous.

**A two-ended object is moved one end at a time**, and the state between the two gestures, a branch that is open, is a legal stored state rather than a transaction held open. That is what makes a branch movable between scopes.

## 2. The principles that follow

Nothing is rewritten behind the author's back. Where an edit would invalidate a connection, the connection is detached and left visibly undone, never moved somewhere unasked.

An intermediate state may be incomplete but is never illegal.

A gesture states its intent precisely enough that no repair is needed. Where two readings of a drop are possible, they are two drop targets.

Legality is decided by the same code that would perform the edit (section 5). There is no second copy of the rules for the pointer to consult.

## 3. What can be dragged

Four node kinds are grab handles, and each stands for a different object.

A **task node** drags itself alone. A **begin node** drags the whole project it opens: its end node and every task, nested project, and branch within its scope. A **start node** drags the whole workflow it opens: its finish node and everything in it, including descendant branches. A **finish node** drags nothing at all; it is the handle for one connection, its workflow's return, and only a branch workflow's finish node is draggable, a main workflow having no return to move.

An end node is never a handle. It is one half of a pair and sits where its scope ends, so moving it alone would quietly resize the scope while leaving the record well-formed, which is the kind of change nothing downstream would object to and the author never asked for. A scope moves by its first node, begin or start, which carries its close.

Junction diamonds are not handles. A branch's departure is moved by its start node and its return by its finish node; the diamond is a target, not a grip.

Dragging always moves. Nothing is ever copied by a drag; copying is the menu's `Copy` and `Paste`.

In the flagged-only review mode nothing is draggable and no drop target exists.

Folding changes none of this. A folded begin or start node drags the whole project or workflow exactly as when open, and a folded branch's finish node stays the handle for its return. The cards a fold hides, and the edge inside the folded pair, present no handle and no target; the pair's outer gaps remain targets.

## 4. The drop-target inventory

A drop target is a hit region in the drawing paired with the command it would issue, expressed in the catalogue's target grammar. Four families exist.

### 4.1 Trunk-edge targets: the three positions in a gap

A gap has three positions, named by the edges that occupy them (structural model, section 2.4): below the branch point on the outgoing edge, between the two points on the middle edge, and above the return point on the incoming edge. Each is an edge target `{edge: gap, position}`.

They are three targets only where they differ. A gap with no departures and no arrivals has nothing at either point, so all three insertions produce the same record, and the gap is **one** target. A gap with departures only splits at its branch point into **two**. A gap with arrivals only splits at its return point into two. A gap with both splits into three.

Every zone is at least `L` tall, the standard trunk-edge length, and this is guaranteed by the geometry rather than by a tolerance rule. The outgoing and incoming edges are each exactly `L` and never stretch, and a middle edge is either zero or at least `L`, never between (layout, section 5). So the unoccupied gap is one zone of `2L`; a gap occupied at one point splits into `L` and at least `L`; and a gap occupied at both splits into three, each at least `L`. There is no case in which a zone is too thin, so there is nothing to apportion, no screen-pixel floor to enforce, and no proportional fallback.

A zone spans the full width of its lane, so the smallest target in the drawing is `L` by a card's width, and an author who wants a larger one zooms in, which grows it in the ordinary way.

### 4.2 Branch-edge targets

Every branch point has targets on both of its sides, and they are what set a branch's side and its order. Each is a branch target `{branch: gap, side, index}`.

On a side already carrying branches, each branch's own lateral is a target, and dropping there inserts the moved workflow **at that branch's position**, pushing it and everything outside it one place out. Beyond the outermost branch on that side there is a further target, occupying the next lane out, which appends. On an empty side there is one target, in the first lane.

The hit region for a branch's lateral is the part of it that is **not shared with its siblings**: from where its own line leaves the run they hold in common, out to its branch. Near the junction several laterals run together by construction (layout, section 4), so no branch is identifiable there; from the point where it turns up into its own lane, exactly one is. This is the same fact that makes the shared run legible to a reader, used as a hit rule.

### 4.3 Return-point targets

A return point is a target for a finish node alone, and issues `attach_return(branch, gap)`. A finish node cannot choose a side or an order: the return is made on the same side as its branch's departure, at the order position the structural model's rule assigns. So a return point offers one target, its diamond (drawn at every point, so the target is visible before the drag begins) and the lane-width band of the incoming edge above it, and only the gaps the catalogue lists as legal for that branch are ever targets.

### 4.4 Main-workflow targets

Main workflows are explicitly ordered left to right within their domain, so there is a target between each adjacent pair and one outside each end, expressed as `{main: index}`. Geometrically these are the gutters between main workflows' bounding boxes and the margins beyond the outermost, each the full height of the drawing.

A drop here does something categorically different from the others: it makes the dragged object a main workflow of its own, or moves an existing one in the order. The indicator is the same chevron pair as everywhere else (D35); its place in a gutter or margin rather than on a line is what says so.

## 5. How legality is decided

Every drop target's legality is decided by trial application, not by a separate rule set.

At the moment a drag begins, the application enumerates every drop target in the current domain and, for each, applies the command it would issue to a copy of the record and keeps the target only if the command neither refuses nor produces a record that fails validation. The legal set is cached for the life of the drag, together with the revision of the record it was computed from. During the drag the pointer is hit-tested against that set alone.

Three properties make this the right design rather than an extravagance. The mutations are pure functions over a cloned record (command layer, section 1), so a trial costs a clone and a call and discards its result; at the scale of a domain that is well under a frame for every target in the drawing. The legality shown to the pointer is by construction identical to the legality the command layer enforces, so the two cannot drift, which is the failure the single write path exists to prevent. And the enumeration is the same one the menus use to decide which items to offer, so a gesture and a menu never disagree about what is possible.

On release, the drag issues exactly one command, carrying the revision the legal set was computed from. If the automation server wrote to the domain during the drag, the command layer refuses it as `stale` (command layer, section 3): the drop is cancelled, nothing is written, the map has already re-rendered to the new state, and the author drags again against the drawing as it now is. A drop is never applied to a record other than the one the author was looking at.

## 6. Feedback and cancellation

While an object is dragged, the pointer over a legal target shows an indicator; over anything else it shows none. One indicator exists (D35), specified in the [mark geometry](mark-geometry.md): the chevron pair, drawn at the point the drop would occupy, which for a main-workflow target is the centre of the gutter or margin the drop would occupy, at the pointer's height. It is drawn in the `--cursor` token and reads at any zoom.

The dragged object is shown by a ghost: its card at 40 percent opacity following the pointer, the original staying in place at 40 percent opacity until the drop lands. The cursor is the grabbing hand.

Release over no indicator cancels, and the record is untouched. A drop that would leave the object in its existing structural position is a no-op: it is not an error, nothing is written, and no log entry is made. Escape during a drag cancels it, as does the window losing focus.

## 7. The drags

Each subsection names the command each target issues. The catalogue holds the preconditions and the refusal text; this section holds what the author sees.

### 7.1 A task node

Targets: the three trunk-edge positions, and a main-workflow target. Each issues `move_task(task, target)`.

Onto a trunk-edge position, the task is removed from where it was, its old position repaired (section 8), and spliced in at the stated position. If the target gap lies inside one or more projects, the task becomes part of the innermost.

Onto a main-workflow target, the task becomes the sole task of a new main workflow. A start node and a finish node are created for it, and the workflow is inserted at the indicated position in the domain's order.

### 7.2 A begin node

Targets: the three trunk-edge positions, a branch-edge target, and a main-workflow target. Each issues `move_project(begin, target)`. The whole project travels.

A project cannot be dropped inside itself or inside any project nested within it. The trial application rejects these without a special rule, since the resulting record fails proper nesting, but the condition is stated here because a builder will want to exclude those targets cheaply before trialling.

Onto a trunk-edge position, the project is spliced in as a task would be, nesting into the innermost project containing the target.

Onto a branch-edge target, the project **becomes a branch workflow**. Its begin node becomes the workflow's start node and its end node becomes its finish node, with their identities, notes, logs, states, and every other field preserved; only `kind` changes, and `endNode` and `beginNode` are replaced by the two ends' membership of one workflow. The contents travel unchanged. The branch is attached at the target's side and order position. If the target's gap lies inside projects, the new branch is part of the innermost.

No return is created. The new branch is open, and the author attaches its return by dragging the finish node. This is deliberate: the application does not know where the author wants it to rejoin, and guessing is the failure section 2 forbids.

Onto a main-workflow target, the project becomes the contents of a new main workflow with a new start and finish node, inserted at the indicated position.

### 7.3 A start node

Targets: a branch-edge target and a main-workflow target always; and, for a branch workflow's start node, the three trunk-edge positions of its own parent workflow. Each issues `move_workflow(workflow, target)`. The whole workflow travels.

A workflow cannot be attached as a branch of itself or of any workflow descended from it. As with a project, the trial application catches this through acyclicity; it is stated so the targets can be excluded cheaply.

Onto a trunk-edge position in the parent, the branch workflow **becomes a project** and is spliced in. Its start node becomes the begin node and its finish node the end node, identities and all other fields preserved, and the two are paired. Everything within travels. Its departure and its return, if it had one, are removed only after the drop has validated, and both lists close up with the order of the remaining branches preserved.

Onto a branch-edge target, the workflow is attached at that side and order position. Three cases differ, and the difference is the whole reason a start node is a handle:

- **Reordered on the same side of the same point.** The return is preserved, and its order position at the return point is updated to correspond to the new departure order.
- **Moved to the other side of the same point.** The return is preserved and moves to the matching side of its return point, its order updated to correspond.
- **Moved to a different branch point.** The old departure and the old return are removed only after the new attachment has validated, and no new return is created. The branch is now open, and the author attaches its return by dragging the finish node.

If the target gap lies inside projects, the moved workflow becomes part of the innermost.

Onto a main-workflow target, a branch workflow's departure and return are removed and it becomes a main workflow at the indicated position; a main workflow simply moves in the order.

### 7.4 A finish node

Only a branch workflow's finish node is a handle, and dragging it moves nothing. It does not reposition the branch, change its side, or change its order; it changes only where the branch returns, by issuing `attach_return(branch, gap)`. Those other changes are made by dragging the start node, and keeping the two handles disjoint is what makes either predictable.

The only legal targets are return points in the branch's current parent workflow, at or above the gap holding its departure, and inside exactly the same projects as that gap. The return is made on the side matching the departure, at the order position the structural model's rule assigns.

If the branch already returns, the existing return is removed only after the new one has validated; the old list closes up with the remaining branches' order preserved.

Where branches departing from different points return to one point, their order on a side is set by the rule in the structural model, section 6: by departure gap index, highest first, ties broken by order in the departure list. A branch that departs higher runs a shorter distance beside its parent and so belongs nearer it.

Branch and return laterals may cross, and are drawn as underpasses where they do. Connections are never reordered to avoid a crossing, since the order is the author's statement and a crossing is only ink.

## 8. Repairing the vacated position

When a task or a project is removed from a line, the gap below it and the gap above it merge into one, exactly as in the structural model, section 2.4. The merged gap keeps the lower gap's id and its branch point, taking the upper gap's departures beyond its own; its return point is the upper gap's, taking the lower gap's arrivals beyond those. Nothing detaches: every branch attached at either gap is attached to the merged gap afterwards, and each retained point keeps its own list in its own order with the orphaned list appended outward of it.

When a branch workflow leaves a departure or return list, the list closes up and the order of the remaining branches is preserved.

Nothing is deleted for being empty (D17). A workflow left with only its start and finish nodes stays, whether or not branches remain attached to its one gap, and a project left with only its begin and end nodes stays as a named placeholder. The author removes either through the delete flow, which confirms first. A start node carries a title, possibly a note, and an activity log, and an automatic deletion would destroy all three without a word.

## 9. Two-ended objects, and the open intermediate

A branch has two ends and one gesture moves one end. Dragging the start node moves the departure; dragging the finish node moves the return. Between the two gestures the branch may be open, which is a legal stored state and not a transaction held open: the application can be closed and reopened with the branch still open, and nothing repairs it.

That is what makes a branch movable between scopes. The author drags the start node to a branch edge inside the new scope, which removes the old return because the new departure cannot legally keep it; the branch is now open. The author then drags the finish node to a return point inside the new scope. Two gestures, each legal, nothing guessed, nothing clamped.

An author may also want a branch to stay open, work that spins off and does not rejoin being an ordinary thing to plan. The finish node's menu carries `Detach return` for that (D18), so the state is reachable directly rather than only as the residue of a move.

## 10. What a drag preserves

A successful drag preserves the identity, title, note reference, activity log, status, flag, here mark, and every other field of every node it moves. A conversion between a workflow boundary and a project boundary (7.2, 7.3) changes `kind` and the pairing, and nothing else.

One entry is appended to the activity log of the node that was dragged, or, when a finish node was dragged, to its workflow's start node, since a finish node carries no log; and to no other node, with the event the catalogue assigns. A cancelled, invalid, stale, or no-op drop appends nothing.

A drag is one command (command layer, section 3), so it is validated in full, persisted atomically, and reversible through the undo slot, the pre-image restoring the log entry's absence along with the structure.

## 11. Pointer mechanics

A press on a handle becomes a drag when the pointer has moved five logical pixels from the press; before that threshold a release is a click, which the chrome interprets (a click on a status glyph cycles status, a double-click on a card body toggles the flag, and so on). The threshold prevents a click with a slight tremor from becoming a no-op drag.

Hit-testing against cards is by the card's axis-aligned box, whatever silhouette it wears; the tilted start ellipse and finish keystone of the mark geometry are inscribed in their boxes for exactly this reason. Hit-testing against drop targets is against the zones section 4 defines, computed from the layout output at drag start and transformed by the camera each frame. A junction diamond's halo (mark geometry, section 9) is a circular hit region of radius 13.

When the pointer, during a drag, comes within 24 logical pixels of the viewport's edge, the viewport pans away from that edge at a rate proportional to the shortfall, up to 12 pixels per frame, so that a target off screen can be reached; the pan stops when the pointer leaves the band.

The ghost is drawn on a layer above every card and track, at the pointer's position offset by the point at which the card was grabbed, so the card does not jump under the hand.

Escape cancels; a release outside the viewport cancels; loss of window focus cancels. A cancelled drag restores the original's full opacity and draws no indicator.

## 12. Within the displayed domain

A drag begins and ends within the currently displayed domain. Objects in other domains are not drawn, so they cannot be targets. A new main workflow created by a drag belongs to the current domain; a branch that becomes a main workflow, and a main workflow that becomes a branch, both stay in it.

## 13. Required properties

The legal target set shown to the pointer is exactly the set of targets whose command the command layer would accept against the record the set was computed from. No drop is refused after its indicator was shown except as `stale`, and no legal drop is hidden.

A cancelled, invalid, stale, or no-op drop leaves the record byte-identical, including every activity log.

Every successful drag is one command, undoable in one step.

No drag produces a record that fails any invariant in the structural model, section 4. In particular, no drag leaves a branch whose departure and return sit in different scopes; where it would, the return is detached instead.

A branch's side and order change only through its start node, and its return changes only through its finish node. No gesture changes both.

Every node moved by a drag has the same field values afterwards as before, except `kind`, `endNode`, and `beginNode` under the two conversions, and except the one appended log entry on the dragged node.
