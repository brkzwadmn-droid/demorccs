#!/usr/bin/env python3
"""Stop the header logo being stretched: preserve its natural aspect ratio.
Insert the override before the LAST </body> (the real document end), not the
first one (which lives inside a junk Grammarly artifact)."""
import glob, os

STYLE = (
    '<style id="rcc-logo-fix">'
    '.navbar-brand__logo-simple,.navbar-brand__logo,.mobile-brand__logo{'
    'height:40px!important;width:auto!important;max-width:260px!important;'
    'object-fit:contain!important;}'
    '@media(max-width:980px){'
    '.navbar-brand__logo-simple,.navbar-brand__logo,.mobile-brand__logo{height:34px!important;}'
    '}'
    '</style>'
)

count = 0
for f in glob.glob("/Users/brookw/demorccs/*.html"):
    with open(f, encoding="utf-8", errors="surrogatepass") as fh:
        html = fh.read()
    # remove any previous (possibly misplaced) injection
    if 'id="rcc-logo-fix"' in html:
        i = html.find('<style id="rcc-logo-fix">')
        j = html.find('</style>', i) + len('</style>')
        html = html[:i] + html[j:]
    # insert before the LAST closing body tag
    pos = max(html.rfind('</body>'), html.rfind('</BODY>'))
    if pos == -1:
        pos = len(html)
    html = html[:pos] + STYLE + html[pos:]
    with open(f, "w", encoding="utf-8", errors="surrogatepass") as fh:
        fh.write(html)
    count += 1
print("Patched:", count, "files")
