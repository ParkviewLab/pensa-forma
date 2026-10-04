#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Regenerate docs/specification/worked-example.md and its HTML twin.

The Small Test domain carried through the specification: the record in canonical
form, the layout the engine's rules compute for it, and the drawing Googie, the
default style, makes of that layout. Every number here follows a rule stated in
docs/specification/layout-engine.md, style-contract.md, or style-googie.md; when a rule
changes, change it here and run this script, so the example never drifts from the
documents. The script draws Googie itself and checks its drawing against the design
page's exported golden masters, styles-masters.json; any drift fails the run.

Usage:  python3 scripts/worked_example.py   (from the repo root)
"""
import json, math, pathlib, re, sys

# ---- constants: layout engine section 12, Googie's constructions -------------------------------
CARD_W, GUTTER = 188, 40
LANE = CARD_W + GUTTER
RAMP_ANGLE = 12                                   # degrees; a parameter, changed in one place
TAN_A = math.tan(math.radians(RAMP_ANGLE))
RISE = LANE * TAN_A
JMARGIN, RAMP_FLOOR, M, DIAMOND = 4, 0.2, 1.5, 12
L = math.ceil((CARD_W / 2) * TAN_A + JMARGIN)     # layout engine section 5: 19.98 + 4, so 24 at the defaults
H = {'start': 58, 'begin': 58, 'end': 58, 'task': 56, 'finish': 52}
PILL = 16                                         # a here card measures 16 taller, for the HERE pill (style contract, section 2)
# the silhouette's insets at the centre x (Googie, section 5.9): how far the outline lies inside the box, top and bottom;
# 'here' is the marquee at 72, m + 0.07h
INSET = {'task': (1.5, 1.5), 'here': (6.54, 6.54), 'begin': (9.33, 2.95), 'end': (2.95, 9.33), 'start': (5.92, 5.92), 'finish': (5.77, 3.13)}
# the start ellipse (Googie 5.5, 5.7): fitted at -3 degrees, major axis 0.7, size 0.85, inset on its own box
ELL = dict(rx=54.28, ry=23.05, irx=48.28, iry=17.55, icx=94.0, icy=26.5)
SCREEN = "M 15.5,1.5 H 172.5 A 14 14 0 0 1 186.5,15.5 V 40.5 A 14 14 0 0 1 172.5,54.5 H 15.5 A 14 14 0 0 1 1.5,40.5 V 15.5 A 14 14 0 0 1 15.5,1.5 Z"
MARQUEE = "M 1.5,1.5 Q 94,11.58 186.5,1.5 Q 177.1,36 186.5,70.5 Q 94,60.42 1.5,70.5 Q 10.9,36 1.5,1.5 Z"
HULL = "M 1.5,7.3 Q 94,14.26 186.5,1.5 L 162.06,53.6 Q 94,56.5 25.94,53.6 Z"
KPATH = "M 17.46,8.55 L 87.54,2.45 Q 98.5,1.5 95.88,12.18 L 89.12,39.82 Q 86.5,50.5 75.51,49.99 L 32.49,48.01 Q 21.5,47.5 17.46,37.27 L 10.54,19.73 Q 6.5,9.5 17.46,8.55 Z"
# the atom (Googie, section 10) and the sputnik (section 9)
ORB = [(72, 12, -30, -38), (66, 13, 40, 215), (68, 11, 103, -38)]
RAYS = [(-6, 1.0), (30, 0.66), (63, 1.12), (99, 0.58), (138, 0.9), (177, 1.2), (210, 0.68), (246, 1.02), (285, 0.82), (318, 1.08)]
G = 1.15                                          # the common glyphs, drawn 15 % above the 11 envelope (style contract, section 3)


def check_masters():
    """Decision 15: this drawing is the script's own, and must agree with the design page's export to two decimals."""
    path = pathlib.Path('docs/specification/styles-masters.json')
    m = json.loads(path.read_text())['styles']['googie']['masters']
    nums = lambda t: [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', t)]
    def same(mine, theirs, what):
        a, b = nums(mine), nums(theirs)
        if len(a) != len(b) or any(abs(x - y) > 0.051 for x, y in zip(a, b)):
            sys.exit(f'worked_example.py: Googie {what} drifts from styles-masters.json')
    def outer(svg):
        return re.search(r' d="([^"]+)"', svg).group(1)
    same(SCREEN, outer(m['task']['svg']), 'screen')
    same(MARQUEE, outer(m['here card']['svg']), 'marquee')
    same(HULL, outer(m['begin node']['svg']), 'hull')
    same(KPATH, outer(m['finish node']['svg']), 'keystone')
    e = nums(re.search(r'<ellipse[^>]*>', m['start node']['svg']).group(0))
    same(f'94 29 {ELL["rx"]} {ELL["ry"]}', ' '.join(map(str, e)), 'start ellipse')
    same(atom(0, 0, 195.5, 28.5), m['flag on a task']['svg'], 'atom')
    same(sputnik(), m['here mark']['svg'], 'sputnik')


def air(departs, arrives):
    """Layout engine section 5: the gap between the cards' edges; the fixed edges clear the laterals on their own."""
    assert L >= (CARD_W / 2) * TAN_A + JMARGIN
    return 3 * L if (departs and arrives) else 2 * L


# ---- the domain -----------------------------------------------------------------------------------
nodes = {}
DONE_AT = '2026-09-17T12:00:00Z'
def node(id, kind, title=None, pair=None, status='todo', here=False, flagged=False):
    n = {'id': id, 'kind': kind}
    if title is not None: n['title'] = title
    if title: assert title not in {m.get('title') for m in nodes.values()}, f'duplicate title {title!r} (I19)'
    if pair: n['endNode' if kind == 'begin' else 'beginNode'] = pair
    if kind == 'task':
        n['status'] = status
        if status == 'completed': n['completedAt'] = DONE_AT
        if here: n['here'] = True
    if flagged: n['flagged'] = True
    if kind in ('start', 'begin', 'task'): n['log'] = []        # a finish or end node carries no log (D11 as amended)
    nodes[id] = n
node('n_s0', 'start', ''); node('n_b1', 'begin', 'XYZ-1', 'n_e1', flagged=True)
node('n_a1', 'task', 'step alpha', status='completed', flagged=True); node('n_a2', 'task', 'step Beta', status='cancelled')
node('n_a3', 'task', 'step gama', status='in-progress', here=True, flagged=True); node('n_e1', 'end', pair='n_b1'); node('n_f0', 'finish')
node('n_s1', 'start', 'doppleganger', flagged=True); node('n_b2', 'begin', 'plan', 'n_e2'); node('n_t0', 'task', 'prepare', status='completed', here=True)
node('n_t1', 'task', '333', status='in-progress'); node('n_t2', 'task', 'think'); node('n_e2', 'end', pair='n_b2'); node('n_f1', 'finish')
node('n_s2', 'start', 'Workflow Fröbel'); node('n_t3', 'task', '111', flagged=True); node('n_t4', 'task', '222', status='in-progress', flagged=True)
node('n_f2', 'finish')
workflows = {
    'w_main': {'id': 'w_main', 'nodes': ['n_s0', 'n_b1', 'n_a1', 'n_a2', 'n_a3', 'n_e1', 'n_f0'], 'gaps': ['g_0', 'g_1', 'g_2', 'g_3', 'g_4', 'g_5']},
    'w_plan': {'id': 'w_plan', 'nodes': ['n_s1', 'n_b2', 'n_t0', 'n_t1', 'n_t2', 'n_e2', 'n_f1'], 'gaps': ['g_6', 'g_7', 'g_8', 'g_9', 'g_10', 'g_11']},
    'w_111': {'id': 'w_111', 'nodes': ['n_s2', 'n_t3', 'n_t4', 'n_f2'], 'gaps': ['g_12', 'g_13', 'g_14']},
}
gaps = {f'g_{i}': {} for i in range(15)}
gaps['g_2'] = {'id': 'g_2', 'branchLeft': ['w_plan', 'w_111']}
gaps['g_3'] = {'id': 'g_3', 'returnLeft': ['w_plan', 'w_111']}
record = {'$schema': 'domain.schema.json', 'schema': 1, 'revision': 1, 'id': 'd_smalltest0', 'name': 'Small Test', 'mains': ['w_main'],
          'workflows': workflows, 'nodes': nodes, 'gaps': gaps}
record_json = json.dumps(record, indent=2, ensure_ascii=False)

# ---- the layout: heights (section 3), lanes (section 6), laterals (section 4) ------------------------
def shape(nid):
    n = nodes[nid]; return 'here' if n.get('here') else n['kind']
def hgt(nid): return H[nodes[nid]['kind']] + (PILL if nodes[nid].get('here') else 0)
top = lambda nid: INSET[shape(nid)][0]
bottom = lambda nid: INSET[shape(nid)][1]
def kinds(wf): return [nodes[i]['kind'] for i in workflows[wf]['nodes']]
def line_heights(wf, u0, airs):
    ids = workflows[wf]['nodes']; u = [u0]
    for i in range(1, len(ids)):
        u.append(u[-1] - top(ids[i - 1]) + airs[i - 1] + hgt(ids[i]) - bottom(ids[i]))   # succession, silhouette to silhouette
    return u

M_ = workflows['w_main']['nodes']
airs_main = [2 * L] * 6; airs_main[2] = air(True, False); airs_main[3] = air(False, True)
u = {'w_main': line_heights('w_main', 0, airs_main)}
bp = u['w_main'][2] - top(M_[2]) + L                                     # the branch point of g_2, L above step alpha's silhouette top
arrive = bp + RISE                                                        # where every departure lateral arrives
foot_bottom = arrive + L - INSET['start'][1]                              # the start cards' box bottom (the silhouette bottom is L above the arrival)
u['w_plan'] = line_heights('w_plan', foot_bottom + H['start'], [2 * L] * 6)
u['w_111'] = line_heights('w_111', foot_bottom + H['start'], [2 * L] * 3)
need = max(u['w_plan'][-1], u['w_111'][-1]) - INSET['finish'][0] + L + RISE + L + hgt(M_[4]) - bottom(M_[4])
if need > u['w_main'][4]:                                                 # the return constraint lifts step gama
    shift = need - u['w_main'][4]
    for i in range(4, 7): u['w_main'][i] += shift
rp = u['w_main'][4] - hgt(M_[4]) + bottom(M_[4]) - L                      # the return point of g_3, L below step gama's silhouette bottom
leave = rp - RISE                                                         # where each return lateral leaves its tail

X0 = 760
xs = {'w_main': X0, 'w_plan': X0 - LANE, 'w_111': X0 - 2 * LANE}
TOP = 30
baseY = u['w_main'][-1] + TOP
Y = lambda v: baseY - v
W, HGT = 1000, int(baseY + H['start'] + 30)
inner_rampJ, outer_rampJ = LANE * (1 - RAMP_FLOOR), LANE * RAMP_FLOOR

def lateral_pts(x1, y1, x2, y2, rampJ):
    """Section 4.1, Googie's route: junction-side ramp, flat, branch-side ramp; the two ramps sum to one lane."""
    d = 1 if x2 > x1 else -1; dx = abs(x2 - x1)
    rampJ = min(rampJ, dx); rampB = min(LANE - rampJ, dx - rampJ); pts = [(x1, y1)]
    if rampJ > 0: pts.append((x1 + d * rampJ, y1 - rampJ * TAN_A))
    if dx > rampJ + rampB: pts.append((x2 - d * rampB, y1 - rampJ * TAN_A))
    pts.append((x2, y2)); return pts

def return_pts(x_branch, rampJ):
    pts = [(X0, Y(rp))]; dx = X0 - x_branch; rampB = min(LANE - rampJ, dx - rampJ)
    pts.append((X0 - rampJ, Y(rp) + rampJ * TAN_A))
    if dx > rampJ + rampB: pts.append((x_branch + rampB, Y(rp) + rampJ * TAN_A))
    pts.append((x_branch, Y(leave))); return pts

laterals = {
    'departure, w_plan (inner)': lateral_pts(X0, Y(bp), xs['w_plan'], Y(arrive), inner_rampJ),
    'departure, w_111 (outer)': lateral_pts(X0, Y(bp), xs['w_111'], Y(arrive), outer_rampJ),
    'return, w_plan (inner)': return_pts(xs['w_plan'], inner_rampJ),
    'return, w_111 (outer)': return_pts(xs['w_111'], outer_rampJ),
}
centre = lambda wf, i: u[wf][i] - hgt(workflows[wf]['nodes'][i]) / 2      # a card's centre height
risers = {
    'w_main': (Y(centre('w_main', 0)), Y(centre('w_main', 6))),            # centre to centre
    'w_plan': (Y(arrive), Y(leave)),                                        # arrival to the tail's turn
    'w_111': (Y(arrive), Y(leave)),
}

# ---- the drawing (Googie) -------------------------------------------------------------------------
f2 = lambda n: f'{round(n, 2):g}'
STATUS = {'todo': ('todo', 'TO DO'), 'in-progress': ('progress', 'IN PROGRESS'), 'completed': ('done', 'DONE'), 'cancelled': ('cancel', 'CANCELLED')}

def glyph(st, x, y):
    """The common glyphs (style contract, section 3): triangle, circle, square, dashed circle."""
    c = f'g{st}'
    if st == 'todo':
        s_ = 13 * G; th = s_ * math.sqrt(3) / 2; cy = y + 1
        return f'<path class="{c}" d="M {f2(x)},{f2(cy - 2 * th / 3)} L {f2(x + s_ / 2)},{f2(cy + th / 3)} L {f2(x - s_ / 2)},{f2(cy + th / 3)} Z"/>'
    if st == 'progress': return f'<circle class="{c}" cx="{x}" cy="{y}" r="{f2(5.5 * G)}"/>'
    if st == 'done':
        a = 11 * G; return f'<rect class="{c}" x="{f2(x - a / 2)}" y="{f2(y - a / 2)}" width="{f2(a)}" height="{f2(a)}"/>'
    return f'<circle class="{c}" cx="{x}" cy="{y}" r="{f2(4.75 * G)}"/>'

def atom(dx, dy, cx, cy):
    """Googie's flag (section 10): the orbits drawn as one emblem in ink."""
    g = ''
    for rx, ry, ang, t in ORB:
        a, b = rx * 0.60, ry * 0.60 * 1.65
        g += (f'<ellipse class="ring" cx="{f2(cx)}" cy="{f2(cy)}" rx="{f2(a)}" ry="{f2(b)}" stroke-width="1.8" stroke-opacity="0.7" '
              f'transform="rotate({ang} {f2(cx)} {f2(cy)})"/>')
        lx, ly = a * math.cos(math.radians(t)), b * math.sin(math.radians(t)); r_ = math.radians(ang)
        g += f'<circle class="ink" r="{f2(4 * 0.6 * 1.8)}" cx="{f2(cx + lx * math.cos(r_) - ly * math.sin(r_))}" cy="{f2(cy + lx * math.sin(r_) + ly * math.cos(r_))}"/>'
    return g + f'<circle class="ink" r="{f2(4 * 0.6 * 2.75)}" cx="{f2(cx)}" cy="{f2(cy)}"/>'

def sputnik(cx=-17.5, cy=32, k=1.2):
    """Googie's here mark (section 9), placed to the left of the card and drawn last."""
    g = f'<g transform="translate({cx} {cy}) scale({k})">'
    for deg, fac in RAYS:
        tx, ty = 15 * fac * math.cos(math.radians(deg)), 15 * fac * math.sin(math.radians(deg))
        g += f'<line class="ray" x1="0" y1="0" x2="{f2(tx)}" y2="{f2(ty)}" stroke-width="1.4"/><circle class="ink" r="2.2" cx="{f2(tx)}" cy="{f2(ty)}"/>'
    return g + '<circle class="ink" r="2.8"/></g>'

def card(nid, x, v):
    n = nodes[nid]; kind = n['kind']; title = n.get('title', ''); h = hgt(nid)
    left, top_ = x - CARD_W / 2, Y(v); g = f'<g transform="translate({left:.1f} {top_:.1f})">'; over = ''
    if kind == 'task':
        st, tag = STATUS[n['status']]
        if n.get('here'):
            g += f'<path class="{st}" d="{MARQUEE}"/><path class="inner" transform="translate(5 6) scale(0.9309 0.8611)" d="{MARQUEE}"/>'
        else:
            g += f'<path class="{st}" d="{SCREEN}"/><path class="inner" transform="translate(7 3.5) scale(0.9202 0.8750)" d="{SCREEN}"/>'
        cls = 'lbl struck' if st == 'cancel' else 'lbl'
        g += glyph(st, 29, 26) + f'<text class="{cls}" x="41" y="30.5">{title}</text><text class="tag" x="18" y="46">{tag}</text>'
        if n.get('here'):
            g += '<rect class="pill" x="18" y="51.5" width="34" height="12" rx="6"/><text class="pilltxt" x="35" y="60.3">HERE</text>'
        if n.get('flagged'): over += atom(0, 0, CARD_W + 7.5, h / 2 + 0.5)
    elif kind == 'begin':
        g += (f'<path class="proj" d="{HULL}"/><path class="tint" transform="translate(8 4) scale(0.9309 0.7931)" d="{HULL}"/>'
              f'<text class="lbl mid" x="94" y="34.5">{title}</text>')
        if n.get('flagged'): over += atom(0, 0, CARD_W - M - 0.13 * CARD_W / 2 + 7.5, h / 2 + 0.5)
    elif kind == 'end':
        g += (f'<path class="proj" transform="translate(188 58) scale(-1 -1)" d="{HULL}"/>'
              f'<path class="tint" transform="translate(188 58) scale(-1 -1) translate(8 4) scale(0.9309 0.7931)" d="{HULL}"/>')
    elif kind == 'start':
        g += (f'<g transform="rotate(-3 94 29)"><ellipse class="line" cx="94" cy="29" rx="{ELL["rx"]}" ry="{ELL["ry"]}"/>'
              f'<ellipse class="inner" cx="{ELL["icx"]}" cy="{ELL["icy"]}" rx="{ELL["irx"]}" ry="{ELL["iry"]}"/></g>')
        words = title.split(' ') if title else []
        lines = [' '.join(words)] if len(title) <= 12 else words[:2]      # the start label wraps to 68.3 (Googie, section 7)
        for i, line in enumerate(lines):
            g += f'<text class="lbl start mid" x="94" y="{f2(33 + (i - (len(lines) - 1) / 2) * 13)}">{line}</text>'
        if n.get('flagged'): over += atom(0, 0, 94 + ELL['rx'] * math.cos(math.radians(3)) + 7.5, h / 2 + 0.5)
    else:
        g += (f'<g transform="rotate(2 94 26) translate(44 0)"><path class="line" d="{KPATH}"/>'
              f'<path class="inner" transform="translate(7 3) scale(0.8800 0.7692)" d="{KPATH}"/></g>')
    here = f'<g transform="translate({left:.1f} {top_:.1f})">{sputnik()}</g>' if n.get('here') else ''
    return g + over + '</g>', here

svg = [f'<path class="track riser" d="M{xs[wf]},{a:.1f} L{xs[wf]},{b:.1f}"/>' for wf, (a, b) in risers.items()]
for pts in laterals.values():
    svg.append(f'<path class="track lat" d="M{" L".join(f"{x:.1f},{y:.1f}" for x, y in pts)}"/>')
half = DIAMOND / 2
points = []                                                               # every gap's two points, on every line (Googie, section 13)
for wf in workflows:
    ids = workflows[wf]['nodes']; x = xs[wf]
    for i in range(len(ids) - 1):
        y_bp = u[wf][i] - top(ids[i]) + L                                 # the branch point, L above the lower silhouette
        y_rp = u[wf][i + 1] - hgt(ids[i + 1]) + bottom(ids[i + 1]) - L     # the return point, L below the upper silhouette
        ys = [(y_bp + y_rp) / 2] if abs(y_bp - y_rp) < 1e-6 else [y_bp, y_rp]
        for v in ys:
            points.append((x, v)); yy = Y(v)
            svg.append(f'<rect class="line" x="{x - half}" y="{yy - half:.1f}" width="{DIAMOND}" height="{DIAMOND}" transform="rotate(45 {x} {yy:.1f})"/>')
here_marks = []
for wf in workflows:
    for nid, v in zip(workflows[wf]['nodes'], u[wf]):
        body, here = card(nid, xs[wf], v); svg.append(body)
        if here: here_marks.append(here)
svg += here_marks                                                         # the here marks are drawn last, over everything
scene = '\n'.join(svg)
check_masters()

# ---- the tables ---------------------------------------------------------------------------------------
rows = []
for wf in workflows:
    for nid, v in zip(workflows[wf]['nodes'], u[wf]):
        k = nodes[nid]['kind']
        rows.append((nid, k, nodes[nid].get('title', ''), wf, xs[wf], round(v, 1), hgt(nid), round(Y(v), 1)))
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
    ("the tail of `w_plan`, from its finish keystone's silhouette top to the turn", f'{leave - (u["w_plan"][-1] - INSET["finish"][0]):.1f}'),
    ('the tail of `w_111`', f'{leave - (u["w_111"][-1] - INSET["finish"][0]):.1f}'),
    ('the middle edge of `g_3`, opened by the branches', f'{(u["w_main"][4] - hgt(M_[4]) + bottom(M_[4])) - (u["w_main"][3] - top(M_[3])) - 2 * L:.1f}'),
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

One small domain carried all the way through: its record in the on-disk canonical form, the layout the [layout engine](layout-engine.md) computes for it, and the drawing Googie, the default style ([style-googie.md](style-googie.md)), makes of that layout, which the HTML sibling of this file renders. The [design page](styles.html) draws the same domain in all five styles. It is a fixture: an implementation that produces these numbers from this record, and this picture from these numbers, has the layout and the marks right. It also shows, on one screen, how a domain reads: two branches leaving one point on the left and returning to one point above, a project inside the main workflow and another inside a branch, the start and finish nodes of every workflow, every status, both marks people set, and a diamond at every point where a branch may depart or arrive. The file is generated by `scripts/worked_example.py` from the rules; when a rule changes, the script changes and the example is regenerated, so the two cannot drift.

The domain: a main workflow whose start node is untitled, holding the project XYZ-1 with the tasks step alpha (done), step Beta (cancelled), and step gama (in progress, marked here); a branch workflow, doppleganger, departing on the left above step alpha and returning above step Beta, whose whole content is the project "plan" holding prepare (done, marked here), 333 (in progress), and think (to do); and a second, outer branch, Workflow Fröbel, departing and returning at the same two points, holding 111 (to do) and 222 (in progress). The begin node XYZ-1, the start node doppleganger, and the tasks step alpha, step gama, 111, and 222 are flagged. No node has a note or a log entry.

## The record

`domain.json`, in the canonical form of the [persistence](persistence.md) document (ids shortened to read; real ids are the twelve characters of the structural model, section 1):

```json
{record_json}
```

## The layout

Constants as the layout engine's section 12 gives them: card width 188, lane step 228, `L` 24, `junctionMargin` 4, `rampFloor` 0.2, rise {RISE:.1f}. `u` is a card's box top above the baseline, up positive, with the main start node's box top at zero; gaps are measured between the silhouettes where the line passes through them, using Googie's insets (section 5.9: task 1.5 and 1.5; here card 6.54 and 6.54 at its height of 72; begin 9.33 and 2.95; end 2.95 and 9.33; start 5.92 and 5.92; finish 5.77 and 3.13, top and bottom); the flags and the here marks play no part (style contract, section 4); screen `y` is `baseY - u` with the baseline placed so that the drawing fits, and the main workflow's line at `x = 760`, the branches one and two lanes to its left.

| Node | Kind | Title | Workflow | x | u (box top) | Height | Screen y of the box top |
| --- | --- | --- | --- | --- | --- | --- | --- |
{md_rows}

{quant_md}

The laterals, as point lists in screen coordinates, each in Googie's route, a ramp, a flat, and a ramp, with the fan split at the shared points (the inner sibling's junction-side ramp longest):

| Lateral | Points |
| --- | --- |
{lat_md}

The risers, in screen coordinates: the main workflow's from the centre of its start card to the centre of its finish card, behind the cards; each branch's from where its departure lateral arrives, `L` beneath its start ellipse's silhouette, to where its return lateral leaves, above its finish keystone.

| Riser | Extent |
| --- | --- |
{ris_md}

A diamond, 12 on a side, marks every branch and return point whether or not a branch attaches there: one at the midpoint of each of the fourteen shut gaps, where the gap's two points coincide, and two in `g_3`, whose middle edge the branches have opened, its branch point `L` above step Beta's silhouette and its return point `L` below step gama's. Sixteen diamonds on the three lines, and no other marks on them. Every shut gap is 48 between silhouettes at the line: from the main start ellipse to the XYZ-1 hull, from the hull to step alpha, from step alpha to step Beta, and so on up the line.

## The drawing

The HTML sibling, [`worked-example.html`](worked-example.html), draws this layout in Googie, light and dark, inside a mock of the application window. What it must show: the untitled start ellipse at the base of the main line and the titled ones at the base of each branch, each riser rising from behind it; the begin hull XYZ-1 and its half-turned end hull enclosing the three steps; the plan branch's begin and end hulls enclosing prepare, 333, and think; each task's glyph by its state, the cancelled label struck through; the two here cards as marquees with their HERE pills, a sputnik to the left of each; an atom at the right end of every flagged node; the three finish keystones, each with its riser ending behind it; a diamond in every gap, two in the opened one; the two departure laterals sharing a stub at the branch point and parting, the outer's flat lower; the two return laterals mirroring them; the gap above step Beta opened by the branches, its middle edge taking the slack, whilst everything at or below the departure stays put.
"""
pathlib.Path('docs/specification/worked-example.md').write_text(md)

# ---- the html -------------------------------------------------------------------------------------------
def window(theme):
    on = lambda t: 'on' if theme == t else ''
    return f'''<div class="win {theme}">
 <div class="bar"><span class="brand">PENSAFORMA</span><span class="sel">Small Test <span>▾</span></span><span class="btn icon danger">✕</span><span class="btn"><span class="dot"></span>MCP</span>
  <span class="right"><span class="seglbl">MODE</span><span class="seg"><span class="{on('azure')}">Light</span><span class="{on('navy')}">Dark</span></span><span class="sel">Googie <span>▾</span></span><span class="btn">Flagged</span><span class="btn icon">−</span><span class="pct">80%</span><span class="btn icon">+</span><span class="btn primary">Fit</span></span></div>
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
.azure{{--ground:#d3e6ef;--panel:#f8f3e8;--ink:#173242;--line:#365b6c;--muted:#5f7d8b;--grid:rgba(23,50,66,.10);--c-todo:#d9a53a;--c-progress:#d75f2e;--c-done:#7d54a6;--c-cancel:#8aa0ab;--teal:#1f8f8a;--tint:#cbe6e4;--cursor:#d75f2e}}
.navy{{--ground:#0f2334;--panel:#1a3a54;--ink:#e8f1f6;--line:#6fb6c9;--muted:#93b3c2;--grid:rgba(111,182,201,.13);--c-todo:#f0bd55;--c-progress:#f27a44;--c-done:#bd93e6;--c-cancel:#7590a0;--teal:#37c2ba;--tint:#356e69;--cursor:#f27a44}}
.bar{{display:flex;align-items:center;gap:12px;padding:9px 14px;border-bottom:1px solid var(--line);color:var(--ink);font-size:12px}}
.brand{{font-weight:800;letter-spacing:.06em;font-size:13px}} .sel,.btn{{border:1px solid var(--line);border-radius:5px;padding:6px 10px}}
.btn.icon{{width:30px;text-align:center;padding:6px 0}} .btn.danger{{color:var(--cursor);border-color:#8f5d4a}} .btn.primary{{background:var(--ink);color:var(--ground)}}
.dot{{display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--teal);margin-right:7px;box-shadow:inset 0 0 0 1px rgba(0,0,0,.25)}}
.right{{margin-left:auto;display:flex;align-items:center;gap:12px}} .seglbl{{font-size:10px;letter-spacing:.12em;color:var(--muted)}}
.seg{{border:1px solid var(--line);border-radius:999px;overflow:hidden;display:inline-flex}} .seg span{{padding:6px 14px;color:var(--muted)}} .seg span.on{{background:var(--ink);color:var(--ground)}}
.pct{{font-size:11px;color:var(--muted);min-width:42px;text-align:center}}
.canvas{{background-color:var(--ground);background-image:radial-gradient(circle, var(--grid) 1px, transparent 1.4px);background-size:40px 40px;display:flex;justify-content:center;padding:10px 0}}
.canvas svg{{zoom:0.8}}
.line{{fill:var(--line)}} .inner{{fill:var(--panel)}} .todo{{fill:var(--c-todo)}} .progress{{fill:var(--c-progress)}} .done{{fill:var(--c-done)}} .cancel{{fill:var(--c-cancel)}}
.gtodo{{fill:var(--c-todo)}} .gprogress{{fill:var(--c-progress)}} .gdone{{fill:var(--c-done)}} .gcancel{{fill:none;stroke:var(--c-cancel);stroke-width:1.5;stroke-dasharray:2.4 2.2}}
.proj{{fill:var(--teal)}} .tint{{fill:var(--tint)}} .ink{{fill:var(--ink)}} .ring{{fill:none;stroke:var(--ink)}} .ray{{stroke:var(--ink);stroke-linecap:round}}
.pill{{fill:var(--cursor)}} .pilltxt{{font:7.5px ui-monospace,Menlo,monospace;letter-spacing:1px;fill:var(--panel);text-anchor:middle}}
.track{{fill:none;stroke:var(--line);stroke-linecap:round;stroke-linejoin:round}} .riser{{stroke-width:3}} .lat{{stroke-width:2.3}}
.lbl{{font:600 13px -apple-system,Helvetica,Arial,sans-serif;fill:var(--ink)}} .lbl.mid{{text-anchor:middle}} .lbl.start{{font-size:11.5px}} .lbl.struck{{fill:var(--muted);text-decoration:line-through}}
.tag{{font:600 8px -apple-system,Helvetica,Arial,sans-serif;fill:var(--muted);letter-spacing:.08em}}
</style></head><body><div class="wrap">
<h1>A worked example: the Small Test domain</h1>
<p>One small domain carried all the way through: its record, the layout the engine computes for it, and the drawing Googie, the default style, makes of that layout. An implementation that produces these numbers from this record, and this picture from these numbers, has the layout and the marks right. The canonical text is <code>worked-example.md</code>, beside this file; both are generated by <code>scripts/worked_example.py</code>.</p>
<h2>The drawing, in Googie light and dark</h2>
{window('azure')}
{window('navy')}
<h2>The record</h2>
<pre>{record_json}</pre>
<h2>The layout</h2>
<p>Card width 188, lane step 228, <code>L</code> 24, <code>junctionMargin</code> 4, <code>rampFloor</code> 0.2, rise {RISE:.1f}. <code>u</code> is a card's top above the baseline, up positive, the main start card's top at zero; gaps are measured between the silhouettes where the line passes through them, with Googie's insets (its section 5.9); screen <code>y</code> is <code>baseY − u</code> with <code>baseY</code> {baseY:.1f}; the main line is at <code>x</code> = 760 and the branches one and two lanes to its left.</p>
<table><thead><tr><th>Node</th><th>Kind</th><th>Title</th><th>Workflow</th><th>x</th><th>u (box top)</th><th>Height</th><th>Screen y of the box top</th></tr></thead><tbody>{html_rows}</tbody></table>
{quant_html}
<table><thead><tr><th>Lateral</th><th>Points (screen)</th></tr></thead><tbody>{lat_html}</tbody></table>
<table><thead><tr><th>Riser</th><th>Extent (screen)</th></tr></thead><tbody>{ris_html}</tbody></table>
<p>Canonical source: <code>worked-example.md</code>, beside this file. If they drift, the Markdown wins.</p>
</div></body></html>'''
pathlib.Path('docs/specification/worked-example.html').write_text(html)
print(f'written: size {W}x{HGT}, baseY {baseY:.1f}, bp {bp:.1f}, arrive {arrive:.1f}, rp {rp:.1f}, leave {leave:.1f}')
