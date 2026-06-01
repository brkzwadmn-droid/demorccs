#!/usr/bin/env python3
"""Inject a self-contained, working navigation bar into every page, and make
local CSS paths relative so the site works on GitHub Pages."""
import glob, os, re

NAV_CSS = """
<style id="rcc-nav-styles">
.rccnav,.rccnav *{box-sizing:border-box}
.rccnav{position:sticky;top:0;z-index:2147483000;background:#004851;font-family:Montserrat,Arial,Helvetica,sans-serif;box-shadow:0 2px 10px rgba(0,0,0,.18)}
.rccnav-inner{max-width:1240px;margin:0 auto;display:flex;align-items:center;padding:8px 16px}
.rccnav-brand{color:#c4d600;font-weight:800;font-size:22px;text-decoration:none;letter-spacing:.4px}
.rccnav-spacer{flex:1}
.rccnav-toggle{position:absolute;left:-9999px}
.rccnav-burger{display:none;cursor:pointer;color:#fff;font-size:26px;line-height:1;padding:6px 10px;user-select:none}
.rccnav-menu{display:flex;align-items:center;gap:2px}
.rccnav-link{color:#fff;text-decoration:none;padding:10px 12px;border-radius:6px;font-size:15px;font-weight:600;white-space:nowrap}
.rccnav-link:hover{background:rgba(255,255,255,.14)}
.rccnav-phone{color:#004851;background:#c4d600;padding:9px 16px;border-radius:999px;font-weight:700;text-decoration:none;white-space:nowrap;margin-left:8px}
.rccnav-phone:hover{filter:brightness(.95)}
.rccnav-group{position:relative}
.rccnav-group>summary{list-style:none;cursor:pointer;color:#fff;padding:10px 12px;border-radius:6px;font-size:15px;font-weight:600;white-space:nowrap}
.rccnav-group>summary::-webkit-details-marker{display:none}
.rccnav-group>summary:after{content:"\\025BE";margin-left:5px;opacity:.85}
.rccnav-group>summary:hover{background:rgba(255,255,255,.14)}
.rccnav-sub{position:absolute;top:100%;left:0;min-width:240px;background:#fff;border-radius:8px;box-shadow:0 10px 28px rgba(0,0,0,.22);padding:6px;display:none;flex-direction:column}
.rccnav-group[open]>.rccnav-sub,.rccnav-group:hover>.rccnav-sub{display:flex}
.rccnav-sub a{color:#143b41;text-decoration:none;padding:9px 12px;border-radius:6px;font-size:14px}
.rccnav-sub a:hover{background:#eef3e0;color:#004851}
@media(max-width:980px){
  .rccnav-burger{display:block}
  .rccnav-menu{display:none;position:absolute;top:100%;left:0;right:0;background:#004851;flex-direction:column;align-items:stretch;padding:8px;gap:2px;max-height:80vh;overflow:auto}
  .rccnav-toggle:checked ~ .rccnav-menu{display:flex}
  .rccnav-group{width:100%}
  .rccnav-group:hover>.rccnav-sub{display:none}
  .rccnav-group[open]>.rccnav-sub{display:flex;position:static;box-shadow:none;background:rgba(255,255,255,.06)}
  .rccnav-group[open]>.rccnav-sub a{color:#fff}
  .rccnav-group[open]>.rccnav-sub a:hover{background:rgba(255,255,255,.14)}
  .rccnav-phone{margin:6px 0 0}
}
</style>
"""

GROUPS = [
    ("Disability", [
        ("Disability overview", "disability.html"),
        ("Disability services", "disability-services.html"),
        ("In-home support", "in-home.html"),
        ("Personal care", "personal-care.html"),
        ("Social & community", "social-and-community.html"),
        ("Transport services", "transport-services.html"),
        ("Night services", "night-services.html"),
        ("24-hour care", "24-hour-care.html"),
        ("Specialist services", "specialists-services.html"),
        ("Disability nursing", "disability-nursing.html"),
    ]),
    ("NDIS", [
        ("How it works", "disability-ndis-how-it-works.html"),
        ("How to apply", "ndis-disability-how-to-apply.html"),
        ("Funding options", "funding-options.html"),
        ("Pricelist", "ndis-pricelist.html"),
    ]),
    ("Plan management", [
        ("Agency-managed", "agency-managed-ndis.html"),
        ("Plan-managed", "plan-management-ndis.html"),
        ("Self-managed", "self-management-ndis.html"),
    ]),
    ("Care & support", [
        ("Care management", "care-management-services.html"),
        ("Carers support", "carers-support.html"),
        ("Aged care", "aged-care.html"),
        ("Mental health", "mental-health.html"),
    ]),
]

def build_nav():
    parts = ['<nav class="rccnav"><div class="rccnav-inner">']
    parts.append('<a class="rccnav-brand" href="index.html">rehoboth</a>')
    parts.append('<div class="rccnav-spacer"></div>')
    parts.append('<input type="checkbox" id="rcc-nav-toggle" class="rccnav-toggle" aria-label="Toggle menu">')
    parts.append('<label for="rcc-nav-toggle" class="rccnav-burger">&#9776;</label>')
    parts.append('<div class="rccnav-menu">')
    parts.append('<a class="rccnav-link" href="index.html">Home</a>')
    for title, items in GROUPS:
        parts.append('<details class="rccnav-group"><summary>%s</summary><div class="rccnav-sub">' % title)
        for label, href in items:
            parts.append('<a href="%s">%s</a>' % (href, label))
        parts.append('</div></details>')
    parts.append('<a class="rccnav-phone" href="tel:1300853095">1300 853 095</a>')
    parts.append('</div></div></nav>')
    return "".join(parts)

NAV_HTML = '\n<!--rcc-nav-->' + NAV_CSS + build_nav() + '<!--/rcc-nav-->\n'

count = 0
for f in glob.glob("/Users/brookw/demorccs/*.html"):
    with open(f, encoding="utf-8", errors="surrogatepass") as fh:
        html = fh.read()

    # 1) make local theme css paths relative (GitHub Pages project-site safe)
    html = html.replace('href="/wp-content/themes/avivo/css/',
                         'href="wp-content/themes/avivo/css/')
    # patch the CSS-rehydrate helper to also relativise /wp-content links
    html = html.replace("href = href.replace(/&amp;/g,'&')",
                        "href = href.replace(/&amp;/g,'&').replace(/^\\/wp-content/,'wp-content')")

    # 2) inject the nav once, right after <body ...>
    if 'rcc-nav' not in html:
        m = re.search(r'<body[^>]*>', html, re.IGNORECASE)
        if not m:
            print("  no <body> in", os.path.basename(f)); continue
        i = m.end()
        html = html[:i] + NAV_HTML + html[i:]

    with open(f, "w", encoding="utf-8", errors="surrogatepass") as fh:
        fh.write(html)
    count += 1
    print("  nav injected:", os.path.basename(f))

print("Total:", count)
