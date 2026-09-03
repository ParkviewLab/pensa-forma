<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# Mark geometry

The geometry of every mark the application draws on its map canvas, in a form
complete enough that an implementation in any language, against any 2D
drawing target, can reproduce them exactly. It is the drawing companion to
the [UI chrome](ui-chrome.md), which covers the shell around the canvas, and
to the [layout engine](layout-engine.md), which positions these marks. Where
the chrome says what a mark means and when it appears, this document says
exactly how it is constructed, with the formulas, the constants, and a worked
instance for each.

The look the marks add up to is a mid-century retrofuturist systems diagram:
a Googie-inspired, Atomic Age flowchart laid out like a retro transit or
control-system map. Every mark below serves that reading or is cut.
For a design brief or an image search, the terms are: mid-century
retrofuturism, Googie diagram, Atomic Age infographic, Jet Age schematic,
retro systems map, 1950s technical illustration.

This document is the sole and final authority for the marks' geometry: build
exactly what it says, and where it is silent, choose any reasonable behaviour
and record the choice. Nothing here presumes a rendering technology; the
implementation notes at the end record the traps any toolkit meets.

## Scope

This covers the mark vocabulary: the complete set of vector marks the canvas
draws, for its cards, its tracks, its junctions, its decorators, and its
standalone markers, including the two drop indicators. The layout supplies
where each mark goes; this document specifies everything that is drawn
there. Where a mark's construction refers to a position (a station anchor, a
junction centre, a track's point list), treat that position as an input
supplied by the layout, not as something this document derives.

## How to read this document

Each mark is given in four registers, and they are redundant on purpose,
because they carry different things and fail differently.

The construction is the authoritative register: the sequence of path
operations written as functions of the card box `(w, h)` and a set of named
constants. It is the general rule, and it is the only register that is
lossless; a formula fixes a curve that a sentence or a picture cannot. The
constants used are listed with each mark and gathered again in the constants
appendix. A golden-master instance follows, the construction evaluated at a
stated `(w, h)` down to concrete numbers; its role is verification, letting
an implementer diff a render against a known-correct instance. The prose
around each is connective, stating intent and the occasional caveat. An HTML
sibling of this file, when authored, renders each mark from the same data, so
the picture a reader sees is the specification executing, not an
illustration of it.

## Foundations

### The coordinate frame and the card box

Coordinates are in logical pixels. The origin is top-left; x grows rightward
and y grows downward, so a smaller y is higher on the screen. Angles are in
degrees measured clockwise from the positive x-axis, the natural sense in a
y-down frame.

Every card silhouette is a function of its box, the pair `(w, h)`. The width
is fixed: a card is 188 pixels wide, and that 188 is the whole drawn box,
inner spacing included, so `w = 188` for every card without exception
(D14). The height varies with the card's content (the label's line count,
the status tag, the HERE pill; the card's inner metrics are in the constants
appendix) and is measured at layout time, not computed here; a silhouette is
drawn to whatever `h` the card measured. The worked instances below state
the `h` they use.

### The outline is a gap between two fills

A card has no stroked border. Its outline is the visible band between two
filled paths: an outer silhouette in the node's colour, and an inner
silhouette in the panel colour laid over it. The inner path is the same path
as the outer, transformed by a translate-and-scale that insets it by a
different amount on each of the four edges. Where the inset is small the
colour band is thin; where it is large the band is thick. That per-edge
asymmetry, a thin top over a heavy bottom, one side steeper than the other,
is the design's mid-century character; a uniform stroke would read as flat
and modern instead. Because the inner is a scaled copy of the outer, the
outline follows any silhouette, straight-edged or curved, without a second
hand-drawn path. The inset amounts are the `BORDERS` four-tuples, one per
shape, and the transform that applies them is derived in the silhouette
section.

Three rules of the style govern every mark (D7). No outline is a
constant-width stroke; a line that carries character is a filled ribbon whose
weight pools along one side, and the two-fill outline is that ribbon. The
workflow boundaries are rotated to a slight, jaunty angle, two to six
degrees, varied from card to card. And shapes are splayed: no silhouette has two
parallel straight edges.

### Path notation

Constructions are written in SVG path grammar, used here purely as a compact
notation for curves; any 2D drawing target can consume or imitate it. `M
x,y` moves to a point, `L x,y` draws a line to a point, `Q cx,cy x,y` draws
a quadratic Bezier through control point `(cx, cy)` to `(x, y)`, and `Z`
closes the path back to the last `M`. Quadratics have a single control
point; there are no cubics in the mark vocabulary. Ellipses and circles are
given as primitives with a centre, semi-axes, and a rotation. A construction
gives each coordinate as an expression in `w`, `h`, and the named constants;
the golden master gives the same with the expressions evaluated.

Two transform operations also appear: `translate(a, b)` and `scale(sx,
sy)`, and a third, `rotate(θ about (x, y))`. A sequence written
`translate(a, b) scale(sx, sy)` applies to a point right to left: scale
first, then translate. Prepending a transform to a sequence places it
leftmost, so it applies last.

### Colour

Every fill and stroke is a role token, not a literal colour, and the token
resolves to one of two values depending on the theme (azure, the light
default, or navy, the dark). Three hues carry meaning: the line colour marks
the boundaries of a workflow (its start and finish nodes, which belong to the
line), teal marks the boundaries of a project (a begin node and its end),
and violet marks a task that is done. The complete token-to-hex table for
both themes is the colour appendix; the marks below name tokens.

## The marks

Paint order, back to front: the ground grid; the track layer (tracks,
junction diamonds, and cursor marks); the station dots; then the cards, each
drawn in this order: its orbits decorator first, then its outer silhouette,
its inner silhouette, and its content, with the note glyph last atop its
corner; then, during a drag, the drop indicator and the ghost. A card
therefore covers the dots and tracks beneath it, and a decorator's overflow
never covers a neighbouring card drawn after it.

### 1. The ground

The canvas is not blank. It carries a dot grid: one dot at every 40-pixel
lattice point, each dot a small filled circle in the `--grid` token, which is
a low-alpha ink (about 10 percent on azure, 13 percent on navy). It is
specified as a repeating 40 by 40 tile whose dot reaches full `--grid` at
radius 1px and fades to transparent by 1.4px; reproduce it as a tiled
texture, or as a loop drawing a filled circle of radius about 1.2px at every
`(40i, 40j)` within the visible rectangle, in `--grid`. The grid belongs to
the viewport, not the map world, so it neither pans nor zooms.

### 2. The station dot

Where a card attaches to its line, the line carries a station dot: a filled
circle of diameter 11 pixels (radius 5.5) in the `--line` token, centred on
the station anchor the layout supplies. It is the subway-map station mark,
and it is the same size as a status glyph so the two read as one family.

```
circle  centre = (anchor.x, anchor.y)  r = 5.5  fill = --line
```

### 3. The card silhouettes

Six silhouettes exist: four axis-aligned polygons and curves for tasks and
project boundaries, and two tilted conics for workflow boundaries. Each is
defined by its outer path and a derived transform, `innerT`, that produces
the inner path from it. The outer path per shape is given first; the shared
inner-path mechanism follows; the tilt of the two conics is given last.

The margin `m = 1.5` is common to all six: every silhouette is inset 1.5
pixels inside the card box. Define `x0 = m`, `x1 = w - m`, `y0 = m`, `y1 = h
- m`, and the centres `cx = (x0 + x1) / 2`, `cy = (y0 + y1) / 2`.

#### 3.1 screen (a plain task)

A rounded rectangle, the quiet default. The corner radius is `R = min(14,
(h - 2m)/2, (w - 2m)/2)`, so a short card rounds less than a tall one but
never more than 14.

```
R = min(14, (h-2m)/2, (w-2m)/2)
M x0+R,y0  L x1-R,y0  Q x1,y0 x1,y0+R  L x1,y1-R  Q x1,y1 x1-R,y1
L x0+R,y1  Q x0,y1 x0,y1-R  L x0,y0+R  Q x0,y0 x0+R,y0  Z
```

Golden master, `w = 188`, `h = 56` (so `R = 14`):

```svg
<path d="M15.5,1.5L172.5,1.5Q186.5,1.5 186.5,15.5L186.5,40.5Q186.5,54.5 172.5,54.5L15.5,54.5Q1.5,54.5 1.5,40.5L1.5,15.5Q1.5,1.5 15.5,1.5Z"/>
```

(A rounded rectangle has parallel edges, and is the one exception to the
splay rule: it is the quiet default against which the characterful shapes
read.)

#### 3.2 marquee (a task carrying the "here" cursor)

A concave cushion: the four corners sit at the box corners, and each of the
four edges bows inward. The top and bottom bow by 0.14 of the height; the
left and right bow by 0.05 of the width.

```
M x0,y0  Q cx,(y0+0.14h) x1,y0  Q (x1-0.05w),cy x1,y1
         Q cx,(y1-0.14h) x0,y1  Q (x0+0.05w),cy x0,y0  Z
```

Golden master, `w = 188`, `h = 72`:

```svg
<path d="M1.5,1.5 Q94,11.6 186.5,1.5 Q177.1,36 186.5,70.5 Q94,60.4 1.5,70.5 Q10.9,36 1.5,1.5 Z"/>
```

#### 3.3 hull (a begin node, and its end node)

A wide, slightly concave top over inward-tapering sides and a convex bottom;
it reads as a base something grows from, which is what a project's begin
node is. The sides taper inward by `inset = 0.13w`. The top and bottom
curves are scaled not by the full height but by a capped height `ch =
min(h, 58)`: past 58 pixels the curve stops growing, so a tall multi-line
begin card does not let its top curve descend into its own centred label.

```
inset = 0.13w
ch    = min(h, 58)
M x0,(y0+0.10*ch)  Q cx,(y0+0.22*ch) x1,y0
L (x1-inset),(y1-0.05*ch)
Q cx,y1 (x0+inset),(y1-0.05*ch)  Z
```

Golden master, `w = 188`, `h = 58` (so `ch = 58`):

```svg
<path d="M1.5,7.3 Q94,14.3 186.5,1.5 L162.1,53.6 Q94,56.5 25.9,53.6 Z"/>
```

The top edge's lowest point, as a fraction of `ch`, is a fixed 0.1424
(`HULL_DIP`), the extremum of a quadratic from 0.10 through control 0.22 to
0; derive it from those two fractions rather than restating it, so it cannot
drift from the path. The capped curve makes the dip a constant 8.3 pixels on
the outer path at any card height, which is why a folded pair needs a
constant overlap to shut its seam (layout engine, section 7).

#### 3.4 the end node (a project's close)

An end node wears the same hull, sized to an empty begin card, turned
through a half turn: mirrored about both of the card's axes. The half turn
is the transform `translate(w, h) scale(-1, -1)`, prepended to both the
outer and the inner path (so the inner is `translate(w, h) scale(-1, -1)`
then `innerT`). Mirroring about both axes, rather than only top-to-bottom,
is what makes the pair read as one shape and its reflection: the hull's top
edge rises from left to right, and after a half turn the close's bottom edge
rises from left to right too, so the two edges bow oppositely and, when a
folded pair is drawn touching, meet twice and enclose a lens. Golden master
flip for a `188 by 58` close:

```
transform = translate(188 58) scale(-1 -1)
```

#### 3.5 ellipse (a start node)

A workflow opens with an ellipse, tilted: the jaunty opener of the style.
The ellipse is the largest one of the card box's proportions that, once
rotated by the card's tilt `θ` (section 3.8), still lies within the box
inset by the margin. Build it axis-aligned from the inscribed semi-axes,
scale it down until its rotated bounding box fits, and rotate it about the
card centre.

```
rx0 = (w - 2m) / 2                      the inscribed semi-axes
ry0 = (h - 2m) / 2
bx  = sqrt(rx0² cos²θ + ry0² sin²θ)     half-extents of the rotated bounding box
by  = sqrt(rx0² sin²θ + ry0² cos²θ)
s   = min(rx0 / bx, ry0 / by)           the scale that makes it fit
rx  = s * rx0
ry  = s * ry0
outer: ellipse  centre=(cx,cy)  semi-axes=(rx,ry)  then rotate(θ about (cx,cy))
```

Golden master, `w = 188`, `h = 58`, `θ = -3°`:

```
rx0 = 92.5   ry0 = 27.5
bx  = 92.38  by  = 27.89
s   = 0.9862
outer: ellipse  centre=(94,29)  semi-axes=(91.22,27.12)  rotate -3° about (94,29)
```

At this slight tilt the fit scale is close to one, so the ellipse all but
fills its box; the lean reads as a hand-set card rather than a tilted one,
whilst the band's weight still pools to the lower right.

The label sits centred in the card, unrotated, as on a begin card: the tilt
belongs to the silhouette, not to the text.

#### 3.6 circle (a finish node)

A workflow closes with a circle, unlabelled, drawn within a finish card of
the minimum height. Its radius is half the lesser inset dimension, which for
a finish card is its height. A circle has no visible tilt; its outline's
weight does (section 3.7), and it rotates with the card's tilt so that the
heavy side sits at a jaunty angle rather than flat underneath.

```
r = min(w - 2m, h - 2m) / 2
outer: circle  centre=(cx,cy)  r
```

Golden master, `w = 188`, `h = 44`: `r = 20.5`, centre `(94, 22)`.

#### 3.7 the inner path and the variable-weight outline

The inner path is the outer path under an affine transform `innerT` that
insets it by the shape's four `BORDERS` values `(t, r, b, l)` (top, right,
bottom, left). With each value first clamped to at most `w/2 - 4` or `h/2 -
4` on its axis, the transform is:

```
sx = (w - l - r) / w
sy = (h - t - b) / h
innerT = translate(l, t) scale(sx, sy)
```

Applied to the outer path, this yields the inner silhouette; the outer is
filled in the node colour and the inner in the panel colour, and the
uncovered band between them is the outline. For the two conics the transform
is applied in the card frame, before the tilt: the inset ellipse or circle is
computed axis-aligned, and both outer and inner are then rotated together
about the card centre, so the heavy side of the band turns with the shape.
The `BORDERS` four-tuples are:

| shape | top | right | bottom | left |
| --- | --- | --- | --- | --- |
| screen | 3.5 | 8 | 3.5 | 7 |
| marquee | 6 | 8 | 4 | 5 |
| hull | 4 | 5 | 8 | 8 |
| ellipse | 3 | 6 | 8 | 6 |
| circle | 3 | 6 | 8 | 6 |
| keystone | 3 | 5 | 9 | 7 |

Worked `innerT` for each golden master above: screen `translate(7, 3.5)
scale(0.9202, 0.8750)`; marquee `translate(5, 6) scale(0.9309, 0.8611)`;
hull `translate(8, 4) scale(0.9309, 0.7931)`; ellipse `translate(6, 3)
scale(0.9362, 0.8103)`, giving an inner ellipse of centre `(94.0, 26.5)` and
semi-axes `(85.40, 21.98)` before the shared rotation; circle `translate(6,
3) scale(0.9362, 0.7500)`, giving an inner ellipse of centre `(94.0, 19.5)`
and semi-axes `(19.19, 15.38)` before rotation. An inset circle is an
ellipse, and that is the point: the band is 3 thick at the top of the circle
and 8 thick at the bottom, the calligraphic weight of the style.

#### 3.8 the tilt

Each start and finish card carries a tilt `θ`, derived from the node's id so
that a given card never changes shape when the map is rearranged, and
varied across cards so that a domain reads as hand-placed rather than
stamped. Hash the id's bytes with 32-bit FNV-1a; take the low ten bits as a
fraction `f = (hash mod 1024) / 1024`; the tilt is `2 + 4f` degrees, and
its sign is positive when bit 10 of the hash is set and negative otherwise.
So every tilt lies in `[2, 6)` degrees either way: slight, never square, and
never so steep that the ellipse must shrink far to fit its box.

```
h = fnv1a32(id)
f = (h mod 1024) / 1024
θ = (h bit 10 ? +1 : -1) * (2 + 4 f)
```

The tilt is a rotation of the finished mark, outer and inner together, about
the card centre. The card's box, its label, its glyphs, its station anchor,
and its hit region are unaffected; the fit rule of section 3.5 guarantees the
rotated silhouette stays inside the box, so the layout and the interaction
layer never see the tilt.

#### 3.9 keystone (reserved)

A rounded, asymmetric quadrilateral, defined and held in reserve for a
future node state; nothing draws it in the initial design. It is built by
rounding the corners of four points at `(x0+0.05w, y0+0.12h)`, `(x1, y0)`,
`(x1-0.12w, y1)`, `(x0+0.20w, y1-0.06h)` to a radius `min(11, 0.22h)`.

```
P = [ (x0+0.05w, y0+0.12h), (x1, y0), (x1-0.12w, y1), (x0+0.20w, y1-0.06h) ]
round the corners of P at radius min(11, 0.22h)
```

The corner-rounding rule: walk the polygon and replace each sharp corner
with a quadratic. At each vertex, step back toward the previous vertex and
forward toward the next, each by the radius (clamped to half the shorter
adjacent edge), and draw a `Q` through the vertex between those two points.
Golden master, `w = 188`, `h = 56`:

```svg
<path d="M16.94,17.41Q10.90,8.22 21.89,7.80L175.51,1.92Q186.50,1.50 182.19,11.62L168.25,44.38Q163.94,54.50 152.94,54.20L50.10,51.44Q39.10,51.14 33.06,41.95Z"/>
```

### 4. The status glyphs

A task card carries a small round glyph beside its label, 11 pixels in
diameter (radius 5.5), showing its status; a begin card carries the
same-sized glyph in the project teal, and a start card in the workflow line
colour. All six fit the same 11-pixel round envelope, differing only in fill
and stroke:

| glyph | meaning | fill | stroke |
| --- | --- | --- | --- |
| done | done | `--c-done` (violet) | none |
| doing | doing | `--c-doing` | none |
| todo | to do | none | 2px solid `--c-todo` |
| cancel | cancelled | none | 1.5px dashed `--c-cancel` (dash 2.4, gap 2.2) |
| project | a begin node | `--c-project` (teal) | none |
| workflow | a start node | `--c-workflow` | none |

```
filled variants: circle r = 5.5, fill token, no stroke
ring variants:   no fill, stroke token at the stated width, drawn at a
                 geometric radius of 5.5 minus half the stroke width, so the
                 stroke lies entirely inside the 11-pixel envelope
                 (todo: r = 4.5, stroke 2; cancel: r = 4.75, stroke 1.5,
                  dash pattern 2.4 on, 2.2 off along the stroke path)
```

The cancel ring is dashed; the todo ring is solid and heavier (2px against
the dashed ring's 1.5). A cancelled task additionally strikes its label
through and greys it, which is a text property, not a mark.

### 5. The orbits decorator

Any flagged node wears the orbits: three heavy, off-axis elliptical rings
centred on the card, each carrying one solid electron ball set back from
apogee, all in the node's own colour (its status colour for a task, the
project teal for a begin or end node, the workflow colour for a start or
finish node). The rings are off-axis and irregular on purpose; rings at 0,
90, and 180 degrees would read as a tidy modern diagram rather than
atomic-age. Each ring is an ellipse of semi-axes `(rx, ry)` rotated by `ang`
degrees about the card centre, stroked at width 2.4 with 0.7 opacity; its
ball is a filled circle of radius 4 at parameter `t` degrees along the
unrotated ellipse, then carried through the same rotation. A core ball of
radius 4 sits at the centre.

```
for each (rx, ry, ang, t) in O:
    ellipse  centre=(cx,cy)  semi-axes=(rx,ry)  rotate ang about (cx,cy)
             stroke=colour  stroke-width=2.4  stroke-opacity=0.7  fill=none
    lx = rx*cos(t°);  ly = ry*sin(t°)
    ball at (cx + lx*cos(ang°) - ly*sin(ang°),  cy + lx*sin(ang°) + ly*cos(ang°))
             r=4  fill=colour
core ball at (cx, cy)  r=4  fill=colour
O = [ (72,12,-30,-38), (66,13,40,215), (68,11,103,-38) ]
```

The three ball offsets from the card centre, evaluated: `(45.4, -34.8)`,
`(-36.6, -40.5)`, `(-5.5, 53.7)`. The decorator is drawn behind the card so
its rings overflow the card box.

### 6. The cursor mark (the atomic starburst)

The "here" cursor (the per-workflow marker of the current task) is marked,
beside the marquee card, by a sputnik: solid rays of irregular length at
irregular angles, each tipped with a ball, around a solid centre. Its colour
is `--ink` (near-black on azure, near-white on navy). The symbol is defined
at a base ray length of 15; the cursor draws it at 1.15 times that. Ten rays
are drawn, each a line from the centre to a tip, with a ball of radius 2.2 at
the tip; a core ball of radius 2.8 sits at the centre.

```
base = 15
for each (deg, f) in rays:
    tip = (base*f*cos(deg°), base*f*sin(deg°))
    line from (0,0) to tip   stroke-width=1.4  round cap
    ball at tip   r=2.2   fill=--ink   (no stroke)
core ball at (0,0)  r=2.8  fill=--ink
rays = [ (-6,1.0),(30,0.66),(63,1.12),(99,0.58),(138,0.9),
         (177,1.2),(210,0.68),(246,1.02),(285,0.82),(318,1.08) ]
cursor draws the whole symbol scaled by 1.15 about its centre
```

The ten tips, evaluated at base scale: `(14.9,-1.6)`, `(8.6,4.9)`,
`(7.6,15)`, `(-1.4,8.6)`, `(-10,9)`, `(-18,0.9)`, `(-8.8,-5.1)`,
`(-6.2,-14)`, `(3.2,-11.9)`, `(12,-10.8)`. (Tips are recorded to one
decimal; the 30-degree ray's y evaluates to exactly 4.95 and is recorded as
4.9, the value the golden masters use.) A second symbol, the four-plus-spoke
starburst (the "burst" atmosphere mark), is specified in the constants
appendix as an optional decoration; it is not drawn by default.

### 7. The tracks

A track is a polyline through a point list the layout supplies, drawn as an
`M x,y L x,y ...` path with no fill, a round cap, and a round join, in the
`--line` token. Three kinds differ only in stroke width:

| kind | role | stroke width |
| --- | --- | --- |
| riser | the vertical spine between stacked nodes on a line | 3 |
| departure | a lateral leaving a branch point for a branch's start node | 2.3 |
| return | a lateral from a branch's finish node to a return point | 2.3 |

(The riser is drawn slightly heavier than the two lateral kinds, so the
spine of a line reads before its branches.)

```
path = "M" + points[0] + " L" + points[1] + " L" + ...   (no Z)
fill = none   stroke = --line   linecap = round   linejoin = round
```

### 8. The underpass

Where a lateral (a departure or a return) crosses another line, a riser or
another lateral, the crossed line runs on unbroken and the crossing lateral
yields: it is cut so a gap opens where it passes behind, and each cut end
carries a short cap lying parallel to the line it passes under, so the cap
reads as a slice of what runs on rather than as a line that simply stops.
The whole construction is drawing-target-neutral geometry; its one
implementation subtlety (that the cut must be parallel to the crossed line,
not square to the lateral) is treated in the implementation notes, because a
naive stroke cannot express it.

The gap is specified by the air wanted across the crossed line, `perpClear =
3` plus the crossed line's half-width (`CROSSED_HALF`: riser 1.5, lateral
1.15). For a crossing whose angle between the two lines has sine `s`, the
cut ends sit back along the lateral by `half = min(breakMax, across / s)`,
where `across = perpClear + crossedHalf` and `breakMax = 12` caps a nearly
parallel crossing (there the air is given up rather than the line). The
strip that removes the ink is a rectangle centred on the crossed line,
`stripLength = 30` long along that line and `2*half*s` wide across it. Each
cut end carries a cap of length `capLength = 9.2`, centred at the cut and
oriented along the crossed line, stroked at width 1.6 in `--line`.

```
across = perpClear + crossedHalf(over)          # over ∈ {riser, lateral}
s      = |sin(angle between lateral and crossed line)|
half   = (s < ε) ? breakMax : min(breakMax, across / s)
# cut strip: rectangle centred on the crossing point,
#   stripLength/2 either way ALONG the crossed line's unit vector,
#   half*s either way ACROSS it
# two caps: at ±half along the lateral from the crossing point,
#   each a segment of length capLength parallel to the crossed line
TUNE = { perpClear:3, breakMax:12, capLength:9.2, stripLength:30 }
CROSSED_HALF = { riser:1.5, lateral:1.15 }
```

### 9. The junction diamond

A branch point or return point with at least one branch attached is marked
by a small diamond centred on the junction point: an 8-pixel square rotated
45 degrees, filled in `--line`, turning to `--ink` when the pointer hovers
it. Every junction carries a transparent circular hit halo of radius 13
centred on the same point (8 pixels of ink is no target for a pointer),
which the interaction layer uses as the drop region for a return-point
target and the hover region for the diamond.

```
diamond: square  centre=(cx,cy)  side=8  rotate 45° about (cx,cy)  fill=--line
halo:    circle  centre=(cx,cy)  r=13  fill=transparent
```

### 10. The note glyph

A card with a note shows a small memo-pad glyph in its bottom-right corner,
on a 16 by 16 design box, stroked in `--muted` (turning to `--ink` when the
pointer hovers it): a rounded body rectangle, two spiral-ring ticks over the
top edge, and three ruled lines, the last shorter.

```
design box: origin (0,0), 16 by 16; rendered at 14 by 14
body:  rect  x=3 y=3 w=10 h=11, corner radius 1.5   (no fill, stroke 1.2)
rings: line (6,1.5)->(6,4.5);  line (10,1.5)->(10,4.5)   (stroke 1.2, round cap)
rules: line (5.5,7.5)->(10.5,7.5);  line (5.5,10)->(10.5,10);  line (5.5,12.5)->(8.5,12.5)   (stroke 1.0, round cap)
```

Where the glyph sits depends on the silhouette, because a card's corner is
empty on a conic and a glyph placed there would land on the ground.

On the four axis-aligned silhouettes (screen, marquee, hull, and the end
node's half-turned hull), the box is inset 11 from the card's right edge and
8 from its bottom, in the card frame.

On the start node's ellipse, the box's bottom-right corner sits at the
inscribed-rectangle corner of the *inner* ellipse, computed before the tilt
and rotated with the mark, so the glyph stays inside the panel, clear of the
band, at any tilt and any card height:

```
corner = (cx_i + rx_i / √2,  cy_i + ry_i / √2)     of the inner ellipse, card frame
box    = (corner.x - 14, corner.y - 14)             then rotate(θ about (cx, cy))
```

For the golden master (inner centre `(94.0, 26.5)`, semi-axes `(85.40,
21.98)`) the corner is `(154.4, 42.0)` and the box `(140.4, 28.0)` before the
rotation.

On the finish node's circle the glyph sits beside the mark rather than in
it, since the circle is too small to hold it and has no label to make room
for: the box's left edge 6 pixels right of the circle's rightmost point, its
vertical centre on the circle's centre, in the card frame and not rotated.
For the golden master that is the box at `(120.5, 15.0)`.

### 11. The drop indicators

Two indicators exist (P8), both in the `--cursor` token, drawn on the
topmost layer during a drag and only over a legal target.

The **chevron pair** marks a trunk-edge, branch-edge, or return-point
target: two chevrons facing each other across the point the drop would
occupy, centred on that point. For a trunk-edge target the point is on the
line at the middle of the zone; for a branch-edge target it is at the base of
the lane the branch would take, level with the branch point's arrival
height; for a return-point target it is the junction centre.

```
left:  M -13,-6  L -7,0  L -13,6      stroke 2.4  round cap and join  no fill
right: M  13,-6  L  7,0  L  13,6
both translated to the target point
```

The **bar** marks a main-workflow target: a vertical line the full height of
the drawing's bounds plus the margin, at the centre x of the gutter or margin
the drop would occupy, stroked at width 3 with round caps.

```
line from (x, bounds.top - margin) to (x, bounds.bottom + margin)   stroke 3  round cap
```

The **ghost** is the dragged card's own marks at 40 percent opacity, drawn
at the pointer offset by the grab point; the original is drawn in place at
40 percent opacity for the drag's duration.

## Constants (the parts list)

Every number the marks use, gathered in one place.

```
Card box:        width 188 (fixed, the whole drawn box);  height measured
Card metrics:    task inner spacing 11 (top/bottom) / 16 (left/right);
                 begin and start inner spacing 16 all round, minimum height 58;
                 folded begin top spacing 24; end minimum height 58; finish height 44;
                 inter-element gap 3; glyph-to-label gap 7; cursor card left/right spacing 24
Silhouette:      margin m = 1.5
  screen:        corner radius R = min(14, (h-2m)/2, (w-2m)/2)
  marquee:       top/bottom bow 0.14h; left/right bow 0.05w
  hull:          side inset 0.13w; top start 0.10*ch, control 0.22*ch; bottom 0.05*ch;
                 ch = min(h, 58); HULL_DIP = 0.1424 (derived)
  ellipse:       inscribed semi-axes, scaled by s = min(rx0/bx, ry0/by) to fit the tilt
  circle:        r = min(w-2m, h-2m)/2
  keystone:      points (x0+0.05w, y0+0.12h), (x1, y0), (x1-0.12w, y1), (x0+0.20w, y1-0.06h);
                 corner radius min(11, 0.22h)
Tilt:            θ = ±(2 + 4 f) degrees, f and sign from FNV-1a of the id (section 3.8)
BORDERS (t,r,b,l):  screen (3.5,8,3.5,7)  marquee (6,8,4,5)  hull (4,5,8,8)
                    ellipse (3,6,8,6)  circle (3,6,8,6)  keystone (3,5,9,7)
                    (each clamped to w/2-4 or h/2-4 on its axis)
Glyph:           11px envelope, strokes inside; filled r 5.5; todo ring r 4.5 stroke 2 solid;
                 cancel ring r 4.75 stroke 1.5 dashed (dash 2.4, gap 2.2)
Station dot:     diameter 11 (r 5.5), fill --line
Orbits:          O = [(72,12,-30,-38),(66,13,40,215),(68,11,103,-38)];
                 ring stroke 2.4, opacity 0.7; ball r 4; core r 4
Sputnik:         base 15; rays (deg,factor) =
                   (-6,1.0)(30,0.66)(63,1.12)(99,0.58)(138,0.9)(177,1.2)(210,0.68)(246,1.02)(285,0.82)(318,1.08);
                 ray stroke 1.4 round cap; ball r 2.2; core r 2.8; cursor scale 1.15
Burst (optional decoration):  four full spokes: vertical and horizontal to ±26, the two diagonals
                 to (±18, ±18); four half spokes to ±14, rotated 22.5/67.5/112.5/157.5 degrees;
                 stroke 1.4; opacity 0.13; colours --burst-a (default) / --burst-b (variant)
Tracks:          riser 3; departure 2.3; return 2.3; round cap and join; colour --line
Underpass:       TUNE perpClear 3, breakMax 12, capLength 9.2, stripLength 30;
                 CROSSED_HALF riser 1.5, lateral 1.15; cap stroke 1.6
Junction:        diamond side 8, rotate 45; halo r 13
Note glyph:      design box 16 rendered at 14; body rect (3,3,10,11) corner radius 1.5 stroke 1.2; rings stroke 1.2; rules stroke 1.0;
                 placement: inset 11 right / 8 bottom on the axis-aligned silhouettes; the inner ellipse's
                 inscribed corner on the start ellipse (rotating with it); 6 right of the circle, centred, on the finish node
Drop indicators: chevrons ±13 wide, ±6 tall, tips 7 from centre, stroke 2.4; bar stroke 3
Ghost:           opacity 0.4 (ghost and original alike)
Ground:          dot lattice pitch 40; dot radius ~1.2 (full --grid at 1px, transparent by 1.4px)
```

## Colours (two themes)

Each token by role, and where relevant by hue, for both themes.

| token | role | azure | navy |
| --- | --- | --- | --- |
| `--ground` | canvas | `#d3e6ef` | `#0f2334` |
| `--panel` | card panel (task, start, finish) | `#f8f3e8` | `#1a3a54` |
| `--ink` | text, cursor mark | `#173242` | `#e8f1f6` |
| `--line` | tracks, dots, diamonds | `#365b6c` | `#6fb6c9` |
| `--muted` | tags, note glyph | `#5f7d8b` | `#93b3c2` |
| `--grid` | ground dots | `#173242` at 10 % | `#6fb6c9` at 13 % |
| `--c-todo` | to-do glyph and screen | `#d9a53a` | `#f0bd55` |
| `--c-doing` | doing | `#d75f2e` | `#f27a44` |
| `--c-done` | done (= `--accent-violet`) | `#7d54a6` | `#bd93e6` |
| `--c-cancel` | cancelled | `#8aa0ab` | `#7590a0` |
| `--c-project` | begin and end hulls (= `--accent-teal`) | `#1f8f8a` | `#37c2ba` |
| `--c-project-tint` | begin and end panel | `#cbe6e4` | `#356e69` |
| `--c-workflow` | start ellipse and finish circle (= `--line`) | `#365b6c` | `#6fb6c9` |
| `--cursor` | HERE pill, drop indicators | `#d75f2e` | `#f27a44` |
| `--burst-a` | atmosphere burst | `#1f8f8a` | `#37c2ba` |
| `--burst-b` | atmosphere burst (variant) | `#d9a53a` | `#f0bd55` |

The hue tokens `--accent-teal` and `--accent-violet` hold the same two values
and are used, outside the map, by surfaces that want a particular colour
rather than a particular meaning (a note link, the automation status dot,
the note editor's syntax colours; see the chrome); those do not move if the
role-to-hue assignment is ever exchanged. `--c-workflow` shares the line
colour deliberately: a workflow's boundaries belong to its line.

## Assignment: kind and state to shape and colour

Which mark is drawn for which node. Policy, not geometry; changeable
independently of the shapes.

| node | shape | fill (outer) | panel (inner) | extras |
| --- | --- | --- | --- | --- |
| task | screen | its status colour | `--panel` | status glyph; status tag |
| task, marked "here" | marquee | its status colour | `--panel` | sputnik beside it; HERE pill |
| start node | ellipse, tilted | `--c-workflow` | `--panel` | workflow glyph; centred label |
| finish node | circle, tilted | `--c-workflow` | `--panel` | no label, glyph, or tag |
| begin node | hull | `--c-project` | `--c-project-tint` | project glyph; centred label |
| end node | hull, half-turned | `--c-project` | `--c-project-tint` | no label, glyph, or tag |
| any flagged node | (its shape) | (unchanged) | (unchanged) | orbits behind, in the node's colour |
| folded begin node | hull | `--c-project` | `--c-project-tint` | end drawn shut on its card; extra top spacing |

A begin node and a start node show no status glyph and no tag and can never
be the cursor, so the teal hull and the line-coloured ellipse read
unambiguously as boundaries rather than tasks. The orbits mark the flagged
state alone and compose with any shape.

## Implementation notes, for any drawing target

The constructions above are geometry; this section records the traps an
implementation meets translating them, whatever the toolkit.

Quadratic Beziers and conics may lack native primitives. Where they do,
flatten each `Q` to a short polyline by sampling the curve at a handful of
parameter values (16 subdivisions is ample at card scale), and an ellipse or
circle at 48 evenly spaced angles; the sampled points join the straight
segments to form one point list per silhouette. Flatten in world coordinates
before any camera transform, so the subdivision density is chosen once at
model scale.

The variable-weight outline is two fills, never a stroke. Build the outer
point list, fill it in the node colour; apply the `innerT` affine to the
same point list, fill the result in the panel colour over the first. Do not
attempt to stroke the silhouette; the whole point of the two-fill
construction is a per-edge-variable band that a constant-width stroke
cannot produce.

Concave fills may need tessellation. Two silhouettes are concave by design:
the hull (its top edge bows inward) and the marquee (all four edges bow
inward). A renderer that fills only convex polygons directly will produce
artifacts on exactly these; triangulate the flattened point list first (any
standard polygon tessellator) and submit triangles. The screen, the ellipse,
the circle, and the glyphs and dots are convex and need no such treatment; a
single "fill this closed point list" helper that routes concave shapes
through the tessellator and convex ones through the fast path keeps the call
sites uniform.

Apply transforms to points, not to a canvas state. The rotations and scales
above (the end node's half turn, the openers' tilt, the junction diamond's
45-degree turn, the sputnik's 1.15 scale, the orbit ring rotations) compose
as affine operations applied to the point list before flattening and
tessellation; no retained transform stack is assumed.

Strokes take the tabulated width and colour with round caps and round joins;
the tracks, the glyph rings, the orbit ellipses (themselves flattened to
polylines), the sputnik rays, the note glyph, and the drop indicators are all
strokes.

The underpass needs care where arbitrary clipping is unavailable. The
construction in section 8 removes a strip of the lateral's ink; a toolkit
that clips only to axis-aligned rectangles cannot cut that way, and
overdrawing the gap in the ground colour is wrong (it would erase the dot
grid). Instead, stop stroking the lateral at the gap and emit the crossing
segment as an explicit ribbon: a quadrilateral of the lateral's own width
whose two end edges are mitred parallel to the crossed line, the mitre angle
and the setback coming from section 8's computation unchanged. Since
laterals are straight runs of constant width, each crossing is one quad, and
the caps fall out of the same geometry.

If text is drawn from a rasterised glyph atlas, it is sampled rather than
re-tessellated per frame; drive zoom through world coordinates and font size
rather than through a layer transform, or labels blur at high zoom while the
vector marks stay crisp. Card measurement, which the layout needs, should
come from the text engine's own layout query, so measured size and drawn size
can never disagree. Card labels are soft-hyphenated (U+00AD at syllable
boundaries) so a long word can break inside the card; verify the text engine
honours soft hyphens as break opportunities, or choose the wrap points
explicitly.
