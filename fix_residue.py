#!/usr/bin/env python3
"""Final residue cleanup:
A) Delete all hidden nested <ul class="dropdown-menu"> fallback lists (stale
   Avivo menu items: veterans, dementia, home modifications, ...) — the
   visible menus are the .cdb-megamenu panels, these ULs never render.
B) Footer: Avivo's Osborne Park address -> Werrington head office.
C) SEO meta/JSON-LD: Rehoboth Live Life, Perth, avivolivelife socials.
D) Replace injected rcc mobile menu with the new IA (fixed end-matching).
E) Remove footer/menu links to SDA/MTA/ILO anchors we don't offer.
"""
import glob, re

MOBILE_NEW = ("p.innerHTML='<a class=\"rcc-mtop\" href=\"index.html\">Home</a>'"
 "+'<details><summary>Accommodation</summary><a href=\"accommodation.html\">Accommodation overview</a><a href=\"accommodation.html#sil\">Supported Independent Living (SIL)</a><a href=\"accommodation.html#sta\">Short Term Accommodation &amp; Respite</a><a href=\"accommodation.html#vacancies\">Current vacancies</a></details>'"
 "+'<details><summary>Services</summary><a href=\"disability-services.html\">All services</a><a href=\"in-home.html\">In-home support</a><a href=\"personal-care.html\">Personal care</a><a href=\"social-and-community.html\">Community participation</a><a href=\"transport-services.html\">Travel &amp; transport</a><a href=\"disability-nursing.html\">Community nursing</a><a href=\"care-management-services.html\">Support coordination</a><a href=\"specialists-services.html\">Specialist &amp; therapy supports</a><a href=\"mental-health.html\">Mental health support</a><a href=\"24-hour-care.html\">24-hour &amp; complex care</a><a href=\"night-services.html\">Night &amp; overnight support</a><a href=\"disability.html\">Who we support</a></details>'"
 "+'<details><summary>NDIS</summary><a href=\"disability-ndis-how-it-works.html\">How it works</a><a href=\"ndis-disability-how-to-apply.html\">How to apply</a><a href=\"funding-options.html\">Funding options</a><a href=\"ndis-pricelist.html\">Pricing</a><a href=\"agency-managed-ndis.html\">Agency-managed</a><a href=\"plan-management-ndis.html\">Plan-managed</a><a href=\"self-management-ndis.html\">Self-managed</a></details>'"
 "+'<details><summary>Carers &amp; respite</summary><a href=\"carers-support.html\">Respite &amp; carer support</a><a href=\"aged-care.html\">Older people &amp; dementia</a></details>'"
 "+'<details><summary>About &amp; resources</summary><a href=\"about.html\">About Rehoboth</a><a href=\"resource-hub.html\">Resource hub &amp; FAQs</a><a href=\"forms.html\">Forms</a><a href=\"refer-to-us.html\">Refer to us</a><a href=\"blog.html\">News &amp; stories</a><a href=\"work-with-us.html\">Work with us</a><a href=\"pay-your-invoice.html\">Pay your invoice</a></details>'"
 "+'<a href=\"contact.html\">Contact us</a>'"
 "+'<a class=\"rcc-mphone\" href=\"tel:1300853095\">Call 1300 853 095</a>';")

stats = {}
def bump(k, n=1): stats[k] = stats.get(k, 0) + n

ul_open = re.compile(r'<ul class="dropdown-menu"[^>]*>', re.IGNORECASE)
ul_tok = re.compile(r'<ul\b[^>]*>|</ul\s*>', re.IGNORECASE)

for f in sorted(glob.glob("/Users/brookw/demorccs/*.html")):
    html = open(f, encoding="utf-8", errors="surrogateescape").read()
    orig = html

    # A) delete nested fallback ULs (balanced), loop until none remain
    while True:
        m = ul_open.search(html)
        if not m: break
        depth, i = 1, m.end()
        while depth:
            t = ul_tok.search(html, i)
            if not t: i = len(html); break
            depth += 1 if t.group(0).lower().startswith('<ul') else -1
            i = t.end()
        html = html[:m.start()] + html[i:]
        bump('fallback-ul-removed')

    # B) footer address
    html, n = re.subn(r'30 Hasler Road, Osborne Park\s*<br\s*/?>\s*Western Australia 6017',
                      '78 William St, Werrington<br /> New South Wales 2747', html)
    bump('footer-address', n)

    # C) SEO meta / JSON-LD
    for old, new in [
        ('Rehoboth Live Life', 'Rehoboth Comprehensive Care'),
        ('Disability Support Services Perth', 'Disability support services across NSW, QLD and NT'),
        (' Perth | Rehoboth', ' | Rehoboth'),
        ('https://www.facebook.com/avivolivelife/', 'https://www.marshillcare.com.au/'),
        ('https://www.linkedin.com/company/avivolivelife/', 'https://www.marshillcare.com.au/'),
        ('https://www.youtube.com/user/PerthHomeCareService', 'https://www.marshillcare.com.au/'),
        ('http://instagram.com/avivolivelife', 'https://www.marshillcare.com.au/'),
    ]:
        n = html.count(old)
        if n:
            html = html.replace(old, new)
            bump('seo:' + old[:24], n)

    # D) mobile menu
    i = html.find("p.innerHTML='<a class=\"rcc-mtop\"")
    if i != -1:
        j = html.find("Call 1300 853 095</a>';", i)
        if j != -1:
            j += len("Call 1300 853 095</a>';")
            html = html[:i] + MOBILE_NEW + html[j:]
            bump('mobile-menu')

    # E) drop li/anchor entries pointing at unoffered accommodation types
    html, n = re.subn(r'<li>\s*<a href="accommodation\.html#(?:sda|mta|ilo)">.*?</a>\s*</li>', '', html, flags=re.DOTALL)
    bump('sda-mta-ilo-li', n)
    html, n = re.subn(r'href="accommodation\.html#(?:sda|mta|ilo)"', 'href="accommodation.html"', html)
    bump('sda-mta-ilo-residual', n)

    if html != orig:
        open(f, "w", encoding="utf-8", errors="surrogateescape").write(html)

print("stats:", stats)
