<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# The command catalogue

Every command the [command layer](command-layer.md) admits, with its
arguments, scope tier, undoability, subject, precondition, effect, refusal
text, and activity-log entry. The window's menus, dialogs, and drags, and the
automation server's tools, are callers of these commands and issue nothing
else; a gesture or a tool that cannot be expressed as one command here does
not exist.

Vocabulary is the [glossary](glossary.md)'s; structure and invariants are the
[structural model](structural-model.md)'s. Where a command's effect is a
consequence of the structural model's own rules (how a gap splits on
insertion, how two gaps merge on removal), this document names the rule rather
than restating it.

---

## 1. Conventions

**Arguments.** Every argument that names an object takes an id and nothing
else. Titles change under a caller between its read and its write, so a
title is never an address on a write. A `node` argument accepts a node of any
kind unless the command says which; a command that takes one kind refuses the
rest and names the command that would accept them.

**Positions.** Several commands place something. They share one target
grammar:

```
Target
  | { edge:   gap, position: outgoing | middle | incoming }   a trunk-edge position
  | { branch: gap, side: left | right, index }               a branch-point position
  | { main:   index }                                         a position in the domain's mains
```

An edge target names a gap by id and one of its three positions (structural
model, section 2.4). A branch target names a gap by id, a side of that gap's
branch point, and an order position on that side, where `index` equal to the
side's length appends outermost. A main target names a position in `mains`,
where `index` equal to the length appends rightmost. A gap id is the stable
address of a departure across insertions, so a target computed from a read
stays meaningful until a write changes the gap in question.

**The subject.** Each command names one node as its subject: the node the
command is about, on whose activity log a `system` entry is written when the
command is structural, and whose title the undo menu shows. A command whose
subject ceases to exist (a deletion) writes no entry.

**Tiers.** `read-write` unless stated; `destructive` where the command
removes nodes or files. Reads are listed in section 9 and are not commands.

**Undoable** means the command fills the undo slot when its origin is `ui`
(command layer, section 8). Every record-writing command is undoable except
those the table marks otherwise.

**Log events.** A structural command appends one entry to its subject's log
with `origin: system`, the `actor` the command carried, an `event` code from
this set, and a frozen prose `text` in the form the command specifies:

| Event | Written by |
| --- | --- |
| `created` | a command that brings the subject into existence |
| `moved` | a command that changes the subject's position, side, or order |
| `converted` | a command that changes the subject's kind between a workflow boundary and a project boundary |
| `attached` | a command that gives a branch a return |
| `detached` | a command that removes a branch's return |
| `wrapped` | a command that closes a run of nodes into a new project |

State commands (title, status, flag, cursor, note text, log entries) write no
`system` entry; they are not structural (decisions, P4).

**Refusal text.** Each command lists its refusals as the message a caller
receives, with the code from the command layer's closed set. A message names
the rule and, where one exists, the legal alternative. Placeholders in angle
brackets are filled with the title of the node concerned, or its id when the
title is empty.

**Vacated positions.** Whenever a command removes a node from a workflow, the
gap below it and the gap above it merge as the structural model, section 2.4,
describes; nothing detaches, and each retained point keeps its own list in its
own order with the orphaned list appended outward. Whenever a command removes
a branch from a side list, the list closes up and the order of the rest is
preserved. Nothing is deleted for being empty (D17). Where two "here" cursors
would meet in one workflow, the receiving workflow's survives and the arriving
one is cleared (D16).

---

## 2. Domains

These three act on the library rather than on a record, so they take no
`revision` and fill no undo slot.

### `create_domain(name)`

Tier read-write. Not undoable. Creates a directory in the library named for
the new domain's id and a slug of its name ([persistence](persistence.md)),
writes an empty record (`schema 1`, `revision 0`, empty `mains`, `workflows`,
`nodes`, and `gaps`), and creates its `notes/` directory.

Refusals. `bad_arguments`: "A domain name is one to sixty-four characters
with no leading or trailing space and no control characters." `refused`: "A
domain named <name> already exists; domain names are unique within the
library."

### `rename_domain(domain, name)`

Tier read-write. Not undoable. Sets the record's `name` and re-derives the
directory's label from it. Refusals as for `create_domain`.

### `delete_domain(domain)`

Tier destructive. Not undoable. Moves the whole domain directory, record,
bookmarks, and notes, to the system's Trash, from which it can be restored.
The argument is required; a caller may not delete "the open domain" by
omission. Refusal `not_found`: "No domain named <domain>."

---

## 3. Workflows

### `create_workflow(title, target?)`

Tier read-write. Undoable. Subject: the new start node. Creates a main
workflow of exactly a start node carrying `title` and a finish node, with one
empty gap between them, and inserts its id in `mains` at the main target given
or, absent one, at the end. Log: `created`, "Created workflow <title>."

Refusal `bad_arguments`: "The target of a new workflow is a position among the
domain's main workflows."

### `move_workflow(workflow, target)`

Tier read-write. Undoable. Subject: the workflow's start node. The whole
workflow travels: its finish node and everything in it, descendant branches
included. Three targets are legal and each does something different.

Onto a **branch target**, the workflow is attached at that gap's branch point,
on that side, at that order position. What happens to an existing return
depends on where the workflow was:

- Reordered on the same side of the same point: the return is preserved, and
  its order position at the return point is set to correspond to the new
  departure order.
- Moved to the other side of the same point: the return is preserved and
  moves to the matching side of its return point, its order set to
  correspond.
- Moved to a different branch point, in this workflow's parent or in any other
  workflow: the old departure and, if it had one, the old return are removed
  only after the new attachment has validated, and no new return is created.
  The branch is now open, and the author attaches its return with
  `attach_return`. The application does not guess where a branch should
  rejoin.

A main workflow moved onto a branch target leaves `mains` and becomes a
branch. If the target gap lies inside projects, the workflow becomes part of
the innermost.

Onto an **edge target** in the workflow's own parent, a branch workflow
**becomes a project** and is spliced in at that position. Its start node
becomes the begin node and its finish node the end node, paired; identities,
titles, notes, logs, states, and every other field are preserved, and only
`kind` changes. Everything within travels. Its departure and its return, if
any, are removed only after the drop has validated. If the target lies inside
projects, the new project nests in the innermost. Log: `converted`, "Became
the project <title> in <parent workflow title>."

Onto a **main target**, a branch workflow's departure and return are removed
and it becomes a main workflow at the indicated position; a main workflow
simply moves in the order.

Log for the branch and main cases: `moved`, with text "Moved to the <side>
of <lower node title> in <parent title>" for a branch target, or "Moved to
position <n> of the domain's workflows" for a main target.

Refusals. `not_found`: "No workflow <id>." `bad_arguments`: "The argument is
a workflow's start node; a project moves with `move_project` and a task with
`move_task`." `refused`: "A workflow cannot become a branch of itself or of a
workflow that descends from it." `refused`: "Only a branch may become a
project, and only in the workflow it departs from; move it to a branch point
there first." `refused`: "That position is where the workflow already is;
nothing to do." (a no-op is not an error in the window, which simply does
nothing; it is reported to an agent so that the agent knows its call changed
nothing.)

### `set_title(node, title)`

Tier read-write. Undoable. Subject: the node. Sets the title of a start,
begin, or task node; may be empty. State, no log entry.

Refusal `bad_arguments`: "A finish node and an end node carry no title; a
workflow is named by its start node and a project by its begin node."

---

## 4. Tasks

### `insert_task(gap, position, title)`

Tier read-write. Undoable. Subject: the new task. Creates a task with `title`,
`status: todo`, in the named gap at the named position; the gap splits as the
structural model, section 2.4, describes, the record following its branch
point. If the gap lies inside projects, the task is part of the innermost.
Log: `created`, "Created above <lower node title>."

The window's `Add task above <node>` issues this command for the gap above
the node at its `outgoing` position (immediately above the node, below any
departures there); `Add task below <node>` issues it for the gap below the
node at its `incoming` position (immediately below the node, above any
arrivals there). A closer has no gap above it and an opener none below, which
is why those items are absent on those nodes.

Refusals. `not_found`: "No gap <id>." `bad_arguments`: "A position is
outgoing, middle, or incoming."

### `move_task(task, target)`

Tier read-write. Undoable. Subject: the task. The task travels alone. Onto an
edge target, it is removed from where it was, its vacated position repaired,
and spliced in at the stated position; if the target lies inside projects, it
becomes part of the innermost. Onto a main target, it becomes the sole task of
a new main workflow: a start node with an empty title and a finish node are
created around it, and the workflow is inserted at the indicated position.
Log: `moved`, "Moved above <lower node title> in <workflow title>" or "Moved
into a new workflow."

The window's `Move up` and `Move down` issue this command for the next
distinct position above or below the task along its workflow, where the
positions of a workflow read, from the bottom, as each gap's outgoing, middle,
and incoming positions in turn, and a zero-length middle edge is skipped.

Refusals. `bad_arguments`: "The argument is a task; a project moves with
`move_project` and a workflow with `move_workflow`." `bad_arguments`: "A task
cannot be dropped at a branch point; open a branch there instead, or move a
project or a workflow." `refused`: the no-op message.

### `set_status(task, status)` and `cycle_status(task)`

Tier read-write. Undoable. Subject: the task. Sets, or advances in the order
todo, doing, done, cancelled, todo, the task's status. State, no log entry.

Refusal `bad_arguments`: "Only a task has a status." `bad_arguments`: "A
status is todo, doing, done, or cancelled."

### `set_here(task)` and `clear_here(task)`

Tier read-write. Undoable. Subject: the task. `set_here` sets the cursor on
the task and clears it from any other task in the same workflow; `clear_here`
clears it. State, no log entry.

Refusal `bad_arguments`: "Only a task can carry the cursor."

### `set_flag(node, flagged)`

Tier read-write. Undoable. Subject: the node. Sets or clears the flag on any
node. State, no log entry.

---

## 5. Projects

### `wrap_run(from, to, title)`

Tier read-write. Undoable. Subject: the new begin node. `from` and `to` are
nodes of one workflow, `from` at or below `to`, neither a start nor a finish.
A begin node carrying `title` is inserted immediately below `from` (the gap
below `from`, at its incoming position) and an end node immediately above
`to` (the gap above `to`, at its outgoing position), and the two are paired.
Every branch departing from a gap inside the run becomes part of the new
project. Log: `wrapped`, "Wrapped <from title> to <to title> as <title>."

A run is legal while it neither straddles a project boundary nor cuts a
branch's scope: it may not take in a begin node without its end or an end
without its begin, and no branch may depart inside the run and return outside
it, or depart outside and return inside. The window's `Wrap as sub-project`
submenu offers each legal `to` from `from` upward, and ends where legality
does.

Refusals. `bad_arguments`: "A run is bounded by two nodes of one workflow,
the lower first, and neither may be its start or finish." `refused`: "The run
would take in the begin node of <title> without its end; a project is wrapped
whole or not at all." `refused`: "The branch <title> departs inside the run
and returns outside it; a branch cannot reach out of its scope. Move its
return inside the run, detach it, or shorten the run."

### `unwrap_project(begin)`

Tier read-write. Undoable. Subject: none; the begin node is removed. Removes
the begin node and its end node, leaving the contents in place on the
workflow; the two vacated positions are repaired, and every branch that was
part of the project becomes part of the enclosing project, or of none. The
begin node's title, note reference, and log are lost with it, which is why
the window confirms first. No log entry.

Refusal `bad_arguments`: "The argument is a begin node; a task or a workflow
is not unwrapped." Use `convert_project_to_task` to keep the begin node's
identity.

### `convert_task_to_project(task)`

Tier read-write. Undoable. Subject: the task, which becomes the begin node.
The task's `kind` becomes `begin`; its `status` and `here` are dropped; a new
end node is inserted immediately above it and paired with it, so the result is
an empty project bearing the task's title, note, log, and flag. Log:
`converted`, "Became a project."

Refusal `bad_arguments`: "Only a task becomes a project."

### `convert_project_to_task(begin)`

Tier read-write. Undoable. Subject: the begin node, which becomes the task.
The begin node's `kind` becomes `task` with `status: todo`; its end node is
removed and the vacated position repaired; the project's contents stay in
place and its branches become part of the enclosing project, or of none. The
node keeps its identity, title, note, log, and flag. Log: `converted`,
"Became a task."

Refusal `bad_arguments`: "Only a begin node becomes a task."

### `move_project(begin, target)`

Tier read-write. Undoable. Subject: the begin node. The whole project
travels: its end node and every task, nested project, and branch within its
scope.

Onto an **edge target**, the project is removed from where it was, its
vacated position repaired, and spliced in at the stated position, nesting in
the innermost project containing the target. Log: `moved`, "Moved above
<lower node title> in <workflow title>."

Onto a **branch target**, the project **becomes a branch workflow**. Its begin
node becomes the workflow's start node and its end node its finish node, with
their identities, notes, logs, states, and every other field preserved; only
`kind` changes, and `pair` is replaced by the two ends' membership of one
workflow. The contents travel unchanged. The branch is attached at the
target's side and order position, and if the target gap lies inside projects
it is part of the innermost. No return is created; the new branch is open,
and the author attaches its return with `attach_return`. Log: `converted`,
"Became the branch <title> off <lower node title>."

Onto a **main target**, the project becomes the contents of a new main
workflow: a start node with an empty title and a finish node are created
around it, and the workflow is inserted at the indicated position. Log:
`moved`, "Moved into a new workflow."

Refusals. `bad_arguments`: "The argument is a begin node; a task moves with
`move_task` and a workflow with `move_workflow`." `refused`: "A project cannot
be dropped inside itself or inside a project nested within it." `refused`:
the no-op message.

---

## 6. Branches

### `open_branch(gap, side, title)`

Tier read-write. Undoable. Subject: the new start node. Creates a branch
workflow of a start node carrying `title` and a finish node, with one empty
gap between them, and appends its id outermost on the named side of the named
gap's branch point. The branch is open. If the gap lies inside projects, the
branch is part of the innermost. Log: `created`, "Opened off <lower node
title> on the <side>."

The window's `Add branch above <node>` issues this for the gap above the
node; `Add branch below <node>` for the gap below it; the side is the one the
menu names, or the pointer's side when opened by a gesture.

Refusals. `not_found`: "No gap <id>." `bad_arguments`: "A side is left or
right."

### `attach_return(branch, gap)`

Tier read-write. Undoable. Subject: the branch's finish node. Makes the
branch return at the named gap's return point, on the same side as its
departure, at the order position the structural model's automatic-return rule
assigns (section 6). If the branch already returns, the old return is removed
only after the new one has validated, and the old list closes up. Log:
`attached`, "Returns above <lower node title>."

The legal gaps are those of the branch's parent workflow at or above its
departure gap and inside exactly the same projects as that gap. The window's
`Merge a branch here` submenu on a node lists the open or returning branches
for which the gap above that node is legal; the finish node's drag targets
are the same set.

Refusals. `bad_arguments`: "The argument is a branch workflow; a main
workflow has no return." `refused`: "The return point is below the branch's
departure; a branch returns at or above where it left." `refused`: "The
return would land outside the project <title> that the branch departs from; a
branch cannot reach out of its scope." `refused`: "The return point is on
another workflow; a branch returns to the workflow it left."

### `detach_return(branch)`

Tier read-write. Undoable. Subject: the branch's finish node. Removes the
branch's return, leaving it open; the return list closes up. Log:
`detached`, "Return detached."

Refusal `refused`: "The branch <title> has no return to detach."

---

## 7. Notes and the activity log

### `set_note(node, text)`

Tier read-write. Not undoable (the note editor keeps its own text undo).
Subject: the node. Writes `text` to the node's note file. When the node has
no note reference and `text` is non-empty, the file is created under the name
the [persistence](persistence.md) document derives and the filename is then
recorded on the node, file first and record second (command layer, section
7); this is the one case in which the command writes the record and
increments the revision. When the node already has a reference, only the file
is written, empty text included: emptying a note is not deleting it. When the
node has no reference and `text` is empty, nothing is written. No log entry.

Refusal `write_failed` with the filesystem's message.

### `delete_note(node)`

Tier destructive. Not undoable. Subject: the node. Deletes the note file and
clears the node's reference. The text is not recoverable, which the window's
dialog says before it asks. No log entry.

Refusal `refused`: "<title> has no note."

### `add_log_entry(node, text)`

Tier read-write. Undoable. Subject: the node. Appends an entry with `origin:
manual`, the command's `actor` as author, `event: null`, and `text`.

### `edit_log_entry(node, entry, text)`

Tier read-write. Undoable. Subject: the node. Replaces the entry's `text` and
sets `editedAt` to now and `editedBy` to the command's actor. A `system` entry
is edited on the same terms as a manual one (P4); its `event` code is kept.

Refusal `not_found`: "No entry <id> on <title>."

### `delete_log_entry(node, entry)`

Tier read-write. Undoable. Subject: the node. Removes the entry.

---

## 8. Deletion and paste

### `delete_node(node)`

Tier destructive. Undoable. Subject: none. What is removed depends on the
kind, and a closer is refused outright.

- A **task**: the node alone; its two gaps merge and every branch attached at
  either survives on the merged gap.
- A **begin node**: the project's whole extent, its end node, its contents,
  and every branch that is part of it, with those branches' own descendants.
  To remove the pair and keep the contents, use `unwrap_project`.
- A **start node**: the whole workflow, its finish node, its contents, and
  every descendant branch. A main workflow leaves `mains`; a branch workflow
  leaves its departure and return lists, which close up.

Note files of removed nodes stay in the domain's `notes/` directory as
orphans; only `delete_note` while the node exists, or `delete_domain`, removes
one. The window confirms before every deletion whose extent holds more than
the node itself.

Refusals. `bad_arguments`: "A finish node and an end node are one half of a
pair and have no life of their own; delete the workflow by its start node, or
the project by its begin node." `refused`: "Deleting <title> would remove
<n> nodes; confirm." (issued to the window only, which turns it into the
dialog; an agent's call carries no confirmation and proceeds.)

### `paste(clip, target)`

Tier read-write. Undoable. Subject: the new opener. A clip is the value
`copy_project` returns (section 9): a project's extent with fresh ids minted
on paste and every note's text carried by value. Onto an edge target, the
clip is spliced in as a project; onto a branch target, as a branch workflow
whose start and finish nodes are the clip's begin and end; onto a main
target, as a new main workflow likewise. Note files are written for every
node that had a note, before the record. Log: `created`, "Pasted."

Refusals. `bad_arguments`: "The clip is malformed." Refusals of the target as
for `move_project`.

---

## 9. Reads

Reads take the lock, read the record, and answer from it with the domain's
`revision`. They pass through no mutation and no validator, and every tier
includes them.

| Read | Returns |
| --- | --- |
| `list_domains()` | each domain's id, name, and path |
| `read_domain(domain, notes?)` | every workflow in outline plus the structured record, and the revision; with `notes` true, each note's text |
| `read_workflow(workflow, notes?)` | one workflow in outline and in structure, with its branches' ids, its departure and return if a branch, and the id of the innermost project containing its departure |
| `read_project(begin, notes?)` | the project's extent, bounded by its end node, with the ids of the enclosing project and the containing workflow |
| `read_node(node, note?)` | one node in structure, with its workflow's id, its index, the innermost project containing it, and for a task its two neighbouring gaps' ids and their positions |
| `read_note(node)` | the note's text, or empty when the node has none |
| `read_log(node)` | the node's activity log, newest first |
| `find_flagged(domain)` | every flagged node with its kind, title, workflow, and innermost project |
| `copy_project(begin)` | a clip for `paste` |

The outline form is a nested text rendering of a workflow: one line per node
with its kind glyph, title, and status, branches indented beneath the lower
node of the gap they depart from and marked with the gap they return to, so
that an agent can read a workflow in one call and address any node or gap by
the id printed beside it.

---

## 10. Required properties

Every command either produces a record that satisfies all seventeen
invariants or refuses, and a refusal leaves the stored record byte-identical.

A command's subject is the only node whose activity log changes, and only a
structural command changes it.

Every field of every node a command moves is preserved, except `kind` and
`pair` under the two conversions, `status` and `here` when a task becomes a
begin node, and the one appended log entry on the subject.

No command creates a return. Only `attach_return` does, and only where the
author points.

No command deletes a node for being empty, moves a return to keep it legal,
or reorders a side list for any reason but the author's instruction.
