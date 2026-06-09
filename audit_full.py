#!/usr/bin/env python3
"""Full link audit: every <a href> across all pages, categorized, with labels."""
import glob, os, re, json
from collections import defaultdict
from html import unescape

root = "/Users/brookw/demorccs"
files = sorted(glob.glob(os.path.join(root, "*.html")))
existing = {os.path.basename(f) for f in files}

a_re = re.compile(r'<a\b[^>]*?\bhref\s*=\s*(["\'])(.*?)\1[^>]*>(.*?)</a>',
                  re.IGNORECASE | re.DOTALL)
tag_re = re.compile(r'<[^>]+>')

def label_of(inner):
    t = tag_re.sub(' ', inner)
    t = unescape(re.sub(r'\s+', ' ', t)).strip()
    return t[:50]

cats = defaultdict(lambda: defaultdict(set))  # cat -> key -> pages
for f in files:
    name = os.path.basename(f)
    with open(f, encoding="utf-8", errors="surrogatepass") as fh:
        html = fh.read()
    for q, href, inner in a_re.findall(html):
        href = unescape(href).strip()
        label = label_of(inner)
        key = f"{href!r} [{label}]"
        low = href.lower()
        if not href:
            cats["EMPTY"][key].add(name)
        elif low.startswith(("tel:", "mailto:")):
            pass  # fine
        elif href == "#" or href.startswith("#"):
            if href == "#":
                cats["HASH-DEAD"][key].add(name)
        elif low.startswith("javascript:") or low.startswith("data:"):
            cats["JS/DATA"][key].add(name)
        elif "avivo.org.au" in low:
            if ".css" in low:
                continue  # noscript CSS refs used by rehydrate, leave
            cats["AVIVO"][key].add(name)
        elif low.startswith(("http://", "https://")):
            cats["EXTERNAL"][key].add(name)
        else:
            base = href.split("#")[0].split("?")[0].lstrip("/")
            if base == "":
                base = "index.html"
            if base in existing:
                cats["LOCAL-OK"][key].add(name)
            else:
                cats["LOCAL-MISSING"][key].add(name)

order = ["LOCAL-MISSING", "AVIVO", "HASH-DEAD", "EXTERNAL", "EMPTY", "JS/DATA", "LOCAL-OK"]
for cat in order:
    items = cats.get(cat, {})
    if cat == "LOCAL-OK":
        print(f"\n=== {cat}: {len(items)} distinct (not listed) ===")
        continue
    print(f"\n=== {cat}: {len(items)} distinct ===")
    for key in sorted(items, key=lambda k: -len(items[k])):
        print(f"  {len(items[key]):2d}pg  {key}")
