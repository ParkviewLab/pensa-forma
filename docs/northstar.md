<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# PensaForma: northstar

This northstar is the canonical statement of this application's purpose. It
is here to guide every design decision and feature proposal, and each is
weighed against it. Where it and any other document disagree, this one is the
authority and the other is the thing to fix; where it and the code disagree,
the code is wrong. A change of intent is therefore made here first, in the
same pull request as the code that follows it, so that no disagreement is
ever left standing by accident.

## What it is

PensaForma is a studio in which people and AI agents visually plan and track
work together, as a living graph of workflows. A workflow orders tasks. It may
contain projects (which group a contiguous run of its tasks and sub-projects)
and branches (which are workflows that run in parallel beside it, and may or
may not rejoin it). Main workflows (those that are not branches) are gathered
into domains (HomeLab, Work, and so on), each a set of plain files on the
user's own disk.

A domain is drawn as a mid-century retrofuturist flowchart, and it is
restructured by dragging tasks, whole projects, and whole workflows. An AI
agent works on a domain through a local Model Context Protocol (MCP)
automation server that runs while the application does. Every workflow,
project, and task may carry a written note and always carries an activity log,
which people and agents both write. A task has a status: to do, in progress,
done, or cancelled. On each workflow one task may be marked here, the place
where the work is in that workflow; and any workflow, project, or task may be
flagged for attention, so that a review can show the flagged items alone.

## Why it exists

Most task tools are flat lists or nested checklists. Neither matches how a
piece of work actually grows: one is somewhere specific, tasks queue up ahead,
and every so often part of the work runs in parallel for a while and then
comes back together, or goes its own way and never does. And most task tools
are built for one kind of author. This application is built so that the tool's
structure is that structure, so that the shape of the work can be seen at a
glance, and so that an AI agent is a first-class author of it, working through
the same operations as a person and leaving the same record.

## Four intents

These are complementary facets of one purpose, not a ranking.

### 1. The structure is the mental model

Workflows, projects, tasks, and branches. A workflow opens at a start node and
closes at a finish node, so it is a bounded run of work rather than an
open-ended pile; a project opens at a begin node and closes at an end node
inside a workflow; a task is one thing to do, sitting on the line between them.
A branch is a workflow of its own that departs from a point between two nodes
of its parent, runs alongside, and either returns to a later point or runs
open. The data model stores exactly this and nothing that contradicts it: five
node kinds, each intrinsic; a gap record between every pair of consecutive
nodes, owning the branch point where branches depart and the return point
where they arrive; on each point two ordered sides.

### 2. Structure is legible at a glance

A domain is drawn as a mid-century retrofuturist flowchart laid out like a
transit map: stations are nodes, tracks are the lines they sit on, and a
junction between two stations is where a branch leaves or returns. Before
reading a single label one can see the shape of the work: where one is (the
task marked here), what is done, in progress, or cancelled (the outline
colour), where a line branches, where it comes back, and where it does not.
The visual channel carries the structure; text only names it.

### 3. It is yours, and it is local

A domain is plain files on the user's own disk: one JSON file in a directory of
its own, beside its per-node markdown notes. No account, no cloud, no lock-in.
The files are grep-able, diff-able, and editable in any other tool; a note is
just markdown. The application owns the formatting of the domain file, never
the user's ability to read, move, or keep the data. The automation server
serves the user's own machine and nothing beyond it.

### 4. People and agents author it together

A person at the window and an agent at the automation server are the same
kind of author. Every change, from either, is one validated, atomic command
through one write path, so neither can put the graph into a state the other
could not have. The window shows an agent's edits as they land, holding the
camera where the person left it. A refusal names the rule and the legal
alternative, so an agent learns the model from the tool surface rather than
retrying blindly. And the activity log on every opener and task is the shared worklog:
the application records structural changes there, and people and agents add
and amend entries at will.

## Trade-offs

- The shape of a graph is determined by its data and its author rather than by
  a tidying algorithm. The picture must not distort the model to look tidy:
  when a layout choice and the data disagree, the data wins and the layout
  accommodates it. Side and order are the author's, so crossings happen, and a
  crossing is drawn as an underpass rather than avoided by reordering.
- Richer capability is built over the plain files, never in place of them.
  Plain JSON and markdown are the floor; search, indexing, or synchronisation,
  if they come, are added over the files, not by replacing them with something
  the user does not own.
- Visual clarity takes precedence over decoration. While the mid-century theme
  is a genuine pleasure, any decoration that does not clarify the structure is
  decoration to remove.
- A person's undo never reaches through an agent's write. A person expects to
  undo; an agent expects its writes to stand. Undo therefore reverses only the
  person's last command, and only while nothing has been written since; an
  agent's write empties the undo slot rather than being undone with it.
- The activity log is a worklog, not an audit trail. It can be edited by
  people and by agents, which is what makes it useful to them. An audit trail,
  if one were ever wanted, would be a separate record that could not be
  altered after its creation.

## Axioms

1. The record stores the structure: a node's kind, and whether a workflow is a
   branch, are set when they are made and never inferred from position or from
   the drawing.
2. One way in, one way out, at every level: a workflow opens at its start node
   and closes at its finish node, and a project opens at its begin node and
   closes at its end node.
3. A branch may return or not, and when it returns it rejoins the workflow it
   left, within the scope it left, so that any scope can be read, and folded,
   as a single block.
4. Side and order are the author's: which side of its parent a branch runs on,
   and its order among the branches sharing a point, are stored and set by
   hand. The drawing obeys them.
5. Every workflow, main or branch, has its own place where the work is, set by
   hand.
6. Status is shown, not inferred: a completed or cancelled task stays on the
   map, recoloured, and only deletion removes it.
7. Structure lives in the visual channel: if the reader must read to see the
   shape of the work, the drawing has failed.
8. The file is the source of truth, and it is the user's: plain JSON and
   markdown on disk, portable and legible without the application.
9. View is not data: what a client has folded, where its camera rests, and its
   zoom are that client's own state, kept out of the domain file. A named,
   saved view may travel with the data; a client's live view never does.
10. Decoration that does not clarify is cut.
11. One write path: every change is one command, validated in full before
    anything is written.
12. Nothing is rewritten behind the author's back: where an edit would
    invalidate a connection, the connection is detached and left visibly
    undone, never moved somewhere unasked.
13. The log is a worklog: every activity log is written by the application, by
    people, and by agents, and any of them may amend it. It records what has
    been recorded.

## Guiding questions

One per intent, in the intents' order; a proposal answers all four.

- Does the record store exactly what the author decided, and derive everything
  else?
- Can the shape of the work still be seen before a label is read?
- Does this leave the domain as plain files the user can read, move, and keep
  without the application?
- If an agent made this edit while the person watched, would the map show it
  without moving under them, and would a refusal have told the agent what to
  do instead?

## What PensaForma is not

- Not a flat list or a nested checklist. The structure is workflows,
  projects, and branches, and the tool's operations are those and no others.
- Not a general graph editor. Nodes have five intrinsic kinds, a workflow is a
  line, and a branch attaches at a point; the constraints are the point.
- Not a cloud service. There is no account and no server beyond the local
  automation server; synchronisation, if it ever comes, is a separate,
  optional capability over the files.
- Not an audit system. The activity log is editable by design.

---
<sub>© 2026 Gary Frattarola · Licensed under [CC-BY-4.0](../LICENSES/CC-BY-4.0.txt)</sub>
