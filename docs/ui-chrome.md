<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# UI chrome

The shell around the map canvas: the application window and its menus, every
widget on the header bar, the right-click menu system with its complete item
inventory, every dialog with its exact strings, the note editor, the activity
log panel, the About window, and the Open Source Licenses window. It is
written so that the interface can be built from it, on the toolkit the
[architecture](architecture.md) names, and it stands with the rest of the set:
the vocabulary is the [glossary](glossary.md)'s, every editing item issues a
command from the [command catalogue](command-catalogue.md), and the drawing
of the canvas itself is the [mark geometry](mark-geometry.md) and the [layout
engine](layout-engine.md).

Two boundaries are deliberate. The map canvas (the drawing of cards, tracks,
and markers that fills the window below the header) is a black box here, and
this document describes only the points where the canvas hands control to the
chrome (a right-click, a click on a card's note glyph or status glyph, a
double-click). Drag-and-drop is the [interaction](interaction.md) document's.

Where the host platform provides a native facility (window chrome, menus,
file dialogs, a clipboard), use it; where it does not, the stated behaviour is
the contract to reproduce. An HTML sibling of this file renders each widget,
menu, and dialog so the target can be seen as well as read.

Conventions: "PensaForma" is the application's name in exact strings.
Colours are given as a token name (for instance `--ink`) whose two values per
theme appear in Appendix A. Sizes are logical pixels. `Mod` means the
platform's primary command modifier (Cmd on macOS, Ctrl elsewhere). An "edge
line" is a 1px line drawn along an element's boundary, inside its stated
size; a "ring" is a line drawn outside the boundary, occupying no layout
space; a drop shadow is given as offset (x, y), blur radius, and colour;
"tracking" is extra letter spacing as a fraction of the font size;
truncation means cutting overflowing text with a trailing `…`.

---

## 1. The application window

- One main window, 1280 × 800 at first launch; no minimum size is enforced.
- The window's first paint is the ground token of the theme that will apply
  on this launch (section 3.5): `#d3e6ef` (azure) unless the stored choice is
  navy, then `#0f2334`, so no foreign colour flashes before the interface
  draws. If the stored choice cannot be read before the first paint, paint
  azure.
- Standard platform window chrome and title bar; nothing custom. The window
  title is `PensaForma`.
- Only one instance runs: launching a second focuses the first, restoring it
  if minimised.
- Links to the outside world always open in the system's default web
  browser, never inside the application; the application itself opens only
  `http(s)` destinations and ignores any other scheme.
- The application never reaches the network on its own; the single exception
  is the About window's explicit update check (section 9).
- No tray icon, no dock badge. The application has no whole-window zoom of
  its own; the only zoom is the map viewport's (section 3.7).
- On platforms whose conventions keep applications resident with no windows
  (macOS-style), follow the convention and recreate the window on
  activation; elsewhere, closing the window quits.

### 1.1 The application menu

Where the host provides a native menu bar, provide:

1. An application menu (on platforms that have one): `About PensaForma`
   (opens the About window, section 9); `Open Source Licenses…` (opens the
   Licenses window, section 10); then the platform's conventional
   services/hide/quit entries.
2. The platform's standard File, Edit, View, and Window menus, per its
   conventions. The Edit menu's first item is `Undo <command>`, labelled with
   the last command's subject title (for instance `Undo move “Backend”`) and
   disabled when the undo slot is empty; there is no Redo item. When a text
   field or the note source pane has focus, the platform's text undo applies
   instead, as the toolkit provides.
3. A Help menu: on platforms without an application menu, first `About Yucca
   Basing` and a separator; then `Open Source Licenses…`; then `Source Code`,
   opening the project's source-hosting page externally.

On platforms with no native menu bar, surface About, Licenses, and Undo
through some other modest affordance (a header overflow menu is one option);
they must remain reachable.

There is no menu item for the automation server; it is surfaced only through
the header-bar pill (section 3.4). The only keyboard shortcuts in the product
are the accelerators the platform's standard menus carry by convention, the
platform's standard text-editing keys, and those listed in section 12.

---

## 2. The shell

The window is a single column: a header bar above a canvas viewport that
fills the rest. The window's ground colour is `--ground`; all text defaults
to `--ink` in the UI face (Appendix B).

The header bar: a full-width row, vertically centred, inner spacing 9px top
and bottom and 14px left and right, a 1px `--line` edge along its bottom. Its
children form two groups pinned to opposite ends, the items within each
group spaced 12px apart. Left group, in order: brand, domain switcher,
delete-domain button, automation pill. Right group, in order: mode label,
Light/Dark segmented toggle, Flagged toggle, zoom cluster (minus, percent
readout, plus, Fit).

The canvas viewport fills the remaining height, clipping its content, ground
`--ground`, with a grab-hand pointer cursor and unselectable text. It carries
the dot grid of the mark geometry's section 1 on its own surface, so the grid
neither pans nor zooms. Inside the viewport sit the transformed map world (a
black box here) and an empty-state overlay (section 2.1).

Shared button style, used by every header button: text 12px in the UI face at
line height 1 (the line box exactly as tall as the text, so text, inner
spacing, and edges alone set the button's height); a 1px `--line` edge;
corner radius 5; inner spacing 6px vertical, 10px horizontal; transparent
fill, text `--ink`; pointer cursor. On hover the fill becomes `--line` at 16
% opacity. Disabled: the whole button at 40 % opacity, default cursor, no
hover fill. Variants: an icon button is 30px wide with centred 14px text and
no horizontal padding; a primary button fills `--ink` with `--ground` text
and an `--ink` edge; a danger button keeps the transparent fill but takes
`--c-doing` text and an edge of the danger blend (Appendix A), and its hover
fill is `--c-doing` at 16 %; a toggle button in its pressed state takes the
primary look (filled `--ink`, `--ground` text).

### 2.1 Empty-state overlay

A message layer covering the viewport, its text centred both ways, `--muted`,
14px with 0.02 tracking. The layer passes all input through to what lies
beneath (essential: the "right-click the canvas" invitation must be
actionable through the message itself). Its texts, verbatim:

| Text | When |
| --- | --- |
| `No domain open yet` | at startup, until the first render |
| `This domain has no workflows yet. Right-click the canvas to start one.` | an open domain whose record has no main workflows |
| `Could not open “<name>”: <error>` | the domain file could not be read |
| `No domains. Use “New domain…” in the switcher to create one.` | the last domain was deleted |
| `No domain library found` | startup found no domains even after seeding samples |

Whenever startup finds the library empty (the first launch, or a launch after
every domain was deleted), the application seeds two sample domains,
`HomeLab` and `Work`, so the ordinary first-run experience opens a populated
map rather than an empty state. Each sample holds two or three main
workflows with a project, a returning branch, an open branch, a cursor, a
flagged task, and one node carrying a note, so that every mark in the
vocabulary appears on the first screen. The sample content is suggested, not
binding; the pattern (seed something real on an empty library) is the
requirement.

---

## 3. The header widgets, left to right

### 3.1 Brand

The application's wordmark, static: display face (Appendix B), 13px, weight
800, 0.06 tracking, uppercase, `--ink`: `PENSAFORMA`. No behaviour.

### 3.2 Domain switcher

A drop-down list of domains (use the platform's native select control where
one exists), with tooltip and accessible label `Domain`: 12px text, `--ink`,
transparent fill, a 1px `--line` edge, radius 5, inner spacing 5px vertical
and 9px horizontal. If the control's open list draws on a surface that the
theme does not reach (a native list surface, typically light), force its rows
to dark ink `#173242`; otherwise, in the dark theme, they inherit the light
ink and turn unreadable on that surface. A list the toolkit draws entirely
itself, in its own readable colours, needs no forcing.

Contents: one entry per domain in alphabetical order by name (locale-aware
compare), then an inert separator row of ten `─` characters (U+2500), then
`New domain…`. The control is never disabled, so `New domain…` stays
reachable even with one domain; after the last domain is deleted the list
holds only the separator and the `New domain…` entry.

On selection: `New domain…` runs the create-domain flow (section 7, the `New
domain` prompt). On cancel or failure the selection is restored to the
current domain, since it otherwise sits on the New entry. On success the
domain list is re-read, the switcher repopulated with the new domain selected
(it slots into alphabetical order), and the new domain opened, showing its
`This domain has no workflows yet…` empty state. Choosing any other entry
opens that domain. Opening a domain closes any open context menu, the note
editor, and the activity log panel, reads the record (failure shows the
`Could not open…` empty state and must unload the previous domain, so no
stale editing surface remains), loads the client's fold state and the
domain's bookmarks, records the domain as the last used (restored on next
launch), clears the undo slot, and renders with a fit. The last-used domain
reopens at startup; if it is gone, the alphabetically first domain opens
instead.

### 3.3 Delete-domain button

An icon button, danger-styled, glyph `✕` (U+2715), tooltip and accessible
label `Delete domain`. Disabled whenever no domain is open. Activating it
runs the delete confirmation (section 7); on confirm the domain and its notes
move to the system Trash (recoverable), never a hard delete. If domains
remain, the alphabetically first one opens; otherwise the switcher reduces to
its separator and `New domain…` entries, and the `No domains…` empty state
shows.

### 3.4 The automation pill

The application exposes a local automation server (its programmatic
interface for external tools and agents; the [automation
server](automation-server.md) document). The pill is that subsystem's one
point of visibility in the chrome.

A button labelled `MCP` with an 8 × 8 status dot before the text, 7px between
dot and text. The dot: a circle, default fill `--c-cancel` (muted, off);
`--accent-teal` when the server runs; `--c-doing` on error; an inward ring of
`--ink` at 25 % opacity, 1px, keeps the dot legible on both grounds.
Precedence: error beats running beats off.

Tooltip, rebuilt on each refresh from segments joined with ` · ` (space,
interpunct, space): `MCP server`, then `running at <url>` or `starting…` or
`off`, then `scope: <scope>` when known, then `error: <error>` when present;
assembled, for instance: `MCP server · running at
http://127.0.0.1:35901/mcp · scope: read-write`.

Activating the pill refreshes the status, then opens the shared menu widget
(section 6's visual spec) anchored at the button's bottom-left corner plus
4px down, with items:

1. A disabled status row: `● ` (running) or `○ ` (not), followed by the
   endpoint URL or `unavailable`.
2. Separator.
3. `Copy endpoint URL` (present only when a URL exists): copies it to the
   system clipboard; if the clipboard write fails, a dialog titled `MCP
   endpoint` shows the URL with an OK button instead.
4. `Turn off` or `Turn on` (by current enabled state): toggles the server and
   refreshes.

Status is polled only at application start and on activation; a server that
dies in between shows a stale dot until the next press. The endpoint has the
form `http://127.0.0.1:<port>/mcp` (default port 35901), loopback only.

### 3.5 Mode label and theme toggle

A tiny uppercase label `Mode` (10px, 0.12 tracking, `--muted`), then a
segmented control: a pill-shaped container (1px `--line` edge, fully rounded
ends, contents clipped) holding two edge-less segments, `Light` and `Dark`
(12px, inner spacing 6px vertical and 14px horizontal, text `--muted`), the
active segment inverted (`--ink` fill, `--ground` text).

Behaviour: choosing a segment sets the theme state to azure (Light) or navy
(Dark) and persists the choice as the `theme` setting. Every colour in the
application is a token resolved through the theme state, so switching
repaints without any re-layout or re-measure; an open note editor re-themes
instantly, syntax colours included. On startup the stored value applies;
anything unrecognised (or an unreadable store) falls back to azure.

### 3.6 Flagged toggle

A toggle button labelled `Flagged`, tooltip `Show only flagged nodes
(read-only)`, its pressed state shown by the inverted primary look and
exposed to accessibility as a pressed toggle.

Pressed, it puts the map into flagged-only review: only flagged cards remain
visible; the whole track layer and every station dot disappear; all cards
become inert to the pointer; drags are disabled; and the right-click menu is
suppressed entirely, so no edit, paste, or bookmark action is reachable. Pan,
wheel zoom, the header, and open dialogs stay live. The state is session
state, never persisted, and survives a domain switch.

### 3.7 Zoom cluster

A row, items 6px apart: icon button `−` (U+2212, accessible label `Zoom
out`), a percent readout, icon button `+` (`Zoom in`), and a primary button
`Fit`.

- The readout: 11px, `--muted`, at least 42px wide, centred, digits at equal
  widths so the number does not jitter; shows the zoom rounded to a whole
  percent, initially `100%`.
- Zoom bounds 0.2 to 3.0, so the readout ranges `20%` to `300%`.
- The buttons zoom by a factor of 1.2 (in) and 1/1.2 (out), anchored at the
  viewport centre. (Scroll-wheel input zooms by 1.1 per step anchored at the
  pointer; noted here because it moves the same readout.)
- `Fit` frames the whole map: zoom = the smaller of viewport/bounds per axis,
  times 0.94 (a 3 % margin per side), clamped to the bounds above, centred
  both axes. Fit also runs on every window resize (discarding the user's
  pan/zoom), on opening a domain, and as the fallback when a bookmark's nodes
  no longer exist.

---

## 4. The canvas boundary

The map itself is out of scope, but four gestures on it invoke the chrome
and must be honoured as triggers:

- Right-click anywhere in the viewport opens a context menu (section 6): on
  a card, that node's menu; anywhere else (tracks, junction diamonds, dots,
  bare canvas), the canvas menu. With no domain open, or in flagged-only
  mode, right-click does nothing.
- Single click on a card's note glyph (the small memo-pad in its
  bottom-right corner) opens the note editor on that node.
- Single click on a task card's status glyph cycles its status (todo → doing
  → done → cancelled → todo), issuing `cycle_status`. A begin card's and a
  start card's glyphs carry no status and ignore the click.
- Double-click on a card's body toggles the node's flag, issuing `set_flag`;
  the glyph and note-glyph sub-regions are excluded. Any node may be flagged,
  closers included.

The chrome also reacts to external writers (the automation server editing
the same library) without user action. An edit to the open domain re-reads
the record and re-renders in place, coalesced to at most one render per
displayed frame, holding the camera, zoom, and fold state; there is no
changed-node highlight; the undo slot clears. A domain created or deleted
externally refreshes the switcher's entry list in place; if the open domain
itself disappears, the note editor and any menu close, and the alphabetically
first remaining domain opens (or the `No domains…` empty state shows). The
open note editor and activity log panel reconcile on these refreshes as
described in sections 8.6 and 8.7.

### 4.1 The vocabulary the menus speak

The menus and dialogs name concepts from the glossary. The chrome does not
implement them (the edit operations run in the command layer and the canvas
draws the result), but a builder must know what each term means for the
items' conditions and labels to make sense.

A domain holds any number of workflows. A workflow opens at a start node and
closes at a finish node; a main workflow is one the domain lists in its
left-to-right order, and a branch workflow is one that departs from a branch
point on another workflow, its parent. A project is a begin node, the end
node paired with it, and everything between; a begin card is the project's
handle for every operation, and an end card, having no title, is never named
on its own. Openers (start and begin) carry titles; closers (finish and end)
do not.

Between every pair of consecutive nodes is a gap, with a branch point below
and a return point above; a node can be added at a gap's outgoing, middle, or
incoming position, which differ in whether it lands below, between, or above
the gap's departures and arrivals. "Above <node>" in a menu means the gap
above the node at its outgoing position; "below <node>" means the gap below
it at its incoming position. A branch departs on the left or the right of its
parent's line, at an order position among its siblings, and either returns to
a return point at or above its departure, on the same side and inside exactly
the same projects, or runs open.

`Make here` sets the "here" cursor on a task: a per-workflow marker of the
current task, at most one per workflow, stored on the task itself and shared
with other writers. Setting it clears the workflow's previous cursor; `Clear
here` removes it. Only a task can carry it.

A flagged node is one marked (by double-click) for the flagged-only review
mode; the flag is stored on the node and shared, unlike the toggle itself.

`Wrap as project` acts on a contiguous run of the clicked node's workflow:
the clicked node is the run's base, and the submenu offers each legal top,
from `Just this one` upward; a run is legal while it neither straddles a
project boundary nor cuts a branch's scope, and the submenu ends where
legality does. `Unwrap…` removes a project's begin and end pair and leaves
its contents in place.

`Return a branch here` offers, on a node, the branches whose return could
legally land on the gap above that node; `Move a branch here` offers those
whose departure could legally move there, keeping the branch's side. Both
name a branch by its start node's title. `Detach return`, on a branch's
finish card, leaves the branch open.

`Move up` and `Move down` move the clicked node to the next distinct position
above or below along its workflow; `Move left` and `Move right`, on a main
workflow's start card, move it in the domain's order.

---

## 5. Menu items and the commands they issue

Every editing item routes through the command layer: the operation runs
against the stored record, is validated, persisted atomically, and the new
record renders without re-fitting (the camera holds). On failure the map is
left as it was and a `Change not saved` dialog appears (section 7.3), with
the refusal's message verbatim. The table gives the command behind each
item; the inventories in section 6 give the items' order and conditions.

| Item | Command |
| --- | --- |
| Status ▸ To do / Doing / Done / Cancelled | `set_status` |
| Make here / Clear here | `set_here` / `clear_here` |
| Make project | `convert_task_to_project` |
| Make task | `convert_project_to_task` |
| Wrap as project ▸ `Just this one` / `Up to “<title>”` | `wrap_run` |
| Unwrap… | `unwrap_project` |
| Move up / Move down | `move_task` or `move_project` to the next position |
| Move left / Move right | `move_workflow` to the neighbouring main position |
| Rename… | `set_title` |
| Add task above / below | `insert_task` |
| Add branch above / below ▸ Left / Right | `open_branch` |
| Return a branch here ▸ `<branch>` | `attach_return` |
| Move a branch here ▸ `<branch>` | `move_workflow` to this gap's branch point, same side, outermost |
| Detach return | `detach_return` |
| Expand / Collapse | fold state (client-local; no command) |
| Copy | `copy_project` (session clipboard) |
| Paste above / Paste below | `paste` at the derived edge target |
| Paste as new workflow | `paste` at the end of the domain's order |
| Export to Markdown… | a read plus the export writer (section 5.1) |
| Edit note… / Delete note… | the note editor / `delete_note` |
| Activity log… | the log panel (section 8.7), which issues the three log commands |
| Delete… | `delete_node` |
| New workflow… | `create_workflow` |
| Add bookmark… / Jump to bookmark ▸ / Delete bookmark ▸ | the bookmarks file (section 11; no command) |

`Copy` snapshots the project's extent and its notes by value into a session
clipboard that survives a domain switch and not a quit.

### 5.1 Export to Markdown

`Export to Markdown…` opens the platform's save dialog (title `Export to
Markdown`, default name `<title>.md`, falling back to `export.md` for a blank
title, filter `Markdown (*.md)`) and writes a one-way serialisation of the
clicked opener's extent as a nested outline, two spaces per level. A
workflow's start node is a plain bullet (`- <title>`) nesting everything in
the workflow one level in; a begin node likewise nests its scope. A run of
tasks along one line stays flat. A task is a checkbox item, `[x]` done, `[ ]`
to do or doing, with a cancelled task's title struck through (`~~title~~`)
and no checkbox change. A branch opens a nested sub-list one level in beneath
the lower node of the gap it departs from, headed by its start node's bullet
and ending with an italic line: `*returns above “<title>”*` when it returns,
naming the lower node of its return gap (an end node named as `the close of
“<project title>”`), or `*runs open*` when it does not. A node's note is
inlined beneath its bullet as an indented continuation paragraph. Closers get
no bullet, though their notes are emitted at their scope's level. The full
extent is exported regardless of the fold state.

---

## 6. The context-menu system

### 6.1 Widget

One menu widget serves every opener (card menus, canvas menu, the automation
pill). Items are a flat list of three shapes: an action (label, optionally
checked, optionally disabled), a submenu (label plus nested items), or a
separator.

Visual spec. The menu floats above everything but dialogs and the note
editor (Appendix C): at least 190px wide, `--panel` fill, `--ink` text at
12.5px, a 1px `--line` edge, corner radius 8, inner spacing 5px all round,
drop shadow (0, 10) blur 30 in black at 28 % opacity; its text is
unselectable. Each item is a row: inner spacing 6px vertical and 10px
horizontal, corner radius 5, single-line, pointer cursor; contents left to
right, 6px apart, are a 12px-wide centred check column (`--muted`, 11px; the
text `✓` when checked, empty otherwise, so labels align), the label (taking
the remaining width), and for submenus a `›` arrow (`--muted`, 10px to the
label's right). Hovered rows fill `--line` at 20 % opacity. Disabled rows
draw at 40 % opacity, no hover fill, no activation. A separator is a 1px
`--line` rule at 50 % opacity with 5px above and below and 6px side insets.

A submenu opens on hover only, anchored to its own row: its left edge at the
parent row's right edge plus 3px, its top 6px above the row's top. It has no
open delay, its parent row is not itself activatable, and it never flips to
the left near a screen edge. Activating an action closes the menu first, then
runs the action, so any dialog it opens appears with the menu already gone.

Placement: at the pointer, in window coordinates (the menu never scales with
map zoom). If the menu would overflow the window it is shifted flush to the
edge with a 4px inset (not flipped); submenus are not clamped.

Dismissal: an action, a press anywhere outside (handled before the pressed
element reacts, so the menu closes at the press and a drag begun outside
dismisses it immediately), Escape, a scroll, a window resize, or another
right-click outside. Opening a domain or deleting one also closes any open
menu.

There is no keyboard navigation (no arrows, no type-ahead, no Enter).

### 6.2 The task-card menu

Right-click on a task card. Items in order; an empty condition column means
always present:

| Item | Condition |
| --- | --- |
| `Status` ▸ `To do` / `Doing` / `Done` / `Cancelled` | the current status row is checked |
| `Clear here` or `Make here` | `Clear here` when this task carries the cursor |
| `Make project` | |
| `Wrap as project` ▸ | legal runs exist; first entry `Just this one`, then `Up to “<title>”` per node further up (an end node shown as `the close of “<project>”`) |
| `Move up` | a distinct position exists above |
| `Move down` | a distinct position exists below |
| `Rename…` | |
| separator | |
| `Add task above` | |
| `Add task below` | |
| `Add branch above` ▸ `Left` / `Right` | |
| `Add branch below` ▸ `Left` / `Right` | |
| `Return a branch here` ▸ | legal candidate branches exist; one entry per branch, labelled by its start node's title, or its id when the title is empty |
| `Move a branch here` ▸ | same rule and labelling, for the branch's departure |
| `Paste above` / `Paste below` | a Copy has been made this session |
| separator | |
| `Edit note…` | |
| `Delete note…` | only when the node has a note (the item's presence is the indicator) |
| `Activity log…` | |
| separator | |
| `Delete…` | |

### 6.3 The begin-card menu

Same builder, with these differences: no `Status` submenu and no here items
(a begin node has neither); `Make project` becomes `Make task`; after the
Wrap item it gains `Unwrap…`, then `Expand` or `Collapse` (by current fold
state), `Copy`, and `Export to Markdown…`. Its `Delete…` deletes the whole
project.

Folded-scope withholdings: when the project is folded, `Add task above`,
`Add branch above`, `Return a branch here`, and `Move a branch here` are
absent (not disabled), because anything added on the gap above a folded begin
node would land invisibly inside the fold; expanding restores them.

### 6.4 The end-card menu

Right-click on a project's close. It has no title, status, or cursor, so the
menu is short: `Add task above`, `Add task below`, `Add branch above` ▸,
`Add branch below` ▸, then `Return a branch here` ▸ and `Move a branch
here` ▸ (only when candidate branches exist), then a separator, then
`Expand` or `Collapse` (resolved against the begin node the close pairs
with, so either end of the pair acts identically), `Edit note…`, `Delete
note…` when a note exists, and `Activity log…`. No `Delete…`: a closer is
deleted with its opener.

### 6.5 The start-card menu

Right-click on a workflow's opener: `Rename…`; for a main workflow `Move
left` and `Move right` (each present when a neighbour exists in the domain's
order); a separator; `Add task above`, `Add branch above` ▸, and, when a
clip exists, `Paste above`; a separator; `Copy` and `Export to Markdown…`;
`Edit note…`, `Delete note…` when a note exists, `Activity log…`; a
separator; `Delete…`, which deletes the whole workflow.

### 6.6 The finish-card menu

Right-click on a workflow's close: for a branch workflow, `Detach return`
when it returns (D18); `Add task below`, `Add branch below` ▸, and `Paste
below` when a clip exists; a separator; `Edit note…`, `Delete note…` when a
note exists, `Activity log…`. A main workflow's finish card omits the first
item. No `Delete…`.

### 6.7 The canvas menu

Right-click on anything that is not a card (junction diamonds included; they
have no menu of their own):

| Item | Condition |
| --- | --- |
| `New workflow…` | |
| `Paste as new workflow` | a Copy has been made this session |
| separator | |
| `Add bookmark…` | always shown; on an empty domain it silently does nothing, since no layout exists to anchor to |
| `Jump to bookmark` ▸ | bookmarks exist; one entry per bookmark, by name |
| `Delete bookmark` ▸ | same list; each entry confirms before deleting |

---

## 7. Dialogs

### 7.1 Widget

Two primitives serve every dialog; both dim the window behind a black overlay
at 35 % opacity and centre a card on it. The card: at least 320px wide, at
most the smaller of 90 % of the window and 440px; `--panel` fill, `--ink`
text, a 1px `--line` edge, corner radius 12, inner spacing 18px vertical and
20px horizontal, drop shadow (0, 20) blur 60 in black at 40 % opacity. Within
it: a title (14px, weight 800, 0.02 tracking, 10px below it); an optional
field label (its own line, 10px, 0.12 tracking, uppercase, `--muted`, 5px
below it); either a single-line text input (full width, 13px, `--ink` text
on a `--ground` fill, 1px `--line` edge, radius 6, inner spacing 8px vertical
and 10px horizontal; when focused, a 2px `--cursor` ring tight against the
edge and the edge itself turning `--cursor`) or a message paragraph (12.5px,
line height 1.5, 4px below it); then a right-aligned row of buttons 8px
apart, 16px above them. A dialog button: 12px text, 1px `--line` edge,
transparent fill, `--ink` text, radius 6, inner spacing 7px vertical and 14px
horizontal; hover fills `--line` at 16 %; a primary button fills `--ink` with
`--ground` text; a danger button fills `--c-doing` with `--ground` text and
matching edge.

Text prompt: title, optional label, the input (focused with its value
pre-selected), then `Cancel` followed by an OK button (primary, default
label `OK`). Enter confirms with the input's value; Escape, Cancel, or a
press on the dimmed backdrop itself cancels. An empty string is a legal
result; each flow decides whether to accept it.

Choice dialog: optional title, optional message, then buttons in the given
order, each with a result value and an optional primary or danger style.
Escape or a backdrop press cancels; Enter does nothing, and no button is
focused on open. With a single OK action it doubles as the application's
alert box.

A dialog raised while the note editor is open must render above the editor.
The specified behaviour has no animation, no focus trap, and no screen-reader
annotations beyond what the toolkit supplies; the builder may improve
accessibility, but visually this is the target.

### 7.2 Text prompts, exact strings

| Flow | Title | Label | Initial value | Blank input |
| --- | --- | --- | --- | --- |
| New workflow | `New workflow` | `Workflow name` | empty | accepted (an untitled workflow) |
| Rename node | `Rename task` / `Rename project` / `Rename workflow` by kind | `Title` | current title | accepted (title cleared) |
| Add task | `Add task above` / `Add task below` | `Title` | empty | accepted (an untitled task) |
| Add branch | `Add branch above` / `Add branch below` | `Branch name` | empty | accepted (an untitled branch) |
| Wrap as project | `Wrap as project` | `Name` | `<from>` or `<from> to <to>` (an end node reads `the close of “<project>”`) | aborts |
| Add bookmark | `Add bookmark` | `Name` | empty | aborts (after trim) |
| New domain | `New domain` | `Domain name` | empty | forwarded; the validator refuses it, surfacing `Could not create domain`. Cancel restores the switcher selection |
| Add log entry | `Add entry` | `Text` | empty | aborts (after trim) |
| Edit log entry | `Edit entry` | `Text` | current text | aborts (after trim) |

Only Cancel/Escape distinguishes abandonment; OK with an empty field resolves
the empty string, and each flow above says what it then does.

### 7.3 Choice dialogs, exact strings

| Trigger | Title | Message | Buttons (value; style) |
| --- | --- | --- | --- |
| Delete a task | no dialog; deletes immediately | | |
| Delete a project | `Delete “<title>”` | `Delete this project and everything in it, including its branches?` | `Cancel` (null) · `Delete project` (danger) |
| Delete a workflow | `Delete “<title>”` | `Delete this workflow and everything in it, including its branches?` | `Cancel` · `Delete workflow` (danger) |
| Unwrap a project | `Unwrap “<title>”` | `Remove the project’s begin and end and keep its contents in place? The begin node’s note and activity log are removed with it.` | `Cancel` · `Unwrap` (danger) |
| Delete a note | `Delete note` | `Delete the note on “<title>”? The text is not recoverable.` (a blank-titled node substitutes its node id for `<title>`) | `Cancel` · `Delete note` (danger) |
| Delete a log entry | `Delete entry` | `Delete this activity-log entry?` | `Cancel` · `Delete` (danger) |
| Delete a bookmark | `Delete bookmark` | `Delete the bookmark “<name>”?` | `Cancel` · `Delete` (danger) |
| Delete a domain | `Delete “<name>”` | `Move “<name>” and all its notes to the Trash? You can restore them from the Trash.` | `Cancel` · `Delete` (danger) |
| Bookmark nodes gone | `Bookmark location is gone` | `None of the nodes “<name>” framed still exist. Showing the whole domain instead.` | `OK` |
| Edit rejected | `Change not saved` | `A change could not be applied: <error>` | `OK` |
| Drop stale | `Change not saved` | `The domain changed while you were dragging. The map has been refreshed; try the drag again.` | `OK` |
| Export failed | `Export failed` | `<error>` | `OK` |
| Domain create failed | `Could not create domain` | `<error>` | `OK` |
| Domain delete failed | `Could not delete domain` | `<error>` | `OK` |
| Clipboard write failed | `MCP endpoint` | `<the URL>` | `OK` |
| Note notices | `Note` | see section 8.6 | `OK` |

Node deletion never touches note files, whichever path removes the node: the
removed nodes' note files stay in the domain's `notes/` directory as
orphans, unread afterwards since a node's recorded filename is the only live
reference. They leave the disk only with the whole domain (the domain-delete
flow) or through the explicit `Delete note…` flow while the node still
exists.

There is no toast layer anywhere; every notice is one of these modals, with a
single exception: a failed note autosave is silent (a diagnostic log line
only; see 8.6). Edit failures are single-flight: while a `Change not saved`
dialog is open, further failures do not stack more dialogs.

---

## 8. The note editor and the activity log panel

### 8.1 The note editor

A full-window overlay above menus and dialogs raised from outside it
(Appendix C), opaque on the ground colour; not a dialog. Opens from `Edit
note…` on any card's menu and from a click on a card's note glyph. There is
no keyboard shortcut to open it.

The editor fills the window as a column:

- A head row: inner spacing 12px vertical and 16px horizontal, items 10px
  apart, a 1px `--line` edge below. Left to right: the title (taking the
  remaining width; 14px, weight 800, 0.02 tracking, truncated with `…`); a
  button `A−` (tooltip `Smaller view text`); a button `A+` (tooltip `Larger
  view text`); the `View`/`Edit` toggle; a close button `✕` (30 × 30, 13px).
- A content row filling the rest: in edit mode, the source pane (a formatting
  toolbar above the text editing area), then a 6px divider, then the preview
  pane; in view mode, the preview pane alone fills the window.

The title shows the node's own title; for an end node it reads `the close of
“<project title>”` and for a finish node `the close of “<workflow title>”`
(curly quotes), or `a close` when the pair cannot be resolved.

The editor always opens in split edit mode (toggle button reading `View`).
The toggle flips between edit (source + preview) and view (preview only);
while editing, the toggle button is inverted ink-on-ground. `A−`/`A+` step
the preview's text size by 2px within 12 to 28 (default 16, the
`note.fontSize` setting), disabling at the ends; the source pane is fixed at
13px and unaffected.

Closing: the `✕` button, or Escape when focus is not inside the text editing
area (inside it, Escape belongs to the editor). Switching or deleting a
domain, and an external deletion of the node, also close it.

### 8.2 The divider

A 6px column-resize handle whose visible rule is the middle 2px in `--line`,
turning `--cursor` on hover. Dragging repositions the split as a fraction of
the content width; each pane keeps a 220px minimum, degrading to a 40 %/60 %
bound when the usable width (the content area minus the 6px divider) falls
below 550px, that is, a window narrower than about 556px. Double-click
resets to half. While resizing, text selection is suppressed and the editing
area ignores the pointer. The fraction persists as the `note.split` setting.

### 8.3 The source pane

A plain-text editing area with markdown syntax highlighting, standard
text-editing behaviour (caret, selection, the toolkit's undo and
input-method support), and an optional line-number gutter. Text: the
platform's monospace face at 13px, line height 1.6. Chrome: transparent
background; the gutter, if drawn, transparent with `--muted` numbers and no
edge; the caret's line tinted `--line` at 12 % opacity; the caret itself
`--cursor`; selection `--cursor` at 24 % opacity; no focus outline. Soft line
wrapping is toggled live by the toolbar's `Wrap` button (the `note.wrap`
setting, default on).

Syntax colours (all tokens, so they follow the theme): headings
`--accent-violet` bold; strong `--ink` bold; emphasis `--ink` italic;
strikethrough `--muted` struck; inline code `--accent-teal`; link text
`--accent-teal` underlined; URLs `--c-doing`; blockquote `--muted` italic;
list markers and link labels `--c-todo`; horizontal rules and every markup
marker (`#`, `**`, `>`, `-`, `1.`, backticks) dimmed `--muted`.

### 8.4 The toolbar

A wrapping row above the source (inner spacing 6px vertical and 8px
horizontal, items 4px apart, a 1px `--line` edge below), each button 12px
with the shared 16 % hover tint. Buttons act on press without stealing the
editing area's focus or selection; each command ends by refocusing the editor
and scrolling the caret into view. In order:

| Button | Tooltip | Effect | Key |
| --- | --- | --- | --- |
| `B` (drawn bold) | `Bold (⌘B)` | wrap each selection in `**` | Mod-b |
| `I` (drawn italic) | `Italic (⌘I)` | wrap in `*` | Mod-i |
| `S` (drawn struck) | `Strikethrough (⌘⇧X)` | wrap in `~~` | Mod-Shift-x |
| `</>` | `Inline code (⌘E)` | wrap in `` ` `` | Mod-e |
| `H` | `Heading` | prefix each selected line with `# ` | |
| `Link` | `Link (⌘K)` | `[text](url)` around the selection, the literal `url` left selected for type-over | Mod-k |
| `List` | `Bullet list` | prefix lines with `- ` | |
| `1.` | `Numbered list` | prefix lines with `1. `, `2. `, … per range | |
| `Quote` | `Blockquote` | prefix lines with `> ` | |
| `Code` | `Code block` | wrap in ```` ```\n … \n``` ```` | |
| `Wrap` (pinned to the row's right end) | `Toggle line wrapping` | toggles soft wrap live; pressed state shown inverted; persists | |

(The `⌘` in tooltips stands for the platform's `Mod` key; render the
platform's own symbol or name.) The commands are insert-only: applying bold
twice nests `**` rather than toggling, and there is no de-prefixing, list
continuation, table, or image command. Wrapping commands operate per
selection range; the line-prefix commands prefix each touched line once even
when two ranges share a line.

### 8.5 The preview pane

The preview renders the note as CommonMark with the common extensions
(tables, strikethrough, task-list checkboxes) plus math: `$…$` inline and
`$$…$$` display, typeset properly, with a malformed formula rendering as
visible error text rather than aborting the preview. Note text is untrusted
input: rendering must not execute anything it contains, and links must be
inert except explicit `http(s)` destinations. The preview re-renders on
every keystroke, debounced to the frame.

Styling (inner spacing 20px vertical and 24px horizontal; base text 16px,
adjustable per 8.1; line height 1.62; `--ink`): headings at levels 1 to 3 in
the display face at 1.7 / 1.4 / 1.18 times the base size, weight 400, line
height 1.15, each with 1.3 times its own size above and 0.45 times its own
size below; block elements share a bottom margin of 0.85 times the base;
links `--accent-teal`, underlined on hover only; inline code in the
monospace face at 0.88 of the base over `--line` at 16 % opacity, inner
spacing 1px and 5px, radius 4; code blocks over `--line` at 14 %, inner
spacing 12px and 14px, radius 8, scrollable; blockquotes carry a 3px `--line`
left edge and `--muted` text; tables rule all cells with 1px `--line` lines,
cells padded 5px and 10px; horizontal rules are a single 1px `--line` line;
images never exceed the pane width.

Link activation in the preview opens externally (only `http(s)`; anything
else is ignored); in-document anchor links behave as ordinary in-pane jumps.

### 8.6 Saving and reconciliation

There is no Save button. Edits autosave on a 500 ms debounce through
`set_note`; leaving edit mode, closing the panel, and quitting the
application each flush a pending save first. A failed write is silent: a
diagnostic log line, no dialog, and the editor keeps its content for the
next attempt. The first non-empty save of a new note records the filename on
the node, which is the moment the card's note glyph appears. Emptying an
existing note is not a delete: the empty text is written to the file, the
node's reference and the card's glyph remain, and only the explicit `Delete
note…` flow removes them. Filenames are the [persistence](persistence.md)
document's.

When another writer (the automation server) changes the domain while a note
is open, the editor reconciles: if the node was deleted, the editor closes
and a `Note` dialog explains `The node whose note you were editing was
removed by another writer, so the note was closed.`; if the file changed and
the editor is clean, it silently reloads; if the file changed while unsaved
edits are pending, the edits are kept and a one-time warning shows: `This
note was changed by another writer while you had unsaved edits. Your edits
are kept; save to keep them.` An in-progress edit is never discarded
silently. These `Note` dialogs must render above the open editor (section
7.1).

Deleting a note from the menu first closes the editor if that note is open,
discarding any pending autosave (the file is about to go), then deletes the
file and clears the node's reference.

### 8.7 The activity log panel

`Activity log…` on any card's menu opens a panel over the map: a card in the
dialog's visual style but anchored to the right edge of the viewport, 380px
wide, the viewport's full height, `--panel` fill, a 1px `--line` edge on its
left, not modal (the map behind stays live, and a right-click on it closes
the panel). Its head row shows the node's title (14px, weight 800,
truncated; closers named as in 8.1) and a close button `✕`; below it, a
primary button `Add entry…`; below that, the entries newest first, each a
block: a first line in `--muted` 11px giving the time (local, `D Mon YYYY,
HH:MM`) and the author (`<name>`, with `· system` for a `system` entry and
`· edited` when `editedAt` is set), then the text in 12.5px with line height
1.5. Hovering an entry reveals two icon buttons at its right, `✎` (`Edit
entry`) and `✕` (`Delete entry`), which open the `Edit entry` prompt and the
`Delete entry` dialog and issue `edit_log_entry` and `delete_log_entry`.
`Add entry…` opens the `Add entry` prompt and issues `add_log_entry`. Entries
page in as the list scrolls; a `system` entry's `event` code is not shown,
its text carrying the meaning.

The panel reconciles like the editor: an external write to the node reloads
the list; an external deletion closes the panel silently. It closes on
domain switch and on Escape.

---

## 9. The About window

Opened from the application menu (where one exists) or the Help menu. A
singleton; opening again focuses the existing window.

A separate window, 420 × 300, fixed size (not resizable, minimisable,
maximisable, or full-screenable), no menu bar of its own, titled `About
PensaForma`. It has its own fixed dark palette independent of the
application's themes: background `#111116`, text `#e9e9ec`, the platform's
standard UI face, text unselectable, content centred with inner spacing 30px
vertical and 34px horizontal.

Content, top to bottom: `PensaForma` (21px, weight 600); `Version <x.y.z>`
(12px, `#9494a0`); an update line (12px, `#9494a0`, held at a fixed minimum
height of 16px so the network answer never shifts the layout); `© 2026 Gary
Frattarola` (11px, `#858590` at 56 % opacity, rendering near `#53535a` over
the `#111116` ground); and a link `Source code` (`#4fc3f7`, 12px, underlined
on hover) to the project's source-hosting page, opened externally.

The update check runs only when the window opens; the application never
reaches the network on its own. It asks the project's release feed for the
latest version (a 5-second timeout) and the line shows one of four states:

| State | Text |
| --- | --- |
| checking (initial) | `Checking for a newer version…` |
| newer version exists | a link, text `PensaForma <version> is available.`, pointing at the project's download page |
| up to date | `PensaForma is up-to-date.` |
| any failure, or an unreadable version | `Could not check for a newer version.` |

Every failure answers unknown, never up-to-date. Nothing downloads or
installs. The answer arrives as data and must be shown as literal text (the
update link constructed deliberately by the application), so a third-party
string is never interpreted or executed, whatever it contains.

---

## 10. The Open Source Licenses window

Opened from `Open Source Licenses…` in the application menu (where one
exists) and the Help menu. A singleton.

A separate window, 720 × 640, minimum 460 × 360, background `#0a1622`,
titled `Open Source Licenses`, no menu bar of its own. Its own fixed dark
palette: background `#0a1622`, panel `#0f1f30`, hairline white at 12 %
opacity, accent `#4fc3f7`; text is layered white-alpha: body at 80 %
opacity, 13px; the header at 60 %; the sub-line and footer at 40 %; card
names at 90 %; card role lines at 50 %; card notes at 42 %; table cells at
72 % with muted version cells at 45 %.

Content: a header `OPEN SOURCE LICENSES` (13px, uppercase, 0.1 tracking) with
the sub-line `PensaForma includes the open-source software below.`; a "Key
components" card list naming the handful of components a user would
recognise, each with a one-line role (the GUI toolkit, the markdown renderer,
the math typesetter, the MCP SDK, the bundled fonts), with versions and links
drawn from the licence inventory generated at package time; then `All
bundled packages (<n>)` as a Package/Version/License table; and a footer
linking the complete third-party notices, opened outside the window.

If the licence inventory is missing (an unpackaged development build), the
window explains that licence notices are generated at package time, with the
project's regeneration step named, and asks the reader to reopen the window
afterwards.

---

## 11. Bookmarks

Bookmarks appear only in the canvas menu (6.7): add, jump (by name), delete
(by name, confirmed). A bookmark is a named saved view stored with the
domain in its bookmarks file: its name, the set of folded projects, and the
set of nodes drawn wholly inside the viewport when it was saved (P5). It
holds no zoom and no camera coordinate.

Jumping applies the fold set (stale entries silently dropped) both to the
live view and to the client's persisted view state, so the restored fold
state survives a restart; it then re-renders and frames the bookmark's
surviving nodes: the smallest camera that shows all of them with a 24px
padding, at a zoom no greater than 1.5, centred. If none survives, the map
fits and the `Bookmark location is gone` dialog names the bookmark. There is
no rename, no reorder, no update-in-place, and no indicator of which bookmark
is active.

---

## 12. Keyboard shortcuts, complete

The application registers no global shortcuts of its own; everything is
mouse-driven except the following, the accelerators the platform's standard
menus carry by convention, and the platform's standard text-editing keys
inside text fields.

| Key | Where | Effect |
| --- | --- | --- |
| Mod-z | the map (no text field focused) | undo the last command, if the slot holds one |
| Escape | context menu | close |
| Escape | either dialog | cancel |
| Escape | a drag | cancel |
| Escape | the activity log panel | close |
| Enter | text-prompt dialog | confirm with the input's value |
| Escape | note editor, focus outside the source pane | close the editor |
| Mod-b / Mod-i / Mod-Shift-x / Mod-e / Mod-k | note source pane | bold / italic / strikethrough / inline code / link |

In the choice dialog Enter does nothing and no button has focus. Inside the
source pane the ordinary text-editing keymap applies.

---

## Appendix A: colour tokens

The theme state selects azure (Light) or navy (Dark); every colour below is
defined per theme. Fonts and the token names are theme-independent. The map's
own role tokens (the status colours, the project and workflow colours, the
cursor) are in the mark geometry's colour appendix; the chrome shares
several.

| Token | Azure (Light) | Navy (Dark) | Used in this document for |
| --- | --- | --- | --- |
| `--ground` | `#d3e6ef` | `#0f2334` | window and note-editor background, inverted-button text |
| `--panel` | `#f8f3e8` | `#1a3a54` | menu, dialog, and panel surfaces |
| `--ink` | `#173242` | `#e8f1f6` | text; active/primary button fill |
| `--line` | `#365b6c` | `#6fb6c9` | edges, separators, hover tints, divider |
| `--muted` | `#5f7d8b` | `#93b3c2` | secondary text, readouts, menu glyphs |
| `--grid` | `#173242` at 10 % | `#6fb6c9` at 13 % | the viewport dot grid |
| `--cursor` | `#d75f2e` | `#f27a44` | focus rings, divider hover |
| `--c-doing` | `#d75f2e` | `#f27a44` | danger buttons, error dot, URL syntax colour |
| `--c-todo` | `#d9a53a` | `#f0bd55` | list-marker syntax colour |
| `--c-cancel` | `#8aa0ab` | `#7590a0` | the automation dot's off state |
| `--accent-teal` | `#1f8f8a` | `#37c2ba` | automation dot on; preview links; code/link syntax |
| `--accent-violet` | `#7d54a6` | `#bd93e6` | heading syntax colour |

### Derived colours, resolved

Every derived tint in this document is a named token drawn at an opacity;
treat them as translucent overlays on whatever lies beneath, or precompute
the composite against the known surface. The complete set used by the
chrome:

| Derived colour | Meaning |
| --- | --- |
| button/menu-item hover tints | `--line` at 16 % (buttons, dialog and note-editor buttons), 20 % (menu items), 12 % (the caret's line in the editor) |
| danger-button hover tint | `--c-doing` at 16 % (the delete-domain button) |
| inline-code and code-block grounds | `--line` at 16 % and 14 % |
| editor selection | `--cursor` at 24 % |
| automation-dot inward ring | `--ink` at 25 % |

One value blends two opaque colours, the danger button's edge, 55 %
`--c-doing` with 45 % `--line`; resolved it is `#8f5d4a` on azure and
`#b79580` on navy. The dialog backdrop is black at 35 % opacity; the shadows
are black at 28 % (menus) and 40 % (dialogs), literal values with no token
behind them.

## Appendix B: fonts and text roles

Two families are bundled with the application (both SIL Open Font License
1.1), plus the platform's monospace face:

- The UI face: League Spartan, a variable face, weights 100 to 900, latin
  and latin-ext coverage. Fall back to the host's standard sans-serif if the
  face is unavailable.
- The display face: Boogaloo, weight 400 only, latin coverage. Fall back to
  League Spartan. Where this document asks for the display face at weight
  800 (the brand), the face has no true 800; render a synthesised bold of
  Boogaloo or League Spartan 800, whichever the toolkit does naturally, and
  keep it consistent.
- Monospace (the note source pane and code): the platform's standard
  monospace face; nothing bundled.

Chrome text roles: brand 13px/800 display uppercase; switcher and buttons
12px UI; icon buttons 14px; mode label and dialog field labels 10px
uppercase with 0.12 tracking; percent readout 11px with equal-width digits;
empty state 14px; menus 12.5px; dialog titles 14px/800; dialog messages
12.5px; dialog inputs 13px; note-editor title 14px/800; note toolbar 12px;
note source 13px monospace; note preview 16px (user-adjustable 12 to 28)
with display-face headings; log panel meta 11px and text 12.5px.

## Appendix C: draw order

Within the main window, from back to front: the map world; the drop
indicator and ghost during a drag; the activity log panel; the context menu;
the dialog layer; the note editor; a dialog raised from within the open note
editor (which must therefore paint above the editor, not on the ordinary
dialog layer). The About and Licenses windows are separate windows above
everything.

## Appendix D: persistence

Every stored value the chrome touches is specified in the
[persistence](persistence.md) document: the theme, the note editor's split,
wrap, and text size, the library root, the last domain, and the automation
server's enablement, port, and scope in `settings.json`; the fold state per
domain in `viewstate.json`; the bookmarks in each domain's `bookmarks.json`;
the notes in each domain's `notes/`. The flagged filter, the copy clipboard,
the zoom and pan, and the undo slot are session-only and never persist.
