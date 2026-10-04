<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# Prairie

A style of the application, specified to the [style contract](style-contract.md) and in its checklist's order. The [design page](styles.html?v=prairie) draws it in both themes and governs how every mark looks (D39); positions are the [layout engine](layout-engine.md)'s.

## 1. Character

The two-dimensional language of the prairie school: its title blocks, letterheads, and light screens rather than its buildings. A task is a long low plane framed by a hairline set in from its edge, not by a border, with a band along its foot that cantilevers past the plane at one corner. The line is a hairline with a small square at every terminal and junction, like the zinc cames of a light screen. Saturated colour is rationed to small accents on earth grounds, and one red square, the here mark, sits at a corner of its card, never centred. Nothing on a plane is stroked heavier than a hair.

## 2. The ground

A dot grid as Googie's: one dot at every 40-pixel lattice point, a circle in `--grid` of radius about 1.2, belonging to the viewport.

## 3. Tokens

| token | light | dark |
| --- | --- | --- |
| `--ground` | `#d6cdb2` | `#181310` |
| `--panel` | `#fbf8f0` | `#4b4033` |
| `--ink` | `#2a2018` | `#f3ece0` |
| `--line` | `#645c3d` | `#b7b283` |
| `--muted` | `#8a7b66` | `#a0927f` |
| `--grid` | `#2a2018` at 9 % | `#efe7d6` at 10 % |
| `--c-todo` | `#c3a47c` | `#8f8579` |
| `--c-progress` | `#c8783d` | `#e0955c` |
| `--c-done` | `#1a8598` | `#4fb3c4` |
| `--c-cancel` | `#b09a8a` | `#6e655b` |
| `--c-project` | `#4a3627` | `#c2a97e` |
| `--c-workflow` | `#d3a52e` | `#e2be52` |
| `--c-shade` | `#9c8f74` | `#7d6c55` |
| `--c-here` | `#91493e` | `#c96b5d` |
| `--cursor` | `#6d9185` | `#8fb3a6` |

Reasons, kept as constraints on retuning: earth grounds, sand for the ground and plaster for the plane, olive for the line, ochre in progress, mustard for the workflow figures, a deep umber for the project bands, a sea green for done, and two sands for to do and cancelled. A card is never more than a tenth colour. `--c-here`, an iron-oxide red, appears nowhere but the here mark.

## 4. Faces

| role | face |
| --- | --- |
| display (card labels; project and workflow names in tracked capitals) | Jost 500 |
| interface (chrome) | Jost 400 |
| data (tags and the HERE pill, in tracked capitals) | Jost 400 |

A name in tracked capitals is set in upper case at 11 with 1.3 of letter spacing, measured that way.

## 5. The silhouettes

Every fill is flat and nothing on a plane is stroked heavier than the hairline, 1.7. Line ends are butt and joins mitred throughout.

### 5.1 Task and here card

A plane `rect(0, 0, 180, h)` in `--panel`, with no border, and a shade strip `rect(177.6, 0, 2.4, h − 4)` in `--c-shade` along its right edge. The inner frame is two L-shaped hairlines in `--muted` at 1.7, set 6 in from the plane's edge and open at the top-right and bottom-left corners, so they read as two planes sliding past each other:

```
M 6,(h−16)  L 6,6  L 158,6
M 174,22  L 174,(h−6)  L 22,(h−6)
```

The state band, the water table, is `rect(0, h − 4, 188, 4)` in the state colour, running the full 188 so that it overhangs the plane by 8 at the bottom right. A cancelled task draws the band as a hairline outline instead, `rect(0.4, h − 3.6, 187.2, 3.2)` stroked in `--c-cancel` at 1.7. The here card is the same, 16 taller.

### 5.2 Begin node: the roof

An 8 band across the top, `rect(0, 4, 188, 8)`, and a 3 band sliding out to the right beneath it, `rect(12, 16, 176, 3)`, both in `--c-project`. Below them sits the name, as on a letterhead (section 7).

### 5.3 End node

The roof mirrored at the foot: `rect(0, h − 19, 176, 3)` and `rect(0, h − 12, 188, 8)`, the thin band sliding out to the left, and nothing else.

### 5.4 Start node: the half-disc on its armature

An armature, a hairline of weight 3 in `--line` from `(30, 29)` to `(158, 29)` with a came square of 8 centred on each end, and a half-disc of radius 18 resting on it at the axis, `M 76,29 A 18 18 0 0 1 112,29 Z`, in `--c-workflow`. A named start sets its name below (section 7) and a second rule under the name; an unnamed start draws the second rule at y 51: a hairline of 3 from `(44, y)` to `(144, y)` with a came square of 8 on each end.

### 5.5 Finish node: the cornice

A hairline of weight 3 in `--line` from `(40, 30)` to `(148, 30)` with a came square of 8 on each end, and five tesserae, squares of 8 with their centres at x 74, 84, 94, 104, and 114 and their tops at 20, in `--c-workflow`.

### 5.6 The silhouettes at the line

| silhouette | top inset | bottom inset | at the base height |
| --- | --- | --- | --- |
| task, here card | 0 | 0 | 0, 0 |
| begin (roof and name) | 4 | `h − (38 + 15(n − 1))` | 4, 20 |
| end | `h − 19` | 4 | 39, 4 |
| start, unnamed | 11 | `h − 55` | 11, 3 |
| start, named | 11 | `h − (59 + 15(n − 1) + 9)` | 11, 0 at one line |
| finish | 20 | `52 − 31` | 20, 21 |

`n` is the number of name lines.

## 6. Folds

A folded project: the end is painted first and the begin over it at its seam offset, with no lift; the two roofs close about the seam, their thin bands sliding opposite ways. A folded workflow: the finish first and the start over it at its seam offset; the cornice and the half-disc stack into one figure.

## 7. Card content and label geometry

On a task: the label from x 24, first baseline 30.5, pitch 15, in the display face at 13; the tag line at `tagY = 30.5 + 15(n − 1) + 15.5`, the glyph opening it, centred at `(28, tagY − 3)`, and the tag text from x 37 in tracked capitals at 8 in `--muted`. The HERE pill is a hairline box 34 by 11 at x 24 and top `30.5 + 15(n − 1) + 21`, filled `--panel` and stroked in `--ink` at 1.7, the word `HERE` centred in it at 7.5 with 1 of tracking, in `--ink`. A cancelled label is struck through and set in `--muted`.

A begin node's name: a square of 4 at `(8, 27)` in `--c-project`, then the name in tracked capitals from x 16, first baseline 34, pitch 15. A start node's name: in tracked capitals from x 30, first baseline 59, pitch 15, each line on a knockout of `--ground` (3 beyond the text at each side, from 8.8 above the baseline to 4 below) so the riser does not run through it, and a second rule 6 below the last baseline, from x 44 to 144, with a came square at each end.

| kind | wrap width | size | line pitch | lines in the base height | growth per further line | padding when named |
| --- | --- | --- | --- | --- | --- | --- |
| task | 140 | 13 | 15 | 1 | 15 | 0 |
| begin | 150 (capitals) | 11 | 15 | 1 | 15 | 0 |
| start | 140 (capitals) | 11 | 15 | 1 | 15 | 10 |

## 8. Glyphs

The common set on a 9 envelope, at the factor 1.15: triangle side 12.65, circle radius 5.175, square side 9.2, cancelled ring radius 4.6.

## 9. The here mark

One square of 14 in `--c-here`, centred on the card's top-left corner, `rect(−7, −7, 14, 14)`, half outside the plane, with no stroke, drawn last over everything. It is the only red on the board and it is never centred.

## 10. The flag

A small standard in `--ink`, drawn over the card after its content: a hairline spine at 1.7 and three bars of height 3.5 and unequal length stepping down it from the spine to the right. On a task the spine stands at x 184 from y 10 to `h − 10`, and the bars start at y 13, 21, and 29 with lengths 16, 11, and 6, overhanging the box by up to 12. On a begin node the same standard stands beside the roof's right end, its spine at x 191.5 from y 4 (level with the roof's top) for `h − 20`, the bars at y 7, 15, and 23. On a start node it stands beside the armature's last came, its spine at x 165.5 from y 25 for `h − 20`, the bars at y 28, 36, and 44, reaching down past the second rule.

## 11. Tracks

Riser 3 and laterals 2.4 in `--line`, butt ends and mitred joins.

The lateral's route is a came: it runs out horizontally at the junction's height to the branch's lane, then vertically to the landing, its corner cut by a 45° chamfer of 12.

```
J = the junction end,  E = the branch end,  sx = sign(E.x − J.x),  sy = sign(E.y − J.y),  c = 12
M J  L (E.x − sx·c, J.y)  L (E.x, J.y + sy·c)  L E
(where the vertical or horizontal run is shorter than c, no chamfer: M J L (E.x, J.y) L E)
```

Siblings sharing a junction share the horizontal run and turn off it at their own lanes, so they meet only along that shared run and at its corners and never cross.

Clearance: the horizontal run lies at the junction's height, `L` from the cards above and below the junction, and the vertical run lies in the branch's own lane, so the route stays within the band the layout reserves.

## 12. The underpass

The common construction, `crossedHalf` 1.5 for a riser and 1.2 for a lateral, butt line ends.

## 13. The junction

A came square of 8, axis-aligned, centred on the point, in `--line`.

## 14. The note glyph

The common design box with square corners and butt line ends, at the common placement.

## 15. The drop indicator

The common chevron pair in `--cursor`.

## 16. Tint

Prairie does not tint by zoom.

## 17. Golden masters

Generated from [styles-masters.json](styles-masters.json) by `scripts/style_masters.py`; do not edit by hand.

<!-- masters:prairie:begin -->

Task, box `188 56`:

```svg
<g><rect x="0" y="0" width="180" height="56" fill="var(--panel)"/><rect x="177.6" y="0" width="2.4" height="52" fill="var(--c-shade)"/><path fill="none" stroke="var(--muted)" stroke-width="1.7" d="M 6,40 L 6,6 L 158,6"/><path fill="none" stroke="var(--muted)" stroke-width="1.7" d="M 174,22 L 174,50 L 22,50"/><rect x="0" y="52" width="188" height="4" fill="var(--c-todo)"/></g>
```

Here card, box `188 72`:

```svg
<g><rect x="0" y="0" width="180" height="72" fill="var(--panel)"/><rect x="177.6" y="0" width="2.4" height="68" fill="var(--c-shade)"/><path fill="none" stroke="var(--muted)" stroke-width="1.7" d="M 6,56 L 6,6 L 158,6"/><path fill="none" stroke="var(--muted)" stroke-width="1.7" d="M 174,22 L 174,66 L 22,66"/><rect x="0" y="68" width="188" height="4" fill="var(--c-progress)"/></g>
```

Begin node, box `188 58`:

```svg
<g><rect x="0" y="4" width="188" height="8" fill="var(--c-project)"/><rect x="12" y="16" width="176" height="3" fill="var(--c-project)"/></g>
```

End node, box `188 58`:

```svg
<g><rect x="0" y="39" width="176" height="3" fill="var(--c-project)"/><rect x="0" y="46" width="188" height="8" fill="var(--c-project)"/></g>
```

Folded project, box `188 94`:

```svg
<g><rect x="0" y="39" width="176" height="3" fill="var(--c-project)"/><rect x="0" y="46" width="188" height="8" fill="var(--c-project)"/></g><g transform="translate(0 36)"><rect x="0" y="4" width="188" height="8" fill="var(--c-project)"/><rect x="12" y="16" width="176" height="3" fill="var(--c-project)"/></g>
```

Start node, box `188 58`:

```svg
<g><path fill="none" stroke="var(--line)" stroke-width="3" d="M 30,29 L 158,29"/><rect x="26" y="25" width="8" height="8" fill="var(--line)"/><rect x="154" y="25" width="8" height="8" fill="var(--line)"/><path fill="var(--c-workflow)" d="M 76,29 A 18 18 0 0 1 112,29 Z"/><path fill="none" stroke="var(--line)" stroke-width="3" d="M 44,51 L 144,51"/><rect x="40" y="47" width="8" height="8" fill="var(--line)"/><rect x="140" y="47" width="8" height="8" fill="var(--line)"/></g>
```

Finish node, box `188 52`:

```svg
<g><path fill="none" stroke="var(--line)" stroke-width="3" d="M 40,30 L 148,30"/><rect x="36" y="26" width="8" height="8" fill="var(--line)"/><rect x="144" y="26" width="8" height="8" fill="var(--line)"/><rect x="70" y="20" width="8" height="8" fill="var(--c-workflow)"/><rect x="80" y="20" width="8" height="8" fill="var(--c-workflow)"/><rect x="90" y="20" width="8" height="8" fill="var(--c-workflow)"/><rect x="100" y="20" width="8" height="8" fill="var(--c-workflow)"/><rect x="110" y="20" width="8" height="8" fill="var(--c-workflow)"/></g>
```

Folded workflow, box `188 75`:

```svg
<g><path fill="none" stroke="var(--line)" stroke-width="3" d="M 40,30 L 148,30"/><rect x="36" y="26" width="8" height="8" fill="var(--line)"/><rect x="144" y="26" width="8" height="8" fill="var(--line)"/><rect x="70" y="20" width="8" height="8" fill="var(--c-workflow)"/><rect x="80" y="20" width="8" height="8" fill="var(--c-workflow)"/><rect x="90" y="20" width="8" height="8" fill="var(--c-workflow)"/><rect x="100" y="20" width="8" height="8" fill="var(--c-workflow)"/><rect x="110" y="20" width="8" height="8" fill="var(--c-workflow)"/></g><g transform="translate(0 17)"><path fill="none" stroke="var(--line)" stroke-width="3" d="M 30,29 L 158,29"/><rect x="26" y="25" width="8" height="8" fill="var(--line)"/><rect x="154" y="25" width="8" height="8" fill="var(--line)"/><path fill="var(--c-workflow)" d="M 76,29 A 18 18 0 0 1 112,29 Z"/><path fill="none" stroke="var(--line)" stroke-width="3" d="M 44,51 L 144,51"/><rect x="40" y="47" width="8" height="8" fill="var(--line)"/><rect x="140" y="47" width="8" height="8" fill="var(--line)"/></g>
```

Glyph to do, box `centred on 0 0`:

```svg
<path d="M 0,-6.3 L 6.32,4.65 L -6.32,4.65 Z" fill="var(--c-todo)"/>
```

Glyph in progress, box `centred on 0 0`:

```svg
<circle cx="0" cy="0" r="5.175" fill="var(--c-progress)"/>
```

Glyph done, box `centred on 0 0`:

```svg
<rect x="-4.6" y="-4.6" width="9.2" height="9.2" fill="var(--c-done)"/>
```

Glyph cancelled, box `centred on 0 0`:

```svg
<circle cx="0" cy="0" r="4.6" fill="none" stroke="var(--c-cancel)" stroke-width="1.5" stroke-dasharray="2.4 2.2"/>
```

Flag on a task, box `188 56`:

```svg
<g transform="translate(0 0)"><path fill="none" stroke="var(--ink)" stroke-width="1.7" d="M 184,10 L 184,46"/><rect x="184" y="13" width="16" height="3.5" fill="var(--ink)"/><rect x="184" y="21" width="11" height="3.5" fill="var(--ink)"/><rect x="184" y="29" width="6" height="3.5" fill="var(--ink)"/></g>
```

Flag on a begin node, box `188 58`:

```svg
<path fill="none" stroke="var(--ink)" stroke-width="1.7" d="M 191.5,4 L 191.5,42"/><rect x="191.5" y="7" width="16" height="3.5" fill="var(--ink)"/><rect x="191.5" y="15" width="11" height="3.5" fill="var(--ink)"/><rect x="191.5" y="23" width="6" height="3.5" fill="var(--ink)"/>
```

Flag on a start node, box `188 58`:

```svg
<path fill="none" stroke="var(--ink)" stroke-width="1.7" d="M 165.5,25 L 165.5,63"/><rect x="165.5" y="28" width="16" height="3.5" fill="var(--ink)"/><rect x="165.5" y="36" width="11" height="3.5" fill="var(--ink)"/><rect x="165.5" y="44" width="6" height="3.5" fill="var(--ink)"/>
```

Here mark, box `188 72`:

```svg
<rect x="-7" y="-7" width="14" height="14" fill="var(--c-here)"/>
```

Junction, box `centred on 0 0`:

```svg
<rect x="-4" y="-4" width="8" height="8" fill="var(--line)"/>
```

Drop indicator, box `centred on 0 0`:

```svg
<g fill="none" stroke="var(--cursor)" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M -13,-6 L -7,0 L -13,6"/><path d="M 13,-6 L 7,0 L 13,6"/></g>
```

Tracks: riser 3, laterals 2.4, line ends butt, joins miter.
The flag is painted over the card.

| token | light | dark |
| --- | --- | --- |
| `--ground` | `#d6cdb2` | `#181310` |
| `--panel` | `#fbf8f0` | `#4b4033` |
| `--ink` | `#2a2018` | `#f3ece0` |
| `--line` | `#645c3d` | `#b7b283` |
| `--muted` | `#8a7b66` | `#a0927f` |
| `--grid` | `rgba(42,32,24,.09)` | `rgba(239,231,214,.10)` |
| `--c-todo` | `#c3a47c` | `#8f8579` |
| `--c-progress` | `#c8783d` | `#e0955c` |
| `--c-done` | `#1a8598` | `#4fb3c4` |
| `--c-cancel` | `#b09a8a` | `#6e655b` |
| `--c-project` | `#4a3627` | `#c2a97e` |
| `--c-workflow` | `#d3a52e` | `#e2be52` |
| `--c-here` | `#91493e` | `#c96b5d` |
| `--c-shade` | `#9c8f74` | `#7d6c55` |
| `--cursor` | `#6d9185` | `#8fb3a6` |
| `--f-disp` | `"Jost",sans-serif` | `"Jost",sans-serif` |
| `--f-ui` | `"Jost",sans-serif` | `"Jost",sans-serif` |
| `--f-mono` | `"Jost",sans-serif` | `"Jost",sans-serif` |

<!-- masters:prairie:end -->

## 18. Settled by eye

The standard's places on the begin and start nodes (2026-09-17, D44). The plane's width, the band and its cantilever, the inner frame's breaks, the came squares, the glyph on the tag line, the second rule under a start's name, the chamfered route, and the palette, from the style's development.
