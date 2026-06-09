#!/usr/bin/env python3
"""Final gate: every <a href> on every page must resolve. Exit 1 on failures."""
import glob, os, re, sys
from html import unescape

root = "/Users/brookw/demorccs"
files = sorted(glob.glob(os.path.join(root, "*.html")))
existing = {os.path.basename(f) for f in files}

EXTERNAL_OK = (
    "https://www.marshillcare.com.au",
    "https://www.ndis.gov.au", "http://www.ndis.gov.au",
    "https://www.carergateway.gov.au",
    "https://www.myagedcare.gov.au",
    "https://www.lifeline.org.au",
    "https://www.clue.com.au",
    "https://duckduckgo.com",
    "https://www.googletagmanager.com",
    "https://youtu.be", "https://www.youtube.com/watch",
    "https://www.google.com/maps",
    "https://www.avivo.org.au/wp-content/uploads/2025/11/Margaret",   # testimonial videos (media files)
    "https://www.avivo.org.au/wp-content/uploads/2025/11/Nina",
)

a_re = re.compile(r'<a\b[^>]*?\bhref\s*=\s*(["\'])(.*?)\1[^>]*>(.*?)</a>', re.IGNORECASE | re.DOTALL)
tag_re = re.compile(r'<[^>]+>')
fails = []
counts = {"local": 0, "external-ok": 0, "tel/mailto": 0, "anchor": 0}

# collect ids per file for fragment checking
ids = {}
for f in files:
    html = open(f, encoding="utf-8", errors="surrogatepass").read()
    ids[os.path.basename(f)] = set(re.findall(r'\bid="([^"]+)"', html))

noscript_re = re.compile(r'<noscript\b.*?</noscript>', re.IGNORECASE | re.DOTALL)

for f in files:
    name = os.path.basename(f)
    html = open(f, encoding="utf-8", errors="surrogatepass").read()
    # anchors inside <noscript> never render with JS on; the corrupted CSS-link
    # markup in there is data for the CSS rehydrate loader, not user-facing links
    html = noscript_re.sub(' ', html)
    for q, href, inner in a_re.findall(html):
        href = unescape(href).strip()
        label = re.sub(r'\s+', ' ', unescape(tag_re.sub(' ', inner))).strip()[:40]
        low = href.lower()
        if not href:
            fails.append((name, href, label, "EMPTY"))
        elif low.startswith(("tel:", "mailto:")):
            counts["tel/mailto"] += 1
        elif href == "#":
            if label:  # labelled dead link
                fails.append((name, href, label, "DEAD #"))
            else:
                counts["anchor"] += 1
        elif href.startswith("#"):
            counts["anchor"] += 1
        elif low.startswith(("http://", "https://")):
            if any(href.startswith(p) for p in EXTERNAL_OK):
                counts["external-ok"] += 1
            else:
                fails.append((name, href, label, "EXTERNAL NOT WHITELISTED"))
        elif low.startswith(("javascript:", "data:")):
            fails.append((name, href, label, "JS/DATA"))
        else:
            target = href.split("#")[0].split("?")[0].lstrip("/")
            frag = href.split("#")[1] if "#" in href else None
            base = target if target else name
            if base not in existing:
                fails.append((name, href, label, "MISSING PAGE"))
            elif frag and frag not in ids.get(base, set()) and frag not in ("main",):
                fails.append((name, href, label, f"MISSING ANCHOR #{frag} in {base}"))
            else:
                counts["local"] += 1

print("OK counts:", counts)
if fails:
    print(f"\nFAILURES: {len(fails)}")
    seen = set()
    for name, href, label, why in fails:
        key = (href, label, why)
        if key in seen: continue
        seen.add(key)
        print(f"  [{why}] {href!r} [{label}] (e.g. {name})")
    sys.exit(1)
print("ALL LINKS RESOLVE ✔")
