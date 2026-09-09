<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# The structural model

The authority for the structure: what exists, how the parts are identified, which arrangements are legal, and what state a node carries. It is written so that an implementation in any language can build the store and the validator from it alone. The vocabulary is the [glossary](glossary.md)'s; the reasoning behind the settled choices is in the [decisions record](decisions.md) and is not restated here.

It is not the authority for how the graph is changed (the [command layer](command-layer.md) and the [command catalogue](command-catalogue.md)), for where the marks are placed (the [layout engine](layout-engine.md)), for how they are drawn (the [mark geometry](mark-geometry.md)), or for the shell around the canvas (the [UI chrome](ui-chrome.md)). Where it is silent, choose any reasonable behaviour and record the choice.

Two conventions. Growth is upward: a node's successor sits above it, and a smaller index is lower. Sets written `{…}` are unordered; lists written `[…]` are ordered and their order is model state.

---

## 1. Identity

Every domain, workflow, node, and gap carries an id: an opaque string, stable for the object's whole life and never reused after deletion.

The form is twelve characters, fixed width: a two-character kind prefix, then a base-36 millisecond timestamp of exactly eight characters, then a two-character base-36 counter that resets each millisecond. So `n_mrtwgppt01`. The prefixes are `d_` for a domain, `w_` for a workflow, `n_` for a node, and `g_` for a gap; the counter is shared across all four, so two objects minted in one millisecond differ whatever their kinds.

Five properties are deliberate.

Entirely lowercase, because a node's id is part of its note's filename (`<nodeId>_<slug>.md`) and a case-normalising filesystem must not be able to conflate two ids.

Fixed width, so that a column of ids lines up in a diff. The eight-character timestamp covers 2004 to 2059; a value that would need nine characters is a loud failure rather than a silently mis-sorted id, and a short one is padded.

A counter rather than a random suffix. Randomness only lowers the chance of a collision; a counter removes it. With one writer per installation, pasting two hundred nodes inside one millisecond is exactly the case a counter handles and a short random suffix does not. On the 1296th id in a millisecond the only correct move is to wait for the next one.

Monotonic against a clock that steps backwards, whether by time synchronisation or by hand. A minting call that sees an earlier millisecond than the last one issued holds the last and keeps counting, so no id is ever re-issued.

Opaque, and never parsed. Nothing may infer an object's kind from its prefix; the prefix is a convenience for reading a stored record. That opacity is also the upgrade path: ids are unique by construction within one installation and are not coordinated beyond it, and on the day a second writer exists a device discriminator can be added to newly minted ids without touching a single old one.

Copy and paste mints fresh ids on paste, which it must do in any case to avoid colliding with the destination, and which is why cross-domain uniqueness is a safety property rather than a requirement.

---

## 2. The entities

### 2.1 Domain

A domain holds workflows and the gaps and nodes inside them.

| Field | Type | Notes |
| --- | --- | --- |
| `$schema` | string | the relative name of the JSON Schema beside the record, `domain.schema.json`; written by the application, not model state (persistence, section 3.1) |
| `schema` | integer | the record's schema version; `1` for this specification |
| `revision` | integer | monotonic, incremented on every successful write (section 7) |
| `id` | id | |
| `name` | string | unique within the library |
| `mains` | list of workflow ids | the main workflows, in explicit left-to-right order |
| `workflows` | map id → Workflow | every workflow in the domain, main and branch alike |
| `nodes` | map id → Node | |
| `gaps` | map id → Gap | |

The `mains` list is the domain's left-to-right order of main workflows, which the layout obeys. Branch workflows appear in `workflows` but never in `mains`; they are reached through the branch-point side lists that hold them. A domain's bookmarks are not part of the record; they live beside it, as the [persistence](persistence.md) document describes.

### 2.2 Workflow

A workflow is a linearly ordered run of nodes with the gaps between them.

| Field | Type | Notes |
| --- | --- | --- |
| `id` | id | |
| `nodes` | list of node ids | at least two; first is a `start`, last is a `finish` |
| `gaps` | list of gap ids | exactly one fewer entry than `nodes` |

`gaps[i]` lies between `nodes[i]` and `nodes[i+1]`. The two lists interleave exactly, which is the invariant that makes an orphaned gap unrepresentable.

A workflow is a *main* workflow when its id appears in its domain's `mains`, and a *branch* workflow when its id appears in some branch point's side list. It is exactly one of the two (I5). Nothing else distinguishes them: a workflow record carries no attachment fields at all, and the attachment lives entirely in the arrays that name it. See section 2.6 for why.

### 2.3 Node

| Field | Type | Notes |
| --- | --- | --- |
| `id` | id | |
| `kind` | `start` \| `finish` \| `begin` \| `end` \| `task` | fixed at creation except by the two conversions the catalogue defines |
| `title` | string | `start`, `begin`, and `task` only; may be empty |
| `endNode` | node id | `begin` only; the id of the project's `end` node |
| `beginNode` | node id | `end` only; the id of the project's `begin` node |
| `note` | filename or null | `start`, `begin`, and `task` only; the reference to the node's note file, which holds its prose |
| `status` | `todo` \| `in-progress` \| `completed` \| `cancelled` | `task` only |
| `completedAt` | timestamp or null | `task` only; present exactly while `status` is `completed` (I18) |
| `flagged` | boolean | `start`, `begin`, and `task` only |
| `here` | boolean | `task` only; at most one true per workflow |
| `log` | list of log entries | `start`, `begin`, and `task` only; section 5 |

A field marked for one kind is absent on the others, not present and null. A validator rejects a `status` on a `begin` node rather than ignoring it, because a field that is silently ignored is a field that silently diverges.

The `title` rule is what makes a boundary pair legible: the node that opens the pair is named and the node that closes it is not, so a workflow is named by its start node and a project by its begin node. A `finish` node and an `end` node carry no label, no note, no flag, and no log, in the model and on the canvas alike: a finish node is its id and its kind, and an end node its id, its kind, and its `beginNode`. Everything a pair records lives on the node that opens it.

### 2.4 Gap, and the two points within it

A gap is the space between two consecutive nodes. It owns two points: a branch point, the lower, at which branches depart; and a return point, the upper, at which branches arrive. A point is addressed as `(gap id, branch|return)` and is not separately stored.

| Field | Type | Notes |
| --- | --- | --- |
| `id` | id | |
| `branchLeft` | list of workflow ids | branches departing here on the left, inner to outer |
| `branchRight` | list of workflow ids | departing here on the right, inner to outer |
| `returnLeft` | list of workflow ids | branches arriving here on the left, inner to outer |
| `returnRight` | list of workflow ids | arriving here on the right, inner to outer |

All four lists are usually empty; a gap with four empty lists is an ordinary space between two nodes and is the common case.

Reading upward through a gap, the sequence is: the lower node, the *outgoing edge*, the branch point, the *middle edge*, the return point, the *incoming edge*, the upper node. Those three edge names are structural positions, not merely drawn objects: they are the three places a node can be inserted within one gap, and they differ in their relation to whatever is attached.

- Inserting on the outgoing edge places the new node below both the departures and the arrivals at this gap.
- Inserting on the middle edge places it above the departures and below the arrivals.
- Inserting on the incoming edge places it above both.

Every insertion splits one gap into two. The gap record follows its branch point: whichever of the two resulting gaps holds the branch point keeps the id, and the other is a fresh record. So a departure's gap id is stable across all three insertions, and an arrival's gap id changes only when a node is inserted on the middle edge, which is the one case that separates the two points.

Removing a node merges the gap below it with the gap above it, and both gaps' attachments survive. The merged gap keeps the lower gap's id. Its branch point is the lower gap's, since the departures nearest the vacated position are the ones that stay put, with the upper gap's departures appended beyond them; its return point is the upper gap's, with the lower gap's arrivals appended beyond those. So each retained point keeps its own list in its own order and receives the orphaned list outward of it, and the upper gap's record is discarded. Nothing detaches: a branch whose departure or arrival sat on either gap is attached to the merged one afterwards.

### 2.5 A project is a node pair, not a record

A project is a `begin` node and the `end` node it names in `endNode`, both in the same workflow, the begin below the end. Everything between them, and every branch departing from a gap between them, is inside its scope. There is no project record: a project has no state of its own beyond what its two nodes carry, and a folded project's fold state is per-client view state keyed by the begin node's id, not model state.

The reference is stored on both nodes, `endNode` on the begin node and `beginNode` on the end node, rather than recovered by matching nesting like brackets, because a stored reference is checked in constant time and a scan is both slow and fragile under partial writes.

### 2.6 A branch attachment is array membership, and nothing else

A branch workflow is attached because some gap's `branchLeft` or `branchRight` names it. Its side is which list, its order is its index in that list, and its host gap is that gap. It returns because some gap's `returnLeft` or `returnRight` names it, and it is open when no return list names it.

Nothing about the attachment is stored on the workflow record. This is deliberate: side would otherwise be recorded twice, once as a field and once by which array holds the id, and a model that stores one fact twice is a model that will eventually store it two ways. An implementation builds a reverse index at load time (workflow id → its departure and its return) and rebuilds it on every write; the index is never persisted.

---

## 3. Position and containment

Positions within a workflow are given by index into its `nodes` and `gaps` lists, counting from zero at the bottom.

A project whose `begin` is at node index `b` and whose `end` is at node index `e` contains the nodes at indices `b+1` through `e-1` and the gaps at indices `b` through `e-1`. The gap range is the useful one: gap `b` is the space immediately above the begin node, and gap `e-1` is the space immediately below the end node, and both are inside.

The **scopes containing a gap** are that gap's workflow and the projects on it whose gap range includes the gap. The **innermost** of them is the project with the largest `b`, which by proper nesting (I7) is unique, or the workflow itself when no project contains the gap. The scopes containing a node are defined the same way over the node range.

A branch workflow is *part of* the innermost project containing its departure gap, or of no project when that gap is in none. This is derived, never stored.

---

## 4. The invariants

The complete list of what must hold of a stored domain. An implementation builds one checker from this list, runs it on load and after every write, and refuses a write that would break any of them. Numbering is stable; add, do not renumber.

**Structure**

- **I1.** Every node belongs to exactly one workflow and appears exactly once in that workflow's `nodes`.
- **I2.** A workflow's `nodes` has at least two entries. The first has kind `start`, the last has kind `finish`, and no other entry has either kind.
- **I3.** A workflow's `gaps` has exactly one fewer entry than its `nodes`.
- **I4.** Every gap belongs to exactly one workflow and appears exactly once in that workflow's `gaps`.
- **I5.** Every workflow appears exactly once across the union of its domain's `mains` and every branch-point side list in the domain. One in `mains` is a main workflow; one in a branch-point list is a branch workflow.

**Projects**

- **I6.** A `begin` node's `endNode` is an `end` node in the same workflow at a higher index; an `end` node's `beginNode` is a `begin` node in the same workflow at a lower index; the two references are symmetric and one-to-one.
- **I7.** Project ranges nest properly: any two projects in one workflow have ranges that are disjoint or nested, never partially overlapping.

**Branches**

- **I8.** A branch workflow appears in at most one return list. One that appears in none is open, which is legal (D3).
- **I9.** If a branch returns, its departure gap and its return gap belong to the same workflow.
- **I10.** If a branch returns, its return is on the same side as its departure: a branch in some gap's `branchLeft` may appear only in a `returnLeft`, and one in a `branchRight` only in a `returnRight`.
- **I11.** If a branch returns, the index of its return gap is greater than or equal to the index of its departure gap. Departing and returning within one gap is legal; returning below the departure is not.
- **I12.** If a branch returns, the set of scopes containing its departure gap equals the set containing its return gap. Not merely the same depth: the same projects.
- **I13.** The branch relation is acyclic. No workflow is a branch of itself or of any workflow reached by following departures from it.

**State**

- **I14.** Only a `start`, a `begin`, or a `task` node has a `title`, a `note`, a `flagged`, or a `log`; only a `begin` node has an `endNode`, and only an `end` node a `beginNode`; only a `task` has a `status`, a `completedAt`, or a `here`.
- **I15.** At most one node in a workflow has `here` true.
- **I18.** A task's `completedAt` is present if and only if its `status` is `completed`.

**References**

- **I16.** Every id named by any list or reference resolves to an object of the expected kind in the same domain. No reference crosses a domain.
- **I17.** Every side list holds distinct ids, and each names a branch workflow of this domain.

I13, together with I11 and proper nesting, is what makes the whole graph directed and acyclic. A drop's legality therefore follows from these structural facts checked on the result, and no separate acyclicity test is needed on the gesture.

---

## 5. Node state and the activity log

`status` takes one of four values, `todo`, `in-progress`, `completed`, `cancelled`, and cycles in that order when the status glyph is clicked. A task entering `completed` is stamped with `completedAt`, the UTC RFC 3339 time of the change, and leaving `completed` clears it, so the field is present exactly while the status is (I18). `flagged` drives the flagged-only review mode and may be set on any start node, begin node, or task. `here` marks the task an author points out within its workflow, at most one per workflow (I15), and is shared with other writers rather than being a local view state.

A node's written prose is its **note**, and that is the only name for it. There is no second, shorter description field: a start node, a begin node, or a task has a note or it has none, and a finish node or an end node has none.

The note is a markdown file in the domain's `notes/` directory, and the node record holds only its filename. Four consequences follow, each of which an implementation will meet.

Whether a node has prose is answered by the reference alone, without opening the file, which is what lets the canvas decide whether to draw a note glyph while drawing several hundred cards.

A note's text is not part of the domain record, so writing it is not part of a domain operation and does not pass through section 7's atomicity. The note editor autosaves on its own debounce, and a note file changed by another writer is reconciled separately from a changed domain record. The single point where the two writes meet is the first non-empty save of a new note, which both creates the file and records its filename on the node; that pair must be ordered file first, so a failure leaves an unreferenced file rather than a reference to nothing.

A note file with no node referencing it is a legal state, not an integrity fault, so I16 does not reach into `notes/`. Deleting a node leaves its note file behind as an orphan; only deleting the whole domain, or the explicit delete-note operation while the node still exists, removes one.

A node may hold a reference to an empty file. Emptying a note is not deleting it, so the reference and the glyph both remain; the glyph means a note exists here, not that it has text in it.

The **activity log** is a list of entries on a start node, a begin node, or a task, oldest first; a finish node or an end node has none.

| Field | Type | Notes |
| --- | --- | --- |
| `id` | id | unique within the node; the `n_` prefix is not used, an entry's id being minted with the prefix `e_` |
| `at` | timestamp | when the entry was created, in UTC, RFC 3339 |
| `author` | `{kind: user\|agent\|system, name}` | who wrote it |
| `origin` | `system` \| `manual` | whether the application wrote it or a person or agent did |
| `event` | string or null | for a `system` entry, the event code the catalogue assigns; null on a manual entry |
| `text` | string | |
| `editedAt` | timestamp or null | set on every revision after the first |
| `editedBy` | author or null | |

The log is editable by users and by agents (D6), which is why `origin`, `editedAt`, and `editedBy` exist: without them a revised entry is indistinguishable from an original one, and the log could not even report its own history honestly. It is a worklog, and it cannot answer what actually happened.

Which commands write a `system` entry, to which node, and with which `event` code, is specified with each command in the [catalogue](command-catalogue.md), under the rule of D31 in the decisions record: one entry, to the command's subject node, for a structural change or a status change.

---

## 6. Ordering

Three orderings are model state, each an ordered array on the containing record (D10): the domain's `mains`, left to right; each branch point's two side lists, inner to outer; each return point's two side lists, inner to outer.

Where the application must place a return automatically rather than being told where, it uses this rule, which is model-side and deterministic: within one return-point side list, order the branches by the index of their departure gap, highest first, and break a tie by their order in that departure list.

The reasoning is worth keeping. A branch departing higher up its parent's line runs a shorter distance alongside it, so it belongs nearer that line; a branch departing lower must span more of the line, and placing it inside a shorter one would force their lines to cross. A rule stated in terms of graphical distance from the parent would make the stored order depend on a layout that then has to read the stored order; departure-gap index is the model-side quantity that graphical distance stands for.

---

## 7. Change, atomicity, and undo

Every change to a domain is a single atomic operation: it is validated in full against section 4 before anything is written, it is persisted as a unit, and a failure leaves the stored domain exactly as it was. A partially applied operation is never observable, by the canvas or by another reader.

Note text sits outside this. A note is a separate file with its own write path (section 5), and the only write that crosses the boundary is the recording of a new note's filename on its node.

**Undo** holds one operation, not a stack (D9). The slot takes the most recent structural or state operation that originated in the local user interface, and undoing it also removes the activity-log entry that operation created. There is no redo.

An operation arriving from the automation server never fills the slot, and it *invalidates* whatever the slot holds rather than being undone through. Reversing across another writer's change is how one silently destroys their work, and the check costs no more than comparing a domain revision counter. Switching or deleting the open domain clears the slot, as does quitting. Note text is not covered; the note editor keeps its own text undo.

**Concurrent writers.** The automation server and the user write the same store. Each domain therefore carries the `revision` counter of section 2.1, incremented on every successful write. A writer holding a stale revision has its write refused rather than merged, and the refusal is what the chrome surfaces as its `Change not saved` dialog.

---

## 8. A worked instance

One small domain in full, as a verification fixture. It exercises a project, a branch that returns inside that project, an open branch, and two here marks in two workflows.

```
domain d_ex01  name "Example"  schema 1  revision 7  mains [w_main]

w_main  nodes [n_s1, n_t1, n_b1, n_t2, n_t3, n_e1, n_t4, n_f1]
        gaps  [g_0,  g_1,  g_2,  g_3,  g_4,  g_5,  g_6]

  n_s1  start  title "Ship v1"
  n_t1  task   "Draft spec"      status completed  completedAt 2026-09-01T16:20:00Z
  n_b1  begin  title "Build"     pair n_e1
  n_t2  task   "Backend"         status in-progress   here
  n_t3  task   "Frontend"        status todo
  n_e1  end    pair n_b1
  n_t4  task   "Announce"        status todo    flagged
  n_f1  finish

  g_3   branchLeft [w_qa]
  g_4   returnLeft [w_qa]
  g_6   branchRight [w_docs]
  (g_0, g_1, g_2, g_5 hold four empty lists)

w_qa    nodes [n_s2, n_t5, n_f2]   gaps [g_7, g_8]
  n_s2  start  title "QA pass"
  n_t5  task   "Write tests"     status in-progress   here
  n_f2  finish

w_docs  nodes [n_s3, n_t6, n_f3]  gaps [g_9, g_10]
  n_s3  start  title "Write docs"
  n_t6  task   "API reference"   status todo
  n_f3  finish
```

Reading it against section 4. The project `n_b1`/`n_e1` sits at node indices 2 and 5, so it contains nodes 3 and 4 and gaps 2, 3, and 4. Branch `w_qa` departs at gap 3 and returns at gap 4, both inside that project and inside no other, so the scope sets are equal and I12 holds; the return index exceeds the departure index, so I11 holds; both are left-side, so I10 holds. Branch `w_docs` departs at gap 6, which lies in no project, and appears in no return list, so it is open, which I8 permits. Two nodes carry `here`, `n_t2` and `n_t5`, but in different workflows, so I15 holds. `n_f1`, `n_f2`, `n_f3`, and `n_e1` carry no title, note, flag, or log, per I14.

Three edits that must be refused, and why: moving `w_qa`'s return to gap 5 breaks I12, since gap 5 lies outside the project while its departure lies inside; moving it to gap 2 breaks I11, since gap 2 is below its departure; attaching `w_main` to a gap inside `w_qa` breaks I13.

The same instance, in the on-disk canonical form, is the first fixture in the [persistence](persistence.md) document.
