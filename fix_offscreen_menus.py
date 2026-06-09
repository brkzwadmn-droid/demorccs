#!/usr/bin/env python3
"""The theme's nav.min.js (still loaded from avivo.org.au) teleports the
megamenu panels stored in the hidden .megamenu-offscreen container (after the
footer) INTO the header menu items at runtime — replacing the corrected
panels with stale, un-rebranded Avivo ones ("Aged care" under Accommodation,
etc.). Fix: overwrite each offscreen panel with the corrected inline panel of
the same id, so the runtime swap becomes a no-op."""
import glob, re

open_div = re.compile(r'<div\b[^>]*>', re.IGNORECASE)
any_div = re.compile(r'<div\b[^>]*>|</div\s*>', re.IGNORECASE)

def balanced_block(html, start):
    """html[start:] begins with <div ...>; return end index of its close."""
    m = open_div.match(html, start)
    if not m:
        return None
    depth, i = 1, m.end()
    while depth:
        t = any_div.search(html, i)
        if not t:
            return None
        depth += 1 if t.group(0).lower().startswith('<div') else -1
        i = t.end()
    return i

def panel_starts(html, region_start, region_end):
    """id -> start offset of each cdb-megamenu opening div in region."""
    out = {}
    for m in re.finditer(r'<div\b[^>]*class="cdb-megamenu dropdown-menu"[^>]*id="(megamenu-\d+)"[^>]*>',
                         html[region_start:region_end]):
        out[m.group(1)] = region_start + m.start()
    return out

changed = 0
for f in sorted(glob.glob("/Users/brookw/demorccs/*.html")):
    html = open(f, encoding="utf-8", errors="surrogateescape").read()
    off = html.find('class="megamenu-offscreen"')
    main = html.find('<main')
    if off == -1 or main == -1:
        print(f"  {f.split('/')[-1]:36s} no offscreen block — skipped")
        continue
    inline = panel_starts(html, 0, main)
    offscreen = panel_starts(html, off, len(html))
    if set(inline) != set(offscreen):
        print(f"  !! id mismatch in {f}: inline={sorted(inline)} offscreen={sorted(offscreen)}")
        continue
    # build replacements right-to-left so offsets stay valid
    repls = []
    ok = True
    for pid, ostart in offscreen.items():
        oend = balanced_block(html, ostart)
        istart = inline[pid]
        iend = balanced_block(html, istart)
        if oend is None or iend is None:
            print(f"  !! unbalanced block for {pid} in {f}")
            ok = False
            break
        repls.append((ostart, oend, html[istart:iend]))
    if not ok:
        continue
    for ostart, oend, block in sorted(repls, key=lambda r: -r[0]):
        html = html[:ostart] + block + html[oend:]
    open(f, "w", encoding="utf-8", errors="surrogateescape").write(html)
    changed += 1
    # verify h3 sets now match
    off2 = html.find('class="megamenu-offscreen"')
    h3i = re.findall(r'<h3>([^<]*)</h3>', html[html.find('id="main-menu"'):html.find('<main')])
    h3o = re.findall(r'<h3>([^<]*)</h3>', html[off2:])
    status = "OK" if h3i[:5] == h3o[:5] else f"STILL DIFFER inline={h3i[:5]} off={h3o[:5]}"
    print(f"  {f.split('/')[-1]:36s} offscreen panels equalised — {status}")
print("Files changed:", changed)
