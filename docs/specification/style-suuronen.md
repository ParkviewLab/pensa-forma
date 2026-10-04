<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# Suuronen

A style of the application, specified to the [style contract](style-contract.md) and in its checklist's order. The [design page](styles.html?v=suuronen) draws it in both themes and governs how every mark looks (D39); positions are the [layout engine](layout-engine.md)'s.

## 1. Character

The same graph reduced: no splay, no tilt, no variable band. Every body is a superellipse drawn at one stroke weight on a robin's-egg ground, with a heavy keel along its outer end in its own colour. A project's boundaries are a task card sawn in two, the begin its lower three fifths and the end its upper two, cut edges facing the tasks between them. A workflow's boundaries are one figure turned two ways: a dome to close and the same dome inverted, a cup under a square-shouldered body, to open. Here is a pair of solid ink pointers with concave bases just touching the card's two ends; flagged is two ink frames standing off it. Cyan to do, yellow in progress, blue done.

## 2. The ground

A dot grid as Googie's: one dot at every 40-pixel lattice point, a circle in `--grid` of radius about 1.2, belonging to the viewport.

## 3. Tokens

| token | light | dark |
| --- | --- | --- |
| `--ground` | `#dae8ef` | `#0e1a20` |
| `--panel` | `#eef4f8` | `#16242b` |
| `--ink` | `#151f26` | `#e5eef2` |
| `--line` | `#5d7a88` | `#85a0ac` |
| `--muted` | `#6c8593` | `#7d93a0` |
| `--grid` | `#151f26` at 10 % | `#e5eef2` at 11 % |
| `--c-todo` | `#008fa8` | `#0ec7de` |
| `--c-progress` | `#d9bd1c` | `#f6d732` |
| `--c-done` | `#3a7bcb` | `#76b4ff` |
| `--c-cancel` | `#abbac2` | `#4a585e` |
| `--c-project` | `#00734b` | `#2eb184` |
| `--c-workflow` | `#0b267d` | `#5477c7` |
| `--c-project-tint` | `#d6f4e6` | `#173226` |
| `--c-workflow-tint` | `#b4cbf9` | `#303f60` |
| `--c-todo-tint` | `#bfeef7` | `#0e363d` |
| `--c-progress-tint` | `#f2e9bb` | `#3c3615` |
| `--c-done-tint` | `#cfe7ff` | `#203147` |
| `--c-cancel-tint` | `#d8e3ea` | `#2b3134` |
| `--c-junction` | `#1b3358` | `#a9ccd3` |
| `--cursor` | `#e2551f` | `#ff6a33` |

Reasons, kept as constraints on retuning: the three live states sit at one lightness, 45° apart in hue; cancelled is the one near-neutral; the two structure families, project green and workflow ultramarine, are the darkest colours on the board. The dark palette was derived from the light rather than tuned (in-flight ideas).

A keel's colour is not a token: it is the colour of the node it belongs to (a task's state, `--c-project`, or `--c-workflow`) mixed 12 % toward `--ink` in OKLab, a rule the application applies.

## 4. Faces

| role | face |
| --- | --- |
| display (card labels) | Familjen Grotesk 600 |
| interface (chrome) | Familjen Grotesk 500 |
| data (tags, HERE pill, numbers) | Spline Sans Mono 400 |

## 5. The silhouettes

`m = 1.5`. A superellipse of exponent `n` in the box `(x, y, W, H)` is `|(px − cx)/(W/2)|^n + |(py − cy)/(H/2)|^n = 1`, sampled at 88 points (176 where it is cut). Every body is filled in `--panel`, tinted by zoom (section 16), and stroked at 2 in the node's colour; then its keel is drawn: an open path along the heavy part of the outline, stroked at 7.5 with round caps and joins in the keel colour of section 3, so its ends are true half-discs however the outline runs there.

### 5.1 Task and here card

A superellipse of exponent 5 in the box `(m, m, w − 2m, h − 2m)`, stroked in the state colour. The keel runs along the outline below the line at two thirds of the card's height, `y = 2h/3`: the lower third. The here card is the same, 16 taller.

### 5.2 Begin node

A task card at 110 % (`bw = 1.1·(w − 2m) = 203.5`, centred on the axis, so it stands about 9 proud of the cards it brackets), sawn across, keeping its lower part with the cut on top. The begin is drawn `hh = 0.66·(h − grow) + grow` tall:

```
fh  = (hh − 2m) / 0.6                        the height of the card it is cut from
box = (94 − bw/2, hh − m − fh, bw, fh)
begin = the superellipse (exponent 5) in box, the part below y = m, closed by the straight cut
keel  = the outline below y = 2hh/3
```

It is stroked and keeled in `--c-project`.

### 5.3 End node

The same card's upper part, with the cut below. The end is drawn `hh = 0.44·h` tall, anchored to the bottom of its box (its top at `off = h − hh`):

```
fh  = (hh − 2m) / 0.4
box = (94 − bw/2, off + m, bw, fh)
end  = the superellipse in box, the part above y = h − m, closed by the cut
keel = the outline above y = off + hh/3
```

### 5.4 Start node: the cup

A cup under a square-shouldered body, the dome of 5.5 inverted with a body added above it because a start carries its workflow's name. With `rx = 0.595·(w − 2m)/2` and `ry = 0.85·(h − grow − 2m)/2` (55.04 and 23.38 at the base height):

```
X0 = 94 − rx,  W = 2rx,  cupH = ry,  bodyH = 20 + grow,  H = bodyH + cupH
Y0 = h/2 − H/2
M X0,Y0  H X0+W  V Y0+bodyH  A W/2 cupH 0 0 1 X0,Y0+bodyH  Z
```

It is stroked and keeled in `--c-workflow`. The keel runs from half the figure's height, `Y0 + H/2`, down: along the straight sides if that line falls in the body, then around the bowl; or, if it falls in the bowl, along the bowl's arc between its two crossings of that line.

### 5.5 Finish node: the dome

A half-ellipse on a flat base, in a box 97 wide centred in the card (offset 44 plus the margin), 24.5 high, its top at 13.75 and its base at 38.25:

```
M 1.5,38.25  A 48.5 24.5 0 0 1 98.5,38.25  Z        then translate(44, 0)
```

The keel is the dome's upper third: the arc above `y = 13.75 + 24.5/3`, between its two crossings of that line.

### 5.6 The silhouettes at the line

| silhouette | top inset | bottom inset | at the base height |
| --- | --- | --- | --- |
| task, here card | `m` | `m` | 1.5, 1.5 |
| begin | `m` | `h − hh + m` | 1.5, 21.22 |
| end | `h − 0.44h + m` | `m` | 33.98, 1.5 |
| start | `Y0` | `h − Y0 − H` | 7.31, 7.31 |
| finish | 13.75 | 13.75 | 13.75, 13.75 |

## 6. Folds

Both folds are painted in reverse, the closing card lifted 10 and painted behind, so the opening card's shoulders stay unbroken: a folded project paints the end lifted 10 first and the begin over it at its seam offset; a folded workflow paints the finish lifted 10 first and the start over it at its seam offset.

## 7. Card content and label geometry

On a task: the glyph centred at `(29, 26)`; the label from x 41, first baseline 30.5, pitch 15, in the display face at 13; the tag at x 18 on `30.5 + 15(n − 1) + 15.5`, in the data face at 8 with 0.9 tracking, in `--muted`. A cancelled label is struck through and set in `--muted`. The HERE pill is Googie's: 34 by 12, radius 6, in `--cursor`, at x 18 and top `30.5 + 15(n − 1) + 21`, the word in `--panel`. A begin node's label is centred on the axis about `hh/2`, a start node's about `Y0 + 0.47H`, a touch above the cup's middle since the bowl narrows; the baselines sit 4.5 below.

| kind | wrap width | size | line pitch | lines in the base height | growth per further line |
| --- | --- | --- | --- | --- | --- |
| task | 133 | 13 | 15 | 1 | 15 |
| begin | 118 | 13 | 15 | 1 | 15 |
| start | 96 | 12 | 13.5 | 2 | 14 |

## 8. Glyphs

The common set at the 11 envelope, except that the done square is a superellipse of exponent 8 in its 12.65 box.

## 9. The here mark

A pair of pointers in `--ink`, one at each end of the card, pointing at it, drawn last over everything. Each is an equilateral triangle of side 28.5 (height 24.68) with its corners rounded at 3 and its base edge, the vertical edge away from the card, bowed inward to a depth of 2.75 (a quadratic whose control point stands twice the depth in from the base's midpoint). The left pointer is centred at `(m − 18, h/2)` pointing right, the right at `(w − m + 18, h/2)` pointing left, so each apex all but touches the outline.

## 10. The flag

Two frames in `--ink` behind the card, painted before it: offsets of the node's own outline at 7.6 and 13.6, stroked at 1.2 and 1, tapering outward. On a task each frame is the superellipse of exponent 5 in the box grown by the offset on every side. On a begin node each frame is the cut card's superellipse grown by the offset and cut by the same line moved out by the offset, so the frames follow the piece's straight edge. On a start node each frame is the cup grown by the offset: `(X0 − o, Y0 − o)`, width `W + 2o`, body `bodyH + o`, cup `cupH + o`. Where a here card is flagged, the pointers sit on the inner frame.

## 11. Tracks

Riser 3 and laterals 2.3 in `--line`, round caps and joins.

The lateral's route is Fröbel's S: one cubic leaving the junction horizontally and arriving at the landing vertically, its control points 60 % of the way toward the corner on each axis (Fröbel, section 11). Siblings leave a junction together and never cross; the clearance statement is Fröbel's.

## 12. The underpass

The common construction, `crossedHalf` 1.5 for a riser and 1.15 for a lateral, round line ends.

## 13. The junction

Concentric rounded squares: an outer square of 13, radius 3, filled `--ground` and stroked in `--line` at 1.6; an inner square of 6.4, radius 1.5, filled `--c-junction`.

## 14. The note glyph

The common design box, body corner radius 1, round line ends, at the common placement.

## 15. The drop indicator

The common chevron pair in `--cursor`.

## 16. Tint

Suuronen tints by zoom (style contract, section 8): every task body takes its state's tint, a begin or end body `--c-project-tint`, and a start or finish body `--c-workflow-tint`.

## 17. Golden masters

Generated from [styles-masters.json](styles-masters.json) by `scripts/style_masters.py`; do not edit by hand.

<!-- masters:suuronen:begin -->

Task, box `188 56`:

```svg
<g><path class="bd bd-todo" fill="var(--panel)" stroke="var(--c-todo)" stroke-width="2" d="M 186.5,28 L 186.41,37.22 L 186.12,40.15 L 185.65,42.26 L 184.98,43.97 L 184.12,45.4 L 183.06,46.65 L 181.8,47.75 L 180.32,48.72 L 178.62,49.59 L 176.7,50.37 L 174.53,51.07 L 172.09,51.69 L 169.37,52.24 L 166.33,52.73 L 162.92,53.15 L 159.09,53.51 L 154.74,53.82 L 149.73,54.07 L 143.79,54.26 L 136.41,54.39 L 126.17,54.47 L 94,54.5 L 61.83,54.47 L 51.59,54.39 L 44.21,54.26 L 38.27,54.07 L 33.26,53.82 L 28.91,53.51 L 25.08,53.15 L 21.67,52.73 L 18.63,52.24 L 15.91,51.69 L 13.47,51.07 L 11.3,50.37 L 9.38,49.59 L 7.68,48.72 L 6.2,47.75 L 4.94,46.65 L 3.88,45.4 L 3.02,43.97 L 2.35,42.26 L 1.88,40.15 L 1.59,37.22 L 1.5,28 L 1.59,18.78 L 1.88,15.85 L 2.35,13.74 L 3.02,12.03 L 3.88,10.6 L 4.94,9.35 L 6.2,8.25 L 7.68,7.28 L 9.38,6.41 L 11.3,5.63 L 13.47,4.93 L 15.91,4.31 L 18.63,3.76 L 21.67,3.27 L 25.08,2.85 L 28.91,2.49 L 33.26,2.18 L 38.27,1.93 L 44.21,1.74 L 51.59,1.61 L 61.83,1.53 L 94,1.5 L 126.17,1.53 L 136.41,1.61 L 143.79,1.74 L 149.73,1.93 L 154.74,2.18 L 159.09,2.49 L 162.92,2.85 L 166.33,3.27 L 169.37,3.76 L 172.09,4.31 L 174.53,4.93 L 176.7,5.63 L 178.62,6.41 L 180.32,7.28 L 181.8,8.25 L 183.06,9.35 L 184.12,10.6 L 184.98,12.03 L 185.65,13.74 L 186.12,15.85 L 186.41,18.78 L 186.5,28 Z"/><path fill="none" style="stroke:color-mix(in oklab,var(--c-todo) 88%,var(--ink))" stroke-width="7.5" stroke-linecap="round" stroke-linejoin="round" d="M 186.4,37.33 L 186.29,38.84 L 186.12,40.15 L 185.91,41.27 L 185.65,42.26 L 185.34,43.15 L 184.98,43.97 L 184.58,44.71 L 184.12,45.4 L 183.62,46.05 L 183.06,46.65 L 182.45,47.21 L 181.8,47.75 L 181.09,48.25 L 180.32,48.72 L 179.5,49.17 L 178.62,49.59 L 177.69,49.99 L 176.7,50.37 L 175.64,50.73 L 174.53,51.07 L 173.34,51.39 L 172.09,51.69 L 170.77,51.98 L 169.37,52.24 L 167.89,52.49 L 166.33,52.73 L 164.67,52.95 L 162.92,53.15 L 161.07,53.34 L 159.09,53.51 L 156.99,53.67 L 154.74,53.82 L 152.33,53.95 L 149.73,54.07 L 146.9,54.17 L 143.79,54.26 L 140.33,54.33 L 136.41,54.39 L 131.82,54.44 L 126.17,54.47 L 118.39,54.49 L 94,54.5 L 69.61,54.49 L 61.83,54.47 L 56.18,54.44 L 51.59,54.39 L 47.67,54.33 L 44.21,54.26 L 41.1,54.17 L 38.27,54.07 L 35.67,53.95 L 33.26,53.82 L 31.01,53.67 L 28.91,53.51 L 26.93,53.34 L 25.08,53.15 L 23.33,52.95 L 21.67,52.73 L 20.11,52.49 L 18.63,52.24 L 17.23,51.98 L 15.91,51.69 L 14.66,51.39 L 13.47,51.07 L 12.36,50.73 L 11.3,50.37 L 10.31,49.99 L 9.38,49.59 L 8.5,49.17 L 7.68,48.72 L 6.91,48.25 L 6.2,47.75 L 5.55,47.21 L 4.94,46.65 L 4.38,46.05 L 3.88,45.4 L 3.42,44.71 L 3.02,43.97 L 2.66,43.15 L 2.35,42.26 L 2.09,41.27 L 1.88,40.15 L 1.71,38.84 L 1.6,37.33"/></g>
```

Here card, box `188 72`:

```svg
<g><path class="bd bd-progress" fill="var(--panel)" stroke="var(--c-progress)" stroke-width="2" d="M 186.5,36 L 186.41,48 L 186.12,51.82 L 185.65,54.57 L 184.98,56.79 L 184.12,58.66 L 183.06,60.28 L 181.8,61.71 L 180.32,62.98 L 178.62,64.11 L 176.7,65.13 L 174.53,66.03 L 172.09,66.84 L 169.37,67.56 L 166.33,68.2 L 162.92,68.75 L 159.09,69.22 L 154.74,69.61 L 149.73,69.93 L 143.79,70.18 L 136.41,70.36 L 126.17,70.46 L 94,70.5 L 61.83,70.46 L 51.59,70.36 L 44.21,70.18 L 38.27,69.93 L 33.26,69.61 L 28.91,69.22 L 25.08,68.75 L 21.67,68.2 L 18.63,67.56 L 15.91,66.84 L 13.47,66.03 L 11.3,65.13 L 9.38,64.11 L 7.68,62.98 L 6.2,61.71 L 4.94,60.28 L 3.88,58.66 L 3.02,56.79 L 2.35,54.57 L 1.88,51.82 L 1.59,48 L 1.5,36 L 1.59,24 L 1.88,20.18 L 2.35,17.43 L 3.02,15.21 L 3.88,13.34 L 4.94,11.72 L 6.2,10.29 L 7.68,9.02 L 9.38,7.89 L 11.3,6.87 L 13.47,5.97 L 15.91,5.16 L 18.63,4.44 L 21.67,3.8 L 25.08,3.25 L 28.91,2.78 L 33.26,2.39 L 38.27,2.07 L 44.21,1.82 L 51.59,1.64 L 61.83,1.54 L 94,1.5 L 126.17,1.54 L 136.41,1.64 L 143.79,1.82 L 149.73,2.07 L 154.74,2.39 L 159.09,2.78 L 162.92,3.25 L 166.33,3.8 L 169.37,4.44 L 172.09,5.16 L 174.53,5.97 L 176.7,6.87 L 178.62,7.89 L 180.32,9.02 L 181.8,10.29 L 183.06,11.72 L 184.12,13.34 L 184.98,15.21 L 185.65,17.43 L 186.12,20.18 L 186.41,24 L 186.5,36 Z"/><path fill="none" style="stroke:color-mix(in oklab,var(--c-progress) 88%,var(--ink))" stroke-width="7.5" stroke-linecap="round" stroke-linejoin="round" d="M 186.41,48 L 186.29,50.11 L 186.12,51.82 L 185.91,53.28 L 185.65,54.57 L 185.34,55.73 L 184.98,56.79 L 184.58,57.76 L 184.12,58.66 L 183.62,59.49 L 183.06,60.28 L 182.45,61.01 L 181.8,61.71 L 181.09,62.36 L 180.32,62.98 L 179.5,63.56 L 178.62,64.11 L 177.69,64.63 L 176.7,65.13 L 175.64,65.59 L 174.53,66.03 L 173.34,66.45 L 172.09,66.84 L 170.77,67.21 L 169.37,67.56 L 167.89,67.89 L 166.33,68.2 L 164.67,68.48 L 162.92,68.75 L 161.07,68.99 L 159.09,69.22 L 156.99,69.42 L 154.74,69.61 L 152.33,69.78 L 149.73,69.93 L 146.9,70.07 L 143.79,70.18 L 140.33,70.28 L 136.41,70.36 L 131.82,70.42 L 126.17,70.46 L 118.39,70.49 L 94,70.5 L 69.61,70.49 L 61.83,70.46 L 56.18,70.42 L 51.59,70.36 L 47.67,70.28 L 44.21,70.18 L 41.1,70.07 L 38.27,69.93 L 35.67,69.78 L 33.26,69.61 L 31.01,69.42 L 28.91,69.22 L 26.93,68.99 L 25.08,68.75 L 23.33,68.48 L 21.67,68.2 L 20.11,67.89 L 18.63,67.56 L 17.23,67.21 L 15.91,66.84 L 14.66,66.45 L 13.47,66.03 L 12.36,65.59 L 11.3,65.13 L 10.31,64.63 L 9.38,64.11 L 8.5,63.56 L 7.68,62.98 L 6.91,62.36 L 6.2,61.71 L 5.55,61.01 L 4.94,60.28 L 4.38,59.49 L 3.88,58.66 L 3.42,57.76 L 3.02,56.79 L 2.66,55.73 L 2.35,54.57 L 2.09,53.28 L 1.88,51.82 L 1.71,50.11 L 1.59,48"/></g>
```

Begin node, box `188 58`:

```svg
<g><path class="bd bd-project" fill="var(--panel)" stroke="var(--c-project)" stroke-width="2" d="M 195.74,1.5 L 195.75,7.38 L 195.72,15.13 L 195.65,17.61 L 195.52,19.4 L 195.33,20.86 L 195.1,22.11 L 194.81,23.21 L 194.47,24.19 L 194.08,25.09 L 193.63,25.92 L 193.13,26.69 L 192.58,27.4 L 191.97,28.07 L 191.3,28.7 L 190.58,29.29 L 189.79,29.84 L 188.95,30.37 L 188.05,30.87 L 187.09,31.34 L 186.06,31.78 L 184.97,32.2 L 183.81,32.6 L 182.58,32.97 L 181.28,33.33 L 179.9,33.66 L 178.44,33.98 L 176.91,34.28 L 175.28,34.56 L 173.56,34.82 L 171.74,35.06 L 169.82,35.28 L 167.77,35.49 L 165.6,35.69 L 163.29,35.86 L 160.82,36.02 L 158.17,36.17 L 155.3,36.3 L 152.19,36.41 L 148.77,36.51 L 144.96,36.59 L 140.65,36.66 L 135.6,36.71 L 129.39,36.75 L 120.83,36.77 L 94,36.78 L 67.17,36.77 L 58.61,36.75 L 52.4,36.71 L 47.35,36.66 L 43.04,36.59 L 39.23,36.51 L 35.81,36.41 L 32.7,36.3 L 29.83,36.17 L 27.18,36.02 L 24.71,35.86 L 22.4,35.69 L 20.23,35.49 L 18.18,35.28 L 16.26,35.06 L 14.44,34.82 L 12.72,34.56 L 11.09,34.28 L 9.56,33.98 L 8.1,33.66 L 6.72,33.33 L 5.42,32.97 L 4.19,32.6 L 3.03,32.2 L 1.94,31.78 L 0.91,31.34 L -0.05,30.87 L -0.95,30.37 L -1.79,29.84 L -2.58,29.29 L -3.3,28.7 L -3.97,28.07 L -4.58,27.4 L -5.13,26.69 L -5.63,25.92 L -6.08,25.09 L -6.47,24.19 L -6.81,23.21 L -7.1,22.11 L -7.33,20.86 L -7.52,19.4 L -7.65,17.61 L -7.72,15.13 L -7.75,7.38 L -7.74,1.5 Z"/><path fill="none" style="stroke:color-mix(in oklab,var(--c-project) 88%,var(--ink))" stroke-width="7.5" stroke-linecap="round" stroke-linejoin="round" d="M 193.86,25.52 L 193.63,25.92 L 193.13,26.69 L 192.58,27.4 L 191.97,28.07 L 191.3,28.7 L 190.58,29.29 L 189.79,29.84 L 188.95,30.37 L 188.05,30.87 L 187.09,31.34 L 186.06,31.78 L 184.97,32.2 L 183.81,32.6 L 182.58,32.97 L 181.28,33.33 L 179.9,33.66 L 178.44,33.98 L 176.91,34.28 L 175.28,34.56 L 173.56,34.82 L 171.74,35.06 L 169.82,35.28 L 167.77,35.49 L 165.6,35.69 L 163.29,35.86 L 160.82,36.02 L 158.17,36.17 L 155.3,36.3 L 152.19,36.41 L 148.77,36.51 L 144.96,36.59 L 140.65,36.66 L 135.6,36.71 L 129.39,36.75 L 120.83,36.77 L 94,36.78 L 67.17,36.77 L 58.61,36.75 L 52.4,36.71 L 47.35,36.66 L 43.04,36.59 L 39.23,36.51 L 35.81,36.41 L 32.7,36.3 L 29.83,36.17 L 27.18,36.02 L 24.71,35.86 L 22.4,35.69 L 20.23,35.49 L 18.18,35.28 L 16.26,35.06 L 14.44,34.82 L 12.72,34.56 L 11.09,34.28 L 9.56,33.98 L 8.1,33.66 L 6.72,33.33 L 5.42,32.97 L 4.19,32.6 L 3.03,32.2 L 1.94,31.78 L 0.91,31.34 L -0.05,30.87 L -0.95,30.37 L -1.79,29.84 L -2.58,29.29 L -3.3,28.7 L -3.97,28.07 L -4.58,27.4 L -5.13,26.69 L -5.63,25.92 L -5.86,25.52"/></g>
```

End node, box `188 58`:

```svg
<g><path class="bd bd-project" fill="var(--panel)" stroke="var(--c-project)" stroke-width="2" d="M -7.74,56.5 L -7.72,54.71 L -7.65,52.34 L -7.52,50.62 L -7.33,49.22 L -7.1,48.03 L -6.81,46.98 L -6.47,46.03 L -6.08,45.17 L -5.63,44.38 L -5.13,43.64 L -4.58,42.96 L -3.97,42.32 L -3.3,41.72 L -2.58,41.15 L -1.79,40.62 L -0.95,40.12 L -0.05,39.64 L 0.91,39.19 L 1.94,38.77 L 3.03,38.36 L 4.19,37.98 L 5.42,37.62 L 6.72,37.28 L 8.1,36.96 L 9.56,36.66 L 11.09,36.38 L 12.72,36.11 L 14.44,35.86 L 16.26,35.63 L 18.18,35.41 L 20.23,35.21 L 22.4,35.03 L 24.71,34.86 L 27.18,34.7 L 29.83,34.57 L 32.7,34.44 L 35.81,34.33 L 39.23,34.24 L 43.04,34.16 L 47.35,34.09 L 52.4,34.04 L 58.61,34.01 L 67.17,33.99 L 94,33.98 L 120.83,33.99 L 129.39,34.01 L 135.6,34.04 L 140.65,34.09 L 144.96,34.16 L 148.77,34.24 L 152.19,34.33 L 155.3,34.44 L 158.17,34.57 L 160.82,34.7 L 163.29,34.86 L 165.6,35.03 L 167.77,35.21 L 169.82,35.41 L 171.74,35.63 L 173.56,35.86 L 175.28,36.11 L 176.91,36.38 L 178.44,36.66 L 179.9,36.96 L 181.28,37.28 L 182.58,37.62 L 183.81,37.98 L 184.97,38.36 L 186.06,38.77 L 187.09,39.19 L 188.05,39.64 L 188.95,40.12 L 189.79,40.62 L 190.58,41.15 L 191.3,41.72 L 191.97,42.32 L 192.58,42.96 L 193.13,43.64 L 193.63,44.38 L 194.08,45.17 L 194.47,46.03 L 194.81,46.98 L 195.1,48.03 L 195.33,49.22 L 195.52,50.62 L 195.65,52.34 L 195.72,54.71 L 195.74,56.5 Z"/><path fill="none" style="stroke:color-mix(in oklab,var(--c-project) 88%,var(--ink))" stroke-width="7.5" stroke-linecap="round" stroke-linejoin="round" d="M -2.34,40.99 L -1.79,40.62 L -0.95,40.12 L -0.05,39.64 L 0.91,39.19 L 1.94,38.77 L 3.03,38.36 L 4.19,37.98 L 5.42,37.62 L 6.72,37.28 L 8.1,36.96 L 9.56,36.66 L 11.09,36.38 L 12.72,36.11 L 14.44,35.86 L 16.26,35.63 L 18.18,35.41 L 20.23,35.21 L 22.4,35.03 L 24.71,34.86 L 27.18,34.7 L 29.83,34.57 L 32.7,34.44 L 35.81,34.33 L 39.23,34.24 L 43.04,34.16 L 47.35,34.09 L 52.4,34.04 L 58.61,34.01 L 67.17,33.99 L 94,33.98 L 120.83,33.99 L 129.39,34.01 L 135.6,34.04 L 140.65,34.09 L 144.96,34.16 L 148.77,34.24 L 152.19,34.33 L 155.3,34.44 L 158.17,34.57 L 160.82,34.7 L 163.29,34.86 L 165.6,35.03 L 167.77,35.21 L 169.82,35.41 L 171.74,35.63 L 173.56,35.86 L 175.28,36.11 L 176.91,36.38 L 178.44,36.66 L 179.9,36.96 L 181.28,37.28 L 182.58,37.62 L 183.81,37.98 L 184.97,38.36 L 186.06,38.77 L 187.09,39.19 L 188.05,39.64 L 188.95,40.12 L 189.79,40.62 L 190.34,40.99"/></g>
```

Folded project, box `188 94`:

```svg
<g transform="translate(0 -10)"><path class="bd bd-project" fill="var(--panel)" stroke="var(--c-project)" stroke-width="2" d="M -7.74,56.5 L -7.72,54.71 L -7.65,52.34 L -7.52,50.62 L -7.33,49.22 L -7.1,48.03 L -6.81,46.98 L -6.47,46.03 L -6.08,45.17 L -5.63,44.38 L -5.13,43.64 L -4.58,42.96 L -3.97,42.32 L -3.3,41.72 L -2.58,41.15 L -1.79,40.62 L -0.95,40.12 L -0.05,39.64 L 0.91,39.19 L 1.94,38.77 L 3.03,38.36 L 4.19,37.98 L 5.42,37.62 L 6.72,37.28 L 8.1,36.96 L 9.56,36.66 L 11.09,36.38 L 12.72,36.11 L 14.44,35.86 L 16.26,35.63 L 18.18,35.41 L 20.23,35.21 L 22.4,35.03 L 24.71,34.86 L 27.18,34.7 L 29.83,34.57 L 32.7,34.44 L 35.81,34.33 L 39.23,34.24 L 43.04,34.16 L 47.35,34.09 L 52.4,34.04 L 58.61,34.01 L 67.17,33.99 L 94,33.98 L 120.83,33.99 L 129.39,34.01 L 135.6,34.04 L 140.65,34.09 L 144.96,34.16 L 148.77,34.24 L 152.19,34.33 L 155.3,34.44 L 158.17,34.57 L 160.82,34.7 L 163.29,34.86 L 165.6,35.03 L 167.77,35.21 L 169.82,35.41 L 171.74,35.63 L 173.56,35.86 L 175.28,36.11 L 176.91,36.38 L 178.44,36.66 L 179.9,36.96 L 181.28,37.28 L 182.58,37.62 L 183.81,37.98 L 184.97,38.36 L 186.06,38.77 L 187.09,39.19 L 188.05,39.64 L 188.95,40.12 L 189.79,40.62 L 190.58,41.15 L 191.3,41.72 L 191.97,42.32 L 192.58,42.96 L 193.13,43.64 L 193.63,44.38 L 194.08,45.17 L 194.47,46.03 L 194.81,46.98 L 195.1,48.03 L 195.33,49.22 L 195.52,50.62 L 195.65,52.34 L 195.72,54.71 L 195.74,56.5 Z"/><path fill="none" style="stroke:color-mix(in oklab,var(--c-project) 88%,var(--ink))" stroke-width="7.5" stroke-linecap="round" stroke-linejoin="round" d="M -2.34,40.99 L -1.79,40.62 L -0.95,40.12 L -0.05,39.64 L 0.91,39.19 L 1.94,38.77 L 3.03,38.36 L 4.19,37.98 L 5.42,37.62 L 6.72,37.28 L 8.1,36.96 L 9.56,36.66 L 11.09,36.38 L 12.72,36.11 L 14.44,35.86 L 16.26,35.63 L 18.18,35.41 L 20.23,35.21 L 22.4,35.03 L 24.71,34.86 L 27.18,34.7 L 29.83,34.57 L 32.7,34.44 L 35.81,34.33 L 39.23,34.24 L 43.04,34.16 L 47.35,34.09 L 52.4,34.04 L 58.61,34.01 L 67.17,33.99 L 94,33.98 L 120.83,33.99 L 129.39,34.01 L 135.6,34.04 L 140.65,34.09 L 144.96,34.16 L 148.77,34.24 L 152.19,34.33 L 155.3,34.44 L 158.17,34.57 L 160.82,34.7 L 163.29,34.86 L 165.6,35.03 L 167.77,35.21 L 169.82,35.41 L 171.74,35.63 L 173.56,35.86 L 175.28,36.11 L 176.91,36.38 L 178.44,36.66 L 179.9,36.96 L 181.28,37.28 L 182.58,37.62 L 183.81,37.98 L 184.97,38.36 L 186.06,38.77 L 187.09,39.19 L 188.05,39.64 L 188.95,40.12 L 189.79,40.62 L 190.34,40.99"/></g><g transform="translate(0 36)"><path class="bd bd-project" fill="var(--panel)" stroke="var(--c-project)" stroke-width="2" d="M 195.74,1.5 L 195.75,7.38 L 195.72,15.13 L 195.65,17.61 L 195.52,19.4 L 195.33,20.86 L 195.1,22.11 L 194.81,23.21 L 194.47,24.19 L 194.08,25.09 L 193.63,25.92 L 193.13,26.69 L 192.58,27.4 L 191.97,28.07 L 191.3,28.7 L 190.58,29.29 L 189.79,29.84 L 188.95,30.37 L 188.05,30.87 L 187.09,31.34 L 186.06,31.78 L 184.97,32.2 L 183.81,32.6 L 182.58,32.97 L 181.28,33.33 L 179.9,33.66 L 178.44,33.98 L 176.91,34.28 L 175.28,34.56 L 173.56,34.82 L 171.74,35.06 L 169.82,35.28 L 167.77,35.49 L 165.6,35.69 L 163.29,35.86 L 160.82,36.02 L 158.17,36.17 L 155.3,36.3 L 152.19,36.41 L 148.77,36.51 L 144.96,36.59 L 140.65,36.66 L 135.6,36.71 L 129.39,36.75 L 120.83,36.77 L 94,36.78 L 67.17,36.77 L 58.61,36.75 L 52.4,36.71 L 47.35,36.66 L 43.04,36.59 L 39.23,36.51 L 35.81,36.41 L 32.7,36.3 L 29.83,36.17 L 27.18,36.02 L 24.71,35.86 L 22.4,35.69 L 20.23,35.49 L 18.18,35.28 L 16.26,35.06 L 14.44,34.82 L 12.72,34.56 L 11.09,34.28 L 9.56,33.98 L 8.1,33.66 L 6.72,33.33 L 5.42,32.97 L 4.19,32.6 L 3.03,32.2 L 1.94,31.78 L 0.91,31.34 L -0.05,30.87 L -0.95,30.37 L -1.79,29.84 L -2.58,29.29 L -3.3,28.7 L -3.97,28.07 L -4.58,27.4 L -5.13,26.69 L -5.63,25.92 L -6.08,25.09 L -6.47,24.19 L -6.81,23.21 L -7.1,22.11 L -7.33,20.86 L -7.52,19.4 L -7.65,17.61 L -7.72,15.13 L -7.75,7.38 L -7.74,1.5 Z"/><path fill="none" style="stroke:color-mix(in oklab,var(--c-project) 88%,var(--ink))" stroke-width="7.5" stroke-linecap="round" stroke-linejoin="round" d="M 193.86,25.52 L 193.63,25.92 L 193.13,26.69 L 192.58,27.4 L 191.97,28.07 L 191.3,28.7 L 190.58,29.29 L 189.79,29.84 L 188.95,30.37 L 188.05,30.87 L 187.09,31.34 L 186.06,31.78 L 184.97,32.2 L 183.81,32.6 L 182.58,32.97 L 181.28,33.33 L 179.9,33.66 L 178.44,33.98 L 176.91,34.28 L 175.28,34.56 L 173.56,34.82 L 171.74,35.06 L 169.82,35.28 L 167.77,35.49 L 165.6,35.69 L 163.29,35.86 L 160.82,36.02 L 158.17,36.17 L 155.3,36.3 L 152.19,36.41 L 148.77,36.51 L 144.96,36.59 L 140.65,36.66 L 135.6,36.71 L 129.39,36.75 L 120.83,36.77 L 94,36.78 L 67.17,36.77 L 58.61,36.75 L 52.4,36.71 L 47.35,36.66 L 43.04,36.59 L 39.23,36.51 L 35.81,36.41 L 32.7,36.3 L 29.83,36.17 L 27.18,36.02 L 24.71,35.86 L 22.4,35.69 L 20.23,35.49 L 18.18,35.28 L 16.26,35.06 L 14.44,34.82 L 12.72,34.56 L 11.09,34.28 L 9.56,33.98 L 8.1,33.66 L 6.72,33.33 L 5.42,32.97 L 4.19,32.6 L 3.03,32.2 L 1.94,31.78 L 0.91,31.34 L -0.05,30.87 L -0.95,30.37 L -1.79,29.84 L -2.58,29.29 L -3.3,28.7 L -3.97,28.07 L -4.58,27.4 L -5.13,26.69 L -5.63,25.92 L -5.86,25.52"/></g>
```

Start node, box `188 58`:

```svg
<g><path class="bd bd-workflow" fill="var(--panel)" stroke="var(--c-workflow)" stroke-width="2" d="M 38.96,7.31 H 149.04 A 0 0 0 0 1 149.04,7.31 V 27.31 A 55.04 23.38 0 0 1 38.96,27.31 V 7.31 A 0 0 0 0 1 38.96,7.31 Z"/><path fill="none" style="stroke:color-mix(in oklab,var(--c-workflow) 88%,var(--ink))" stroke-width="7.5" stroke-linecap="round" stroke-linejoin="round" d="M 39.11,29 A 55.04 23.38 0 0 0 148.89,29"/></g>
```

Finish node, box `188 52`:

```svg
<g><g transform="translate(44 0)"><path class="bd bd-workflow" fill="var(--panel)" stroke="var(--c-workflow)" stroke-width="2" d="M 1.5,38.25 V 38.25 A 48.5 24.5 0 0 1 98.5,38.25 Z"/><path fill="none" style="stroke:color-mix(in oklab,var(--c-workflow) 88%,var(--ink))" stroke-width="7.5" stroke-linecap="round" stroke-linejoin="round" d="M 13.85,21.92 A 48.5 24.5 0 0 1 86.15,21.92"/></g></g>
```

Folded workflow, box `188 75`:

```svg
<g transform="translate(0 -10)"><g transform="translate(44 0)"><path class="bd bd-workflow" fill="var(--panel)" stroke="var(--c-workflow)" stroke-width="2" d="M 1.5,38.25 V 38.25 A 48.5 24.5 0 0 1 98.5,38.25 Z"/><path fill="none" style="stroke:color-mix(in oklab,var(--c-workflow) 88%,var(--ink))" stroke-width="7.5" stroke-linecap="round" stroke-linejoin="round" d="M 13.85,21.92 A 48.5 24.5 0 0 1 86.15,21.92"/></g></g><g transform="translate(0 17)"><path class="bd bd-workflow" fill="var(--panel)" stroke="var(--c-workflow)" stroke-width="2" d="M 38.96,7.31 H 149.04 A 0 0 0 0 1 149.04,7.31 V 27.31 A 55.04 23.38 0 0 1 38.96,27.31 V 7.31 A 0 0 0 0 1 38.96,7.31 Z"/><path fill="none" style="stroke:color-mix(in oklab,var(--c-workflow) 88%,var(--ink))" stroke-width="7.5" stroke-linecap="round" stroke-linejoin="round" d="M 39.11,29 A 55.04 23.38 0 0 0 148.89,29"/></g>
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
<path d="M 6.32,0 L 6.32,3.27 L 6.31,3.88 L 6.29,4.29 L 6.26,4.61 L 6.22,4.86 L 6.18,5.08 L 6.12,5.26 L 6.06,5.42 L 5.98,5.57 L 5.9,5.69 L 5.8,5.8 L 5.69,5.9 L 5.57,5.98 L 5.42,6.06 L 5.26,6.12 L 5.08,6.18 L 4.86,6.22 L 4.61,6.26 L 4.29,6.29 L 3.88,6.31 L 3.27,6.32 L 0,6.32 L -3.27,6.32 L -3.88,6.31 L -4.29,6.29 L -4.61,6.26 L -4.86,6.22 L -5.08,6.18 L -5.26,6.12 L -5.42,6.06 L -5.57,5.98 L -5.69,5.9 L -5.8,5.8 L -5.9,5.69 L -5.98,5.57 L -6.06,5.42 L -6.12,5.26 L -6.18,5.08 L -6.22,4.86 L -6.26,4.61 L -6.29,4.29 L -6.31,3.88 L -6.32,3.27 L -6.32,0 L -6.32,-3.27 L -6.31,-3.88 L -6.29,-4.29 L -6.26,-4.61 L -6.22,-4.86 L -6.18,-5.08 L -6.12,-5.26 L -6.06,-5.42 L -5.98,-5.57 L -5.9,-5.69 L -5.8,-5.8 L -5.69,-5.9 L -5.57,-5.98 L -5.42,-6.06 L -5.26,-6.12 L -5.08,-6.18 L -4.86,-6.22 L -4.61,-6.26 L -4.29,-6.29 L -3.88,-6.31 L -3.27,-6.32 L 0,-6.32 L 3.27,-6.32 L 3.88,-6.31 L 4.29,-6.29 L 4.61,-6.26 L 4.86,-6.22 L 5.08,-6.18 L 5.26,-6.12 L 5.42,-6.06 L 5.57,-5.98 L 5.69,-5.9 L 5.8,-5.8 L 5.9,-5.69 L 5.98,-5.57 L 6.06,-5.42 L 6.12,-5.26 L 6.18,-5.08 L 6.22,-4.86 L 6.26,-4.61 L 6.29,-4.29 L 6.31,-3.88 L 6.32,-3.27 L 6.32,0 Z" fill="var(--c-done)"/>
```

Glyph cancelled, box `centred on 0 0`:

```svg
<circle cx="0" cy="0" r="5.4624999999999995" fill="none" stroke="var(--c-cancel)" stroke-width="1.5" stroke-dasharray="2.4 2.2"/>
```

Flag on a task, box `188 56`:

```svg
<g transform="translate(0 0)"><path fill="none" stroke="var(--ink)" stroke-width="1.2" d="M 194.1,28 L 194,39.86 L 193.69,43.63 L 193.18,46.35 L 192.46,48.54 L 191.53,50.39 L 190.38,52 L 189.01,53.41 L 187.41,54.66 L 185.58,55.78 L 183.49,56.79 L 181.14,57.69 L 178.51,58.49 L 175.56,59.2 L 172.27,59.82 L 168.59,60.37 L 164.44,60.83 L 159.73,61.22 L 154.31,61.54 L 147.88,61.79 L 139.89,61.96 L 128.81,62.07 L 94,62.1 L 59.19,62.07 L 48.11,61.96 L 40.12,61.79 L 33.69,61.54 L 28.27,61.22 L 23.56,60.83 L 19.41,60.37 L 15.73,59.82 L 12.44,59.2 L 9.49,58.49 L 6.86,57.69 L 4.51,56.79 L 2.42,55.78 L 0.59,54.66 L -1.01,53.41 L -2.38,52 L -3.53,50.39 L -4.46,48.54 L -5.18,46.35 L -5.69,43.63 L -6,39.86 L -6.1,28 L -6,16.14 L -5.69,12.37 L -5.18,9.65 L -4.46,7.46 L -3.53,5.61 L -2.38,4 L -1.01,2.59 L 0.59,1.34 L 2.42,0.22 L 4.51,-0.79 L 6.86,-1.69 L 9.49,-2.49 L 12.44,-3.2 L 15.73,-3.82 L 19.41,-4.37 L 23.56,-4.83 L 28.27,-5.22 L 33.69,-5.54 L 40.12,-5.79 L 48.11,-5.96 L 59.19,-6.07 L 94,-6.1 L 128.81,-6.07 L 139.89,-5.96 L 147.88,-5.79 L 154.31,-5.54 L 159.73,-5.22 L 164.44,-4.83 L 168.59,-4.37 L 172.27,-3.82 L 175.56,-3.2 L 178.51,-2.49 L 181.14,-1.69 L 183.49,-0.79 L 185.58,0.22 L 187.41,1.34 L 189.01,2.59 L 190.38,4 L 191.53,5.61 L 192.46,7.46 L 193.18,9.65 L 193.69,12.37 L 194,16.14 L 194.1,28 Z"/><path fill="none" stroke="var(--ink)" stroke-width="1" d="M 200.1,28 L 199.99,41.95 L 199.67,46.38 L 199.12,49.58 L 198.36,52.16 L 197.37,54.33 L 196.16,56.22 L 194.7,57.88 L 193.01,59.36 L 191.07,60.67 L 188.86,61.85 L 186.37,62.91 L 183.57,63.85 L 180.45,64.69 L 176.96,65.42 L 173.06,66.06 L 168.66,66.61 L 163.67,67.07 L 157.92,67.44 L 151.11,67.73 L 142.64,67.94 L 130.9,68.06 L 94,68.1 L 57.1,68.06 L 45.36,67.94 L 36.89,67.73 L 30.08,67.44 L 24.33,67.07 L 19.34,66.61 L 14.94,66.06 L 11.04,65.42 L 7.55,64.69 L 4.43,63.85 L 1.63,62.91 L -0.86,61.85 L -3.07,60.67 L -5.01,59.36 L -6.7,57.88 L -8.16,56.22 L -9.37,54.33 L -10.36,52.16 L -11.12,49.58 L -11.67,46.38 L -11.99,41.95 L -12.1,28 L -11.99,14.05 L -11.67,9.62 L -11.12,6.42 L -10.36,3.84 L -9.37,1.67 L -8.16,-0.22 L -6.7,-1.88 L -5.01,-3.36 L -3.07,-4.67 L -0.86,-5.85 L 1.63,-6.91 L 4.43,-7.85 L 7.55,-8.69 L 11.04,-9.42 L 14.94,-10.06 L 19.34,-10.61 L 24.33,-11.07 L 30.08,-11.44 L 36.89,-11.73 L 45.36,-11.94 L 57.1,-12.06 L 94,-12.1 L 130.9,-12.06 L 142.64,-11.94 L 151.11,-11.73 L 157.92,-11.44 L 163.67,-11.07 L 168.66,-10.61 L 173.06,-10.06 L 176.96,-9.42 L 180.45,-8.69 L 183.57,-7.85 L 186.37,-6.91 L 188.86,-5.85 L 191.07,-4.67 L 193.01,-3.36 L 194.7,-1.88 L 196.16,-0.22 L 197.37,1.67 L 198.36,3.84 L 199.12,6.42 L 199.67,9.62 L 199.99,14.05 L 200.1,28 Z"/></g>
```

Flag on a begin node, box `188 58`:

```svg
<path fill="none" stroke="var(--ink)" stroke-width="1.2" d="M 203.21,-6.1 L 203.24,-5.49 L 203.32,-2.38 L 203.35,7.38 L 203.32,17.14 L 203.24,20.25 L 203.1,22.51 L 202.9,24.34 L 202.65,25.91 L 202.34,27.3 L 201.98,28.54 L 201.56,29.67 L 201.08,30.71 L 200.54,31.68 L 199.94,32.58 L 199.28,33.42 L 198.57,34.21 L 197.79,34.95 L 196.95,35.65 L 196.04,36.31 L 195.08,36.94 L 194.04,37.53 L 192.94,38.09 L 191.76,38.62 L 190.52,39.12 L 189.19,39.59 L 187.8,40.04 L 186.32,40.46 L 184.75,40.86 L 183.1,41.23 L 181.35,41.58 L 179.5,41.91 L 177.55,42.21 L 175.48,42.5 L 173.28,42.76 L 170.95,43 L 168.47,43.23 L 165.81,43.43 L 162.96,43.61 L 159.88,43.77 L 156.53,43.92 L 152.86,44.04 L 148.77,44.14 L 144.13,44.23 L 138.71,44.3 L 132.03,44.34 L 122.83,44.37 L 94,44.38 L 65.17,44.37 L 55.97,44.34 L 49.29,44.3 L 43.87,44.23 L 39.23,44.14 L 35.14,44.04 L 31.47,43.92 L 28.12,43.77 L 25.04,43.61 L 22.19,43.43 L 19.53,43.23 L 17.05,43 L 14.72,42.76 L 12.52,42.5 L 10.45,42.21 L 8.5,41.91 L 6.65,41.58 L 4.9,41.23 L 3.25,40.86 L 1.68,40.46 L 0.2,40.04 L -1.19,39.59 L -2.52,39.12 L -3.76,38.62 L -4.94,38.09 L -6.04,37.53 L -7.08,36.94 L -8.04,36.31 L -8.95,35.65 L -9.79,34.95 L -10.57,34.21 L -11.28,33.42 L -11.94,32.58 L -12.54,31.68 L -13.08,30.71 L -13.56,29.67 L -13.98,28.54 L -14.34,27.3 L -14.65,25.91 L -14.9,24.34 L -15.1,22.51 L -15.24,20.25 L -15.32,17.14 L -15.35,7.38 L -15.32,-2.38 L -15.24,-5.49 L -15.21,-6.1 Z"/><path fill="none" stroke="var(--ink)" stroke-width="1" d="M 208.91,-12.1 L 209.09,-10.2 L 209.23,-7.58 L 209.32,-3.96 L 209.35,7.38 L 209.32,18.72 L 209.23,22.34 L 209.09,24.96 L 208.88,27.09 L 208.61,28.92 L 208.29,30.53 L 207.9,31.97 L 207.46,33.29 L 206.95,34.5 L 206.38,35.62 L 205.75,36.66 L 205.06,37.64 L 204.31,38.56 L 203.48,39.42 L 202.6,40.23 L 201.64,41 L 200.62,41.73 L 199.53,42.42 L 198.36,43.07 L 197.13,43.68 L 195.81,44.26 L 194.42,44.81 L 192.94,45.33 L 191.38,45.82 L 189.73,46.28 L 187.99,46.72 L 186.14,47.13 L 184.19,47.51 L 182.13,47.86 L 179.95,48.19 L 177.63,48.5 L 175.17,48.78 L 172.55,49.04 L 169.75,49.27 L 166.74,49.49 L 163.49,49.67 L 159.96,49.84 L 156.09,49.98 L 151.78,50.11 L 146.88,50.2 L 141.16,50.28 L 134.12,50.34 L 124.41,50.37 L 94,50.38 L 63.59,50.37 L 53.88,50.34 L 46.84,50.28 L 41.12,50.2 L 36.22,50.11 L 31.91,49.98 L 28.04,49.84 L 24.51,49.67 L 21.26,49.49 L 18.25,49.27 L 15.45,49.04 L 12.83,48.78 L 10.37,48.5 L 8.05,48.19 L 5.87,47.86 L 3.81,47.51 L 1.86,47.13 L 0.01,46.72 L -1.73,46.28 L -3.38,45.82 L -4.94,45.33 L -6.42,44.81 L -7.81,44.26 L -9.13,43.68 L -10.36,43.07 L -11.53,42.42 L -12.62,41.73 L -13.64,41 L -14.6,40.23 L -15.48,39.42 L -16.31,38.56 L -17.06,37.64 L -17.75,36.66 L -18.38,35.62 L -18.95,34.5 L -19.46,33.29 L -19.9,31.97 L -20.29,30.53 L -20.61,28.92 L -20.88,27.09 L -21.09,24.96 L -21.23,22.34 L -21.32,18.72 L -21.35,7.38 L -21.32,-3.96 L -21.23,-7.58 L -21.09,-10.2 L -20.91,-12.1 Z"/>
```

Flag on a start node, box `188 58`:

```svg
<path fill="none" stroke="var(--ink)" stroke-width="1.2" d="M 31.36,-0.29 H 156.64 A 0 0 0 0 1 156.64,-0.29 V 27.31 A 62.64 30.98 0 0 1 31.36,27.31 V -0.29 A 0 0 0 0 1 31.36,-0.29 Z"/><path fill="none" stroke="var(--ink)" stroke-width="1" d="M 25.36,-6.29 H 162.64 A 0 0 0 0 1 162.64,-6.29 V 27.31 A 68.64 36.98 0 0 1 25.36,27.31 V -6.29 A 0 0 0 0 1 25.36,-6.29 Z"/>
```

Here mark, box `188 72`:

```svg
<path d="M -2.64,34.5 L -22.13,23.25 Q -24.73,21.75 -24.73,24.75 Q -19.23,36 -24.73,47.25 Q -24.73,50.25 -22.13,48.75 L -2.64,37.5 Q -0.05,36 -2.64,34.5 Z" fill="var(--ink)"/><path d="M 190.64,34.5 L 210.13,23.25 Q 212.73,21.75 212.73,24.75 Q 207.23,36 212.73,47.25 Q 212.73,50.25 210.13,48.75 L 190.64,37.5 Q 188.05,36 190.64,34.5 Z" fill="var(--ink)"/>
```

Junction, box `centred on 0 0`:

```svg
<rect x="-6.5" y="-6.5" width="13" height="13" rx="3" fill="var(--ground)" stroke="var(--line)" stroke-width="1.6"/><rect x="-3.2" y="-3.2" width="6.4" height="6.4" rx="1.5" fill="var(--c-junction)"/>
```

Drop indicator, box `centred on 0 0`:

```svg
<g fill="none" stroke="var(--cursor)" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M -13,-6 L -7,0 L -13,6"/><path d="M 13,-6 L 7,0 L 13,6"/></g>
```

Tracks: riser 3, laterals 2.3, line ends round, joins round.
The flag is painted beneath the card.

| token | light | dark |
| --- | --- | --- |
| `--ground` | `#dae8ef` | `#0e1a20` |
| `--panel` | `#eef4f8` | `#16242b` |
| `--ink` | `#151f26` | `#e5eef2` |
| `--line` | `#5d7a88` | `#85a0ac` |
| `--muted` | `#6c8593` | `#7d93a0` |
| `--grid` | `rgba(21,31,38,.10)` | `rgba(229,238,242,.11)` |
| `--c-todo` | `#008fa8` | `#0ec7de` |
| `--c-progress` | `#d9bd1c` | `#f6d732` |
| `--c-done` | `#3a7bcb` | `#76b4ff` |
| `--c-cancel` | `#abbac2` | `#4a585e` |
| `--c-project` | `#00734b` | `#2eb184` |
| `--c-project-tint` | `#d6f4e6` | `#173226` |
| `--c-workflow` | `#0b267d` | `#5477c7` |
| `--c-workflow-tint` | `#b4cbf9` | `#303f60` |
| `--c-todo-tint` | `#bfeef7` | `#0e363d` |
| `--c-progress-tint` | `#f2e9bb` | `#3c3615` |
| `--c-done-tint` | `#cfe7ff` | `#203147` |
| `--c-cancel-tint` | `#d8e3ea` | `#2b3134` |
| `--c-junction` | `#1b3358` | `#a9ccd3` |
| `--cursor` | `#e2551f` | `#ff6a33` |
| `--f-disp` | `"Familjen Grotesk",sans-serif` | `"Familjen Grotesk",sans-serif` |
| `--f-ui` | `"Familjen Grotesk",sans-serif` | `"Familjen Grotesk",sans-serif` |
| `--f-mono` | `"Spline Sans Mono",monospace` | `"Spline Sans Mono",monospace` |

<!-- masters:suuronen:end -->

## 18. Settled by eye

The pointers' side, concave base, corner radius, and stand-off (2026-09-17, D44); the frames on the begin and start nodes as offsets of the piece and the cup (D44). The keel, the sawn project card at 110 %, the turned workflow figure, the fold lift of 10, and the palette, from the style's development. Open: the dark palette, derived rather than tuned, and adjacent flagged pieces (in-flight ideas).
