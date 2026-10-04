<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# Googie

The application's default style, specified to the [style contract](style-contract.md) and in its checklist's order. The [design page](styles.html?v=googie) draws it in both themes; where this document and the page disagree on how a mark looks, the page governs and this document is corrected (D39). Positions are the [layout engine](layout-engine.md)'s.

## 1. Character

A mid-century retrofuturist systems diagram: the outline of every card is a band of variable weight, heavy on one side and thin on another, made as the gap between two fills; the shapes are splayed, so that none but the plain task has two parallel straight edges; and a workflow's boundaries lean at a slight, fixed angle. For a design brief or an image search, the terms are mid-century retrofuturism, Googie diagram, Atomic Age infographic, Jet Age schematic, and 1950s technical illustration. The two marks people set are in ink: a ten-ray starburst beside a here card, and an atom at the right end of a flagged card.

Three rules govern every mark (D7). No outline is a constant-width stroke; a line that carries character is a filled ribbon whose weight pools along one side, and the two-fill outline is that ribbon. The workflow boundaries are rotated, the start ellipse by −3 degrees and the finish keystone by +2, the same on every card. And shapes are splayed: no silhouette has two parallel straight edges, the screen excepted.

## 2. The ground

The canvas carries a dot grid: one dot at every 40-pixel lattice point, a filled circle in `--grid` reaching full colour at radius 1 and transparent by 1.4. Reproduce it as a tiled texture, or by drawing a circle of radius about 1.2 at every `(40i, 40j)` within the visible rectangle. The grid belongs to the viewport, not the map world, so it neither pans nor zooms.

## 3. Tokens

The light palette is named azure and the dark navy.

| token | role | light (azure) | dark (navy) |
| --- | --- | --- | --- |
| `--ground` | canvas | `#d3e6ef` | `#0f2334` |
| `--panel` | card body (task, start, finish) | `#f8f3e8` | `#1a3a54` |
| `--ink` | text, the marks people set | `#173242` | `#e8f1f6` |
| `--line` | tracks, dots, diamonds | `#365b6c` | `#6fb6c9` |
| `--muted` | tags, note glyph | `#5f7d8b` | `#93b3c2` |
| `--grid` | ground dots | `#173242` at 10 % | `#6fb6c9` at 13 % |
| `--c-todo` | to do | `#d9a53a` | `#f0bd55` |
| `--c-progress` | in progress | `#d75f2e` | `#f27a44` |
| `--c-done` | done | `#7d54a6` | `#bd93e6` |
| `--c-cancel` | cancelled | `#8aa0ab` | `#7590a0` |
| `--c-project` | begin and end hulls | `#1f8f8a` | `#37c2ba` |
| `--c-project-tint` | begin and end body | `#cbe6e4` | `#356e69` |
| `--c-workflow` | start ellipse and finish keystone (the line colour) | `#365b6c` | `#6fb6c9` |
| `--cursor` | HERE pill, drop indicator | `#d75f2e` | `#f27a44` |
| `--burst-a` | atmosphere burst (optional) | `#1f8f8a` | `#37c2ba` |
| `--burst-b` | atmosphere burst, variant (optional) | `#d9a53a` | `#f0bd55` |

Three hues carry meaning: the line colour marks a workflow's boundaries, which belong to its line; teal marks a project's; and violet marks a task that is done. `--c-workflow` shares the line colour deliberately.

## 4. Faces

| role | face |
| --- | --- |
| display (card labels) | Boogaloo |
| interface (chrome) | League Spartan, weight 600 for tags in the drawing |
| data (tags, HERE pill, numbers) | Spline Sans Mono 400 |

## 5. The silhouettes

Six silhouettes: four axis-aligned shapes for tasks and project boundaries, and two tilted shapes for a workflow's boundaries. Each is an outer path in the node's colour and an inner copy in the body colour, produced by the transform `innerT` (5.7); the band between them is the outline.

The margin `m = 1.5` is common to all six: every silhouette lies 1.5 inside the card box. Define `x0 = m`, `x1 = w − m`, `y0 = m`, `y1 = h − m`, and the centres `cx = (x0 + x1) / 2`, `cy = (y0 + y1) / 2`.

### 5.1 Screen (a task)

A rounded rectangle, the quiet default, and the one exception to the splay rule. The corner radius is `R = min(14, (h − 2m)/2, (w − 2m)/2)`.

```
R = min(14, (h-2m)/2, (w-2m)/2)
M x0+R,y0  L x1-R,y0  Q x1,y0 x1,y0+R  L x1,y1-R  Q x1,y1 x1-R,y1
L x0+R,y1  Q x0,y1 x0,y1-R  L x0,y0+R  Q x0,y0 x0+R,y0  Z
```

### 5.2 Marquee (a task carrying the here mark)

A concave cushion: the four corners at the box corners, each edge bowed inward, the top and bottom by 0.14 of the height and the sides by 0.05 of the width. Googie is the one style whose here card changes shape.

```
M x0,y0  Q cx,(y0+0.14h) x1,y0  Q (x1-0.05w),cy x1,y1
         Q cx,(y1-0.14h) x0,y1  Q (x0+0.05w),cy x0,y0  Z
```

### 5.3 Hull (a begin node)

A wide, slightly concave top over inward-tapering sides and a convex bottom: a base something grows from. The sides taper inward by `inset = 0.13w`. The curves are scaled by the capped height `ch = min(h, 58)`, so a tall begin card does not let its top curve descend into its label.

```
inset = 0.13w
ch    = min(h, 58)
M x0,(y0+0.10*ch)  Q cx,(y0+0.22*ch) x1,y0
L (x1-inset),(y1-0.05*ch)
Q cx,y1 (x0+inset),(y1-0.05*ch)  Z
```

The top edge's lowest point, as a fraction of `ch`, is `HULL_DIP = 0.1424`, the extremum of a quadratic from 0.10 through control 0.22 to 0; derive it from those fractions rather than restating it. The capped curve makes the dip a constant 8.3 on the outer path, which is why a folded pair needs a constant overlap (layout engine, section 7).

### 5.4 The end node

The same hull, sized to an empty begin card, turned through a half turn: the transform `translate(w, h) scale(−1, −1)`, prepended to both the outer and the inner path. Mirroring about both axes, rather than top to bottom only, makes the pair read as one shape and its reflection: the hull's top edge rises from left to right, and after the half turn the end's bottom edge does too, so the two edges bow oppositely and, when folded (section 6), meet twice and enclose a lens.

### 5.5 Ellipse (a start node)

A tilted medallion. First find the largest ellipse of the box's proportions that, once rotated by the tilt `θ = −3°`, still lies within the box inset by the margin; then hold its major axis to 0.7 and both axes to 0.85 of that; then rotate it about the card centre.

```
rx0 = (w - 2m) / 2                      the inscribed semi-axes
ry0 = (h - 2m) / 2
bx  = sqrt(rx0² cos²θ + ry0² sin²θ)     half-extents of the rotated bounding box
by  = sqrt(rx0² sin²θ + ry0² cos²θ)
s   = min(rx0 / bx, ry0 / by)
rx  = 0.7 * 0.85 * s * rx0
ry  = 0.85 * s * ry0
outer: ellipse centre=(cx,cy) semi-axes=(rx,ry), then rotate(θ about (cx,cy))
```

At `188 by 58` this gives semi-axes `(54.28, 23.05)`.

### 5.6 Keystone (a finish node)

A narrow, unlabelled cap, wider at the top than at its base, its right side steeper than its left: a rounded quadrilateral built in a box of its own and centred in the finish card. Take the corners `(x0+0.05kw, y0+0.12kh0)`, `(x1, y0)`, `(x1−0.12kw, y1)`, `(x0+0.20kw, y1−0.06kh0)` of a box of 100 by 50, then grow the box by 2 at the top, the top-right corner rising to the new top edge and the other three lowered by 2; round each corner at radius `min(11, 0.22·kh0) = 11`; translate by `(44, 0)` into the card and rotate by +2° about the card centre. The finish card is 52 high.

```
kw = 100   kh0 = 50   lift = 2   kh = 52   x0 = m   x1 = kw - m   y0 = m   y1 = kh0 - m
P  = [ (x0 + 0.05 kw, y0 + 0.12 kh0 + lift),
       (x1,           y0),
       (x1 - 0.12 kw, y1 + lift),
       (x0 + 0.20 kw, y1 - 0.06 kh0 + lift) ]
round the corners of P at radius 11; translate(44, 0); rotate(+2° about (cx, cy))
```

The corner-rounding rule: at each vertex, step back toward the previous vertex and forward toward the next, each by the radius (clamped to half the shorter adjacent edge), and join the two points by a quadratic whose control point is the vertex.

### 5.7 The inner path and the variable-weight outline

The inner path is the outer under `innerT`, which insets it by the shape's four `BORDERS` values `(t, r, b, l)`, each first clamped to at most `w/2 − 4` or `h/2 − 4` on its axis:

```
sx = (w - l - r) / w
sy = (h - t - b) / h
innerT = translate(l, t) scale(sx, sy)
```

For the ellipse the transform is built on the ellipse's own bounding box, so its band has the stated thicknesses whatever its size: the inner ellipse has semi-axes `rx − (l + r)/2` and `ry − (t + b)/2`, its centre offset by `((l − r)/2, (t − b)/2)`. For the keystone it is built on the keystone's own 100 by 52 box. Both are computed axis-aligned, and outer and inner are rotated together, so the heavy side of the band turns with the shape.

| shape | top | right | bottom | left |
| --- | --- | --- | --- | --- |
| screen | 3.5 | 8 | 3.5 | 7 |
| marquee | 6 | 8 | 4 | 5 |
| hull | 4 | 5 | 8 | 8 |
| ellipse | 3 | 6 | 8 | 6 |
| keystone | 3 | 5 | 9 | 7 |

The outer is filled in the node's colour (a task's state token, `--c-project`, or `--c-workflow`); the inner in `--panel`, or `--c-project-tint` for a begin or an end node.

### 5.8 The tilt

Every start card is tilted −3 degrees and every finish card +2 (D7), chosen by eye: −3 is the lean at which the ellipse reads as a hand-set card while its band still pools to the lower right, and +2 completes the keystone's own lean rather than cancelling or exaggerating it. The tilt rotates the finished mark about the card centre; the box, label, hit region, and line anchor are unaffected, and the fit rule of 5.5 keeps the rotated silhouette inside the box.

### 5.9 The silhouettes at the line

| silhouette | top inset | bottom inset | at 188 by 56 or 58 |
| --- | --- | --- | --- |
| screen | `m` | `m` | 1.50, 1.50 |
| marquee | `m + 0.07h` | `m + 0.07h` | 6.54, 6.54 (h 72) |
| hull (begin) | `m + 0.135 ch` | `m + 0.025 ch` | 9.33, 2.95 |
| hull, half-turned (end) | `m + 0.025 ch` | `m + 0.135 ch` | 2.95, 9.33 |
| ellipse (start) | `h/2 − r_v` | `h/2 − r_v` | 5.92, 5.92 |
| keystone (finish) | the top edge's line at the centre, rotated | the bottom edge's line, rotated | 5.77, 3.13 |

The marquee's and the hull's figures are the quadratics evaluated at their midpoint. `r_v` is the ellipse's semi-extent along the vertical through its centre after the tilt, `1 / sqrt(cos²α / rx² + sin²α / ry²)` with `α = 90° + θ`. The keystone's are its two edge lines rotated by +2° and met at the centre of its box. An implementation that flattens its silhouettes may read the insets off the flattened path instead; the two must agree.

## 6. Folds

A folded project: the end card overlaps the begin card by the seam, 22, so two cards of 58 make a pair 188 by 94. The begin card is painted first (outer, then inner), then the end card (outer, then inner), then the begin card's label. The end's bottom band lies across the begin's top band where the two edges bow apart, and the silhouettes cross: a thin lens of the tint runs between the two bands, and at each side the corners cross into a pair of tips; no ground shows within the pair. A folded begin card takes 24 of top spacing, so its label clears the end's ink.

A folded workflow: the start card overlaps the finish card by 35, and the order is reversed: finish outer, finish inner, start outer, start inner, then the start's title. A start of 58 and a finish of 52 make a pair 188 by 75, the keystone's lower part behind the ellipse and its upper part rising above it, the two tilts unchanged. An untitled start folds to an empty ellipse. Neither fold lifts a card.

## 7. Card content and label geometry

On a task card the glyph is centred at `(29, 26)`; the label is set from x 41, its first baseline at 30.5 and each further line 15 below; the tag (`TO DO`, `IN PROGRESS`, `DONE`, `CANCELLED`) at x 18 on the baseline `30.5 + 15(n − 1) + 15.5`, in the data face at 8 with 0.9 tracking, in `--muted`. A cancelled task's label is struck through and set in `--muted`. A begin node's label and a start node's are centred on the axis with no glyph: the begin's about `hh/2 + 5.5`, the start's about `h/2 + 4`, a multi-line label stacked about that centre.

| kind | wrap width | size | line pitch | lines in the base height | growth per further line |
| --- | --- | --- | --- | --- | --- |
| task | 133 | 13 | 15 | 1 | 15 |
| begin | 118 | 13 | 15 | 1 | 15 |
| start | 68.3 | 11.5 | 13 | 2 | 14 |

The start's wrap width is the inscribed width of the inner ellipse, `2 · rx_i / √2`, which does not grow with the card's height; a long title makes a tall medallion rather than a wide one.

## 8. Glyphs

The common set at the 11 envelope (style contract, section 3), with no variation.

## 9. The here mark

The here card wears the marquee (5.2) and carries the HERE pill: a 34 by 12 rounded rectangle of radius 6 in `--cursor`, its left edge at x 18 and its top at `30.5 + 15(n − 1) + 21`, the word `HERE` centred in it in the data face at 7.5 with 1 of tracking, in `--panel`.

The mark itself is a sputnik in `--ink`: ten rays of irregular length at irregular angles, each tipped with a ball, around a solid centre, defined at a base ray length of 15 and drawn at 1.20 times that, centred 17.5 left of the box's left edge and 32 below its top, so it stands to the left of the card. It is drawn last, over everything.

```
base = 15
for each (deg, f) in rays:
    tip = (base*f*cos(deg°), base*f*sin(deg°))
    line from (0,0) to tip   stroke-width 1.4, round cap
    ball at tip   r 2.2
core ball at (0,0)  r 2.8
rays = [ (-6,1.0),(30,0.66),(63,1.12),(99,0.58),(138,0.9),
         (177,1.2),(210,0.68),(246,1.02),(285,0.82),(318,1.08) ]
the whole symbol scaled by 1.20 about its centre, placed at (-17.5, 32) in the card's frame
```

The tips at base scale: `(14.9,−1.6)`, `(8.6,4.9)`, `(7.6,15)`, `(−1.4,8.6)`, `(−10,9)`, `(−18,0.9)`, `(−8.8,−5.1)`, `(−6.2,−14)`, `(3.2,−11.9)`, `(12,−10.8)`.

## 10. The flag

The flag is an atom in `--ink`, drawn over the card after its content: three off-axis elliptical rings about one centre, each carrying an electron, and a nucleus. The rings are off-axis and irregular on purpose; rings at 0, 90, and 180 degrees would read as a tidy modern diagram.

```
O = [ (72,12,-30,-38), (66,13,40,215), (68,11,103,-38) ]     (rx, ry, ang, t)
for each (rx, ry, ang, t) in O:
    a = 0.60·rx,  b = 0.60·1.65·ry
    ellipse  centre (cx,cy)  semi-axes (a,b)  rotate ang about (cx,cy)
             stroke --ink  width 1.8  opacity 0.7  no fill
    lx = a·cos(t°);  ly = b·sin(t°)
    electron at (cx + lx·cos(ang°) − ly·sin(ang°),  cy + lx·sin(ang°) + ly·cos(ang°))  r 4.32
nucleus at (cx, cy)  r 6.6
```

The semi-axes are `(43.2, 11.88)`, `(39.6, 12.87)`, and `(40.8, 10.89)`; the electrons stand at `(25.82, −23.36)`, `(−20.1, −26.51)`, and `(−0.7, 32.84)` from the centre. The centre is placed at the card's right end, 0.5 below the drawn part's mid-height:

| node | centre, in the card's frame |
| --- | --- |
| task | `(w + 7.5, h/2 + 0.5)`, 101.5 right of the card's centre |
| begin node | `(x1 − 0.13w/2 + 7.5, h/2 + 0.5)`, 7.5 beyond the hull's side at mid-height |
| start node | `(cx + rx·cos 3° + 7.5, h/2 + 0.5)`, 7.5 beyond the ellipse's right extent |

The atom reaches about 45 beyond the card's edge, past the gutter's middle; no rule limits a flag's reach (style contract, section 4).

## 11. Tracks

A track is a polyline through the layout's point list, stroked in `--line` with round caps and round joins: the riser at 3, a departure and a return at 2.3. The riser is heavier, so a line's spine reads before its branches.

The lateral's route is the ramp, the flat run, and the ramp of the layout engine, section 4.1: it leaves its junction at `rampAngle` (12° by default), runs flat, and climbs the rest into its arrival. Siblings sharing a junction fan by splitting the lane between their two ramps (layout engine, section 4.3), so their flat runs sit at distinct heights and never cross. Every segment is flat or at exactly `tan(rampAngle)`.

Clearance: this route is the one from which `L` is derived (layout engine, section 5), so it clears by `junctionMargin` by construction.

## 12. The underpass

The common construction, with `crossedHalf` 1.5 for a riser and 1.15 for a lateral, and round line ends on the caps.

## 13. The junction

A diamond at every branch point and return point, whether or not a branch attaches there: a 12 square rotated 45°, filled in `--line`, `--ink` on hover. In a shut gap one diamond stands at the gap's midpoint; in an open gap two stand `L` from the cards on their sides.

## 14. The note glyph

The common design box, with a body corner radius of 1.5 and round line ends. On the screen, the marquee, and the hull its box sits 11 inside the card's right edge and 8 above its bottom. On the start ellipse its box's bottom-right corner sits at the inscribed-rectangle corner of the inner ellipse, computed before the tilt and rotated with the mark:

```
corner = (cx_i + rx_i / √2,  cy_i + ry_i / √2)
box    = (corner.x − 14, corner.y − 14), then rotate(θ about (cx, cy))
```

## 15. The drop indicator

The common chevron pair in `--cursor`.

## 16. Tint

Googie does not tint by zoom. A begin and an end node's body is `--c-project-tint` at every zoom.

## 17. The burst (optional decoration)

A starburst atmosphere mark, not drawn by default: four full spokes (vertical and horizontal to ±26, the two diagonals to (±18, ±18)) and four half spokes to ±14 at 22.5°, 67.5°, 112.5°, and 157.5°, stroke 1.4, opacity 0.13, in `--burst-a` or `--burst-b`.

## 18. Golden masters

Generated from [styles-masters.json](styles-masters.json) by `scripts/style_masters.py`; do not edit by hand. Each is the outer path at the stated box, before the inner transform, with the transform that gives the inner.

<!-- masters:googie:begin -->

Task, box `188 56`:

```svg
<g><path fill="var(--c-todo)" transform="" d="M 15.5,1.5 H 172.5 A 14 14 0 0 1 186.5,15.5 V 40.5 A 14 14 0 0 1 172.5,54.5 H 15.5 A 14 14 0 0 1 1.5,40.5 V 15.5 A 14 14 0 0 1 15.5,1.5 Z"/><path fill="var(--panel)" transform="translate(7 3.5) scale(0.92 0.88)" d="M 15.5,1.5 H 172.5 A 14 14 0 0 1 186.5,15.5 V 40.5 A 14 14 0 0 1 172.5,54.5 H 15.5 A 14 14 0 0 1 1.5,40.5 V 15.5 A 14 14 0 0 1 15.5,1.5 Z"/></g>
```

Here card, box `188 72`:

```svg
<g><path fill="var(--c-progress)" transform="" d="M 1.5,1.5 Q 94,11.58 186.5,1.5 Q 177.1,36 186.5,70.5 Q 94,60.42 1.5,70.5 Q 10.9,36 1.5,1.5 Z"/><path fill="var(--panel)" transform="translate(5 6) scale(0.93 0.86)" d="M 1.5,1.5 Q 94,11.58 186.5,1.5 Q 177.1,36 186.5,70.5 Q 94,60.42 1.5,70.5 Q 10.9,36 1.5,1.5 Z"/></g>
```

Begin node, box `188 58`:

```svg
<g><path fill="var(--c-project)" transform="" d="M 1.5,7.3 Q 94,14.26 186.5,1.5 L 162.06,53.6 Q 94,56.5 25.94,53.6 Z"/><path fill="var(--c-project-tint)" transform="translate(8 4) scale(0.93 0.79)" d="M 1.5,7.3 Q 94,14.26 186.5,1.5 L 162.06,53.6 Q 94,56.5 25.94,53.6 Z"/></g>
```

End node, box `188 58`:

```svg
<g><path fill="var(--c-project)" transform="translate(188 58) scale(-1 -1) " d="M 1.5,7.3 Q 94,14.26 186.5,1.5 L 162.06,53.6 Q 94,56.5 25.94,53.6 Z"/><path fill="var(--c-project-tint)" transform="translate(188 58) scale(-1 -1) translate(8 4) scale(0.93 0.79)" d="M 1.5,7.3 Q 94,14.26 186.5,1.5 L 162.06,53.6 Q 94,56.5 25.94,53.6 Z"/></g>
```

Folded project, box `188 94`:

```svg
<g transform="translate(0 36)"><path fill="var(--c-project)" transform="" d="M 1.5,7.3 Q 94,14.26 186.5,1.5 L 162.06,53.6 Q 94,56.5 25.94,53.6 Z"/><path fill="var(--c-project-tint)" transform="translate(8 4) scale(0.93 0.79)" d="M 1.5,7.3 Q 94,14.26 186.5,1.5 L 162.06,53.6 Q 94,56.5 25.94,53.6 Z"/></g><g><path fill="var(--c-project)" transform="translate(188 58) scale(-1 -1) " d="M 1.5,7.3 Q 94,14.26 186.5,1.5 L 162.06,53.6 Q 94,56.5 25.94,53.6 Z"/><path fill="var(--c-project-tint)" transform="translate(188 58) scale(-1 -1) translate(8 4) scale(0.93 0.79)" d="M 1.5,7.3 Q 94,14.26 186.5,1.5 L 162.06,53.6 Q 94,56.5 25.94,53.6 Z"/></g>
```

Start node, box `188 58`:

```svg
<g><g transform="rotate(-3 94 29)"><ellipse fill="var(--c-workflow)" cx="94" cy="29" rx="54.28" ry="23.05"/><ellipse fill="var(--panel)" cx="94" cy="26.5" rx="48.28" ry="17.55"/></g></g>
```

Finish node, box `188 52`:

```svg
<g><g transform="rotate(2 94 26) translate(44 0)"><path fill="var(--c-workflow)" d="M 17.46,8.55 L 87.54,2.45 Q 98.5,1.5 95.88,12.18 L 89.12,39.82 Q 86.5,50.5 75.51,49.99 L 32.49,48.01 Q 21.5,47.5 17.46,37.27 L 10.54,19.73 Q 6.5,9.5 17.46,8.55 Z"/><path fill="var(--panel)" transform="translate(7 3) scale(0.88 0.77)" d="M 17.46,8.55 L 87.54,2.45 Q 98.5,1.5 95.88,12.18 L 89.12,39.82 Q 86.5,50.5 75.51,49.99 L 32.49,48.01 Q 21.5,47.5 17.46,37.27 L 10.54,19.73 Q 6.5,9.5 17.46,8.55 Z"/></g></g>
```

Folded workflow, box `188 75`:

```svg
<g><g transform="rotate(2 94 26) translate(44 0)"><path fill="var(--c-workflow)" d="M 17.46,8.55 L 87.54,2.45 Q 98.5,1.5 95.88,12.18 L 89.12,39.82 Q 86.5,50.5 75.51,49.99 L 32.49,48.01 Q 21.5,47.5 17.46,37.27 L 10.54,19.73 Q 6.5,9.5 17.46,8.55 Z"/><path fill="var(--panel)" transform="translate(7 3) scale(0.88 0.77)" d="M 17.46,8.55 L 87.54,2.45 Q 98.5,1.5 95.88,12.18 L 89.12,39.82 Q 86.5,50.5 75.51,49.99 L 32.49,48.01 Q 21.5,47.5 17.46,37.27 L 10.54,19.73 Q 6.5,9.5 17.46,8.55 Z"/></g></g><g transform="translate(0 17)"><g transform="rotate(-3 94 29)"><ellipse fill="var(--c-workflow)" cx="94" cy="29" rx="54.28" ry="23.05"/><ellipse fill="var(--panel)" cx="94" cy="26.5" rx="48.28" ry="17.55"/></g></g>
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
<ellipse cx="195.5" cy="28.5" rx="43.2" ry="11.88" fill="none" stroke="var(--ink)" stroke-width="1.8" stroke-opacity="0.7" transform="rotate(-30 195.5 28.5)"/><circle r="4.32" cx="221.32" cy="5.14" fill="var(--ink)"/><ellipse cx="195.5" cy="28.5" rx="39.6" ry="12.87" fill="none" stroke="var(--ink)" stroke-width="1.8" stroke-opacity="0.7" transform="rotate(40 195.5 28.5)"/><circle r="4.32" cx="175.4" cy="1.99" fill="var(--ink)"/><ellipse cx="195.5" cy="28.5" rx="40.8" ry="10.89" fill="none" stroke="var(--ink)" stroke-width="1.8" stroke-opacity="0.7" transform="rotate(103 195.5 28.5)"/><circle r="4.32" cx="194.8" cy="61.34" fill="var(--ink)"/><circle r="6.6" cx="195.5" cy="28.5" fill="var(--ink)"/>
```

Flag on a begin node, box `188 58`:

```svg
<ellipse cx="181.78" cy="29.5" rx="43.2" ry="11.88" fill="none" stroke="var(--ink)" stroke-width="1.8" stroke-opacity="0.7" transform="rotate(-30 181.78 29.5)"/><circle r="4.32" cx="207.6" cy="6.14" fill="var(--ink)"/><ellipse cx="181.78" cy="29.5" rx="39.6" ry="12.87" fill="none" stroke="var(--ink)" stroke-width="1.8" stroke-opacity="0.7" transform="rotate(40 181.78 29.5)"/><circle r="4.32" cx="161.68" cy="2.99" fill="var(--ink)"/><ellipse cx="181.78" cy="29.5" rx="40.8" ry="10.89" fill="none" stroke="var(--ink)" stroke-width="1.8" stroke-opacity="0.7" transform="rotate(103 181.78 29.5)"/><circle r="4.32" cx="181.08" cy="62.34" fill="var(--ink)"/><circle r="6.6" cx="181.78" cy="29.5" fill="var(--ink)"/>
```

Flag on a start node, box `188 58`:

```svg
<ellipse cx="155.7" cy="29.5" rx="43.2" ry="11.88" fill="none" stroke="var(--ink)" stroke-width="1.8" stroke-opacity="0.7" transform="rotate(-30 155.7 29.5)"/><circle r="4.32" cx="181.53" cy="6.14" fill="var(--ink)"/><ellipse cx="155.7" cy="29.5" rx="39.6" ry="12.87" fill="none" stroke="var(--ink)" stroke-width="1.8" stroke-opacity="0.7" transform="rotate(40 155.7 29.5)"/><circle r="4.32" cx="135.6" cy="2.99" fill="var(--ink)"/><ellipse cx="155.7" cy="29.5" rx="40.8" ry="10.89" fill="none" stroke="var(--ink)" stroke-width="1.8" stroke-opacity="0.7" transform="rotate(103 155.7 29.5)"/><circle r="4.32" cx="155" cy="62.34" fill="var(--ink)"/><circle r="6.6" cx="155.7" cy="29.5" fill="var(--ink)"/>
```

Here mark, box `188 72`:

```svg
<g transform="translate(-17.5 32) scale(1.2)"><line x1="0" y1="0" x2="14.92" y2="-1.57" stroke="var(--ink)" stroke-width="1.4" stroke-linecap="round"/><circle r="2.2" cx="14.92" cy="-1.57" fill="var(--ink)"/><line x1="0" y1="0" x2="8.57" y2="4.95" stroke="var(--ink)" stroke-width="1.4" stroke-linecap="round"/><circle r="2.2" cx="8.57" cy="4.95" fill="var(--ink)"/><line x1="0" y1="0" x2="7.63" y2="14.97" stroke="var(--ink)" stroke-width="1.4" stroke-linecap="round"/><circle r="2.2" cx="7.63" cy="14.97" fill="var(--ink)"/><line x1="0" y1="0" x2="-1.36" y2="8.59" stroke="var(--ink)" stroke-width="1.4" stroke-linecap="round"/><circle r="2.2" cx="-1.36" cy="8.59" fill="var(--ink)"/><line x1="0" y1="0" x2="-10.03" y2="9.03" stroke="var(--ink)" stroke-width="1.4" stroke-linecap="round"/><circle r="2.2" cx="-10.03" cy="9.03" fill="var(--ink)"/><line x1="0" y1="0" x2="-17.98" y2="0.94" stroke="var(--ink)" stroke-width="1.4" stroke-linecap="round"/><circle r="2.2" cx="-17.98" cy="0.94" fill="var(--ink)"/><line x1="0" y1="0" x2="-8.83" y2="-5.1" stroke="var(--ink)" stroke-width="1.4" stroke-linecap="round"/><circle r="2.2" cx="-8.83" cy="-5.1" fill="var(--ink)"/><line x1="0" y1="0" x2="-6.22" y2="-13.98" stroke="var(--ink)" stroke-width="1.4" stroke-linecap="round"/><circle r="2.2" cx="-6.22" cy="-13.98" fill="var(--ink)"/><line x1="0" y1="0" x2="3.18" y2="-11.88" stroke="var(--ink)" stroke-width="1.4" stroke-linecap="round"/><circle r="2.2" cx="3.18" cy="-11.88" fill="var(--ink)"/><line x1="0" y1="0" x2="12.04" y2="-10.84" stroke="var(--ink)" stroke-width="1.4" stroke-linecap="round"/><circle r="2.2" cx="12.04" cy="-10.84" fill="var(--ink)"/><circle r="2.8" fill="var(--ink)"/></g>
```

Junction, box `centred on 0 0`:

```svg
<rect x="-6" y="-6" width="12" height="12" fill="var(--line)" transform="rotate(45 0 0)"/>
```

Drop indicator, box `centred on 0 0`:

```svg
<g fill="none" stroke="var(--cursor)" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M -13,-6 L -7,0 L -13,6"/><path d="M 13,-6 L 7,0 L 13,6"/></g>
```

Tracks: riser 3, laterals 2.3, line ends round, joins round.
The flag is painted over the card.

| token | light | dark |
| --- | --- | --- |
| `--ground` | `#d3e6ef` | `#0f2334` |
| `--panel` | `#f8f3e8` | `#1a3a54` |
| `--ink` | `#173242` | `#e8f1f6` |
| `--line` | `#365b6c` | `#6fb6c9` |
| `--muted` | `#5f7d8b` | `#93b3c2` |
| `--grid` | `rgba(23,50,66,.10)` | `rgba(111,182,201,.13)` |
| `--c-todo` | `#d9a53a` | `#f0bd55` |
| `--c-progress` | `#d75f2e` | `#f27a44` |
| `--c-done` | `#7d54a6` | `#bd93e6` |
| `--c-cancel` | `#8aa0ab` | `#7590a0` |
| `--c-project` | `#1f8f8a` | `#37c2ba` |
| `--c-project-tint` | `#cbe6e4` | `#356e69` |
| `--c-workflow` | `#365b6c` | `#6fb6c9` |
| `--cursor` | `#d75f2e` | `#f27a44` |
| `--f-disp` | `'Boogaloo',cursive` | `'Boogaloo',cursive` |
| `--f-ui` | `'League Spartan',sans-serif` | `'League Spartan',sans-serif` |
| `--f-mono` | `'Spline Sans Mono',monospace` | `'Spline Sans Mono',monospace` |

<!-- masters:googie:end -->

## 19. Settled by eye

The tilts (D7). The fold seams and paint orders (D15, D27). The sputnik's place to the left of the here card and its scale, and the atom that replaced the orbits, with its ring scale, minor axes, weights, and place, settled on 2026-09-17 over a two-line title (D47). The glyph set and the begin card's loss of its glyph are common rulings (D43).
