#!/usr/bin/env python3
"""Give disability-services.html a nicer design: replace the two plain
stacked text-list sections with one responsive service-card grid."""
import re

P = "/Users/brookw/demorccs/disability-services.html"
h = open(P, encoding="utf-8", errors="surrogateescape").read()

def svg(inner):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="#1f3d3a" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round">' + inner + '</svg>')

SERVICES = [
 ("in-home.html", "In-home support",
  "Compassionate care in the comfort of your own home, helping you live independently, confidently and with dignity.",
  '<path d="M3 9.5 12 3l9 6.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>'),
 ("personal-care.html", "Personal care",
  "Respectful, discreet help with showering, dressing, grooming, mobility and the personal tasks of daily living.",
  '<circle cx="12" cy="8" r="4"/><path d="M5.5 21a6.5 6.5 0 0 1 13 0"/>'),
 ("social-and-community.html", "Community participation",
  "Support to explore new experiences, build confidence, connect with others and be an active part of your community.",
  '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>'),
 ("disability-nursing.html", "Community nursing",
  "Professional nursing care in your own home for complex health needs, claimable through your NDIS plan where eligible.",
  '<path d="M19 14c1.5-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/><path d="M3.5 11H9l1-2.5 2.5 5L14 11h6.5"/>'),
 ("transport-services.html", "Travel &amp; transport",
  "Reliable, personalised travel support to reach appointments, activities and community life safely and with confidence.",
  '<path d="M5 13 6.5 8.5A2 2 0 0 1 8.4 7h7.2a2 2 0 0 1 1.9 1.5L19 13"/><path d="M5 13h14v4a1 1 0 0 1-1 1h-1a1 1 0 0 1-1-1v-1H8v1a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1z"/><circle cx="7.5" cy="15.5" r=".6"/><circle cx="16.5" cy="15.5" r=".6"/>'),
 ("care-management-services.html", "Support coordination",
  "Help to understand and make the most of your NDIS plan, connect with the right providers and reach your goals.",
  '<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88"/>'),
 ("accommodation.html", "Supported Independent Living",
  "Safe, welcoming homes with the everyday support you need to live more independently, your way.",
  '<rect x="5" y="3" width="14" height="18" rx="1.5"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2"/><path d="M10 21v-4h4v4"/>'),
 ("carers-support.html", "Respite &amp; short stays",
  "Short term accommodation that gives participants new experiences and gives families and carers a chance to rest.",
  '<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>'),
 ("specialists-services.html", "Specialist &amp; therapy supports",
  "Therapy and allied health, complex high-care support and more, tailored to people with higher or changing needs.",
  '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>'),
]

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" '
         'stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')

cards = "".join(
 f'<a class="rcc-svc__card" href="{href}">'
 f'<span class="rcc-svc__ic">{svg(ic)}</span>'
 f'<span class="rcc-svc__t">{title}</span>'
 f'<span class="rcc-svc__d">{desc}</span>'
 f'<span class="rcc-svc__more">Learn more {ARROW}</span></a>'
 for href, title, desc, ic in SERVICES)

GRID_SECTION = (
 '<section class="section cdb-intro_text sc-lightgrey spt-lg spb-lg">'
 '<div class="container section-container"><div class="content-container">'
 '<div class="section-heading"><div class="section-heading__title">'
 '<div class="title_wrapper center intro_text__title title_wrapper--h2"><h2 class="title h2">How we can help you</h2></div></div>'
 '<div class="section-heading__description"><p class="rcc-svc__lead">Comprehensive NDIS services tailored to each person&#8217;s goals, lifestyle and level of support.</p></div></div>'
 f'<div class="rcc-svc">{cards}</div>'
 '</div></div></section>'
)

STYLE = (
 '<style id="rcc-svc-style">'
 '.rcc-svc__lead{text-align:center;max-width:720px;margin:0 auto 6px}'
 '.rcc-svc{max-width:1180px;margin:34px auto 0;display:grid;grid-template-columns:repeat(3,1fr);gap:24px}'
 '.rcc-svc__card{display:flex;flex-direction:column;align-items:flex-start;text-align:left;'
 'background:#fff;border:1px solid #e7ead9;border-radius:18px;padding:30px 28px;text-decoration:none;'
 'transition:transform .2s ease,box-shadow .2s ease,border-color .2s ease}'
 '.rcc-svc__card:hover{transform:translateY(-5px);box-shadow:0 18px 38px rgba(31,61,58,.13);border-color:#cdd9b3}'
 '.rcc-svc__ic{width:58px;height:58px;border-radius:15px;background:#eef3e0;display:flex;align-items:center;justify-content:center;margin-bottom:20px}'
 '.rcc-svc__ic svg{width:30px;height:30px}'
 '.rcc-svc__t{font-size:20px;font-weight:700;color:#1f3d3a;margin:0 0 9px;line-height:1.25}'
 '.rcc-svc__d{font-size:15px;line-height:1.6;color:#51615f;margin:0 0 20px;flex:1}'
 '.rcc-svc__more{font-weight:700;color:#1f3d3a;font-size:15px;display:inline-flex;align-items:center;gap:7px;margin-top:auto}'
 '.rcc-svc__card:hover .rcc-svc__more{color:#74900f}'
 '.rcc-svc__more svg{width:18px;height:18px;transition:transform .2s ease}'
 '.rcc-svc__card:hover .rcc-svc__more svg{transform:translateX(5px)}'
 '@media(max-width:980px){.rcc-svc{grid-template-columns:repeat(2,1fr);gap:18px}}'
 '@media(max-width:600px){.rcc-svc{grid-template-columns:1fr}}'
 '</style>'
)

# --- replace the two middle service-list sections with the grid ---
m1 = re.search(r'<main[^>]*>', h); m2 = h.rfind('</main>')
inner = h[m1.end():m2]
open_sec = re.compile(r'<section\b[^>]*>', re.I); tok = re.compile(r'<section\b[^>]*>|</section\s*>', re.I)
blocks, i = [], 0
pre = inner[:open_sec.search(inner).start()]
while True:
    s = open_sec.search(inner, i)
    if not s: break
    depth, j = 1, s.end()
    while depth:
        t = tok.search(inner, j); depth += 1 if t.group(0).lower().startswith('<section') else -1; j = t.end()
    blocks.append(inner[s.start():j]); i = j
post = inner[i:]
assert len(blocks) == 5, f"expected 5 sections, got {len(blocks)}"

# keep [0]hero [1]intro, replace [2]+[3] with grid, keep [4]cta
new_inner = pre + blocks[0] + blocks[1] + GRID_SECTION + blocks[4] + post
h = h[:m1.end()] + new_inner + h[m2:]

# inject style before real </body>
if 'rcc-svc-style' not in h:
    p = max(h.rfind('</body>'), h.rfind('</BODY>'))
    h = h[:p] + STYLE + h[p:]

open(P, "w", encoding="utf-8", errors="surrogateescape").write(h)
print("disability-services.html redesigned:", len(SERVICES), "service cards; sections 5 ->", 3 + 1)
