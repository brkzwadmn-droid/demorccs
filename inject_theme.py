#!/usr/bin/env python3
import glob, re

LINKS = ('<link rel="stylesheet" data-theme-base="1" '
         'href="/wp-content/themes/avivo/css/theme.min.css">\n'
         '<link rel="stylesheet" data-theme-base="1" '
         'href="/wp-content/themes/avivo/css/nav.min.css">\n')

count = 0
for f in glob.glob("/Users/brookw/demorccs/*.html"):
    with open(f, "r", encoding="utf-8", errors="surrogatepass") as fh:
        html = fh.read()
    if 'data-theme-base' in html:
        continue
    m = re.search(r'<head[^>]*>', html, re.IGNORECASE)
    if not m:
        print("  no <head> in", f)
        continue
    i = m.end()
    html = html[:i] + "\n" + LINKS + html[i:]
    with open(f, "w", encoding="utf-8", errors="surrogatepass") as fh:
        fh.write(html)
    count += 1
    print("  themed:", f.split("/")[-1])

print("Total:", count)
