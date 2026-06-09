#!/usr/bin/env python3
"""Stop the header phone number and 'Start your journey' button from stacking
at mid-desktop widths (~1200px). Keep them on a single row. Insert before the
LAST </body> (real document, not the decoy Grammarly artifact)."""
import glob

STYLE = ('<style id="rcc-fix-header-actions">'
         '.mn-light .navbar__actions .btn-row{flex-wrap:nowrap!important;align-items:center!important}'
         '.mn-light .navbar__actions .btn-row>*{white-space:nowrap!important;flex:0 0 auto!important}'
         '</style>')

count = 0
for f in glob.glob("/Users/brookw/demorccs/*.html"):
    with open(f, encoding="utf-8", errors="surrogatepass") as fh:
        html = fh.read()
    if 'rcc-fix-header-actions' in html:
        continue
    pos = max(html.rfind('</body>'), html.rfind('</BODY>'))
    if pos == -1:
        pos = len(html)
    html = html[:pos] + STYLE + html[pos:]
    with open(f, "w", encoding="utf-8", errors="surrogatepass") as fh:
        fh.write(html)
    count += 1
print("Patched:", count, "files")
