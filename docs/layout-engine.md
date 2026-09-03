<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# The layout engine

The authority for where every mark goes. It takes a validated record and the
measured size of every card, and it produces the position of every station,
the point list of every track, the centre of every junction, and the bounds
of the drawing. It decides nothing about what a mark looks like, which is the
[mark geometry](mark-geometry.md), and nothing about what a mark means, which
is the [UI chrome](ui-chrome.md). The [interaction](interaction.md) document
derives its drop targets from this document's output.

---

The [worked example](worked-example.md) carries one small domain through this
engine and lists every number it produces.

## 1. The problem

A domain is drawn as a forest. Each main workflow is a vertical spine growing
upward, with branches forking off it to the left and right, each branch
itself a vertical spine that can fork again. Cards must not overlap, laterals
must not disappear behind cards, and where two lines do cross, the crossing
must be drawn as an underpass rather than as an ambiguity.

Two quantities are solved: a height for every node, and a lane for every
line. They are solved in that order, and the reason they can be is section
4's constant rise.

## 2. What the layout runs over

A **line** is a workflow. Its nodes are drawn colinear at one x, in index
order, the lowest at the bottom. The workflow record is the line, already in
order; nothing has to be derived by walking pointers.

A line's **children** are the branch workflows attached at any of its gaps,
partitioned into two lists by the side they are stored on, each already in
its inner-to-outer order. That gives a **line tree** per main workflow,
rooted at it. Main workflows are laid out independently and then placed left
to right in the domain's `mains` order.

Every node occupies a box of the same fixed width (D14), so a subtree's
horizontal contour is an integer count of lanes and every offset is a whole
number of lanes. Heights vary and are measured before the layout runs. The
tilted silhouettes of the start and finish nodes are inscribed in their boxes
(mark geometry, section 3), so the layout treats every card as its
axis-aligned box and knows nothing of tilt.

## 3. Heights: a longest-path solve

Write `u(n)` for the height of node `n`'s card top above the drawing's
baseline, up positive, so screen y is `baseY - u`. Every constraint is a
lower bound on one node given another; none is an upper bound.

Every card has two station anchors, points on its line from which the
gaps beside it are measured: an **upper anchor** `anchorGap` above its top
edge and a **lower anchor** `anchorGap` below its bottom edge. Nothing is
drawn at either. The gap between two cards therefore runs, from the lower
card's top edge upward, through `anchorGap`, the outgoing edge `L`, the
middle edge, the incoming edge `L`, and `anchorGap` again to the upper
card's bottom edge, so the two junction-bearing edges stand the same
distance, `anchorGap + L`, from the card on their side. Cards are painted
over tracks, so a card hides whatever passes behind it.

**Succession.** For consecutive nodes `A` and `B` in one workflow, `B`
directly above `A`:

```
u(B) >= u(A) + anchorGap + air(A, B) + anchorGap + cardH(B)
```

`air(A, B)` is the clearance between `A`'s upper anchor and `B`'s lower
anchor, the outgoing edge, the middle edge, and the incoming edge together,
and section 5 derives it.

**Fork.** For a branch workflow `X` departing at the branch point of the gap
above node `A`, with `F` being `X`'s own start node, whose departure lateral
arrives `L` below `F`'s lower anchor:

```
u(F) >= u(A) + anchorGap + L + rise + L + anchorGap + cardH(F)
```

**Return.** For a branch workflow `X` arriving at the return point of the gap
below node `P`, with tip `T` being `X`'s own finish node, whose return
lateral leaves the tail above `T`'s upper anchor:

```
u(P) >= u(T) + anchorGap + L + rise + L + anchorGap + cardH(P)
```

The three run over the same graph the validator has already proved acyclic,
so one pass in topological order taking the maximum at each node solves them
all. Infeasibility is not a failure mode: no constraint puts a ceiling on
anything, so a tall branch simply stretches the line it hangs from, and every
defect is a bad drawing rather than an impossible one. Height is the only
cost.

The fork constraint is an equality in practice, a branch's start node having
no other incoming edge. The return constraint is a genuine inequality, and
its slack is the branch's **tail**, the line drawn above the branch's finish
node:

```
tail(X) = u(P) - cardH(P) - anchorGap - L - rise - u(T) - anchorGap
```

The constraint is exactly what guarantees the tail is at least `L`, so the
departure clearance is a floor the tail can only exceed, and it may exceed it
without limit. When a returning branch is the shorter side, it is the
branch's own line that stretches, not the line it returns to; a branch that
leaves low and rejoins near the top of a tall parent runs most of that
parent's height as bare line before it turns. That stretch is drawn, and
section 4.2 says how.

An **open branch** contributes a fork constraint and no return constraint. It
therefore never stretches the line it left, and it has no tail. Its riser
simply ends at its finish card's centre, behind the keystone.

### 3.1 Where the slack goes

Every constraint is a lower bound and the solve takes the maximum, so a node
sits as low as its constraints allow and slack appears only where something
forces it. Two elements are built to absorb that slack, and they are the only
two.

Within a gap, the **middle edge** takes it. The outgoing and incoming edges
are the two fixed clearances and never stretch, so whatever the succession
constraint leaves over is the middle edge's length (section 5). This is the
mechanism by which a tall branch forces the line it hangs from to open up
between its departure and its return.

On a return, the **tail** takes it, as a vertical run in the branch's own
lane before the return lateral turns toward the return point (section 4.2).
The return constraint is the one genuine inequality in the solve, and its
slack is the tail.

Together these give a property worth having rather than merely a tidy one.
Sibling branches sharing a branch point have their start nodes placed by the fork
constraint, which is an equality in practice, so every sibling's start node
has its card bottom at exactly `u(A) + 2 anchorGap + 2L + rise`. They are
level, whatever their branches contain. A short branch and a tall one sharing
both a branch point and a return point therefore need no reconciliation: the
short one's start node is not raised to meet the tall one's, and its own cards are
not spread apart to lift its tip, because its riser simply rises further
before its return lateral turns. A branch's cards stay tightly spaced, its
start node stays level with its siblings', and the stretch lands in bare line,
where it costs nothing to read.

Beyond that, nothing is aligned across lanes. Two cards in different main
workflows, or one on a line and one on a branch beside it, share a height
only by coincidence.

## 4. Why the rise is constant

Every lateral in the drawing climbs the same amount, `rise`, whatever
horizontal distance it covers. This is the fact that lets heights be solved
before lanes are assigned, and it is not an aesthetic choice.

A rise proportional to the lanes a lateral spans would make a node's height
depend on lane assignment, which depends on vertical extents, which depend on
heights. The dependency is circular and there is no order in which to solve
it. Fixing the rise breaks the cycle: heights first, lanes second, and
neither reads back.

The lateral itself is a **ramp, a flat run, and a ramp**. It leaves its
junction at twelve degrees, runs flat across whatever span remains, and
climbs the rest into its arrival. The two ramps together always cover exactly
one lane of horizontal run, because the total climb is `rise = laneStep *
tan 12` and both ramps are at twelve degrees; how that one lane is split
between them is free, and section 4.3 uses the freedom. A branch one lane
out is therefore a single straight twelve-degree diagonal; every wider branch
climbs the same total over a longer flat middle.

### 4.1 The lateral, exactly

One construction serves every lateral, at either end of a branch. Given a
start point, an end point, the direction between them, and the length of the
ramp at the junction end, `rampJ`, with the branch-end ramp taking the
remainder of the lane:

```
dir    = sign(to.x - from.x)
dx     = |to.x - from.x|
rampJ  = clamp(rampJ, 0, min(laneStep, dx))
rampB  = min(laneStep - rampJ, dx - rampJ)
climbJ = rampJ * tan12
climbB = rampB * tan12
points = [ from ]
if rampJ > 0:              points += [ (from.x + dir*rampJ, from.y - climbJ) ]
if dx > rampJ + rampB:     points += [ (to.x - dir*rampB, from.y - climbJ) ]
points += [ to ]
```

A branch is never in its parent's lane, so `dx` is at least one lane and the
two ramps together always climb exactly `rise`. At exactly one lane apart the
flat run has zero length and the lateral is a single straight diagonal. Wider
than that, the middle runs flat. The clamps are defensive, for a separation
narrower than one lane, which the packer never produces.

A departure runs from the shared branch point to each branch's arrival beneath
its start node; a return runs from each tip's departure above its finish node
to the shared return point. They are mirror images through this one
construction, so nothing whatever distinguishes the two ends of a branch in
the drawing.

### 4.2 The tail is riser, not lateral

A line's riser is drawn from the **centre** of its first card to the centre
of its last, the cards painted over it, so that it meets every silhouette
whatever its shape: an opener's ellipse and a closer's keystone do not fill
their boxes, and a riser stopped at the box edge would float clear of them.
For a branch it runs further at both ends, from where its own incoming
lateral arrives, `anchorGap + L` beneath its start card, up to where its
return departs, above its finish card. Only a main workflow's line, which
has neither an incoming lateral nor a return, runs from centre to centre and
no further.

So the tail of section 3.1, the slack in the return constraint, is drawn as
riser. Two things follow, and both are why it belongs there rather than on
the return lateral. The return lateral stays exactly ramp-flat-ramp with the
constant rise and no special case, which is what lets one construction serve
both ends. And the branch's spine reads as one continuous heavy line with a
lighter connector leaving its top, the riser being drawn heavier than a
lateral, which is the subway idiom the whole mark vocabulary is built on.

The tail is unbounded above and nothing caps it. A branch that leaves low on
a tall parent and rejoins near its top runs most of that parent's height as
bare riser, turns once, and crosses whatever lies between. The height was
already paid for by whatever made the parent tall, so the long run costs the
drawing nothing it had not already spent.

### 4.3 A junction is one point, and the fan that leaves it

Several branches meeting one point share one junction, and each connects to
it directly (D13). The drawing shows one diamond per point, not one per line
meeting it: two branches leaving one gap share a branch point, and two
branches returning to one gap share a return point. A junction is therefore
an address rather than only ink: its kind, the gap whose point holds it, and
the list of branches attached there, which is exactly what the gap record
already holds in its side lists.

Drawn naively the siblings do not read as several: every lateral at one
junction has the same two endpoint heights and the same total climb, so
their flat runs all sit at one height and overlap exactly from the innermost
branch's lane inward. The drawing then shows one line with peel-offs rather
than a fan, the count cannot be read, and the stored inner-to-outer order has
no visible effect.

The mechanism that separates them costs nothing. Since the two ramps of a
lateral always sum to exactly one lane of horizontal run, how that lane is
**split** between them is free: it moves the flat run up or down without
moving either endpoint, without changing the rise, and therefore without
touching the height solve at all. Fanning is a drawing rule, not a
constraint.

The rule. Within one junction's side list, the **junction-side ramp** is
longest for the innermost branch and shortens with each position outward;
the branch-side ramp takes the remainder. For `n` siblings on a side, the
innermost takes `rampJ = laneStep * (1 - rampFloor)` and the outermost
`rampJ = laneStep * rampFloor`, with the rest spaced evenly between; with one
sibling the split is immaterial and `rampJ = laneStep / 2`. `rampFloor` is
0.2, so no ramp is shorter than a fifth of a lane and the stub every
sibling shares leaving the junction stays short.

Three things follow. The flats sit at distinct heights, so no two siblings
run collinear except over the stub they share leaving the junction, which is
the length of the outermost's junction-side ramp and is short by
construction. That stub is correct rather than a defect: the lines do meet
there. And siblings cannot cross one another, since on a departure every
outer branch runs below every inner one over the inner one's whole span, and
on a return above it, which is what a common endpoint and a common opposite
height force in each direction.

The innermost branch at exactly one lane out has a flat run of zero length,
so its split is immaterial and it draws as the single straight twelve-degree
diagonal it always was.

The air rule of section 5 needs no adjustment. Its worst case is a lateral
climbing at twelve degrees across the whole of a card's half-width, which is
the longest junction-side ramp, that of the innermost sibling; every
shortened ramp turns flat sooner and clears by more.

The count and the order are both legible from the verticals: each branch is
identified by where its own line leaves the shared run, those departure
points are a full lane apart, and their order along the run is the stored
inner-to-outer order with the innermost nearest the parent's line.

## 5. The air on a gap, and the two points within it

A gap carries a branch point and a return point, both of which may be
occupied (structural model, section 2.4). The gap's vertical extent must hold
both junctions and keep them apart.

One length governs the gap's interior: **L**, the standard trunk-edge length.
The **branch point** sits `L` above the lower node's upper anchor, and the
**return point** sits `L` below the upper node's lower anchor, so the
outgoing edge and the incoming edge are both exactly `L` and neither ever
stretches, and each junction stands `anchorGap + L` clear of the card on its
side. The span between the two points is the middle edge, and it absorbs
every stretch the height solve adds.

A middle edge is **either zero or at least L**, never between. At zero the
two points coincide, which is the shut gap, and the whole gap is `2L`. Any
occupied gap is at least `3L`. Nothing is ever drawn in the band between, so
no interval within a gap is ever shorter than `L`, which is what makes each
of the three positions large enough to aim a pointer at without a tolerance
rule (interaction, section 4.1).

`L` is also exactly the separation two junction diamonds need when one gap
carries both, so a departure clearance, an arrival clearance, and a diamond
gap are one named length here.

The air the gap needs is the largest of four figures:

```
air = 2 * L                                        # the shut gap: middle edge zero
if the gap has departures:
    air = max(air, L + (cardW / 2) * tan12 + junctionMargin)
if the gap has arrivals:
    air = max(air, L + (cardW / 2) * tan12 + junctionMargin)
if the gap has both:
    air = max(air, 3 * L)                          # two diamonds, L apart
if 2 * L < air < 3 * L:  air = 3 * L               # a middle edge is 0 or >= L
```

Each of the three raised cases has a reason, and the reasons are the
specification rather than the numbers.

A departing lateral leaves at the lower node's x and climbs as it goes
outward, so the card it could vanish behind is the upper one, directly above
the junction it just left. It climbs `(cardW / 2) * tan 12` whilst crossing
that card's own half-width, so the gap must hold that climb plus the
departure clearance, or the line passes behind the card and re-emerges beyond
it.

An arriving lateral is the mirror: it descends as it goes outward from the
card it joins, so what it can run into is the lower node's card, whose top
edge lies `anchorGap` below the anchor; the same figure as the departure
case covers it, with that much room to spare.

A gap that both departs and arrives must keep its two diamonds apart.
Nothing in the height solve relates them, because one is bounded through its
branch and the other is not, so the separation is imposed here.

The final clause is the quantisation, and it costs almost nothing. The
forbidden band is the open interval between `2L` and `3L`; above `3L` the air
is continuous, so a gap that needs more takes exactly what it needs. Only a
gap whose solve lands strictly inside that band is rounded up, by less than
`L`.

With the constants of section 12 the three raised figures land at or near
`3L`: a gap with departures needs about `3L`, and a gap with both needs
exactly `3L`, which is some evidence the length is the right one rather than
an imposition.

## 6. Lanes: a subtree-aware band packer

Two rules place branches horizontally. The line of each main workflow is
pinned at lane zero of that workflow.

**Ordering.** On each side, siblings run inner to outer in the order the
record stores, read as the line from the top down with each gap's side list
in its own stored order. The order is the author's, and the layout obeys it
(D4).

**Band reservation.** Each branch reserves a contiguous band of lanes wide
enough for its entire subtree, its own line plus every descendant's lanes on
both sides. Bands are placed first-fit against the vertical extents already
parked on that side, so two subtrees whose extents never overlap share lanes,
and bands that would collide are pushed outward a whole band at a time. A
line's extent is widened at each end by the reach of its own laterals, since
a departing ramp dips below its first card and an arriving one rises above
its last.

The packer is a post-order walk: lay out each child subtree, learn its width
and its vertical extent, place it, then bubble the composed width up. A final
top-down pass turns per-parent relative lanes into absolute ones. This is
`O(n · depth)` in the worst case, which is negligible at the scale of a task
forest; the classic linear-time thread-and-shift optimisation is available if
it ever matters.

### 6.1 What open branches do to planarity

A branch's **span** is the stretch of its parent's line it runs alongside. A
returning branch has a bounded span, from its departure gap to its return
gap. An open branch has an unbounded span: it leaves and never comes back, so
it runs alongside everything above its departure.

Two unbounded spans on one side always nest, one inside the other, so an
ordering by departure height alone guarantees a planar drawing. Two bounded
spans may overlap without nesting, and no ordering can then avoid a crossing.
This model has both at once, and a bounded span may also cross an unbounded
one, when the open branch departs above the returning branch's departure and
below its return.

So crossings are unavoidable in general, ordering is the author's, and every
crossing is drawn as an underpass (section 8). One useful consequence falls
out: an open branch placed outermost on its side crosses nothing, because its
span contains every span inside it. Where the application must place a
branch automatically rather than being told where, an open branch goes
outermost.

## 7. Folded scopes

A folded project (D15) is the one edge exempt from section 3. The client's
view keeps the `begin`/`end` pair and drops the body, and the `end` node is
placed flush on the `begin` node's card, bottom edge to top edge, with no
`anchorGap` and no air. The air that edge reports is therefore negative by
exactly `anchorGap`, since the project's own dot falls inside the closing
card and is covered by it.

The two hull silhouettes cross there into a lens, which is what makes a shut
scope read as one closed object rather than as two cards touching. The
overlap needed to shut the seam is

```
seam = 2 * m  +  HULL_DIP * ( curveHeight(hBegin) + curveHeight(hEnd) )
```

where `m` is the silhouette margin, `HULL_DIP` the fraction of its curve
height by which a hull's edge bows away from the seam, and `curveHeight(h) =
min(h, 58)` the capped height from the mark geometry. Each silhouette is
inset by the margin and each of the two meeting edges bows away by up to its
own dip; less than this and a lens of the ground shows through the middle.

The formula is general, but the value is constant in practice, because both
heights are capped at 58 and a begin card's minimum height is already 58, so
`curveHeight` returns 58 on both sides whatever the cards contain. At `m =
1.5` and `HULL_DIP = 0.1424` that is 19.5, and a floor a shade above it, 22,
is what the layout uses. A taller begin card takes nothing more.

Every branch that is part of a folded project is hidden with the body; its
departure and return laterals are not drawn, and its lanes are not reserved.
A branch departing inside the fold and returning inside it vanishes whole;
by I12 no branch departs inside and returns outside, so nothing can be left
dangling.

Fold state is client-local view state, so no stored record ever asks for
this, and folding never changes the record.

## 8. The underpass

Where a lateral crosses another line, it passes behind: the crossed line runs
on unbroken and the lateral is cut, each severed end carrying a cap lying
parallel to the line it passes under, so the cap reads as a slice of what
runs on rather than as a line that stops. The construction is specified in
the mark geometry; the layout's job is to identify the crossings and mark
them.

The precedence is a single rule with two clauses: a departure lateral yields
to a return lateral, and both yield to a riser. Nothing yields to a departure
lateral. The return is the line by which a branch rejoins its parent, so it
reads as the more structural of the two laterals, and one stated rule is
easier to read off a drawing than a relative test such as "whichever is
further from its own spine".

A crossing counts only if it is **proper**. An endpoint touch does not count,
since two lines meeting at a junction meet there on purpose and a break over
that point would deny the join the drawing is making. Nor do collinear runs,
which is what sibling laterals leaving a shared junction do by construction
over their shared stub (section 4.3). Only a segment passing strictly through
another is cut.

The cut is made by clipping the lateral with a strip along the crossed line
rather than by shortening its path, because a stroke can only end square to
its own direction, and its round cap adds a bulb of ink half a stroke beyond
that, which is exactly what shows past a cap where two lines meet shallowly.
Each break therefore carries the direction of the line being passed under,
since that is what its caps are drawn along; for a riser that direction is
always vertical.

## 9. The repair pass

One rule cannot be guaranteed by construction: that no crossing falls inside
a node's space. After the solve, every lateral segment is tested against the
rectangle of every node whose x-range it spans.

A conflict is repaired by **lifting, never by widening**. Widening would
change nothing about the rise, which is constant, and would re-open the
packing; lifting is monotone. Which node is lifted follows the record of which
constraint set each node's height, so a node whose height a lateral pins is
repaired by lifting the host of the branch that pins it, rather than by
bending that lateral off twelve degrees. A folded pair's closing node pins to
its own begin node for the same reason: the pair is one object, and slack
given to the close would come out of the seam rather than move anything.

Two properties of the pass matter more than the mechanism. It is bounded by
a pass count, and whatever it cannot close is reported on the layout's own
conflict list rather than drawn in silence. And it keeps the **best**
placement rather than the last: a lift is not guaranteed to clear the line it
was asked to clear, it can move a card into another line's path, and a pass
that buys nothing still costs the height it added. Fewer conflicts therefore
wins, and between two placements with the same count, the shorter drawing
wins.

## 10. Output

The layout returns the station anchor of every node, the point list of every
track with its kind, the centre of every junction with the gap and point it
stands for and the branches attached there, the crossings marked as
underpasses with the direction of the crossed line, the drawing's bounds, the
metrics it used, and the unresolved conflict list. Everything downstream
reads only that.

The camera is the chrome's: `Fit` frames the bounds with a margin, and the
zoom and pan are view state the layout does not see.

## 11. Required properties

These are the acceptance criteria, and they are testable directly against the
output.

No two tracks properly cross without the crossing being marked as an
underpass. No lateral segment lies inside a node's rectangle, except as
reported on the conflict list. Every lateral segment is flat or at exactly
`tan 12`, and no lateral segment is vertical, the tail being drawn as riser.
A branch's riser runs from its incoming lateral's arrival to its return's
departure, and a main workflow's runs from its start card to its finish
card. The four clearances hold to
the pixel. The minimum air is met everywhere, and is tight on a branch-free
workflow. No two cards overlap. A branch's start node sits above the node it
leaves and below that node's successor. Sibling branches sharing a branch
point have their start nodes' card bottoms at one height, whatever those
branches contain, and a branch's own gaps stay at their minimum air unless
something inside that branch forces otherwise. A tall branch stretches its
parent above its return point whilst everything at or below its departure
stays put. Lane order follows the stored side lists read from the top down.
A nested subtree reserves a band, so an inner branch cannot collide with an
outer sibling. Sibling laterals at one junction have flat runs at distinct
heights and never cross one another. The drawing is deterministic under a
permuted key order in the record, lies entirely inside its reported bounds,
and is monotone: adding a card to a branch moves nothing at or below that
branch's departure.

## 12. Constants

```
cardW           card width                             188
gutter          horizontal gutter between lanes         40
laneStep        cardW + gutter                          228
tan12           tan(12°)                                0.2126
rise            laneStep * tan12                        48.5
rampFloor       the shortest junction-side ramp, as a fraction of a lane   0.2
L               the standard trunk-edge length: the outgoing edge, the incoming
                edge, the floor on a non-zero middle edge, and the least
                separation of two junctions sharing a gap                  12
anchorGap       each anchor's distance from its card's edge, above the top and below the bottom   8
minAir          2L, the shut gap; air is never inside the open band (2L, 3L)  24
junctionMargin  slack added to a junction-bearing gap                       4
seam            overlap of a folded pair                                    22
repairPasses    bound on the repair loop                                    8
margin          drawing margin inside the bounds                            24
```

Where a number is derived, the derivation governs and the value is a
consequence: `rise` from `laneStep` and the angle, `minAir` from the two
clearances, `seam` from the margin and the hull's dip, and the two raised airs
from the angle and the card's half-width.

## Lineage

The packing is the tidy-tree problem, whose aesthetic guarantees, that edges
do not cross, that a subtree is drawn identically wherever it sits, and that
horizontal distance is minimal, are the invariants wanted here. Knuth (1971)
and Wetherell and Shannon (1979) established the postorder parent-centring
approach; Reingold and Tilford (1981) added the rule that a subtree is drawn
the same wherever it appears, which is what forbids interleaving; Walker
(1990) generalised it to unbounded degree; Buchheim, Jünger, and Leipert
(2002) corrected Walker to linear time; van der Ploeg (2014) extended it to
non-layered trees with varying node sizes, which is the form to adopt if D14
is ever reversed.

The reusable mechanism is the contour: each subtree carries the extreme
coordinates it occupies at each level, and a sibling is shifted out by exactly
the overlap between one's right contour and the other's left. Because cards
here are a fixed width and every height is solved before any lane is chosen,
the contour reduces to a per-side occupancy of integer lanes over an interval
of real y, which is what section 6 implements.
