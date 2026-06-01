#!/usr/bin/env python3
"""Remove the footer 'rehoboth' logo (the dark wordmark on the teal footer)
from every page. Insert before the LAST </body> so it lands in the real
document, not the decoy Grammarly artifact."""
import glob, os

STYLE = '<style id="rcc-footer-logo-hide">.footer__logo{display:none!important}</style>'

count = 0
for f in glob.glob("/Users/brookw/demorccs/*.html"):
    with open(f, encoding="utf-8", errors="surrogatepass") as fh:
        html = fh.read()
    if 'rcc-footer-logo-hide' in html:
        continue
    pos = max(html.rfind('</body>'), html.rfind('</BODY>'))
    if pos == -1:
        pos = len(html)
    html = html[:pos] + STYLE + html[pos:]
    with open(f, "w", encoding="utf-8", errors="surrogatepass") as fh:
        fh.write(html)
    count += 1
print("Patched:", count, "files")
