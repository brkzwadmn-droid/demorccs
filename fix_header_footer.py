#!/usr/bin/env python3
"""Global header/footer overhaul for the real-Rehoboth IA:
- Toggles: Disability->Services, Veterans->NDIS (labels, titles, hrefs)
- All 5 inline mega-panels rebuilt with correct links/copy (simple columns)
- Footer: acknowledgement WA->Australia, copyright line with real entity,
  veteran links relabelled
- Delete the inert hc-offcanvas-nav (stale Avivo menu content)
- Update the injected rcc mobile menu to the new IA
- Restore empty <img src=""> from data-savepage-src URLs
"""
import glob, re

def panel(title, desc, learn, cols):
    colhtml = ''.join(
        '<div class="megamenu__column"><h6>%s</h6><ul>%s</ul></div>' %
        (ct, ''.join(f'<li><a href="{h}">{l}</a></li>' for h, l in items))
        for ct, items in cols)
    return ('<div class="megamenu-wrapper"><div class="container">'
            f'<div class="megamenu__description"><h3>{title}</h3><p>{desc}</p>'
            f'<a href="{learn}" class="btn t-tagline"><span class="link-text">Learn more</span></a></div>'
            f'<div class="megamenu__content">{colhtml}</div>'
            '</div></div>')

PANELS = {
 'megamenu-22': panel('Accommodation',
   'A home should feel like yours. Our supported homes are safe, comfortable, and shaped around how you want to live.',
   'accommodation.html',
   [('Accommodation', [('accommodation.html#sil','Supported Independent Living (SIL)'),
                       ('accommodation.html#sta','Short Term Accommodation (STA) &amp; Respite'),
                       ('accommodation.html#vacancies','Current vacancies')]),
    ('Getting started', [('funding-options.html','Funding options'),
                         ('ndis-disability-how-to-apply.html','How to apply'),
                         ('refer-to-us.html','Make a referral'),
                         ('contact.html','Contact us')])]),
 'megamenu-2325': panel('Our services',
   'Personalised NDIS support that empowers independence and connection &#8212; at home and in your community.',
   'disability-services.html',
   [('Everyday support', [('in-home.html','In-home support'),
                          ('personal-care.html','Personal care'),
                          ('social-and-community.html','Community participation'),
                          ('transport-services.html','Travel &amp; transport'),
                          ('disability-nursing.html','Community nursing')]),
    ('Specialist support', [('specialists-services.html','Specialist &amp; therapy supports'),
                            ('mental-health.html','Mental health support'),
                            ('24-hour-care.html','24-hour &amp; complex care'),
                            ('night-services.html','Night &amp; overnight support'),
                            ('care-management-services.html','Support coordination')]),
    ('Who we support', [('disability.html','Disabilities we support'),
                        ('aged-care.html','Older people &amp; dementia'),
                        ('carers-support.html','Respite &amp; carers')])]),
 'megamenu-24': panel('Resources',
   'Guides, forms and answers to the questions families ask us most.',
   'resource-hub.html',
   [('Resources', [('resource-hub.html','Resource hub &amp; FAQs'),
                   ('forms.html','Forms'),
                   ('refer-to-us.html','Refer to us'),
                   ('blog.html','News &amp; stories'),
                   ('privacy-policy.html','Privacy policy')]),
    ('Help', [('ndis-pricelist.html','Pricing'),
              ('pay-your-invoice.html','Pay your invoice'),
              ('work-with-us.html','Work with us'),
              ('contact.html','Contact us')])]),
 'megamenu-2327': panel('NDIS made clear',
   'New to the NDIS? We help you understand how it works, how to apply, and how to use your funding.',
   'disability-ndis-how-it-works.html',
   [('Understand the NDIS', [('disability-ndis-how-it-works.html','How the NDIS works'),
                             ('ndis-disability-how-to-apply.html','How to apply'),
                             ('funding-options.html','Funding options'),
                             ('ndis-pricelist.html','Pricing')]),
    ('Manage your plan', [('agency-managed-ndis.html','Agency-managed'),
                          ('plan-management-ndis.html','Plan-managed'),
                          ('self-management-ndis.html','Self-managed')])]),
 'megamenu-2328': panel('Carers &amp; respite',
   'Support to help carers rest, recharge, and keep providing the care that matters most.',
   'carers-support.html',
   [('For carers', [('carers-support.html','Respite &amp; carer support'),
                    ('accommodation.html#sta','Short Term Accommodation (STA)'),
                    ('refer-to-us.html','Make a referral'),
                    ('contact.html','Contact us')]),
    ('More', [('funding-options.html','Funding options'),
              ('https://www.carergateway.gov.au/','Carer Gateway (government support)')])]),
}

open_div = re.compile(r'<div\b[^>]*>', re.IGNORECASE)
any_div = re.compile(r'<div\b[^>]*>|</div\s*>', re.IGNORECASE)

def balanced(html, start, opentag=re.compile(r'<div\b[^>]*>', re.I), tok=any_div, open_name='<div'):
    m = opentag.match(html, start)
    depth, i = 1, m.end()
    while depth:
        t = tok.search(html, i)
        if not t: return None
        depth += 1 if t.group(0).lower().startswith(open_name) else -1
        i = t.end()
    return i

MOBILE_OLD_START = "p.innerHTML='<a class=\"rcc-mtop\" href=\"index.html\">Home</a>'"
MOBILE_NEW = """p.innerHTML='<a class="rcc-mtop" href="index.html">Home</a>'
      +'<details><summary>Accommodation</summary><a href="accommodation.html">Accommodation overview</a><a href="accommodation.html#sil">Supported Independent Living (SIL)</a><a href="accommodation.html#sta">Short Term Accommodation &amp; Respite</a><a href="accommodation.html#vacancies">Current vacancies</a></details>'
      +'<details><summary>Services</summary><a href="disability-services.html">All services</a><a href="in-home.html">In-home support</a><a href="personal-care.html">Personal care</a><a href="social-and-community.html">Community participation</a><a href="transport-services.html">Travel &amp; transport</a><a href="disability-nursing.html">Community nursing</a><a href="care-management-services.html">Support coordination</a><a href="specialists-services.html">Specialist &amp; therapy supports</a><a href="mental-health.html">Mental health support</a><a href="24-hour-care.html">24-hour &amp; complex care</a><a href="night-services.html">Night &amp; overnight support</a><a href="disability.html">Who we support</a></details>'
      +'<details><summary>NDIS</summary><a href="disability-ndis-how-it-works.html">How it works</a><a href="ndis-disability-how-to-apply.html">How to apply</a><a href="funding-options.html">Funding options</a><a href="ndis-pricelist.html">Pricing</a><a href="agency-managed-ndis.html">Agency-managed</a><a href="plan-management-ndis.html">Plan-managed</a><a href="self-management-ndis.html">Self-managed</a></details>'
      +'<details><summary>Carers &amp; respite</summary><a href="carers-support.html">Respite &amp; carer support</a><a href="aged-care.html">Older people &amp; dementia</a></details>'
      +'<details><summary>About &amp; resources</summary><a href="about.html">About Rehoboth</a><a href="resource-hub.html">Resource hub &amp; FAQs</a><a href="forms.html">Forms</a><a href="refer-to-us.html">Refer to us</a><a href="blog.html">News &amp; stories</a><a href="work-with-us.html">Work with us</a><a href="pay-your-invoice.html">Pay your invoice</a></details>'
      +'<a href="contact.html">Contact us</a>'
      +'<a class="rcc-mphone" href="tel:1300853095">Call 1300 853 095</a';"""

stats = {}
def bump(k, n=1): stats[k] = stats.get(k, 0) + n

for f in sorted(glob.glob("/Users/brookw/demorccs/*.html")):
    html = open(f, encoding="utf-8", errors="surrogateescape").read()
    orig = html

    # A) toggles
    n = html.count('title="Disability" href="disability.html"')
    html = html.replace('title="Disability" href="disability.html"', 'title="Services" href="disability-services.html"')
    bump('toggle-services', n)
    html, n = re.subn(r'(class="nav-link__text">)\s*Disability\s*(</span>)', r'\g<1>Services\g<2>', html); bump('label-services', n)
    n = html.count('title="Veterans" href="veterans.html"')
    html = html.replace('title="Veterans" href="veterans.html"', 'title="NDIS" href="disability-ndis-how-it-works.html"')
    bump('toggle-ndis', n)
    html, n = re.subn(r'(class="nav-link__text">)\s*Veterans\s*(</span>)', r'\g<1>NDIS\g<2>', html); bump('label-ndis', n)

    # B) rebuild INLINE megamenu panel contents (header region only; offscreen equalized later)
    main_pos = html.find('<main')
    for pid, content in PANELS.items():
        m = re.search(r'<div\b[^>]*class="cdb-megamenu dropdown-menu"[^>]*id="' + pid + '"[^>]*>', html[:main_pos])
        if not m: continue
        end = balanced(html, m.start())
        html = html[:m.end()] + content + '</div>' + html[end:]
        main_pos = html.find('<main')
        bump('panel-rebuilt')

    # C) footer fixes
    html, n = re.subn(r'throughout Western Australia', 'throughout Australia', html); bump('ack', n)
    html, n = re.subn(r'Copyright © 2025 Rehoboth Live Life',
        'Copyright © 2026 Rehoboth Comprehensive Care Services &middot; Community Regain Pty Ltd &middot; ABN 12 657 939 896 &middot; NDIS Provider 4050134271', html)
    bump('copyright', n)
    # footer veteran links -> NDIS guide / services
    html, n = re.subn(r'(<a href=")veterans\.html("[^>]*>)\s*Veteran[^<]*(</a>)', r'\g<1>disability-ndis-how-it-works.html\g<2>NDIS guide\g<3>', html); bump('footer-vet-links', n)
    # any remaining anchors TO veterans.html -> services
    html, n = re.subn(r'href="veterans\.html"', 'href="disability-services.html"', html); bump('vet-href-residual', n)

    # D) delete inert offcanvas nav (stale content incl. veterans/SDA labels)
    m = re.search(r'<nav\b[^>]*class="[^"]*hc-offcanvas-nav[^"]*"[^>]*>', html)
    if m:
        end = balanced(html, m.start(), opentag=re.compile(r'<nav\b[^>]*>', re.I),
                       tok=re.compile(r'<nav\b[^>]*>|</nav\s*>', re.I), open_name='<nav')
        if end:
            html = html[:m.start()] + html[end:]
            bump('offcanvas-removed')

    # E) update rcc mobile menu (replace from p.innerHTML= ... up to the closing ;)
    i = html.find(MOBILE_OLD_START)
    if i != -1:
        j = html.find("'Call 1300 853 095</a>';", i)
        if j != -1:
            j += len("'Call 1300 853 095</a>';")
            html = html[:i] + MOBILE_NEW.replace("</a';", "</a>';") + html[j:]
            bump('mobile-menu')

    # F) More menu: drop the invented "The Rehoboth Foundation" item
    html, n = re.subn(r'<li>\s*<a href="about\.html"[^>]*>\s*The Rehoboth Foundation\s*</a>\s*</li>', '', html); bump('foundation-li', n)

    # G) restore empty lazy-load img srcs from data-savepage-src
    html, n = re.subn(r'(data-savepage-src="(https://www\.avivo\.org\.au[^"]+)"[^>]*?\bsrc=")"',
                      lambda mo: mo.group(1) + mo.group(2) + '"', html)
    bump('img-src-restored', n)

    if html != orig:
        open(f, "w", encoding="utf-8", errors="surrogateescape").write(html)

print("stats:", stats)
