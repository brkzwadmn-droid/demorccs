#!/usr/bin/env python3
"""Remove the injected teal 'rehoboth' nav bar (everything between the
<!--rcc-nav--> ... <!--/rcc-nav--> markers) from every page, so the original
Avivo-style header is the only header."""
import glob, re, os

count = 0
for f in glob.glob("/Users/brookw/demorccs/*.html"):
    with open(f, encoding="utf-8", errors="surrogatepass") as fh:
        html = fh.read()
    new = re.sub(r'\n?<!--rcc-nav-->.*?<!--/rcc-nav-->\n?', '', html, flags=re.DOTALL)
    if new != html:
        with open(f, "w", encoding="utf-8", errors="surrogatepass") as fh:
            fh.write(new)
        count += 1
        print("  nav removed:", os.path.basename(f))
print("Total:", count)
