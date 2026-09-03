<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# A worked example: the Small Test domain

One small domain carried all the way through: its record in the on-disk
canonical form, the layout the [layout engine](layout-engine.md) computes
for it, and the drawing the [mark geometry](mark-geometry.md) makes of that
layout, which the HTML sibling of this file renders. It is a fixture: an
implementation that produces these numbers from this record, and this
picture from these numbers, has the layout and the marks right. It also
shows, on one screen, how a domain reads: two branches leaving one point on
the left and returning to one point above, a project inside the main
workflow and another inside a branch, and the openers and closers of every
workflow.

The domain: a main workflow whose start node is untitled, holding the project
XYZ-1 with the tasks step alpha, step Beta, and step gama; a branch workflow
departing on the left above step alpha and returning above step Beta, whose
whole content is the project "plan" holding 333 and think; and a second,
outer branch departing and returning at the same two points, holding the
single task 111. Every task is to do; no node has a note or a log entry.

## The record

`domain.json`, in the canonical form of the [persistence](persistence.md)
document (ids shortened to read; real ids are the twelve characters of the
structural model, section 1):

```json
{
  "schema": 1,
  "revision": 1,
  "id": "d_smalltest0",
  "name": "Small Test",
  "mains": [
    "w_main"
  ],
  "workflows": {
    "w_main": {
      "id": "w_main",
      "nodes": [
        "n_s0",
        "n_b1",
        "n_a1",
        "n_a2",
        "n_a3",
        "n_e1",
        "n_f0"
      ],
      "gaps": [
        "g_0",
        "g_1",
        "g_2",
        "g_3",
        "g_4",
        "g_5"
      ]
    },
    "w_plan": {
      "id": "w_plan",
      "nodes": [
        "n_s1",
        "n_b2",
        "n_t1",
        "n_t2",
        "n_e2",
        "n_f1"
      ],
      "gaps": [
        "g_6",
        "g_7",
        "g_8",
        "g_9",
        "g_10"
      ]
    },
    "w_111": {
      "id": "w_111",
      "nodes": [
        "n_s2",
        "n_t3",
        "n_f2"
      ],
      "gaps": [
        "g_11",
        "g_12"
      ]
    }
  },
  "nodes": {
    "n_s0": {
      "id": "n_s0",
      "kind": "start",
      "title": "",
      "log": []
    },
    "n_b1": {
      "id": "n_b1",
      "kind": "begin",
      "title": "XYZ-1",
      "pair": "n_e1",
      "log": []
    },
    "n_a1": {
      "id": "n_a1",
      "kind": "task",
      "title": "step alpha",
      "status": "todo",
      "log": []
    },
    "n_a2": {
      "id": "n_a2",
      "kind": "task",
      "title": "step Beta",
      "status": "todo",
      "log": []
    },
    "n_a3": {
      "id": "n_a3",
      "kind": "task",
      "title": "step gama",
      "status": "todo",
      "log": []
    },
    "n_e1": {
      "id": "n_e1",
      "kind": "end",
      "pair": "n_b1",
      "log": []
    },
    "n_f0": {
      "id": "n_f0",
      "kind": "finish",
      "log": []
    },
    "n_s1": {
      "id": "n_s1",
      "kind": "start",
      "title": "",
      "log": []
    },
    "n_b2": {
      "id": "n_b2",
      "kind": "begin",
      "title": "plan",
      "pair": "n_e2",
      "log": []
    },
    "n_t1": {
      "id": "n_t1",
      "kind": "task",
      "title": "333",
      "status": "todo",
      "log": []
    },
    "n_t2": {
      "id": "n_t2",
      "kind": "task",
      "title": "think",
      "status": "todo",
      "log": []
    },
    "n_e2": {
      "id": "n_e2",
      "kind": "end",
      "pair": "n_b2",
      "log": []
    },
    "n_f1": {
      "id": "n_f1",
      "kind": "finish",
      "log": []
    },
    "n_s2": {
      "id": "n_s2",
      "kind": "start",
      "title": "",
      "log": []
    },
    "n_t3": {
      "id": "n_t3",
      "kind": "task",
      "title": "111",
      "status": "todo",
      "log": []
    },
    "n_f2": {
      "id": "n_f2",
      "kind": "finish",
      "log": []
    }
  },
  "gaps": {
    "g_0": {},
    "g_1": {},
    "g_2": {
      "id": "g_2",
      "branchLeft": [
        "w_plan",
        "w_111"
      ]
    },
    "g_3": {
      "id": "g_3",
      "returnLeft": [
        "w_plan",
        "w_111"
      ]
    },
    "g_4": {},
    "g_5": {},
    "g_6": {},
    "g_7": {},
    "g_8": {},
    "g_9": {},
    "g_10": {},
    "g_11": {},
    "g_12": {}
  }
}
```

## The layout

Constants as the layout engine's section 12 gives them: card width 188, lane
step 228, `L` 12, `anchorGap` 8, `junctionMargin` 4, `rampFloor` 0.2, rise
48.5. `u` is a card's top above the baseline, up positive, with the main
start node's card top at zero; the anchor is `u + anchorGap`; screen `y` is
`baseY - u` with the baseline placed so that the drawing fits, and the main
workflow's line at `x = 760`, the branches one and two lanes to its left.

| Node | Kind | Title | Workflow | x | u (card top) | Height | Anchor | Screen y of the top |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `n_s0` | start |  | `w_main` | 760 | 0 | 58 | 8 | 1096.9 |
| `n_b1` | begin | XYZ-1 | `w_main` | 760 | 90 | 58 | 98 | 1006.9 |
| `n_a1` | task | step alpha | `w_main` | 760 | 178 | 56 | 186 | 918.9 |
| `n_a2` | task | step Beta | `w_main` | 760 | 278 | 56 | 286 | 818.9 |
| `n_a3` | task | step gama | `w_main` | 760 | 892.9 | 56 | 900.9 | 204.0 |
| `n_e1` | end |  | `w_main` | 760 | 982.9 | 58 | 990.9 | 114.0 |
| `n_f0` | finish |  | `w_main` | 760 | 1066.9 | 52 | 1074.9 | 30.0 |
| `n_s1` | start |  | `w_plan` | 532 | 316.5 | 58 | 324.5 | 780.5 |
| `n_b2` | begin | plan | `w_plan` | 532 | 406.5 | 58 | 414.5 | 690.5 |
| `n_t1` | task | 333 | `w_plan` | 532 | 494.5 | 56 | 502.5 | 602.5 |
| `n_t2` | task | think | `w_plan` | 532 | 582.5 | 56 | 590.5 | 514.5 |
| `n_e2` | end |  | `w_plan` | 532 | 672.5 | 58 | 680.5 | 424.5 |
| `n_f1` | finish |  | `w_plan` | 532 | 756.5 | 52 | 764.5 | 340.5 |
| `n_s2` | start |  | `w_111` | 304 | 316.5 | 58 | 324.5 | 780.5 |
| `n_t3` | task | 111 | `w_111` | 304 | 404.5 | 56 | 412.5 | 692.5 |
| `n_f2` | finish |  | `w_111` | 304 | 488.5 | 52 | 496.5 | 608.5 |

| Quantity | Value |
| --- | --- |
| air of an ordinary gap (2L) | 24 |
| air of `g_2` (departures) and `g_3` (arrivals) before the branches stretch them | 36 |
| the branch point of `g_2` (u) | 198.0 |
| the start cards' bottom, every departing branch (u) | 258.5 |
| the return point of `g_3` (u) | 824.9 |
| where each return lateral leaves its branch's tail (u) | 776.5 |
| the tail of `w_plan` (from its finish card's anchor to the turn) | 12.0 |
| the tail of `w_111` | 280.0 |
| the middle edge of `g_3`, opened by the branches | 526.9 |
| junction-side ramps at the shared points, inner and outer | 182.4 and 45.6 |
| baseY (screen y of u = 0) | 1096.9 |

The laterals, as point lists in screen coordinates, each a ramp, a flat, and
a ramp with the fan split at the shared points (the inner sibling's
junction-side ramp longest):

| Lateral | Points |
| --- | --- |
| departure, w_plan (inner) | (760.0, 898.9) → (577.6, 860.2) → (532.0, 850.5) |
| departure, w_111 (outer) | (760.0, 898.9) → (714.4, 889.2) → (486.4, 889.2) → (304.0, 850.5) |
| return, w_plan (inner) | (760.0, 272.0) → (577.6, 310.8) → (532.0, 320.5) |
| return, w_111 (outer) | (760.0, 272.0) → (714.4, 281.7) → (486.4, 281.7) → (304.0, 320.5) |

The risers run from card to card: the main workflow's from its start card's
top to its finish card's bottom; each branch's from `L` below its start card
(where its departure lateral arrives) to where its return lateral leaves.
The two junction diamonds sit at the branch point of `g_2` and the return
point of `g_3`, and there are no other marks on the lines.

## The drawing

The HTML sibling, [`worked-example.html`](worked-example.html), draws this
layout with the marks of the geometry document on both grounds, inside a
mock of the application window. What it must show: the untitled start
ellipse at the base of the main line and of each branch; the begin hull
XYZ-1 and its half-turned end hull enclosing the three steps; the plan
branch's begin and end hulls enclosing 333 and think; the three finish
keystones; the two diamonds; the two departure laterals sharing a stub at
the branch point and parting, the outer's flat lower; the two return
laterals mirroring them; the gap above step Beta opened by the branches, its
middle edge taking the slack, whilst everything at or below the departure
stays put.
