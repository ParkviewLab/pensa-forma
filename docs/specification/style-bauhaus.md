<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# Bauhaus

A style of the application, specified to the [style contract](style-contract.md) and in its checklist's order. The [design page](styles.html?v=bauhaus) draws it in both themes and governs how every mark looks (D39); positions are the [layout engine](layout-engine.md)'s.

## 1. Character

Every mark is a filled plane and nothing is outlined. A task is a white plane with a state bar down its left edge; a project boundary is a heavy black bar; a workflow boundary is one of the elementary forms in black, a disc to open and a square to close. The composition is asymmetric: the state bar and the hanging labels at the left, the flag on the corner, so a card is weighted left and marked right and reads left to right as a page does. The three live states take the primaries on their bars, in the manner of Mondrian's later work: yellow to do, red in progress, blue done. Structure is black throughout, so at any zoom the black is the graph and the colour is the work. The author's marks are black planes.

## 2. The ground

The poster's unbleached stock, with no grid: the sheet is an asymmetric field, not a gridded one. `--grid` is defined for the chrome only.

## 3. Tokens

| token | light | dark |
| --- | --- | --- |
| `--ground` | `#e4ddcc` | `#0f0f0f` |
| `--panel` | `#ffffff` | `#2f2f2f` |
| `--ink` | `#141414` | `#f3efe6` |
| `--line` | `#141414` | `#f3efe6` |
| `--muted` | `#6b6760` | `#a8a49c` |
| `--grid` | `#141414` at 8 % | `#f3efe6` at 10 % |
| `--c-todo` | `#f0c419` | `#f5cf3a` |
| `--c-progress` | `#d8402b` | `#ef5a44` |
| `--c-done` | `#1f4fa0` | `#5b8ee0` |
| `--c-cancel` | `#c4c0b6` | `#5a5852` |
| `--c-project` | `#141414` | `#f3efe6` |
| `--c-workflow` | `#141414` | `#f3efe6` |
| `--cursor` | `#4d6a8a` | `#8fa9c6` |

Reasons, kept as constraints on retuning: the planes are white and the ink near-black, and the ink is also the line and both scoping families; there are no tints, so a body is white at every zoom and colour lives only in the bars and the glyphs.

## 4. Faces

| role | face |
| --- | --- |
| display (card labels and hanging names) | Jost 500 |
| interface (chrome) | Jost 400 |
| data (tags and the HERE pill, in tracked capitals) | Jost 400 |

## 5. The silhouettes

Nothing is stroked; every shape is a filled plane.

### 5.1 Task and here card

A plane `rect(0, 0, 188, h)` in `--panel`, and a state bar `rect(0, 0, 16, h)` in the state colour. A cancelled task keeps its bar, in `--c-cancel`, and strikes its label. The here card is the same, 16 taller.

### 5.2 Begin node

A bar of 14 across the top of the box, `rect(0, 0, 188, 14)`, in `--c-project`, the project's name hanging below it (section 7).

### 5.3 End node

The same bar on the bottom edge, `rect(0, h − 14, 188, 14)`, and nothing else.

### 5.4 Start node

A solid disc of radius 21 centred at `(94, 29)`, in `--c-workflow`; a name, if any, hangs below it (section 7).

### 5.5 Finish node

A solid square of 40, `rect(74, 6, 40, 40)`, in `--c-workflow`.

### 5.6 The silhouettes at the line

| silhouette | top inset | bottom inset | at the base height |
| --- | --- | --- | --- |
| task, here card | 0 | 0 | 0, 0 |
| begin (bar and name) | 0 | `h − (24 + 15·max(1, n))` | 0, 19 |
| end | `h − 14` | 0 | 44, 0 |
| start, unnamed | 8 | `h − 50` | 8, 8 |
| start, named | 8 | 0 | 8, 0 |
| finish | 6 | 6 | 6, 6 |

`n` is the number of name lines.

## 6. Folds

A folded project: the end is painted first and the begin over it at its seam offset, with no lift; the two bars close into one rule of 22. A folded workflow: the finish first and the start over it at its seam offset; the square and the disc join into one black figure.

## 7. Card content and label geometry

On a task the content hangs from the bar: the glyph centred at `(33, 26)`; the label from x 45, first baseline 30.5, pitch 16, in the display face at 14.5; the tag at x 45 on `30.5 + 15(n − 1) + 15.5`, in tracked capitals at 8 in `--muted`. The HERE pill is a black plane, `rect(45, 30.5 + 15(n − 1) + 21, 34, 12)` in `--ink`, the word `HERE` reversed out of it in `--panel` at 7.5 with 1 of tracking.

A begin node's name hangs below its bar, flush left from x 12, first baseline 31, pitch 16, at 14. A start node's name hangs below its disc from x 12, first baseline 66, pitch 16, at 14. Each line of a hanging name sits on a knockout of `--ground` (3 beyond the text at each side, from 0.78 of the type size above the baseline to 4 below), so that type crossing the riser sits in its own paper, as type over a rule does on a printed sheet.

| kind | wrap width | size | line pitch | lines in the base height | growth per further line | padding when named |
| --- | --- | --- | --- | --- | --- | --- |
| task | 131 | 14.5 | 16 | 1 | 16 | 0 |
| begin | 164 | 14 | 16 | 1 | 16 | 0 |
| start | 164 | 14 | 16 | 0 | 16 | 8 |

## 8. Glyphs

The common set at the 11 envelope, with no variation.

## 9. The here mark

A solid equilateral triangle in `--ink` at the card's left end, of half-height 21, its apex 22 inside the card's left edge at mid-height, pointing at the card, so its base stands `21·√3 − 22 = 14.37` outside the box. Under it, a knockout in `--panel` 3 wider all round cuts the state bar away around the point, as paper is left between two planes on a printed sheet:

```
cy = h/2
knockout: [ (−17.37, cy − 26.2), (28, cy), (−17.37, cy + 26.2) ]   fill --panel
pointer:  [ (−14.37, cy − 21),   (22, cy), (−14.37, cy + 21) ]     fill --ink
```

Both are drawn last, over everything.

## 10. The flag

A black square of 22 in `--ink`, drawn over the card after its content. On a task it is centred on the box's top-right corner, `(188, 0)`. On a begin node it is centred 10 right of and 10 above that corner, `(198, −10)`, capping the bar's end. On a start node it stands against the disc's upper right, centred 34 from the disc's centre at 45° and then 2.5 right and 1 down: `(120.54, 5.96)`.

## 11. Tracks

Riser 4 and laterals 3 in `--line`, butt ends and mitred joins.

The lateral's route is orthogonal: out horizontally at the junction's height to the branch's lane, then vertically to the landing, with a square corner.

```
M J  L (E.x, J.y)  L E
```

Siblings sharing a junction share the horizontal run and turn off it at their own lanes; they never cross.

Clearance: the horizontal run lies at the junction's height, `L` from the cards above and below the junction, and the vertical run lies in the branch's own lane.

## 12. The underpass

The common construction, `crossedHalf` 2 for a riser and 1.5 for a lateral, butt line ends.

## 13. The junction

A square of 12, axis-aligned, centred on the point, in `--line`.

## 14. The note glyph

The common design box with square corners and butt line ends, at the common placement.

## 15. The drop indicator

The common chevron pair in `--cursor`.

## 16. Tint

Bauhaus does not tint by zoom.

## 17. Golden masters

Generated from [styles-masters.json](styles-masters.json) by `scripts/style_masters.py`; do not edit by hand.

<!-- masters:bauhaus:begin -->

Task, box `188 56`:

```svg
<g><rect x="0" y="0" width="188" height="56" fill="var(--panel)"/><rect x="0" y="0" width="16" height="56" fill="var(--c-todo)"/></g>
```

Here card, box `188 72`:

```svg
<g><rect x="0" y="0" width="188" height="72" fill="var(--panel)"/><rect x="0" y="0" width="16" height="72" fill="var(--c-progress)"/></g>
```

Begin node, box `188 58`:

```svg
<g><rect x="0" y="0" width="188" height="14" fill="var(--c-project)"/></g>
```

End node, box `188 58`:

```svg
<g><rect x="0" y="44" width="188" height="14" fill="var(--c-project)"/></g>
```

Folded project, box `188 94`:

```svg
<g><rect x="0" y="44" width="188" height="14" fill="var(--c-project)"/></g><g transform="translate(0 36)"><rect x="0" y="0" width="188" height="14" fill="var(--c-project)"/></g>
```

Start node, box `188 58`:

```svg
<g><circle cx="94" cy="29" r="21" fill="var(--c-workflow)"/></g>
```

Finish node, box `188 52`:

```svg
<g><rect x="74" y="6" width="40" height="40" fill="var(--c-workflow)"/></g>
```

Folded workflow, box `188 75`:

```svg
<g><rect x="74" y="6" width="40" height="40" fill="var(--c-workflow)"/></g><g transform="translate(0 17)"><circle cx="94" cy="29" r="21" fill="var(--c-workflow)"/></g>
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
<rect x="177" y="-11" width="22" height="22" fill="var(--ink)"/>
```

Flag on a begin node, box `188 58`:

```svg
<rect x="187" y="-21" width="22" height="22" fill="var(--ink)"/>
```

Flag on a start node, box `188 58`:

```svg
<rect x="109.54" y="-5.04" width="22" height="22" fill="var(--ink)"/>
```

Here mark, box `188 72`:

```svg
<path fill="var(--panel)" d="M -17.37,9.8 L 28,36 L -17.37,62.2 Z"/><path fill="var(--ink)" d="M -14.37,15 L 22,36 L -14.37,57 Z"/>
```

Junction, box `centred on 0 0`:

```svg
<rect x="-6" y="-6" width="12" height="12" fill="var(--line)"/>
```

Drop indicator, box `centred on 0 0`:

```svg
<g fill="none" stroke="var(--cursor)" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M -13,-6 L -7,0 L -13,6"/><path d="M 13,-6 L 7,0 L 13,6"/></g>
```

Tracks: riser 4, laterals 3, line ends butt, joins miter.
The flag is painted over the card.

| token | light | dark |
| --- | --- | --- |
| `--ground` | `#e4ddcc` | `#0f0f0f` |
| `--panel` | `#ffffff` | `#2f2f2f` |
| `--ink` | `#141414` | `#f3efe6` |
| `--line` | `#141414` | `#f3efe6` |
| `--muted` | `#6b6760` | `#a8a49c` |
| `--grid` | `rgba(20,20,20,.08)` | `rgba(243,239,230,.10)` |
| `--c-todo` | `#f0c419` | `#f5cf3a` |
| `--c-progress` | `#d8402b` | `#ef5a44` |
| `--c-done` | `#1f4fa0` | `#5b8ee0` |
| `--c-cancel` | `#c4c0b6` | `#5a5852` |
| `--c-project` | `#141414` | `#f3efe6` |
| `--c-workflow` | `#141414` | `#f3efe6` |
| `--cursor` | `#4d6a8a` | `#8fa9c6` |
| `--f-disp` | `"Jost",sans-serif` | `"Jost",sans-serif` |
| `--f-ui` | `"Jost",sans-serif` | `"Jost",sans-serif` |
| `--f-mono` | `"Jost",sans-serif` | `"Jost",sans-serif` |

<!-- masters:bauhaus:end -->

## 18. Settled by eye

The three primaries on the bars, the tags in tracked capitals, and the ungridded ground (2026-09-17, D48). The flag's places on the begin and start nodes (D44). The bar widths, the disc and the square, the knockouts under hanging names and under the pointer, and the palette, from the style's development.
