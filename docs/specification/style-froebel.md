<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# Fröbel

A style of the application, specified to the [style contract](style-contract.md) and in its checklist's order. The [design page](styles.html?v=froebel) draws it in both themes and governs how every mark looks (D39); positions are the [layout engine](layout-engine.md)'s.

## 1. Character

The primaries on white. Three families are told apart by silhouette: a rounded rectangle for a task, a tapered tag for a project's boundaries, and an ellipse cut into a lid and a bowl for a workflow's. A solid band on the outer edge of every boundary says which way it faces, so a fold reads dark at both ends and pale between. The marks people set are white-and-ink objects that belong to no state: here is a pointer, a triangle laid over the card's left end and aimed at it; flagged is a circle of the pointer's own height standing off the card's right end. The palette is the painter's primaries, cadmium yellow to do, cobalt in progress, and vermilion done, with viridian for a project's boundaries, ultramarine for a workflow's, and black for the line.

Weight is a hierarchy of three: structure is drawn at 1.5 (the tag, the bowl, the lid), work at 2 (a task's outline in its state colour), and the author's marks at 2.5 (the flag and the pointer, in ink). A card is never heavier than its marks nor lighter than its scope.

## 2. The ground

A dot grid as Googie's: one dot at every 40-pixel lattice point, a circle in `--grid` of radius about 1.2, belonging to the viewport.

## 3. Tokens

| token | light | dark |
| --- | --- | --- |
| `--ground` | `#e1e6df` | `#0e0e0e` |
| `--panel` | `#ffffff` | `#262626` |
| `--ink` | `#111111` | `#f2f0ea` |
| `--line` | `#1a1a1a` | `#dcdcdc` |
| `--muted` | `#606060` | `#9a9a9a` |
| `--grid` | `#111111` at 10 % | `#f2f0ea` at 10 % |
| `--c-todo` | `#e6b000` | `#ecca6c` |
| `--c-progress` | `#0a55e0` | `#6f9ce2` |
| `--c-done` | `#e60541` | `#e97079` |
| `--c-cancel` | `#c6c4bc` | `#4a4a4a` |
| `--c-project` | `#0a5c44` | `#75ad97` |
| `--c-workflow` | `#212883` | `#8495d0` |
| `--c-project-tint` | `#dcf4e8` | `#213b30` |
| `--c-workflow-tint` | `#e5edff` | `#2b324c` |
| `--c-todo-tint` | `#fff3bd` | `#3b331f` |
| `--c-progress-tint` | `#deeeff` | `#27334b` |
| `--c-done-tint` | `#ffe5e3` | `#462b2c` |
| `--c-cancel-tint` | `#f0eeea` | `#2d2c29` |
| `--cursor` | `#7b4fb6` | `#a589cf` |

Reasons, kept as constraints on retuning. The three states are pigments rather than the screen's lemon and pure blue, so no state is a tint or a compromise. The two scoping colours are the deepest and quietest on the board, so structure recedes and the primaries on the work come forward. All six colours sit in one band of chroma, so none is electric beside another. The six tints sit at one lightness. The dark palette is the same hues lifted and then desaturated by a quarter. The junction is a solid dot so that at a distance it cannot be read as a to-do glyph.

## 4. Faces

| role | face |
| --- | --- |
| display (card labels) | Instrument Sans 500 |
| interface (chrome) | Instrument Sans 400 |
| data (tags, HERE pill, numbers) | Spline Sans Mono 400 |

## 5. The silhouettes

`m = 1.5`; `x0 = m`, `x1 = w − m`, `y0 = m`. Every body is filled in `--panel` and tinted by zoom (section 16).

### 5.1 Task and here card

A rounded rectangle at the margin, corner radius 14, stroked in the state colour at 2. The here card is the same shape, 16 taller.

### 5.2 Begin node: the tag

A sharp-cornered tag drawn at two thirds of its box and anchored to the top: its drawn height is `hh = (h − grow)·2/3 + grow`, where `grow` is what extra label lines added. With `y1 = hh − m` and `ty = y1 − 14`:

```
P = [ (x0,y0), (x1,y0), (x1,ty), (x1−20,y1), (x0+20,y1), (x0,ty) ]
```

full width on the edge facing the tasks, then a 14-high taper of 20 a side to the narrow base. The body is `--panel`, then a keel 7 high along the base (from `y1 − 7` to `y1`), filled in `--c-project` and clipped to the tag, then the tag's outline stroked in `--c-project` at 1.5 with mitred joins.

### 5.3 End node

The same tag at half its box, `hh = h/2`, anchored to the bottom (its top at `h − hh`), turned through a half turn: `translate(w, h) scale(−1, −1)`, so the keel lies along its top.

### 5.4 Start node: the bowl

The workflow figure is one ellipse 54.75 tall, drawn at 80 % of the card's width (150.4, offset 18.8 into the box) and cut at 23 below its top, 42 % of its height. The start is the segment below the cut: in the start card's frame the figure's top stands at `10.1 − 17 = −6.9`, the cut at `16.1`, and the base at `47.85 + grow`, the figure growing by what extra lines add.

```
W  = 0.8·188 = 150.4,  rx = (W − 2m)/2 = 73.7,  ry = (54.75 + grow)/2
centre = (94, −6.9 + ry)
bowl = the ellipse's segment below y 16.1, closed along the chord
```

The body is `--panel`, then a band 7 high along the base (from `47.85 + grow − 7`), filled in `--c-workflow` and clipped to the bowl, then the bowl's outline stroked in `--c-workflow` at 1.5.

### 5.5 Finish node: the lid

The same ellipse in the finish card's frame, its top at 10.1 and its cut at 33.1; the finish is the segment above the cut, with a band 7 high along its crown (from 10.1), in `--c-workflow`, clipped to the lid, and the outline at 1.5.

### 5.6 The silhouettes at the line

| silhouette | top inset | bottom inset | at the base height |
| --- | --- | --- | --- |
| task, here card | `m − 1` | `m − 1` | 0.5, 0.5 (the stroke's outer edge) |
| begin (tag) | `m` | `h − hh + m` | 1.5, 20.83 |
| end (tag, half-turned) | `h/2 + m` | `m` | 30.5, 1.5 |
| start (bowl) | 16.1 | `h − (47.85 + grow)` | 16.1, 10.15 |
| finish (lid) | 10.1 | `52 − 33.1` | 10.1, 18.9 |

## 6. Folds

A folded project: the end is lifted 8 and painted first, behind the begin, which follows at its seam offset (36 into a pair of 188 by 94); the two tags close into a hexagon with a band at each end. A folded workflow: the finish is painted first and the start over it at its seam offset (17); the lid and the bowl close into the whole ellipse, banded top and bottom. Neither fold lifts the start.

## 7. Card content and label geometry

On a task: the glyph centred at `(29, 26)`; the label from x 41, first baseline 30.5, pitch 15, in the display face at 13; the tag at x 18 on `30.5 + 15(n − 1) + 15.5`, in the data face at 8 with 0.9 tracking, in `--muted`. A cancelled label is struck through and set in `--muted`. A begin node's label is centred on the axis about `(hh − 14)/2 + 0.2`, its baselines 4.5 below; a start node's about the bowl's middle, `(16.1 + 47.85 + grow − 7)/2`, its baselines 4.5 below.

| kind | wrap width | size | line pitch | lines in the base height | growth per further line | padding when named |
| --- | --- | --- | --- | --- | --- | --- |
| task | 133 | 13 | 15 | 1 | 15 | 0 |
| begin | 118 | 13 | 15 | 1 | 15 | 0 |
| start | 108 | 12 | 13.5 | 1 | 14 | 10 |

## 8. Glyphs

The common set at the 11 envelope, with no variation.

## 9. The here mark

The pointer: a triangle laid over the card's left end, base out to the left, apex 15.5 inside the card's edge, aimed at the card. It is 3 taller than the box at each end beyond 10 of air (from `y0 − 11.5` to `h − m + 11.5`), 32.4 from base to apex, so its base stands 16.9 outside the box:

```
top = m − 10 − 1.5,  bot = h − m + 10 + 1.5,  cy = (top + bot)/2
P = [ (−16.9, top), (15.5, cy), (−16.9, bot) ]
the two base corners rounded at 12, the apex sharp
fill --panel, stroke --ink at 2.5, mitred joins
```

It is drawn last, over everything. Put behind the card, with its point under it, a triangle reads as a lens or a horn on the card's side; laid over it, it reads as a pointer.

The HERE pill is drawn in the same treatment: a rounded rectangle 32.5 by 10.5, radius 5.25, inset 0.75 in a 34 by 12 box at x 18 and top `30.5 + 15(n − 1) + 21`, filled `--panel` and stroked in `--ink` at 1.5, the word `HERE` centred in the data face at 7.5 with 1 of tracking, in `--ink`.

## 10. The flag

A circle in the pointer's treatment, `--panel` under an `--ink` edge at 2.5, drawn over the card after its content. Its diameter is the pointer's height (the drawn part's height plus 23) scaled, and it is centred off the drawn part's right edge at its mid-height:

| node | centre, in the card's frame | radius |
| --- | --- | --- |
| task | `(w − m + 15.5, h/2)` | `(h + 23)/2 · 0.55` |
| begin node | `(w − m + 9, hh/2 − 5)` | `(hh + 23)/2 · 0.70` |
| start node | `(94 + dx + 10.5, cy − 6)` | `(hb − ht + 23)/2 · 0.75` |

For the start node, `ht = 16.1` and `hb = 47.85 + grow` are the bowl's top and base, `cy` their midpoint, and `dx` the bowl's half-width at `cy`: `rx · sqrt(1 − ((cy − ecy)/ry)²)` with `ecy` the ellipse's centre.

## 11. Tracks

Riser 3 and laterals 2.3 in `--line`, round caps and joins.

The lateral's route is an S: one cubic leaving the junction horizontally and arriving at the landing vertically, its control points 60 % of the way toward the corner on each axis.

```
J = the junction end,  E = the branch end
C1 = (J.x + 0.6·(E.x − J.x), J.y)
C2 = (E.x, E.y − 0.6·(E.y − J.y))
M J  C C1 C2 E
```

Siblings sharing a junction leave it together, each curve running to its own lane; a nearer sibling's curve turns sooner and lies above a farther one's on a departure (below on a return), so they never cross.

Clearance: the curve leaves the junction horizontally, so across the half-width of the card beside it it climbs at most 3.54 at one lane and 0.81 at two, against the 20 that `L − junctionMargin` allows; at its other end it arrives vertically in the branch's own lane, `L` below the start's silhouette or above the finish's.

## 12. The underpass

The common construction, `crossedHalf` 1.5 for a riser and 1.15 for a lateral, round line ends.

## 13. The junction

A solid dot of radius 5.5 in `--line`.

## 14. The note glyph

The common design box, body corner radius 1, round line ends, at the common placement.

## 15. The drop indicator

The common chevron pair in `--cursor`.

## 16. Tint

Fröbel tints by zoom (style contract, section 8): every task body takes its state's tint, a begin or end body `--c-project-tint`, and a start or finish body `--c-workflow-tint`. The fade starts at 72 %, where a 2 outline still carries the state on its own.

## 17. Golden masters

Generated from [styles-masters.json](styles-masters.json) by `scripts/style_masters.py`; do not edit by hand.

<!-- masters:froebel:begin -->

Task, box `188 56`:

```svg
<g><path class="bd bd-todo" fill="var(--panel)" d="M 15.5,1.5 H 172.5 A 14 14 0 0 1 186.5,15.5 V 40.5 A 14 14 0 0 1 172.5,54.5 H 15.5 A 14 14 0 0 1 1.5,40.5 V 15.5 A 14 14 0 0 1 15.5,1.5 Z"/><path fill="none" stroke="var(--c-todo)" stroke-width="2" d="M 15.5,1.5 H 172.5 A 14 14 0 0 1 186.5,15.5 V 40.5 A 14 14 0 0 1 172.5,54.5 H 15.5 A 14 14 0 0 1 1.5,40.5 V 15.5 A 14 14 0 0 1 15.5,1.5 Z"/></g>
```

Here card, box `188 72`:

```svg
<g><path class="bd bd-progress" fill="var(--panel)" d="M 15.5,1.5 H 172.5 A 14 14 0 0 1 186.5,15.5 V 56.5 A 14 14 0 0 1 172.5,70.5 H 15.5 A 14 14 0 0 1 1.5,56.5 V 15.5 A 14 14 0 0 1 15.5,1.5 Z"/><path fill="none" stroke="var(--c-progress)" stroke-width="2" d="M 15.5,1.5 H 172.5 A 14 14 0 0 1 186.5,15.5 V 56.5 A 14 14 0 0 1 172.5,70.5 H 15.5 A 14 14 0 0 1 1.5,56.5 V 15.5 A 14 14 0 0 1 15.5,1.5 Z"/></g>
```

Begin node, box `188 58`:

```svg
<g><g><path class="bd bd-project" fill="var(--panel)" d="M 1.5,1.5 L 186.5,1.5 L 186.5,23.17 L 166.5,37.17 L 21.5,37.17 L 1.5,23.17 Z"/><clipPath id="mc1"><path d="M 1.5,1.5 L 186.5,1.5 L 186.5,23.17 L 166.5,37.17 L 21.5,37.17 L 1.5,23.17 Z"/></clipPath><rect x="1.5" y="30.17" width="185" height="7" fill="var(--c-project)" clip-path="url(#mc1)"/><path fill="none" stroke="var(--c-project)" stroke-width="1.5" stroke-linejoin="miter" d="M 1.5,1.5 L 186.5,1.5 L 186.5,23.17 L 166.5,37.17 L 21.5,37.17 L 1.5,23.17 Z"/></g></g>
```

End node, box `188 58`:

```svg
<g><g transform="translate(188 58) scale(-1 -1)"><path class="bd bd-project" fill="var(--panel)" d="M 1.5,1.5 L 186.5,1.5 L 186.5,13.5 L 166.5,27.5 L 21.5,27.5 L 1.5,13.5 Z"/><clipPath id="mc2"><path d="M 1.5,1.5 L 186.5,1.5 L 186.5,13.5 L 166.5,27.5 L 21.5,27.5 L 1.5,13.5 Z"/></clipPath><rect x="1.5" y="20.5" width="185" height="7" fill="var(--c-project)" clip-path="url(#mc2)"/><path fill="none" stroke="var(--c-project)" stroke-width="1.5" stroke-linejoin="miter" d="M 1.5,1.5 L 186.5,1.5 L 186.5,13.5 L 166.5,27.5 L 21.5,27.5 L 1.5,13.5 Z"/></g></g>
```

Folded project, box `188 94`:

```svg
<g transform="translate(0 -8)"><g transform="translate(188 58) scale(-1 -1)"><path class="bd bd-project" fill="var(--panel)" d="M 1.5,1.5 L 186.5,1.5 L 186.5,13.5 L 166.5,27.5 L 21.5,27.5 L 1.5,13.5 Z"/><clipPath id="mc3"><path d="M 1.5,1.5 L 186.5,1.5 L 186.5,13.5 L 166.5,27.5 L 21.5,27.5 L 1.5,13.5 Z"/></clipPath><rect x="1.5" y="20.5" width="185" height="7" fill="var(--c-project)" clip-path="url(#mc3)"/><path fill="none" stroke="var(--c-project)" stroke-width="1.5" stroke-linejoin="miter" d="M 1.5,1.5 L 186.5,1.5 L 186.5,13.5 L 166.5,27.5 L 21.5,27.5 L 1.5,13.5 Z"/></g></g><g transform="translate(0 36)"><g><path class="bd bd-project" fill="var(--panel)" d="M 1.5,1.5 L 186.5,1.5 L 186.5,23.17 L 166.5,37.17 L 21.5,37.17 L 1.5,23.17 Z"/><clipPath id="mc4"><path d="M 1.5,1.5 L 186.5,1.5 L 186.5,23.17 L 166.5,37.17 L 21.5,37.17 L 1.5,23.17 Z"/></clipPath><rect x="1.5" y="30.17" width="185" height="7" fill="var(--c-project)" clip-path="url(#mc4)"/><path fill="none" stroke="var(--c-project)" stroke-width="1.5" stroke-linejoin="miter" d="M 1.5,1.5 L 186.5,1.5 L 186.5,23.17 L 166.5,37.17 L 21.5,37.17 L 1.5,23.17 Z"/></g></g>
```

Start node, box `188 58`:

```svg
<g><g transform="translate(18.8 0)"><path class="bd bd-workflow" fill="var(--panel)" d="M 147.95,16.1 A 73.7 27.38 0 1 1 2.45,16.1 Z"/><clipPath id="mc5"><path d="M 147.95,16.1 A 73.7 27.38 0 1 1 2.45,16.1 Z"/></clipPath><rect x="0" y="40.85" width="150.4" height="7" fill="var(--c-workflow)" clip-path="url(#mc5)"/><path fill="none" stroke="var(--c-workflow)" stroke-width="1.5" d="M 147.95,16.1 A 73.7 27.38 0 1 1 2.45,16.1 Z"/></g></g>
```

Finish node, box `188 52`:

```svg
<g><g transform="translate(18.8 0)"><path class="bd bd-workflow" fill="var(--panel)" d="M 2.45,33.1 A 73.7 27.38 0 0 1 147.95,33.1 Z"/><clipPath id="mc6"><path d="M 2.45,33.1 A 73.7 27.38 0 0 1 147.95,33.1 Z"/></clipPath><rect x="0" y="10.1" width="150.4" height="7" fill="var(--c-workflow)" clip-path="url(#mc6)"/><path fill="none" stroke="var(--c-workflow)" stroke-width="1.5" d="M 2.45,33.1 A 73.7 27.38 0 0 1 147.95,33.1 Z"/></g></g>
```

Folded workflow, box `188 75`:

```svg
<g><g transform="translate(18.8 0)"><path class="bd bd-workflow" fill="var(--panel)" d="M 2.45,33.1 A 73.7 27.38 0 0 1 147.95,33.1 Z"/><clipPath id="mc7"><path d="M 2.45,33.1 A 73.7 27.38 0 0 1 147.95,33.1 Z"/></clipPath><rect x="0" y="10.1" width="150.4" height="7" fill="var(--c-workflow)" clip-path="url(#mc7)"/><path fill="none" stroke="var(--c-workflow)" stroke-width="1.5" d="M 2.45,33.1 A 73.7 27.38 0 0 1 147.95,33.1 Z"/></g></g><g transform="translate(0 17)"><g transform="translate(18.8 0)"><path class="bd bd-workflow" fill="var(--panel)" d="M 147.95,16.1 A 73.7 27.38 0 1 1 2.45,16.1 Z"/><clipPath id="mc8"><path d="M 147.95,16.1 A 73.7 27.38 0 1 1 2.45,16.1 Z"/></clipPath><rect x="0" y="40.85" width="150.4" height="7" fill="var(--c-workflow)" clip-path="url(#mc8)"/><path fill="none" stroke="var(--c-workflow)" stroke-width="1.5" d="M 147.95,16.1 A 73.7 27.38 0 1 1 2.45,16.1 Z"/></g></g>
```

Glyph to do, box `centred on 0 0`:

```svg
<path d="M 0,-7.63 L 7.48,5.32 L -7.47,5.32 Z" fill="var(--c-todo)"/>
```

Glyph in progress, box `centred on 0 0`:

```svg
<circle cx="0" cy="0" r="6.324999999999999" fill="var(--c-progress)"/>
```

Glyph done, box `centred on 0 0`:

```svg
<rect x="-6.32" y="-6.32" width="12.649999999999999" height="12.649999999999999" fill="var(--c-done)"/>
```

Glyph cancelled, box `centred on 0 0`:

```svg
<circle cx="0" cy="0" r="5.4624999999999995" fill="none" stroke="var(--c-cancel)" stroke-width="1.5" stroke-dasharray="2.4 2.2"/>
```

Flag on a task, box `188 56`:

```svg
<g transform="translate(0 0)"><circle cx="202" cy="28" r="21.73" fill="var(--panel)" stroke="var(--ink)" stroke-width="2.5"/></g>
```

Flag on a begin node, box `188 58`:

```svg
<circle cx="195.5" cy="14.33" r="21.58" fill="var(--panel)" stroke="var(--ink)" stroke-width="2.5"/>
```

Flag on a start node, box `188 58`:

```svg
<circle cx="171.38" cy="25.98" r="20.53" fill="var(--panel)" stroke="var(--ink)" stroke-width="2.5"/>
```

Here mark, box `188 72`:

```svg
<path fill="var(--panel)" stroke="var(--ink)" stroke-width="2.5" stroke-linejoin="miter" d="M -9.99,-0.19 L 15.5,36 L -9.99,72.19 Q -16.9,82 -16.9,70 L -16.9,2 Q -16.9,-10 -9.99,-0.19 Z"/>
```

Junction, box `centred on 0 0`:

```svg
<circle cx="0" cy="0" r="5.5" fill="var(--line)"/>
```

Drop indicator, box `centred on 0 0`:

```svg
<g fill="none" stroke="var(--cursor)" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M -13,-6 L -7,0 L -13,6"/><path d="M 13,-6 L 7,0 L 13,6"/></g>
```

Tracks: riser 3, laterals 2.3, line ends round, joins round.
The flag is painted over the card.

| token | light | dark |
| --- | --- | --- |
| `--ground` | `#e1e6df` | `#0e0e0e` |
| `--panel` | `#ffffff` | `#262626` |
| `--ink` | `#111111` | `#f2f0ea` |
| `--line` | `#1a1a1a` | `#dcdcdc` |
| `--muted` | `#606060` | `#9a9a9a` |
| `--grid` | `rgba(17,17,17,.10)` | `rgba(242,240,234,.10)` |
| `--c-todo` | `#e6b000` | `#ecca6c` |
| `--c-progress` | `#0a55e0` | `#6f9ce2` |
| `--c-done` | `#e60541` | `#e97079` |
| `--c-cancel` | `#c6c4bc` | `#4a4a4a` |
| `--c-project` | `#0a5c44` | `#75ad97` |
| `--c-project-tint` | `#dcf4e8` | `#213b30` |
| `--c-workflow` | `#212883` | `#8495d0` |
| `--c-workflow-tint` | `#e5edff` | `#2b324c` |
| `--c-todo-tint` | `#fff3bd` | `#3b331f` |
| `--c-progress-tint` | `#deeeff` | `#27334b` |
| `--c-done-tint` | `#ffe5e3` | `#462b2c` |
| `--c-cancel-tint` | `#f0eeea` | `#2d2c29` |
| `--cursor` | `#7b4fb6` | `#a589cf` |
| `--f-disp` | `"Instrument Sans",sans-serif` | `"Instrument Sans",sans-serif` |
| `--f-ui` | `"Instrument Sans",sans-serif` | `"Instrument Sans",sans-serif` |
| `--f-mono` | `"Spline Sans Mono",monospace` | `"Spline Sans Mono",monospace` |

<!-- masters:froebel:end -->

## 18. Settled by eye

The flag circle's scales and offsets on the three kinds, and the move from the index tab to the circle (2026-09-17, D44). The tint thresholds and curve (D46). The weight hierarchy, the tag's taper, the ellipse's cut at 42 %, the fold lift of 8, and the palette, from the style's development. Open: Fröbel's density on a large domain, the to-do colour, and the dark flag at fit (in-flight ideas).
