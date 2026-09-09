#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Regenerate docs/specification/worked-example.md and its HTML twin.

The Small Test domain carried through the specification: the record in canonical
form, the layout the engine's rules compute for it, and the drawing the mark
geometry makes of that layout. Every number here follows a rule stated in
docs/specification/layout-engine.md or docs/specification/mark-geometry.md; when a rule changes, change it
here and run this script, so the example never drifts from the documents.

Usage:  python3 scripts/worked_example.py   (from the repo root)
"""
import json, math, pathlib

# ---- constants: layout engine section 12, mark geometry constants ------------------------------
CARD_W, GUTTER = 188, 40
LANE = CARD_W + GUTTER
TAN12 = math.tan(math.radians(12))
RISE = LANE * TAN12
L, JMARGIN, RAMP_FLOOR, M, DIAMOND = 24, 4, 0.2, 1.5, 12
H = {'start': 58, 'begin': 58, 'end': 58, 'task': 56, 'finish': 52}
# the silhouette's insets at the centre x (mark geometry 3.9): how far the outline lies inside the box, top and bottom
INSET = {'task': (1.5, 1.5), 'begin': (9.33, 2.95), 'end': (2.95, 9.33), 'start': (5.92, 5.92), 'finish': (5.77, 3.13)}
top = lambda k: INSET[k][0]
bottom = lambda k: INSET[k][1]
# the start ellipse (geometry 3.5, 3.7): fitted at -3 degrees, major axis 0.7, size 0.85, inset on its own box
ELL = dict(rx=54.28, ry=23.05, irx=48.28, iry=17.55, icx=94.0, icy=26.5)
SCREEN = "M15.5,1.5L172.5,1.5Q186.5,1.5 186.5,15.5L186.5,40.5Q186.5,54.5 172.5,54.5L15.5,54.5Q1.5,54.5 1.5,40.5L1.5,15.5Q1.5,1.5 15.5,1.5Z"
HULL = "M1.5,7.3 Q94,14.3 186.5,1.5 L162.1,53.6 Q94,56.5 25.9,53.6 Z"
KPATH = "M10.54,19.73Q6.50,9.50 17.46,8.55L87.54,2.45Q98.50,1.50 95.88,12.18L89.12,39.82Q86.50,50.50 75.51,49.99L32.49,48.01Q21.50,47.50 17.46,37.27Z"


def air(departs, arrives):
    """Layout engine section 5: the gap between the cards' edges; the fixed edges clear the laterals on their own."""
    assert L >= (CARD_W / 2) * TAN12 + JMARGIN
    return 3 * L if (departs and arrives) else 2 * L


# ---- the domain -----------------------------------------------------------------------------------
nodes = {}
def node(id, kind, title=None, pair=None):
    n = {'id': id, 'kind': kind}
    if title is not None: n['title'] = title
    if pair: n['pair'] = pair
    if kind == 'task': n['status'] = 'todo'
    if kind in ('start', 'begin', 'task'): n['log'] = []        # a finish or end node carries no log (D11 as amended)
    nodes[id] = n
node('n_s0', 'start', ''); node('n_b1', 'begin', 'XYZ-1', 'n_e1'); node('n_a1', 'task', 'step alpha')
node('n_a2', 'task', 'step Beta'); node('n_a3', 'task', 'step gama'); node('n_e1', 'end', pair='n_b1'); node('n_f0', 'finish')
node('n_s1', 'start', ''); node('n_b2', 'begin', 'plan', 'n_e2'); node('n_t1', 'task', '333'); node('n_t2', 'task', 'think')
node('n_e2', 'end', pair='n_b2'); node('n_f1', 'finish')
node('n_s2', 'start', ''); node('n_t3', 'task', '111'); node('n_f2', 'finish')
workflows = {
    'w_main': {'id': 'w_main', 'nodes': ['n_s0', 'n_b1', 'n_a1', 'n_a2', 'n_a3', 'n_e1', 'n_f0'], 'gaps': ['g_0', 'g_1', 'g_2', 'g_3', 'g_4', 'g_5']},
    'w_plan': {'id': 'w_plan', 'nodes': ['n_s1', 'n_b2', 'n_t1', 'n_t2', 'n_e2', 'n_f1'], 'gaps': ['g_6', 'g_7', 'g_8', 'g_9', 'g_10']},
    'w_111': {'id': 'w_111', 'nodes': ['n_s2', 'n_t3', 'n_f2'], 'gaps': ['g_11', 'g_12']},
}
gaps = {f'g_{i}': {} for i in range(13)}
gaps['g_2'] = {'id': 'g_2', 'branchLeft': ['w_plan', 'w_111']}
gaps['g_3'] = {'id': 'g_3', 'returnLeft': ['w_plan', 'w_111']}
record = {'$schema': 'domain.schema.json', 'schema': 1, 'revision': 1, 'id': 'd_smalltest0', 'name': 'Small Test', 'mains': ['w_main'],
          'workflows': workflows, 'nodes': nodes, 'gaps': gaps}
record_json = json.dumps(record, indent=2, ensure_ascii=False)

# ---- the layout: heights (section 3), lanes (section 6), laterals (section 4) ------------------------
def kinds(wf): return [nodes[i]['kind'] for i in workflows[wf]['nodes']]
def line_heights(wf, u0, airs):
    ks = kinds(wf); u = [u0]
    for i in range(1, len(ks)):
        u.append(u[-1] - top(ks[i - 1]) + airs[i - 1] + H[ks[i]] - bottom(ks[i]))   # succession, silhouette to silhouette
    return u

airs_main = [2 * L] * 6; airs_main[2] = air(True, False); airs_main[3] = air(False, True)
u = {'w_main': line_heights('w_main', 0, airs_main)}
bp = u['w_main'][2] - top('task') + L                                     # the branch point of g_2, L above step alpha's silhouette top
arrive = bp + RISE                                                        # where every departure lateral arrives
foot_bottom = arrive + L - bottom('start')                                # the start cards' box bottom (the silhouette bottom is L above the arrival)
u['w_plan'] = line_heights('w_plan', foot_bottom + H['start'], [2 * L] * 5)
u['w_111'] = line_heights('w_111', foot_bottom + H['start'], [2 * L] * 2)
need = max(u['w_plan'][-1], u['w_111'][-1]) - top('finish') + L + RISE + L + H['task'] - bottom('task')
if need > u['w_main'][4]:                                                 # the return constraint lifts step gama
    shift = need - u['w_main'][4]
    for i in range(4, 7): u['w_main'][i] += shift
rp = u['w_main'][4] - H['task'] + bottom('task') - L                      # the return point of g_3, L below step gama's silhouette bottom
leave = rp - RISE                                                         # where each return lateral leaves its tail

X0 = 760
xs = {'w_main': X0, 'w_plan': X0 - LANE, 'w_111': X0 - 2 * LANE}
TOP = 30
baseY = u['w_main'][-1] + TOP
Y = lambda v: baseY - v
W, HGT = 1000, int(baseY + H['start'] + 30)
inner_rampJ, outer_rampJ = LANE * (1 - RAMP_FLOOR), LANE * RAMP_FLOOR

def lateral_pts(x1, y1, x2, y2, rampJ):
    """Section 4.1: junction-side ramp, flat, branch-side ramp; the two ramps sum to one lane."""
    d = 1 if x2 > x1 else -1; dx = abs(x2 - x1)
    rampJ = min(rampJ, dx); rampB = min(LANE - rampJ, dx - rampJ); pts = [(x1, y1)]
    if rampJ > 0: pts.append((x1 + d * rampJ, y1 - rampJ * TAN12))
    if dx > rampJ + rampB: pts.append((x2 - d * rampB, y1 - rampJ * TAN12))
    pts.append((x2, y2)); return pts

def return_pts(x_branch, rampJ):
    pts = [(X0, Y(rp))]; dx = X0 - x_branch; rampB = min(LANE - rampJ, dx - rampJ)
    pts.append((X0 - rampJ, Y(rp) + rampJ * TAN12))
    if dx > rampJ + rampB: pts.append((x_branch + rampB, Y(rp) + rampJ * TAN12))
    pts.append((x_branch, Y(leave))); return pts

laterals = {
    'departure, w_plan (inner)': lateral_pts(X0, Y(bp), xs['w_plan'], Y(arrive), inner_rampJ),
    'departure, w_111 (outer)': lateral_pts(X0, Y(bp), xs['w_111'], Y(arrive), outer_rampJ),
    'return, w_plan (inner)': return_pts(xs['w_plan'], inner_rampJ),
    'return, w_111 (outer)': return_pts(xs['w_111'], outer_rampJ),
}
centre = lambda wf, i: u[wf][i] - H[kinds(wf)[i]] / 2                      # a card's centre height
risers = {
    'w_main': (Y(centre('w_main', 0)), Y(centre('w_main', 6))),            # centre to centre
    'w_plan': (Y(arrive), Y(leave)),                                        # arrival to the tail's turn
    'w_111': (Y(arrive), Y(leave)),
}

# ---- the drawing (mark geometry) ------------------------------------------------------------------
def card(kind, title, x, v):
    left, top = x - CARD_W / 2, Y(v); g = f'<g transform="translate({left:.1f} {top:.1f})">'
    if kind == 'task':
        g += (f'<path class="todo" d="{SCREEN}"/><path class="inner" transform="translate(7 3.5) scale(0.9202 0.8750)" d="{SCREEN}"/>'
              f'<circle class="gtodo" cx="27" cy="26" r="4.5"/><text class="lbl" x="39" y="30.5">{title}</text><text class="tag" x="16" y="47">TO DO</text>')
    elif kind == 'begin':
        tw = 7.2 * len(title); gx = 94 - (tw + 7 + 11) / 2
        g += (f'<path class="proj" d="{HULL}"/><path class="tint" transform="translate(8 4) scale(0.9309 0.7931)" d="{HULL}"/>'
              f'<circle class="gproj" cx="{gx + 5.5:.1f}" cy="30" r="5.5"/><text class="lbl" x="{gx + 18:.1f}" y="34.5">{title}</text>')
    elif kind == 'end':
        g += (f'<path class="proj" transform="translate(188 58) scale(-1 -1)" d="{HULL}"/>'
              f'<path class="tint" transform="translate(188 58) scale(-1 -1) translate(8 4) scale(0.9309 0.7931)" d="{HULL}"/>')
    elif kind == 'start':
        g += (f'<g transform="rotate(-3 94 29)"><ellipse class="line" cx="94" cy="29" rx="{ELL["rx"]}" ry="{ELL["ry"]}"/>'
              f'<ellipse class="inner" cx="{ELL["icx"]}" cy="{ELL["icy"]}" rx="{ELL["irx"]}" ry="{ELL["iry"]}"/></g>')
        if title: g += f'<text class="lbl mid" x="94" y="33.5">{title}</text>'
    else:
        g += (f'<g transform="rotate(2 94 26) translate(44 0)"><path class="line" d="{KPATH}"/>'
              f'<path class="inner" transform="translate(7 3) scale(0.8800 0.7692)" d="{KPATH}"/></g>')
    return g + '</g>'

svg = [f'<path class="track riser" d="M{xs[wf]},{a:.1f} L{xs[wf]},{b:.1f}"/>' for wf, (a, b) in risers.items()]
for pts in laterals.values():
    svg.append(f'<path class="track lat" d="M{" L".join(f"{x:.1f},{y:.1f}" for x, y in pts)}"/>')
half = DIAMOND / 2
points = []                                                               # every gap's two points, on every line (geometry section 9)
for wf in workflows:
    ks = kinds(wf); x = xs[wf]
    for i in range(len(ks) - 1):
        y_bp = u[wf][i] - top(ks[i]) + L                                  # the branch point, L above the lower silhouette
        y_rp = u[wf][i + 1] - H[ks[i + 1]] + bottom(ks[i + 1]) - L         # the return point, L below the upper silhouette
        ys = [(y_bp + y_rp) / 2] if abs(y_bp - y_rp) < 1e-6 else [y_bp, y_rp]
        for v in ys:
            points.append((x, v)); yy = Y(v)
            svg.append(f'<rect class="line" x="{x - half}" y="{yy - half:.1f}" width="{DIAMOND}" height="{DIAMOND}" transform="rotate(45 {x} {yy:.1f})"/>')
for wf in workflows:
    for nid, v in zip(workflows[wf]['nodes'], u[wf]):
        svg.append(card(nodes[nid]['kind'], nodes[nid].get('title', ''), xs[wf], v))
scene = '\n'.join(svg)

# ---- the tables ---------------------------------------------------------------------------------------
rows = []
for wf in workflows:
    for nid, v in zip(workflows[wf]['nodes'], u[wf]):
        k = nodes[nid]['kind']
        rows.append((nid, k, nodes[nid].get('title', ''), wf, xs[wf], round(v, 1), H[k], round(Y(v), 1)))
md_rows = '\n'.join(f'| `{r[0]}` | {r[1]} | {r[2]} | `{r[3]}` | {r[4]} | {r[5]} | {r[6]} | {r[7]} |' for r in rows)
html_rows = ''.join('<tr>' + ''.join(f'<td>{c if i not in (0, 3) else f"<code>{c}</code>"}</td>' for i, c in enumerate(r)) + '</tr>' for r in rows)
lat_md = '\n'.join(f'| {name} | {" → ".join(f"({x:.1f}, {y:.1f})" for x, y in pts)} |' for name, pts in laterals.items())
lat_html = ''.join(f'<tr><td>{name}</td><td>{" → ".join(f"({x:.1f}, {y:.1f})" for x, y in pts)}</td></tr>' for name, pts in laterals.items())
ris_md = '\n'.join(f'| `{wf}` | x = {xs[wf]}, from screen y {a:.1f} to {b:.1f} |' for wf, (a, b) in risers.items())
ris_html = ''.join(f'<tr><td><code>{wf}</code></td><td>x = {xs[wf]}, from screen y {a:.1f} to {b:.1f}</td></tr>' for wf, (a, b) in risers.items())
quant = [
    ('air of an ordinary gap, 2L', f'{2 * L}'),
    ('air of `g_2` (departures) and of `g_3` (arrivals) before the branches stretch them', f'{air(True, False)}'),
    ('the least distance between two cards, 2L', f'{2 * L}'),
    ('the branch point of `g_2` (u)', f'{bp:.1f}'),
    ('where the departure laterals arrive, L below the start ellipses\' silhouette bottom (u)', f'{arrive:.1f}'),
    ("the start cards' box bottom, every departing branch (u)", f'{foot_bottom:.1f}'),
    ('the return point of `g_3` (u)', f'{rp:.1f}'),
    ("where each return lateral leaves its branch's tail (u)", f'{leave:.1f}'),
    ("the tail of `w_plan`, from its finish keystone's silhouette top to the turn", f'{leave - (u["w_plan"][-1] - top("finish")):.1f}'),
    ('the tail of `w_111`', f'{leave - (u["w_111"][-1] - top("finish")):.1f}'),
    ('the middle edge of `g_3`, opened by the branches', f'{(u["w_main"][4] - H["task"] + bottom("task")) - (u["w_main"][3] - top("task")) - 2 * L:.1f}'),
    ('junction-side ramps at the shared points, inner and outer', f'{inner_rampJ:.1f} and {outer_rampJ:.1f}'),
    ('baseY, the screen y of u = 0', f'{baseY:.1f}'),
]
quant_md = '| Quantity | Value |\n| --- | --- |\n' + '\n'.join(f'| {a} | {b} |' for a, b in quant)
quant_html = '<table><thead><tr><th>Quantity</th><th>Value</th></tr></thead><tbody>' + ''.join(f'<tr><td>{a.replace("`", "")}</td><td>{b}</td></tr>' for a, b in quant) + '</tbody></table>'

# ---- the markdown ---------------------------------------------------------------------------------------
md = f"""<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0
-->

# A worked example: the Small Test domain

One small domain carried all the way through: its record in the on-disk canonical form, the layout the [layout engine](layout-engine.md) computes for it, and the drawing the [mark geometry](mark-geometry.md) makes of that layout, which the HTML sibling of this file renders. It is a fixture: an implementation that produces these numbers from this record, and this picture from these numbers, has the layout and the marks right. It also shows, on one screen, how a domain reads: two branches leaving one point on the left and returning to one point above, a project inside the main workflow and another inside a branch, the start and finish nodes of every workflow, and a diamond at every point where a branch may depart or arrive. The file is generated by `scripts/worked_example.py` from the rules; when a rule changes, the script changes and the example is regenerated, so the two cannot drift.

The domain: a main workflow whose start node is untitled, holding the project XYZ-1 with the tasks step alpha, step Beta, and step gama; a branch workflow departing on the left above step alpha and returning above step Beta, whose whole content is the project "plan" holding 333 and think; and a second, outer branch departing and returning at the same two points, holding the single task 111. Every task is to do; no node has a note or a log entry.

## The record

`domain.json`, in the canonical form of the [persistence](persistence.md) document (ids shortened to read; real ids are the twelve characters of the structural model, section 1):

```json
{record_json}
```

## The layout

Constants as the layout engine's section 12 gives them: card width 188, lane step 228, `L` 24, `junctionMargin` 4, `rampFloor` 0.2, rise {RISE:.1f}. `u` is a card's box top above the baseline, up positive, with the main start node's box top at zero; gaps are measured between the silhouettes where the line passes through them, using the insets of the mark geometry's section 3.9 (task 1.5 and 1.5; begin 9.33 and 2.95; end 2.95 and 9.33; start 5.92 and 5.92; finish 5.77 and 3.13, top and bottom); screen `y` is `baseY - u` with the baseline placed so that the drawing fits, and the main workflow's line at `x = 760`, the branches one and two lanes to its left.

| Node | Kind | Title | Workflow | x | u (box top) | Height | Screen y of the box top |
| --- | --- | --- | --- | --- | --- | --- | --- |
{md_rows}

{quant_md}

The laterals, as point lists in screen coordinates, each a ramp, a flat, and a ramp with the fan split at the shared points (the inner sibling's junction-side ramp longest):

| Lateral | Points |
| --- | --- |
{lat_md}

The risers, in screen coordinates: the main workflow's from the centre of its start card to the centre of its finish card, behind the cards; each branch's from where its departure lateral arrives, `L` beneath its start ellipse's silhouette, to where its return lateral leaves, above its finish keystone.

| Riser | Extent |
| --- | --- |
{ris_md}

A diamond, 12 on a side, marks every branch and return point whether or not a branch attaches there: one at the midpoint of each of the twelve shut gaps, where the gap's two points coincide, and two in `g_3`, whose middle edge the branches have opened, its branch point `L` above step Beta's silhouette and its return point `L` below step gama's. Fourteen diamonds on the three lines, and no other marks. Every shut gap is 48 between silhouettes at the line: from the main start ellipse to the XYZ-1 hull, from the hull to step alpha, from step alpha to step Beta, and so on up the line.

## The drawing

The HTML sibling, [`worked-example.html`](worked-example.html), draws this layout with the marks of the geometry document on both grounds, inside a mock of the application window. What it must show: the untitled start ellipse at the base of the main line and of each branch, its riser rising from behind it; the begin hull XYZ-1 and its half-turned end hull enclosing the three steps; the plan branch's begin and end hulls enclosing 333 and think; the three finish keystones, each with its riser ending behind it; a diamond in every gap, two in the opened one; the two departure laterals sharing a stub at the branch point and parting, the outer's flat lower; the two return laterals mirroring them; the gap above step Beta opened by the branches, its middle edge taking the slack, whilst everything at or below the departure stays put.
"""
pathlib.Path('docs/specification/worked-example.md').write_text(md)

# ---- the html -------------------------------------------------------------------------------------------
def window(theme):
    on = lambda t: 'on' if theme == t else ''
    return f'''<div class="win {theme}">
 <div class="bar"><span class="brand">PENSAFORMA</span><span class="sel">Small Test <span>▾</span></span><span class="btn icon danger">✕</span><span class="btn"><span class="dot"></span>MCP</span>
  <span class="right"><span class="seglbl">MODE</span><span class="seg"><span class="{on('azure')}">Light</span><span class="{on('navy')}">Dark</span></span><span class="btn">Flagged</span><span class="btn icon">−</span><span class="pct">80%</span><span class="btn icon">+</span><span class="btn primary">Fit</span></span></div>
 <div class="canvas"><svg width="{W}" height="{HGT}" viewBox="0 0 {W} {HGT}">{scene}</svg></div>
</div>'''
html = f'''<!DOCTYPE html>
<!--
SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
SPDX-License-Identifier: CC-BY-4.0

Presentation sibling of worked-example.md, generated by scripts/worked_example.py.
The Markdown is canonical; if the two drift, the Markdown wins and this file
is regenerated. One self-contained file: inline style, no script, no network,
system fonts (the application's own faces are named in the chrome document's
Appendix B).
-->
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>PensaForma worked example</title>
<style>
body{{margin:0;background:#efe9dc;font:14px/1.5 -apple-system,Helvetica,Arial,sans-serif;color:#173242;padding:24px}}
.wrap{{max-width:1040px;margin:0 auto}} h1{{font-size:22px;margin:0 0 6px}} h2{{font-size:16px;margin:28px 0 8px}} p{{max-width:72ch;color:#3d4f5a}}
table{{border-collapse:collapse;font-size:12.5px;margin:8px 0 16px}} th,td{{border:1px solid #cfc6b3;padding:4px 8px;text-align:left;vertical-align:top}} th{{background:#e7e0cf}}
pre{{background:#161412;color:#ece5d4;padding:12px 14px;border-radius:8px;font-size:11.5px;overflow:auto;max-height:420px}}
.win{{border-radius:10px;overflow:hidden;margin:12px 0 18px;box-shadow:0 10px 30px rgba(0,0,0,.18);background:var(--ground)}}
.azure{{--ground:#d3e6ef;--panel:#f8f3e8;--ink:#173242;--line:#365b6c;--muted:#5f7d8b;--grid:rgba(23,50,66,.10);--c-todo:#d9a53a;--teal:#1f8f8a;--tint:#cbe6e4;--cursor:#d75f2e}}
.navy{{--ground:#0f2334;--panel:#1a3a54;--ink:#e8f1f6;--line:#6fb6c9;--muted:#93b3c2;--grid:rgba(111,182,201,.13);--c-todo:#f0bd55;--teal:#37c2ba;--tint:#356e69;--cursor:#f27a44}}
.bar{{display:flex;align-items:center;gap:12px;padding:9px 14px;border-bottom:1px solid var(--line);color:var(--ink);font-size:12px}}
.brand{{font-weight:800;letter-spacing:.06em;font-size:13px}} .sel,.btn{{border:1px solid var(--line);border-radius:5px;padding:6px 10px}}
.btn.icon{{width:30px;text-align:center;padding:6px 0}} .btn.danger{{color:var(--cursor);border-color:#8f5d4a}} .btn.primary{{background:var(--ink);color:var(--ground)}}
.dot{{display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--teal);margin-right:7px;box-shadow:inset 0 0 0 1px rgba(0,0,0,.25)}}
.right{{margin-left:auto;display:flex;align-items:center;gap:12px}} .seglbl{{font-size:10px;letter-spacing:.12em;color:var(--muted)}}
.seg{{border:1px solid var(--line);border-radius:999px;overflow:hidden;display:inline-flex}} .seg span{{padding:6px 14px;color:var(--muted)}} .seg span.on{{background:var(--ink);color:var(--ground)}}
.pct{{font-size:11px;color:var(--muted);min-width:42px;text-align:center}}
.canvas{{background-color:var(--ground);background-image:radial-gradient(circle, var(--grid) 1px, transparent 1.4px);background-size:40px 40px;display:flex;justify-content:center;padding:10px 0}}
.canvas svg{{zoom:0.8}}
.line{{fill:var(--line)}} .inner{{fill:var(--panel)}} .todo{{fill:var(--c-todo)}} .gtodo{{fill:none;stroke:var(--c-todo);stroke-width:2}}
.proj{{fill:var(--teal)}} .tint{{fill:var(--tint)}} .gproj{{fill:var(--teal)}}
.track{{fill:none;stroke:var(--line);stroke-linecap:round;stroke-linejoin:round}} .riser{{stroke-width:3}} .lat{{stroke-width:2.3}}
.lbl{{font:600 13px -apple-system,Helvetica,Arial,sans-serif;fill:var(--ink)}} .lbl.mid{{text-anchor:middle}}
.tag{{font:600 8px -apple-system,Helvetica,Arial,sans-serif;fill:var(--muted);letter-spacing:.08em}}
</style></head><body><div class="wrap">
<h1>A worked example: the Small Test domain</h1>
<p>One small domain carried all the way through: its record, the layout the engine computes for it, and the drawing the mark geometry makes of that layout. An implementation that produces these numbers from this record, and this picture from these numbers, has the layout and the marks right. The canonical text is <code>worked-example.md</code>, beside this file; both are generated by <code>scripts/worked_example.py</code>.</p>
<h2>The drawing, on both grounds</h2>
{window('azure')}
{window('navy')}
<h2>The record</h2>
<pre>{record_json}</pre>
<h2>The layout</h2>
<p>Card width 188, lane step 228, <code>L</code> 24, <code>junctionMargin</code> 4, <code>rampFloor</code> 0.2, rise {RISE:.1f}. <code>u</code> is a card's top above the baseline, up positive, the main start card's top at zero; gaps are measured between the silhouettes where the line passes through them, with the insets of the mark geometry's section 3.9; screen <code>y</code> is <code>baseY − u</code> with <code>baseY</code> {baseY:.1f}; the main line is at <code>x</code> = 760 and the branches one and two lanes to its left.</p>
<table><thead><tr><th>Node</th><th>Kind</th><th>Title</th><th>Workflow</th><th>x</th><th>u (box top)</th><th>Height</th><th>Screen y of the box top</th></tr></thead><tbody>{html_rows}</tbody></table>
{quant_html}
<table><thead><tr><th>Lateral</th><th>Points (screen)</th></tr></thead><tbody>{lat_html}</tbody></table>
<table><thead><tr><th>Riser</th><th>Extent (screen)</th></tr></thead><tbody>{ris_html}</tbody></table>
<p>Canonical source: <code>worked-example.md</code>, beside this file. If they drift, the Markdown wins.</p>
</div></body></html>'''
pathlib.Path('docs/specification/worked-example.html').write_text(html)
print(f'written: size {W}x{HGT}, baseY {baseY:.1f}, bp {bp:.1f}, arrive {arrive:.1f}, rp {rp:.1f}, leave {leave:.1f}')
