#!/usr/bin/env python3
"""Remove raw bullet dots from all body-content lists on every page.
Targets only class-less <ul> inside content description containers (so it
never touches the icon-lists, nav menus, footer columns, or the homepage
pill list, which all carry classes). Replaces the disc with a clean,
left-aligned layout and a small brand-green check marker. Inserted before
the real (last) </body>."""
import glob, os

CHECK = ("url('data:image/svg+xml;utf8,"
         "<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22 fill=%22none%22 "
         "stroke=%22%23a9c81e%22 stroke-width=%223.5%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22>"
         "<path d=%22M20 6 9 17l-5-5%22/></svg>')")

STYLE = (
 '<style id="rcc-list-style">'
 '.section-heading__description ul:not([class]),'
 '.content__description ul:not([class]),'
 '.richtext-imageblob__content ul:not([class]){'
 'list-style:none!important;padding:0!important;margin:14px auto!important;'
 'display:inline-block;text-align:left!important;max-width:760px}'
 '.section-heading__description ul:not([class]) li,'
 '.content__description ul:not([class]) li,'
 '.richtext-imageblob__content ul:not([class]) li{'
 'list-style:none!important;position:relative;padding-left:28px!important;'
 'margin:0 0 10px!important;text-align:left!important}'
 '.section-heading__description ul:not([class]) li::marker,'
 '.content__description ul:not([class]) li::marker,'
 '.richtext-imageblob__content ul:not([class]) li::marker{content:""!important}'
 '.section-heading__description ul:not([class]) li::before,'
 '.content__description ul:not([class]) li::before,'
 '.richtext-imageblob__content ul:not([class]) li::before{'
 'content:"";position:absolute;left:0;top:.3em;width:15px;height:15px;'
 'background:no-repeat center/contain ' + CHECK + '}'
 '</style>'
)

count = 0
for f in glob.glob("/Users/brookw/demorccs/*.html"):
    if os.path.basename(f).startswith('_'): continue
    html = open(f, encoding="utf-8", errors="surrogateescape").read()
    if 'rcc-list-style' in html:
        continue
    pos = max(html.rfind('</body>'), html.rfind('</BODY>'))
    if pos == -1: pos = len(html)
    html = html[:pos] + STYLE + html[pos:]
    open(f, "w", encoding="utf-8", errors="surrogateescape").write(html)
    count += 1
print("Patched:", count, "files")
