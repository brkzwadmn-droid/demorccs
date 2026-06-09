#!/usr/bin/env python3
"""Master link rewrite: point every dead/Avivo/misdirected link at a real
local page (or whitelisted external). Also fixes the leftover Avivo phone
number in body CTAs, the search form, the head-office map link, and socials.
Run AFTER the new pages exist."""
import glob, re
from html import unescape

BASE = "https://www.avivo.org.au"

# 1) Exact-URL map (longest first). CSS/media URLs are intentionally absent.
URL_MAP = {
    BASE + "/resource-hub/policies/privacy-policy": "privacy-policy.html",
    BASE + "/about-avivo/customer-involvement": "about.html",
    BASE + "/about-avivo/the-avivo-foundation": "about.html",
    BASE + "/about-avivo/diversity-inclusion": "about.html",
    BASE + "/about-avivo/our-partnerships": "about.html",
    BASE + "/about-avivo/our-initiatives": "about.html",
    BASE + "/about-avivo/how-we-work": "about.html",
    BASE + "/about-avivo/our-team": "about.html",
    BASE + "/about-avivo/about-us": "about.html",
    BASE + "/disability/disability-services": "accommodation.html",
    BASE + "/contact-us/feedback": "contact.html",
    BASE + "/contact-us": "contact.html",
    BASE + "/customer-portal": "contact.html",
    BASE + "/your-journey": "contact.html",
    BASE + "/locations": "contact.html#locations",
    BASE + "/resource-hub": "resource-hub.html",
    BASE + "/work-with-us": "work-with-us.html",
    BASE + "/refer-to-us": "refer-to-us.html",
    BASE + "/pay-your-invoice": "pay-your-invoice.html",
    # PDFs: brochures/fees -> contact (request a copy); pricelist -> official NDIS pricing
    BASE + "/wp-content/uploads/2026/03/MAR26-AGED-CARE-BROCHURE-12pp-FINAL.pdf": "contact.html",
    BASE + "/wp-content/uploads/2026/03/MAR26-DISABILITY-BROCHURE-WEB.pdf": "contact.html",
    BASE + "/wp-content/uploads/2025/12/NDIS-rates-schedule-AUG25.pdf": "https://www.ndis.gov.au/providers/pricing-arrangements",
    BASE + "/wp-content/uploads/2025/10/FFS-Fees-JUL25.pdf": "contact.html",
    BASE + "/wp-content/uploads/2025/10/FFS-Remote-Fees-JUL25.pdf": "contact.html",
    BASE + "/wp-content/uploads/2025/10/FFS-Very-Remote-Fees-JUL25.pdf": "contact.html",
}
# prefix rules for whole families
PREFIX_MAP = [
    (BASE + "/blog", "blog.html"),
    (BASE + "/veterans", "veterans.html"),
]

# 2) '#'-link labels -> targets
HASH_LABELS = {
    "supported independent living (sil)": "accommodation.html#sil",
    "specialist disability accommodation (sda)": "accommodation.html#sda",
    "short term accommodation (sta) & respite": "accommodation.html#sta",
    "medium term accommodation (mta)": "accommodation.html#mta",
    "individualised living options (ilo)": "accommodation.html#ilo",
    "support in your home": "in-home.html",
    "help with daily living": "personal-care.html",
    "personal care": "personal-care.html",
    "high support and complex care": "specialists-services.html",
    "household tasks": "in-home.html",
    "building independence and life skills": "social-and-community.html",
    "community participation": "social-and-community.html",
    "getting started": "ndis-disability-how-to-apply.html",
    "specialist services": "specialists-services.html",
    "view all crisis contacts": "mental-health.html",
}
# 3) labels wrongly pointing at index.html -> real targets
INDEX_LABELS = {
    "work with us": "work-with-us.html",
    "customer portal": "contact.html",
    "resource hub": "resource-hub.html",
    "blog": "blog.html",
    "pay your invoice": "pay-your-invoice.html",
    "locations": "contact.html#locations",
    "careers": "work-with-us.html",
}

SOCIALS = {
    "https://www.facebook.com/avivolivelife/": "https://www.marshillcare.com.au/",
    "https://www.linkedin.com/company/avivolivelife/": "https://www.marshillcare.com.au/",
    "https://www.youtube.com/user/PerthHomeCareService": "https://www.marshillcare.com.au/",
    "http://instagram.com/avivolivelife": "https://www.marshillcare.com.au/",
}

MAPS_NEW = "https://www.google.com/maps/search/?api=1&query=78+William+St%2C+Werrington+NSW+2747"

tag_re = re.compile(r'<[^>]+>')
a_hash_re = re.compile(r'(<a\b[^>]*?\bhref\s*=\s*")(#)("[^>]*>)(.*?)(</a>)', re.IGNORECASE | re.DOTALL)
a_index_re = re.compile(r'(<a\b[^>]*?\bhref\s*=\s*")(index\.html)("[^>]*>)(.*?)(</a>)', re.IGNORECASE | re.DOTALL)

def norm(inner):
    return unescape(tag_re.sub(' ', inner)).strip().lower().replace('’', "'").replace('&amp;', '&')

def norm_label(inner):
    return re.sub(r'\s+', ' ', norm(inner))

stats = {}
def bump(k, n=1):
    stats[k] = stats.get(k, 0) + n

for f in sorted(glob.glob("/Users/brookw/demorccs/*.html")):
    with open(f, encoding="utf-8", errors="surrogatepass") as fh:
        html = fh.read()
    orig = html

    # exact URL map (also handle trailing slash variants)
    for url, tgt in sorted(URL_MAP.items(), key=lambda kv: -len(kv[0])):
        for variant in (url, url + "/"):
            for q in ('"', "'"):
                needle = f'href={q}{variant}{q}'
                n = html.count(needle)
                if n:
                    html = html.replace(needle, f'href={q}{tgt}{q}')
                    bump('url-map', n)

    # prefix families (blog/*, veterans/*)
    def family(mo):
        bump('prefix-map')
        return f'href={mo.group(1)}{mo.group(3)}{mo.group(1)}'
    for pre, tgt in PREFIX_MAP:
        html = re.sub(
            r'href=(["\'])' + re.escape(pre) + r'[^"\']*\1',
            lambda mo, t=tgt: (bump('prefix-map') or f'href={mo.group(1)}{t}{mo.group(1)}'),
            html)

    # '#' labels
    def fix_hash(mo):
        label = norm_label(mo.group(4))
        tgt = HASH_LABELS.get(label)
        if tgt:
            bump('hash-label')
            return mo.group(1) + tgt + mo.group(3) + mo.group(4) + mo.group(5)
        return mo.group(0)
    html = a_hash_re.sub(fix_hash, html)

    # index.html mislabels
    def fix_index(mo):
        label = norm_label(mo.group(4))
        tgt = INDEX_LABELS.get(label)
        if tgt:
            bump('index-label')
            return mo.group(1) + tgt + mo.group(3) + mo.group(4) + mo.group(5)
        return mo.group(0)
    html = a_index_re.sub(fix_index, html)

    # socials
    for old, new in SOCIALS.items():
        n = html.count(f'href="{old}"')
        if n:
            html = html.replace(f'href="{old}"', f'href="{new}"')
            bump('socials', n)

    # head office map link (any google.com/maps/dir variant)
    html, n = re.subn(r'href="https://www\.google\.com/maps/dir/[^"]*"',
                      f'href="{MAPS_NEW}"', html)
    bump('maps', n)

    # leftover Avivo phone in body CTAs
    for old in ('tel:1300%20428%20486', 'tel:1300 428 486', 'tel:1300428486'):
        n = html.count(f'href="{old}"')
        if n:
            html = html.replace(f'href="{old}"', 'href="tel:1300853095"')
            bump('phone-href', n)
    n = html.count('1300 428 486')
    if n:
        html = html.replace('1300 428 486', '1300 853 095')
        bump('phone-text', n)

    # search form -> DuckDuckGo site search
    new_form = ('<form method="get" id="searchform" action="https://duckduckgo.com/" role="search">'
                '<input type="hidden" name="sites" value="brkzwadmn-droid.github.io">')
    n = html.count('<form method="get" id="searchform" action="https://www.avivo.org.au/" role="search">')
    if n:
        html = html.replace('<form method="get" id="searchform" action="https://www.avivo.org.au/" role="search">', new_form)
        html = html.replace('id="s" name="s" type="text"', 'id="s" name="q" type="text"')
        bump('searchform', n)

    if html != orig:
        with open(f, "w", encoding="utf-8", errors="surrogatepass") as fh:
            fh.write(html)

print("Rewrite stats:", stats)
