#!/usr/bin/env python3
"""Remove the redundant original fixed header (.mn-light) and its 117px
spacer (.page-spacer) on every page. The injected .rccnav is the working
header now. Insert before the LAST </body> (real document, not the decoy)."""
import glob

STYLE = ('<style id="rcc-hide-old-header">'
         '.mn-light{display:none!important}'
         '.page-spacer{display:none!important}'
         '</style>')

count = 0
for f in glob.glob("/Users/brookw/demorccs/*.html"):
    with open(f, encoding="utf-8", errors="surrogatepass") as fh:
        html = fh.read()
    if 'rcc-hide-old-header' in html:
        continue
    pos = max(html.rfind('</body>'), html.rfind('</BODY>'))
    if pos == -1:
        pos = len(html)
    html = html[:pos] + STYLE + html[pos:]
    with open(f, "w", encoding="utf-8", errors="surrogatepass") as fh:
        fh.write(html)
    count += 1
print("Patched:", count, "files")
