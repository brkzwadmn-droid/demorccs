#!/usr/bin/env python3
import glob, re, os
from collections import defaultdict
from html import unescape

root = "/Users/brookw/demorccs"
files = sorted(glob.glob(os.path.join(root, "*.html")))
existing = {os.path.basename(f) for f in files}

# href values that are not page navigation
def classify(href):
    h = href.strip()
    if not h: return "empty"
    low = h.lower()
    if low.startswith(("http://","https://")): return "external"
    if low.startswith(("tel:","mailto:","javascript:","data:")): return "scheme"
    if h.startswith("#"): return "anchor"
    return "internal"

broken = defaultdict(set)        # target -> set(pages referencing)
internal_ok = defaultdict(set)
ext_count = defaultdict(int)

href_re = re.compile(r'<a\b[^>]*?\bhref\s*=\s*"([^"]*)"', re.IGNORECASE)

for f in files:
    name = os.path.basename(f)
    with open(f, encoding="utf-8", errors="surrogatepass") as fh:
        html = fh.read()
    for raw in href_re.findall(html):
        href = unescape(raw)
        kind = classify(href)
        if kind != "internal":
            if kind == "external": ext_count[href] += 1
            continue
        # strip query and fragment
        target = href.split("#")[0].split("?")[0]
        if target == "": continue          # pure fragment handled above
        base = target.lstrip("/")
        if base == "" : base = "index.html"
        # resolve: file must exist
        if base in existing:
            internal_ok[base].add(name)
        else:
            broken[href].add(name)

print("=== BROKEN internal links (target not found) ===")
for tgt in sorted(broken, key=lambda t: -len(broken[t])):
    print(f"  {len(broken[tgt]):3d} refs  ->  {tgt}")
print()
print("=== Internal links that resolve OK ===")
for tgt in sorted(internal_ok):
    print(f"  {len(internal_ok[tgt]):3d} refs  ->  {tgt}")
print()
print(f"Existing html files: {len(existing)}")
