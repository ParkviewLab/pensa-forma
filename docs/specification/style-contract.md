<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# The style contract

The authority for what every visual style of the application must define, and for the parts of the drawing that are the same in every style. A style is one complete way of drawing a domain (glossary, [Style](glossary.md#style)); the application ships five, each specified in its own document, in the order the style control lists them:

| Style | Stored value | Document |
| --- | --- | --- |
| Fröbel | `froebel` | [style-froebel.md](style-froebel.md) |
| Prairie | `prairie` | [style-prairie.md](style-prairie.md) |
| Bauhaus | `bauhaus` | [style-bauhaus.md](style-bauhaus.md) |
| Googie | `googie` | [style-googie.md](style-googie.md) |
| Suuronen | `suuronen` | [style-suuronen.md](style-suuronen.md) |

Googie is the default. Where this document and a style document disagree, this document governs what must be defined and the style document governs how its own marks look.

The [design page](styles.html) draws all five styles in both themes, over the same domains, and is the authority for every drawing: how each mark looks, its shape, colour, type, and paint order. The style documents are written from it, and their golden masters are generated from the page's own export (section 12). Where marks go is not the page's business: the page carries a simplified layout of its own, and the [layout engine](layout-engine.md) alone is the authority for position. A change to a drawing is made on the design page first and carried into the style document.

## 1. What a style may vary, and what it may not

A style supplies the silhouettes, the marks, the tracks' weights and the lateral's route, the colours for both themes, and the faces. The chrome follows the style's colours and faces; its layout, sizes, strings, and behaviour are fixed by the [UI chrome](ui-chrome.md).

A style may not change the record, the commands, the layout's rules or constants, the card's width, the base heights below, the seams, the glyph shapes, the meaning of a mark, or which nodes carry which marks. Switching style changes nothing in the domain. A style switch re-measures every card in the new style's faces and re-runs the layout; the camera and the zoom hold, as after any edit. Switching theme is a colour change alone.

The test of a style is the northstar's: the visual channel carries the structure, and text only names it. Each style meets it through the checklist of section 11.

## 2. The frame every style draws in

Coordinates are logical pixels, origin top-left, x rightward and y downward; angles are degrees clockwise from the positive x-axis. Constructions are written in SVG path grammar (`M`, `L`, `Q`, `C`, `A`, `Z`), used as notation; transforms are written `translate`, `scale`, and `rotate`, a sequence applying right to left.

Every card is 188 wide (D14), the whole drawn box. Its base height is fixed by its kind, the same in every style:

| kind | base height |
| --- | --- |
| task | 56 |
| begin node | 58 |
| end node | 58 |
| start node | 58 |
| finish node | 52 |

A task carrying the here mark measures 16 taller, for the HERE pill. A card grows by its style's line pitch for every label line beyond those its base height holds, and some styles add a fixed padding to a named card (each style's label geometry). A silhouette is drawn to whatever height its card measured; a style may draw a boundary shorter than its box, and says so in its insets.

## 3. State, and the common glyphs

Only a task carries state. A start node and a begin node carry their label alone, with no glyph; a finish node and an end node carry nothing.

One glyph shape stands for each state in every style, so a state reads without its colour: a filled equilateral triangle for to do, a filled circle for in progress, a filled square for done, and a dashed open circle for cancelled. Each is filled or stroked in its state's token (`--c-todo`, `--c-progress`, `--c-done`, `--c-cancel`).

The set is defined on an 11 envelope and drawn 15 % larger (factor `G = 1.15`):

```
triangle  side 13·G = 14.95, apex up, its centroid 1 below the glyph centre
circle    r 5.5·G = 6.325
square    side 11·G = 12.65, axis-aligned
cancelled r 4.75·G = 5.4625, no fill, stroke 1.5, dash 2.4 on and 2.2 off
```

A style may set its glyphs on a smaller envelope and say so: Prairie's is 9 (triangle 12.65, circle r 5.175, square 9.2, ring r 4.6, all at `G`). A style may round the square's corners and say so: Suuronen's is a superellipse of exponent 8. No other variation is allowed.

## 4. The marks people set

The here mark and the flag mark are pointers set by people and agents (glossary, [Here mark](glossary.md#here-mark) and [Flag mark](glossary.md#flag-mark)). In every style, without exception:

- They belong to no state. They are drawn in `--ink`, in the panel colour under an ink edge, or in a colour of the style's own that no state uses (`--c-here`), never in a state, project, or workflow colour.
- The layout never considers them. Toggling either moves nothing; a mark may reach past its card into the gutter, and no rule limits how far.
- The here mark is drawn last of all, over every card and track.
- The flag is drawn on a task, a begin node, and a start node. A finish node and an end node carry no flag. Each style declares whether it paints the flag beneath its card or over it after the card's content.

A here card carries the HERE pill, drawn by the style, in the label column below the tag.

## 5. The lateral interface

The layout owns a lateral's two ends; the style owns the path between them, its route.

A departure runs from the branch point to the landing `L` beneath the branch's start silhouette, and a return from the departure `L` above the branch's finish silhouette (the top of the tail) to the return point. The vertical distance between the two ends is always `rise`, and the horizontal distance a whole number of lanes. The layout also supplies each lateral's rank among the siblings sharing its junction and side, innermost first, and their count.

A route is a function of those inputs alone. It must:

1. Stay within the rectangle its two ends span, and be monotone in both x and y, so that it never doubles back.
2. Clear every card it passes by at least `junctionMargin` (4), given the common `L` (layout engine, section 5). The derivation of `L` assumes Googie's route, the worst case being a ramp climbing at `rampAngle` across a card's half-width; a style whose route climbs more steeply than that near either end must prove its clearance in its own document, and every style document states its proof.
3. Never cross a sibling's route. Whether siblings run apart or share a run is the style's; they never cross.
4. Be delivered to the layout as a point list, curves flattened, so that the underpass detection and the repair pass (layout engine, sections 8 and 9) run over the route actually drawn.

A riser is common: it runs from the centre of a line's first card to the centre of its last, behind the cards, and for a branch on to its incoming lateral's landing and up through its tail.

## 6. The silhouette at the line

The layout measures every gap between the silhouettes where the line passes through them (layout engine, section 3). Each style therefore tabulates, for each of its silhouettes, a top inset and a bottom inset: how far the drawn part lies inside the box's top and bottom edges at the centre x. Where a style draws a boundary shorter than its box, or hangs a name below a bar, the inset measures to what is drawn, name included. The layout receives these insets from the style as part of its parameters and knows nothing else about the style.

## 7. Folds

A folded project's end card overlaps its begin card by `seam` (22), and a folded workflow's start card overlaps its finish card by `seamW` (35); both are the layout's constants (layout engine, section 7) and are the same in every style. Which card of a pair is painted first, and whether the closing card is lifted before it is painted, is the style's, and each style document gives its two folds with their paint order and lift.

## 8. Tint by zoom

One mechanism serves every style that tints its bodies. A participating style draws each body (a task card's, a project boundary's, a workflow figure's) in `--panel` at working zoom and mixes in that body's tint token as the drawing is zoomed out:

```
t = clamp((0.72 − zoom) / (0.72 − 0.45), 0, 1)
k = 1 − (1 − t)²
fill = mix in OKLab: k of the tint token, 1 − k of --panel
```

Bodies are paper at and above 72 % and fully tinted at and below 45 %; the curve is front-loaded, so most of the tint has arrived by 60 %. A drawing viewed at 80 % is therefore untinted; the application opens a domain fitted to the window (UI chrome, section 3.7), so a large domain opens tinted. The tint tokens are `--c-todo-tint`, `--c-progress-tint`, `--c-done-tint`, `--c-cancel-tint`, `--c-project-tint`, and `--c-workflow-tint`. Fröbel and Suuronen take part; Googie, Bauhaus, and Prairie do not. Specimens drawn at 100 % are paper.

## 9. Tokens and faces

A style supplies a value for every required token in both themes, light and dark:

| token | role |
| --- | --- |
| `--ground` | the canvas |
| `--panel` | a card's body |
| `--ink` | text, and the marks people set |
| `--line` | tracks and junctions |
| `--muted` | tags and the note glyph |
| `--grid` | the ground's dots (a style without a grid still defines it, for the chrome) |
| `--c-todo`, `--c-progress`, `--c-done`, `--c-cancel` | the four states |
| `--c-project` | a project's boundaries |
| `--c-workflow` | a workflow's boundaries |
| `--cursor` | the drop indicator, and the HERE pill where the style draws it in colour |

and, where it uses them, the optional tokens: `--c-project-tint` and `--c-workflow-tint` (a boundary's body), the four state tints of section 8, `--c-here` (a here mark in a colour of its own), `--c-junction` (a junction's centre where it differs from `--line`), and `--c-shade` (a shadow on a card's body). A colour chosen by eye is a token per theme; its derivation is recorded in the style document as its reason and as a constraint on retuning, not computed. A colour defined as a relation between two tokens (Suuronen's keel, a mix toward `--ink`) is a rule the application applies, like the tint curve.

A style names three faces by role: the display face, in which card labels are set; the interface face, in which the chrome is set; and the data face, in which tags, the HERE pill, and numbers are set. Every face is bundled with the application under the SIL Open Font License 1.1. The chrome's type follows the style's interface face; the About window and the note editor keep faces of their own in every style, Instrument Sans and, for note source and code, Spline Sans Mono (UI chrome, Appendix B). No platform font is used as a face; the platform's fonts supply only characters that no bundled face holds.

## 10. The common constructions

These are drawn the same way in every style, at that style's track widths, line ends, and colours.

The underpass. Where a lateral crosses another line, the crossed line runs on and the lateral is cut, each cut end capped parallel to the line it passes under. The gap gives `perpClear = 3` of air plus the crossed line's half-width; for a crossing whose angle has sine `s`, the cut ends sit back along the lateral by `half = min(breakMax, (perpClear + crossedHalf) / s)`, `breakMax = 12`, and each cut end carries a cap of length 9.2 centred on the cut and parallel to the crossed line, stroked at 1.6 in `--line` with the style's line end. The strip removing the ink is centred on the crossed line, 30 long along it and `2·half·s` across it. `crossedHalf` is half the crossed line's width in the style. The layout decides which line yields (layout engine, section 8).

The drop indicator (D35). Two chevrons facing each other across the target point, in `--cursor`, stroke 2.4, round caps and joins, drawn on the topmost layer during a drag and only over a legal target:

```
left:  M -13,-6  L -7,0  L -13,6
right: M  13,-6  L  7,0  L  13,6
both translated to the target point
```

The ghost. The dragged card's own marks at 40 % opacity, drawn at the pointer offset by the grab point; the original is drawn in place at 40 % for the drag's duration.

Hover. A junction mark and the note glyph turn `--ink` while the pointer is over them. Every junction carries a transparent hit halo of radius 13; hit-testing against cards is by the card's box, whatever is drawn in it (interaction, section 11).

The note glyph's design box is common: a memo pad on a 16 by 16 box, rendered at 14 by 14, stroked in `--muted`: a body `rect(3, 3, 10, 11)` at stroke 1.2, two rings `(6,1.5)–(6,4.5)` and `(10,1.5)–(10,4.5)` at 1.2, and three rules `(5.5,7.5)–(10.5,7.5)`, `(5.5,10)–(10.5,10)`, `(5.5,12.5)–(8.5,12.5)` at 1.0. The style sets the body's corner radius and the line ends. Unless the style says otherwise, the glyph's box sits 11 inside the right edge and 8 above the bottom edge of the drawn part of a task, a begin node, or a start node. A finish node and an end node carry no note.

## 11. The checklist

Every style document defines the following, in this order, and nothing in it is left to an implementer's judgement:

1. Its character, in a paragraph.
2. The ground, and its grid or the absence of one.
3. Its tokens, for light and for dark.
4. Its three faces.
5. Its six silhouettes (task, here card, begin, end, start, finish), each as a construction, with its top and bottom insets at the line.
6. Its two folds, with paint order and lift.
7. Each card's content: where the glyph, the label, the tag, and the HERE pill sit, and its label geometry per kind (the wrap width, the type size, the line pitch, the lines its base height holds, the growth per further line).
8. Its glyph envelope, and any variation section 3 allows.
9. Its here mark, the HERE pill, and where the here mark is painted.
10. Its flag on a task, a begin node, and a start node, and where it is painted.
11. Its tracks (the riser's and the laterals' widths, line ends, and joins), its lateral route, how siblings run, and its clearance statement.
12. Its underpass widths (`crossedHalf` for the riser and for a lateral).
13. Its junction mark.
14. Its note glyph's corners, line ends, and placement where it differs from section 10.
15. Its drop indicator's colour (the common construction in its `--cursor`).
16. Whether it tints by zoom, and its tint tokens.
17. Its golden masters.
18. What was settled by eye, with the decisions that settled it.

## 12. Golden masters

The design page exports its own golden masters. Opened with `?export=masters` in its address, it writes one JSON file, [styles-masters.json](styles-masters.json): for every style, the path data of every silhouette and mark at the stated box, and the style's constants and tokens, together with a fingerprint of the page's code. [`scripts/style_masters.py`](../../scripts/style_masters.py) writes the golden-master section of each style document from that file, and fails if the file's fingerprint no longer matches the page, so a drawing changed on the page and not re-exported is caught. An implementation's golden-path tests read the same file.

## 13. Paint order

From back to front, in every style: the ground and its grid; the risers and laterals; the junction marks; then each card in turn, as its flag if the style paints it beneath, the card's silhouettes, its content (glyph, label, tag, HERE pill), its note glyph, and its flag if the style paints it over; then every here mark; then, during a drag, the drop indicator and the ghost. A style may fix a finer order within a card, and says so.

## 14. Implementation notes, for any drawing target

Quadratic and cubic Béziers, arcs, ellipses, and superellipses may lack native primitives. Flatten each curve to a short polyline by sampling (16 subdivisions per Bézier, 48 points per ellipse, and 88 to 176 per superellipse are ample at card scale), in world coordinates before any camera transform, so the density is chosen once at model scale.

A two-fill outline (Googie) is two fills, never a stroke. A stroked outline (Fröbel, Suuronen) is a stroke of the stated width centred on the path. A band clipped to a silhouette (Fröbel) is the intersection of a rectangle with the silhouette's polygon. Every such band spans its silhouette's full width at one edge, and every silhouette so banded is convex, so where the target cannot clip to a path the band is computed as the flattened silhouette cut by one straight line at the band's inner edge, keeping the part beyond it; the result is convex and fills on the fast path. A style that banded a concave silhouette, or a band short of the full width, would need a general polygon intersection.

Every stroke keeps the ends and corners its style states; where the target's strokes carry none, stroke through a tessellator that does.

Concave silhouettes need tessellation where the target fills only convex polygons; route concave fills through any standard tessellator and convex ones through the fast path, behind one helper.

Apply transforms to points, not to a canvas state: the half turns, tilts, scales, and rotations compose as affine operations on the point list before flattening and tessellation.

A colour mix in OKLab (the tint, Suuronen's keel) converts both colours to OKLab, interpolates each component linearly, and converts back; it is never a mix in sRGB.

Where arbitrary clipping is unavailable, an underpass is drawn as an explicit ribbon: stop stroking the lateral at the gap and emit the crossing segment as a quadrilateral of the lateral's width whose end edges are mitred parallel to the crossed line. Overdrawing the gap in the ground colour is wrong, since it erases the grid.

If text is drawn from a rasterised glyph atlas, drive zoom through world coordinates and font size rather than a layer transform, or labels blur at high zoom while the marks stay crisp. Card measurement must come from the text engine's own layout query in the style's faces, so that measured and drawn size never disagree. Labels are soft-hyphenated (U+00AD at syllable boundaries); a word wider than the wrap width with no soft hyphen breaks wherever it must, so nothing overruns a card.
