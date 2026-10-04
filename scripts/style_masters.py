#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Gary Frattarola <garyf@parkviewlab.ai>
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Write the golden-master sections of the five style documents from styles-masters.json.

The design page, docs/specification/styles.html, is the authority for every drawing. Opened
with ?export=masters it exports docs/specification/styles-masters.json: every style's
silhouettes and marks at their stated boxes, its constants and tokens, and a fingerprint of the
page's style and script. This script checks that fingerprint against the page, so a drawing
changed on the page and not re-exported fails, and writes each style document's masters
between its markers.

Usage:  python3 scripts/style_masters.py           write the masters into the style documents
        python3 scripts/style_masters.py --check   change nothing; fail if anything is stale
"""
import hashlib, json, pathlib, re, sys

SPEC = pathlib.Path(__file__).resolve().parent.parent / 'docs' / 'specification'
ORDER = ['froebel', 'prairie', 'bauhaus', 'googie', 'suuronen']


def fingerprint(html):
    """The SHA-256 of the page's style and script text, in document order, as the page computes it."""
    return hashlib.sha256(''.join(m.group(2) for m in re.finditer(r'<(style|script)>(.*?)</\1>', html, re.S)).encode()).hexdigest()


def section(key, style):
    out = [f'<!-- masters:{key}:begin -->', '']
    for name, m in style['masters'].items():
        out += [f'{name.capitalize()}, box `{m["box"]}`:', '', '```svg', m['svg'], '```', '']
    out += ['Tracks: riser {riser}, laterals {lateral}, line ends {cap}, joins {join}.'.format(**style['tracks']),
            f'The flag is painted {style["flagPainted"]} the card.', '']
    rows = ['| token | light | dark |', '| --- | --- | --- |']
    for t in style['tokens']['light']:
        rows.append(f'| `{t}` | `{style["tokens"]["light"][t]}` | `{style["tokens"]["dark"].get(t, "")}` |')
    out += rows + ['', f'<!-- masters:{key}:end -->']
    return '\n'.join(out)


def main(check):
    page = (SPEC / 'styles.html').read_text()
    data = json.loads((SPEC / 'styles-masters.json').read_text())
    if data['fingerprint'] != fingerprint(page):
        sys.exit('styles-masters.json is stale: open styles.html?export=masters and save its export')
    stale = []
    for key in ORDER:
        path = SPEC / f'style-{key}.md'
        text = path.read_text()
        pattern = re.compile(rf'<!-- masters:{key}:begin -->.*?<!-- masters:{key}:end -->', re.S)
        assert pattern.search(text), f'{path.name}: no masters markers'
        new = pattern.sub(lambda _: section(key, data['styles'][key]), text)
        if new != text:
            stale.append(path.name)
            if not check:
                path.write_text(new)
    if check and stale:
        sys.exit('stale golden masters: ' + ', '.join(stale) + '; run python3 scripts/style_masters.py')
    print('golden masters current' if check else f'wrote {len(stale)} style documents')


if __name__ == '__main__':
    main('--check' in sys.argv[1:])
