#!/usr/bin/env python3
"""Semantic menu pass:
1. Rename top item 'Forms' -> 'Veterans' (its panel is the Veterans panel;
   Avivo's real menu had Veterans, and veterans.html now exists).
2. Re-point mislabelled menu links that the original rebrand flattened onto
   resource-hub.html / accommodation.html, matching label -> proper page."""
import glob, re
from html import unescape

# (current href, normalised label) -> new href
RULES = {
 'resource-hub.html': {
    'mental health services': 'mental-health.html',
    'mental health': 'mental-health.html',
    'in-home support': 'in-home.html',
    'social & community support': 'social-and-community.html',
    'respite for carers': 'carers-support.html',
    'specialist services': 'specialists-services.html',
    'icls (individualised community living)': 'mental-health.html',
    'psychosocial support program': 'mental-health.html',
    'family & carer support': 'carers-support.html',
    'veterans': 'veterans.html',
    'veteran services': 'veterans.html',
    'veteran care': 'veterans.html',
    'post-hospital care': 'specialists-services.html',
    'nursing': 'disability-nursing.html',
    'funding options': 'funding-options.html',
    'funding option': 'funding-options.html',
    'how to apply': 'ndis-disability-how-to-apply.html',
    'how it works': 'disability-ndis-how-it-works.html',
    'accommodation': 'accommodation.html',
    'forms': 'forms.html',
    'learn more': None,                      # keep -> resource-hub
    'what is psychosocial support? learn about support available for mental health recovery.': 'mental-health.html',
    'about veteran home care (vhc) find out how to access support through dva programs.': 'veterans.html',
 },
 'accommodation.html': {
    'post-hospital care': 'specialists-services.html',
    'post hospital care': 'specialists-services.html',
    'nursing': 'disability-nursing.html',
    'dementia care': 'aged-care.html',
    'end-of-life care': 'aged-care.html',
    'care management': 'care-management-services.html',
    'agency-managed': 'agency-managed-ndis.html',
    'self-managed': 'self-management-ndis.html',
    'how it works': 'disability-ndis-how-it-works.html',
    'pricelist': 'ndis-pricelist.html',
    'funding options': 'funding-options.html',
    'how to apply': 'ndis-disability-how-to-apply.html',
    'specialist services': 'specialists-services.html',
    'disability support': 'disability.html',
 },
 'contact.html': {
    'make a referral': 'refer-to-us.html',
 },
}

tag_re = re.compile(r'<[^>]+>')
def norm(inner):
    t = unescape(tag_re.sub(' ', inner))
    return re.sub(r'\s+', ' ', t).strip().lower()

a_re = re.compile(r'(<a\b[^>]*?\bhref=")([^"]+)("[^>]*>)(.*?)(</a>)', re.IGNORECASE | re.DOTALL)

stats = {'relink': 0, 'rename': 0}
for f in sorted(glob.glob("/Users/brookw/demorccs/*.html")):
    html = open(f, encoding="utf-8", errors="surrogateescape").read()
    orig = html

    def fix(mo):
        href, label = mo.group(2), norm(mo.group(4))
        rules = RULES.get(href)
        if rules and label in rules and rules[label]:
            stats['relink'] += 1
            return mo.group(1) + rules[label] + mo.group(3) + mo.group(4) + mo.group(5)
        return mo.group(0)
    html = a_re.sub(fix, html)

    # rename top menu item Forms -> Veterans (toggle anchor in both menu copies
    # + the small offcanvas list)
    n = len(re.findall(r'title="Forms"', html))
    html = html.replace('title="Forms" href="resource-hub.html"',
                        'title="Veterans" href="veterans.html"')
    html = re.sub(r'(<span class="nav-link__text">)\s*Forms\s*(</span>)',
                  r'\g<1>Veterans\g<2>', html)
    stats['rename'] += n

    if html != orig:
        open(f, "w", encoding="utf-8", errors="surrogateescape").write(html)
print("stats:", stats)
