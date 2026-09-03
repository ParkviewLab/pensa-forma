<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# Yucca Basing: northstar

The canonical statement of what this application is for. Design decisions and
feature proposals are weighed against it. Where it and any other document
disagree, this one is the authority and the other is the thing to fix; where
it and the code disagree, the code is wrong.

## What it is

Yucca Basing is a studio in which people and AI agents plan and track work
together, as a living graph of workflows. A workflow orders tasks. It may
contain projects, which group a contiguous run of its nodes, and branches,
which run in parallel beside it and may rejoin it or not. Workflows are
gathered into domains (HomeLab, Work, and so on), each a set of plain files on
the user's own disk. The graph is drawn as a subway map, and it is
restructured by dragging tasks, whole projects, and whole workflows. Every
node may carry a written note and always carries an activity log, which
people and agents both write.

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

These are complementary facets of one purpose, not a ranking; the tensions
between them, below, are where the design is decided.

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
where they arrive; on each point two ordered sides. The action that creates a
node decides the structure it takes, and ordering never does.

### 2. Structure is legible at a glance

A domain is drawn as a mid-century retrofuturist systems diagram, a
Googie-inspired Atomic Age flowchart laid out like a retro transit or
control-system map: stations are nodes, tracks are the lines they sit on, and
a junction between two stations is where a branch leaves or returns. Before reading a single label one can see the shape of the work:
where one is (the cursor's card), what is done, in progress, or cancelled (the
outline colour), where a line branches, where it comes back, and where it
does not. The visual channel carries the structure; text only names it. The
mid-century skin, the atomic-age decorators and the jaunty openers, is in
service of this and not the reverse.

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
retrying blindly. And the activity log on every node is the shared worklog:
the application records structural changes there, and people and agents add
and amend entries at will.

## Tensions (these are design-revealing)

- Legibility against faithful structure. The picture must not distort the
  model to look tidy; when a layout choice and the data disagree, the data
  wins and the layout accommodates it. Side and order are the author's, so
  crossings happen, and a crossing is drawn as an underpass rather than
  avoided by reordering.
- Local files against richer capability. Plain JSON and markdown are the
  floor; later richness (search, indexing, synchronisation) is added over the
  files, not by replacing them with something the user does not own.
- Skin against clarity. The mid-century theme is a genuine pleasure, but any
  decoration that does not clarify the structure is decoration to remove.
- One authority against two writers. A person expects to undo; an agent
  expects its writes to stand. Undo therefore reverses only the person's last
  command, and an agent's write invalidates it rather than being reversed
  through.
- A worklog against a record of fact. An editable log is more useful to the
  people and agents keeping it, and less trustworthy as evidence. The
  application chooses the worklog and says so; it does not pretend the log is
  an audit trail.

## Axioms

1. The creating action decides structure, not order: inserting a task
   continues the line at the edge it names; opening a branch starts a parallel
   workflow off a point.
2. One way in, one way out, at every level: a workflow opens at its start node
   and closes at its finish node, a project opens at its begin node and closes
   at its end node, and growth rises between them.
3. A branch may return or not. When it returns, it rejoins the workflow it
   left, at or above where it departed, on the side it departed from, and
   inside exactly the same projects. No branch reaches out of its scope, so any
   scope can be read, and folded, as a single block.
4. Side and order are the author's: which side of its parent a branch runs on,
   and its order among the branches sharing a point, are stored and set by
   hand. The drawing obeys them.
5. One cursor per workflow, set by hand and clearable; a branching workflow
   may show several, one per branch.
6. Status is shown, not inferred: completing or cancelling a task leaves it on
   the map, recoloured; only delete removes it. Only a task has a status.
7. Structure lives in the visual channel: if the reader must read to see the
   shape of the work, the drawing has failed.
8. The file is the source of truth, and it is the user's: plain JSON and
   markdown on disk, portable and legible without the application.
9. View is not data: what a client has folded, where its camera rests, and its
   zoom are that client's own state, kept out of the domain file. A named,
   saved view may travel with the data; a client's live view never does.
10. Decoration that does not clarify is cut.
11. One write path, and nothing rewritten behind the author's back: every
    change is one command, validated in full before anything is written, and
    where an edit would invalidate a connection the connection is detached and
    left visibly undone, never moved somewhere unasked.
12. The log is a worklog: every node's activity log is written by the
    application, by people, and by agents, and any of them may amend it. It
    records what has been recorded.

## Guiding questions

- Could a person or an agent, given only these documents, build the
  application, and could a person, given only the README, use it?
- Does the record store exactly what the author decided, and derive
  everything else?
- If this edit were made by an agent while the person watched, would the map
  show it without moving under them, and would a refusal have told the agent
  what to do instead?
- Is there exactly one source of truth for this fact?

## What Yucca Basing is not

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
