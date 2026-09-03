<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# Glossary

The vocabulary every document in this set uses, and the only vocabulary the
application's menus, dialogs, refusal messages, and automation tools may speak.
A term is admitted here when a rule constrains it or an operation touches it as
a unit; a word that merely describes a region of the drawing does not earn a
place. Where a term has a stored counterpart, the field is named beside it.

Two conventions run through the set. Growth is upward: a node's successor sits
above it on the screen, and a smaller index is lower. Sets written `{…}` are
unordered; lists written `[…]` are ordered, and their order is model state.

## The application

**PensaForma** (pensa, tasks; forma, shape) is the product's name in prose
and on screen, written with the seam between its two roots shown. `pensa-forma`
is the repository, the binary, and the bundle identifier's last segment
(`ai.parkviewlab.pensa-forma`); `pensa_forma` is the Rust workspace's root
crate name. Documents refer to "the application" where the name itself is not
the point.

**Domain.** The unit of storage and of display: a set of workflows kept
together (HomeLab, Work, and so on), held as one directory on disk. The
application shows one domain at a time. A domain has an `id` and a `name`; the
name is unique within the library.

**Library.** The directory holding every domain directory. The library root is
a user setting; its default is the application's data directory.

**Automation server.** The application's programmatic interface: a local
server, speaking the Model Context Protocol (MCP), through which external tools
and AI agents read and write the open library while the application runs.

## Nodes

**Node.** The building block of a workflow. Every node has an `id`, a `kind`,
an optional **note**, a `flagged` mark, and an **activity log**. Kinds are
intrinsic: a node's kind is a stored property, never inferred from its
position.

**The five kinds.**

| Kind | Bounds | Carries |
| --- | --- | --- |
| `start` | opens a workflow | a `title` |
| `finish` | closes a workflow | nothing beyond the common fields |
| `begin` | opens a project | a `title` and a `pair` |
| `end` | closes a project | a `pair` |
| `task` | one thing to do | a `status`, and possibly the `here` cursor |

**Opener, closer.** A `start` or `begin` node is an opener; a `finish` or
`end` node is its closer. An opener carries the title, so a workflow is named
by its start node and a project by its begin node; a closer carries no title
and is never named on its own.

**Title.** The name of a workflow (on its start node), a project (on its begin
node), or a task. A title may be empty.

**Status.** A task's state, one of `todo`, `doing`, `done`, `cancelled`, shown
on screen as To do, Doing, Done, Cancelled. Only a task has a status. Status is
shown, not inferred: a done or cancelled task stays on the map, recoloured;
only deletion removes it.

**Here (the cursor).** A mark on at most one task per workflow, set by hand,
recording where the author is on that workflow. A main workflow and each of
its branches carry their own, so parallel threads each have a position. Shared
model state, not view state.

**Flag.** A mark on any node that selects it for attention: the flagged-only
review mode shows flagged nodes alone, and an agent's "work the flagged
nodes" begins from them.

**Note.** A node's written prose: a markdown file in the domain's `notes/`
directory, referenced from the node by filename. A node has a note or has
none; there is no second, shorter description field. The **note glyph** on a
card means a note exists, not that it has text.

**Activity log.** A time-stamped list of entries on every node, oldest first,
written by the application on structural changes and by people and agents at
will. It is editable, and is therefore a worklog rather than an audit trail.

## Workflows and projects

**Workflow.** A linearly ordered run of nodes with the gaps between them: a
`start` node first, a `finish` node last, and tasks, projects, and gaps
between. A workflow is **main** when the domain's `mains` list names it, and a
**branch** when some branch point's side list names it; it is exactly one of
the two, and nothing on the workflow record itself says which.

**Main workflow.** A workflow that branches from no other. The domain orders
its main workflows left to right in `mains`, and that order is the author's.

**Branch workflow, branch.** A workflow that departs from a point on another
workflow, its **parent**, runs beside it, and may return to it. A branch that
returns is **closed**; one that does not is **open**, and open is a legal,
persisted state.

**Project.** A `begin` node, the `end` node it names in `pair`, and everything
between them on one workflow. A project has no record of its own; its
identity, title, note, and log are its begin node's. Projects nest: two
projects on one workflow are disjoint or one lies wholly within the other,
never partially overlapping.

**Sub-project.** A project contained within another project.

**Scope.** Everything strictly between a project's begin node and its end
node: the nodes, the gaps, and every branch departing from those gaps. The
**innermost** scope containing a position is the one whose begin node is
highest. A branch is *part of* the innermost project containing its departure
gap, or of no project when that gap is in none.

**Extent.** What travels with a node when it is moved, copied, or deleted as a
whole: a task alone; a project with its end node and its whole scope; a
workflow with its finish node and everything in it, descendant branches
included.

## Gaps, points, and edges

**Gap.** The stored record for the space between two consecutive nodes of one
workflow. A workflow with n nodes has exactly n−1 gaps, interleaved with them,
and gap `i` lies between node `i` and node `i+1`. A gap owns two points.

**Branch point.** The lower of a gap's two points, at which branches depart.
Addressed as `(gap, branch)`. It has a left side and a right side, each an
ordered list of branch workflows, inner to outer (`branchLeft`,
`branchRight`).

**Return point.** The upper of a gap's two points, at which branches arrive.
Addressed as `(gap, return)`. It likewise has two sides (`returnLeft`,
`returnRight`).

**Side.** Left or right of the parent workflow's line. A branch's side is
which list holds it, and its return is made on the same side as its
departure.

**Order.** A branch's index in its side list, counted from the innermost
(nearest the parent's line) outward. The order is the author's and the
drawing obeys it.

**Departure, arrival.** A branch's departure is its membership in a branch
point's side list; its arrival, when it has one, is its membership in a return
point's side list. A branch's **departure gap** and **return gap** are the gaps
owning those points.

**The three edges of a gap.** Reading upward: the **outgoing edge**, from the
lower node to the branch point; the **middle edge**, from the branch point to
the return point; and the **incoming edge**, from the return point to the
upper node. They are structural positions, not merely drawn objects: the three
places a node can be inserted within one gap, differing in whether the
inserted node sits below, between, or above the gap's departures and
arrivals. The middle edge has length zero when nothing separates the two
points, and is then no drop target.

**Trunk edge.** Any of the three edges of a gap, as distinct from a lateral.

**Branch edge.** The connection from a branch point to a branch workflow's
start node. **Return edge.** The connection from a branch workflow's finish
node to a return point. Neither carries nodes.

**Junction.** A branch point or return point with at least one branch
attached, as drawn: one diamond per point, shared by every branch meeting it.

## The drawing

The look, in one phrase: a mid-century retrofuturist systems diagram; a
Googie-inspired Atomic Age flowchart laid out like a retro transit or
control-system map.
For a design brief or an image search: mid-century retrofuturism, Googie
diagram, Atomic Age infographic, Jet Age schematic, retro systems map, 1950s
technical illustration.

**Line.** A workflow as drawn: its nodes colinear at one x, lowest at the
bottom, joined by a **riser**.

**Card.** The drawn body of a node, of fixed width and measured height, wearing
the silhouette its kind and state assign.

**Station.** Where a card sits on its line: the card itself, which is the
mark; nothing separate is drawn there, and the layout measures each gap
between the silhouettes where the line passes through them.

**Lateral.** The drawn track of a branch edge or a return edge: a ramp, a flat
run, and a ramp, climbing a constant rise whatever its horizontal span.

**Lane.** A column one card wide plus a gutter; branches are placed a whole
number of lanes from their parent's line.

**Underpass.** The drawn form of a crossing: the crossed line runs on and the
crossing lateral is cut, each severed end capped parallel to the line it
passes beneath.

**Fold.** A project drawn shut, its begin and end cards touching with the body
hidden. Fold state is client view state keyed by the begin node's id, never a
field of the record.

**Bookmark.** A named, saved view stored with the domain: a name, the set of
folded projects, and the set of nodes in view when it was saved.

## Change

**Command.** The unit of change: a name, a domain, an argument list, an origin
(`ui` or `automation`), and an actor. Every change to a domain is one command
through one write path.

**Mutation.** A pure function from a record and arguments to a new record; the
body of a command.

**Precondition.** A mutation's own check that the command makes sense, whose
refusal names the rule and, where one exists, the legal alternative.

**Invariant.** A property every stored domain satisfies, checked after every
mutation and on every load; the list is in the structural model.

**Refusal.** A command's failure, carrying a code from a small closed set and a
message written to be read by a person in a dialog or by an agent as a tool
result.

**Undo.** One slot holding the pre-image of the last command that originated in
the user interface. There is no redo.

**Scope tier.** The automation server's configured reach: `read-only`,
`read-write`, or `destructive`, each including the ones before it.
