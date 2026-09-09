<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# Glossary

To avoid ambiguity, this glossary defines the words and phrases that are used as technical terms in the documents of this specification. A term is defined here because what it defines is either constrained by a rule or acted upon by an operation.

By convention in these documents, unordered sets are denoted as `{…}`, ordered lists as `[…]`, and the names of fields or values stored in files are denoted with a monospaced font.

## PensaForma

PensaForma is the product's formal name. It is to be written with the capitalization as shown.

`pensa-forma` is the repository, the binary, and the bundle identifier's last segment (`ai.parkviewlab.pensa-forma`). 

`pensa_forma` is the Rust workspace's root crate name.

Specification documents should refer to it as "the application" so that any required future name changes are less costly.

## Workflows and Projects

### Workflow
A workflow is a linearly ordered run of [nodes](#nodes) separated by [gaps](#gap).

The first node in a workflow is a [`start` node](#start-node) and the last is a [`finish` node](#finish-node). Between those may be [task nodes](#task-node), [projects](#project), and branches.

Workflows are drawn from the bottom up with the start node at the bottom, then each node is above its predecessor, and the finish node at the top.

A workflow is either a main or a branch based on its location alone.

### Main workflow

A **main workflow** is not a branch of any other workflow and is included in the domain's `mains` list. The domain orders its main workflows left to right in its `mains` list. That is the order in which they are drawn, and that order is set by and may be changed by the author.

### Branch workflow
A **branch workflow** is a branch off of some other workflow and is included in some [branch point](#branch-point)'s side list.

The workflow from which it branches is referred to as its **parent workflow**.

A branch workflow runs beside its parent, and *may* return to it.

A branch that returns is referred to as a **closed branch**. A branch that does not is referred to as an **open branch**. Both states (open and closed) are legal and persisted.

### Project

A project is used to group consecutive nodes together.

A project can be drawn collapsed or not.

The first node in a project is a [`begin` node](#begin-node) and the last is an [`end` node](#end-node). Between those may be tasks, [sub-projects](#sub-project), and branches.

A project has no record of its own; its identity, title, note, and log are defined in its [begin node](#begin-node).

Projects may be nested. Two projects in one workflow will either be disjoint or one will lie wholly within the other. Projects can never partially overlap.

### Sub-project
This is a project contained within another project.

### Scope
This is everything strictly between the two nodes that bound a workflow or a project: for a workflow, between its start node and its finish node; for a project, between its begin node and its end node. A scope comprises the nodes, the gaps, and every branch departing from those gaps. Every project scope lies within its workflow's scope, and project scopes may nest; the **innermost** scope containing a position is the one whose first node is highest. A branch is *part of* the innermost scope containing its branch point.

### Extent
This is what travels with a node when it is moved, copied, or deleted as a whole: a task alone; a project with its end node and its whole scope; a workflow with its finish node and its whole scope.

## Domain

This is the unit of storage and of display. It is a set of workflows kept together (such as HomeLab, Work, and so on). 

Domains are stored on disk as a directory with a [record](#record) JSON file, its JSON Schema file, and a README file that describes the record's format.

The application shows one domain at a time.

A domain has an `id` and a `name`. Domain names are unique within their library.

## Library
This is the directory holding every domain. The library root is a user setting; its default is the application's data directory.

## Record
This is file in which all graph data for all workflows in a single domain is stored. This is a JSON file and is accompanied by its JSON Schema file. The only workflow data not stored in this file are the notes' markdown files.

## Automation server
This is the application's programmatic interface. It is a local Model Context Protocol (MCP) server which external tools and AI agents can use to read and write domains in the library while the application is running. The other documents may refer to this as the automation server for short.

## Nodes

Nodes are the building blocks of a workflow.

### Start node

The first node of every workflow is a start node.

Start nodes may optionally have: a [title](#node-title), a note, and a flag.

Start nodes must have: an [ID](#node-id), and an activity log.

### Finish node

The last node of every workflow is a finish node.

Finish nodes must have: an ID.


### Begin node

The first node of every project is a begin node.

Begin nodes may optionally have: a [title](#node-title), a note, and a flag.

Begin nodes must have: an ID, the ID of its matching [end node](#end-node), and an activity log.

### End node

The last node of every project is an end node.

End nodes must have: an ID, and the ID of its matching [begin node](#begin-node).

### Task node

A task node defines a single task.

Task nodes may optionally have: a [title](#node-title), a note, a flag, and a here mark.

Task nodes must have: an ID, a [status](#status), and an activity log.



## Node data

### Node ID
A unique identification string for a node. The schema for these IDs is defined in the [structural model document](structural-model.md#1-identity).

### Node kind

Every node has a kind: start, finish, begin, end, or task, stored in its `kind` field.

A node's kind is set when the node is made, and changes only under the two conversions the [command catalogue](command-catalogue.md#convert_project_to_taskbegin) defines.

### Node title
This is the name of a workflow (on its start node), a project (on its begin node), or a task.

A title may be empty.

A title must be unique within its domain.

### Node status
This is a task's state, one of `todo`, `in-progress`, `completed`, `cancelled`, shown under a card as to do, in progress, done, cancelled and in the status menu as To do, In progress, Completed, Cancelled (D30). Only a task has a status. A completed task also carries `completedAt`, the time it became completed, present exactly while it is. Status is shown, not inferred: a done or cancelled task stays on the map, recoloured; only deletion removes it.

### Here mark
This is a mark on at most one task per workflow, set by hand, by which a person or an agent points that task out to the others working the workflow: where the workflow itself is being worked upon now, where the work is now, where it should be by some date, where a branch ought to be added, or whatever else its setter means by it. A main workflow and each of its branches carry their own, so parallel threads each have a pointer. It is shared model state, not view state.

### Flag mark
This is a mark on a start node, a begin node, or a task by which a person or an agent draws the others' attention to it, for whatever reason its setter has: the flagged-only review mode shows flagged nodes alone, and an agent's "work the flagged nodes" begins from them.

### Note
This is a node's written prose: a markdown file in the domain's `notes/` directory, referenced from the node by filename. A start node, a begin node, or a task has a note or has none, and a finish node or an end node never has one; there is no second, shorter description field. The **note glyph** on a card means a note exists, not that it has text.

### Activity log
This is a time-stamped list of entries on every start node, begin node, and task, oldest first, written by the application on structural changes and by people and agents at will. It is editable, and is therefore a worklog rather than an audit trail.

## Gaps, points, and edges

### Gap

A gap is the stored record for the space between two consecutive nodes of one [workflow](#workflow).

A workflow with n nodes has exactly n-1 gaps, interleaved with the nodes: gap `i` lies between node `i` and node `i+1`.

Every gap has an ID, in the scheme the [structural model](structural-model.md#1-identity) defines, and owns two points: a [branch point](#branch-point) and a [return point](#return-point).

### Branch point

A branch point is the lower of a [gap](#gap)'s two points. Branches depart from it.

It is addressed as `(gap, branch)`.

It has a left side and a right side. Each side is an ordered list of [branch workflows](#branch-workflow), from the innermost outward, stored as `branchLeft` and `branchRight`.

### Return point

A return point is the upper of a [gap](#gap)'s two points. Branches arrive at it.

It is addressed as `(gap, return)`.

It has a left side and a right side, stored as `returnLeft` and `returnRight`.

### Side

A branch's side is the left or the right of its parent workflow's line. Which side list holds the branch decides its side.

A branch returns on the same side as it departs.

### Order

A branch's order is its index in its side list, counted from the innermost (nearest the parent's line) outward.

The order is set by the author, and the drawing obeys it.

### Departure and arrival

A branch's departure is its membership in a [branch point](#branch-point)'s side list.

A branch's arrival, when it has one, is its membership in a [return point](#return-point)'s side list.

A branch's **departure gap** and **return gap** are the gaps that own those two points.

### The three edges of a gap

Reading upward, a [gap](#gap) has three edges: the **outgoing edge**, from the lower node to the branch point; the **middle edge**, from the branch point to the return point; and the **incoming edge**, from the return point to the upper node.

The edges are structural positions, not merely drawn objects. They are the three places a node can be inserted within one gap, and they differ in whether the inserted node sits below, between, or above the gap's departures and arrivals.

The middle edge has length zero when nothing separates the two points, and is then no drop target.

### Trunk edge

A trunk edge is any of the three edges of a gap, as distinct from a [lateral](#lateral).

### Branch edge and return edge

A branch edge is the connection from a [branch point](#branch-point) to a branch workflow's [start node](#start-node).

A return edge is the connection from a branch workflow's [finish node](#finish-node) to a [return point](#return-point).

Neither carries nodes.

### Junction

A junction is a branch point or a return point as drawn: a diamond.

A diamond is drawn at every point whether or not a branch attaches there: one where a gap's two points coincide, and two where its middle edge has opened.

A junction is shared by every branch meeting it.

## The drawing

The look is, in one phrase, a mid-century retrofuturist systems diagram: a Googie-inspired Atomic Age flowchart laid out like a retro transit or control-system map. The terms for a design brief or an image search are mid-century retrofuturism, Googie diagram, Atomic Age infographic, Jet Age schematic, retro systems map, and 1950s technical illustration.

### Line

A line is a [workflow](#workflow) as drawn: its nodes colinear at one x, the lowest at the bottom, joined by a **riser**.

### Card

A card is the drawn body of a node. It has a fixed width and a measured height, and wears the silhouette its kind and state assign.

### Station

A station is where a card sits on its line. The card itself is the mark; nothing separate is drawn there.

The layout measures each gap between the silhouettes where the line passes through them.

### Lateral

A lateral is the drawn track of a branch edge or a return edge: a ramp, a flat run, and a ramp.

A lateral climbs a constant rise whatever its horizontal span.

### Lane

A lane is a column one card wide plus a gutter.

Branches are placed a whole number of lanes from their parent's line.

### Underpass

An underpass is the drawn form of a crossing. The crossed line runs on and the crossing lateral is cut, each severed end capped parallel to the line it passes beneath.

### Fold

A fold is a project or a workflow drawn shut: its begin and end cards, or its start and finish cards, overlap with the body hidden (mark geometry, 3.11 and 3.12).

Fold state is client view state keyed by the ID of the start or begin node. It is never a field of the record.

### Bookmark

A bookmark is a named, saved view stored with the domain.

It holds a name, the set of folded [scopes](#scope), and the set of nodes in view when it was saved.

## Change

### Command

A command is the unit of change: a name, a domain, an argument list, an origin (`ui` or `automation`), and an actor.

Every change to a domain is one command through one write path.

### Mutation

A mutation is a pure function from a record and arguments to a new record. It is the body of a command.

### Precondition

A precondition is a mutation's own check that the command makes sense.

Its refusal names the rule and, where one exists, the legal alternative.

### Invariant

An invariant is a property every stored domain satisfies. Invariants are checked after every mutation and on every load.

The list is in the [structural model](structural-model.md#4-the-invariants).

### Refusal

A refusal is a command's failure. It carries a code from a small closed set and a message written to be read by a person in a dialog or by an agent as a tool result.

### Undo

Undo is one slot holding the pre-image of the last command that originated in the user interface. There is no redo.

### Scope tier

The scope tier is the automation server's configured reach: `read-only`, `read-write`, or `destructive`, each including the ones before it.
