#!/usr/bin/env python3
"""Homepage surgery: keep the design, replace the content with real
Rehoboth facts; delete sections that can't be made truthful."""
import re, sys

P = "/Users/brookw/demorccs/index.html"
src = open(P, encoding="utf-8", errors="surrogateescape").read()
m1 = re.search(r'<main[^>]*>', src); m2 = src.rfind('</main>')
head, inner, tail = src[:m1.end()], src[m1.end():m2], src[m2:]

# ── split into top-level <section> blocks ──
open_sec = re.compile(r'<section\b[^>]*>', re.IGNORECASE)
tok = re.compile(r'<section\b[^>]*>|</section\s*>', re.IGNORECASE)
blocks, i = [], 0
pre = inner[:open_sec.search(inner).start()]
while True:
    m = open_sec.search(inner, i)
    if not m: break
    depth, j = 1, m.end()
    while depth:
        t = tok.search(inner, j)
        if not t: j = len(inner); break
        depth += 1 if t.group(0).lower().startswith('<section') else -1
        j = t.end()
    blocks.append(inner[m.start():j]); i = j
post = inner[i:]
assert len(blocks) == 19, f"expected 19 sections, got {len(blocks)}"

def must_replace(b, old, new, what):
    if old not in b:
        print(f"  !! MISSING [{what}]: {old[:70]!r}"); sys.exit(1)
    return b.replace(old, new, 1)

def swap_blob(b, subtitle, title, items, what):
    """Replace subtitle/title and the icon-list labels+hrefs; drop extra <li>s."""
    b = re.sub(r'(<div class="subtitle subtitle--default above">)\s*.*?\s*(</div>)',
               r'\g<1>' + subtitle + r'\g<2>', b, count=1, flags=re.DOTALL)
    b = re.sub(r'(<div class="title h3">)\s*.*?\s*(</div>)',
               r'\g<1>' + title + r'\g<2>', b, count=1, flags=re.DOTALL)
    lis = re.findall(r'<li class="featured-iconlist__item">.*?</li>', b, re.DOTALL)
    if len(lis) < len(items):
        print(f"  !! [{what}] only {len(lis)} li slots for {len(items)} items"); sys.exit(1)
    for k, li in enumerate(lis):
        if k < len(items):
            href, label = items[k]
            new_li = re.sub(r'(<a href=")[^"]*(")', r'\g<1>' + href + r'\g<2>', li, count=1)
            new_li = re.sub(r'(<h6 class="featured-iconlist__title">)\s*.*?\s*(</h6>)',
                            r'\g<1>' + label + r'\g<2>', new_li, count=1, flags=re.DOTALL)
            b = b.replace(li, new_li, 1)
        else:
            b = b.replace(li, '', 1)
    return b

# ── [0] hero: real homepage copy ──
blocks[0] = must_replace(blocks[0], 'Helping you live life, the way you choose.',
    'Hello! We&#8217;re Rehoboth.', 'hero h1')
blocks[0] = must_replace(blocks[0],
    '<p>Rehoboth is a registered NDIS provider supporting people across NSW, QLD, and NT.\n\t\t\t\t\t\t\t\t\tFrom in-home support to supported independent living, we help you live\n\t\t\t\t\t\t\t\t\tindependently, stay connected to your community, and feel safe and supported.</p>',
    '<p>We support NDIS participants across NSW, QLD and NT to achieve wellbeing, independence, and meaningful outcomes that matter to them &#8212; at home, in the community and in our supported independent living homes.</p>',
    'hero lede') if 'Helping' not in blocks[0] else blocks[0]

# ── [1] flip cards: rewrite card texts/links (keep colors/icons) ──
cards = re.findall(r'<a class="flip-card flip-card--vertical".*?</a>', blocks[1], re.DOTALL)
print(f"  flip cards found: {len(cards)}")
NEW_CARDS = [
    ('accommodation.html', 'Accommodation', 'Accommodation',
     'Supported independent living in a place that feels like home, with the everyday help you need to live safely, comfortably, and your way.'),
    ('disability-services.html', 'Services', 'Our services',
     'In-home support, community participation, nursing, transport, respite and support coordination &#8212; personalised to you.'),
    ('disability-ndis-how-it-works.html', 'NDIS', 'NDIS made clear',
     'New to the NDIS? We explain how it works, how to apply, and how your funding can be used.'),
]
for k, card in enumerate(cards):
    if k < len(NEW_CARDS):
        href, front, backtitle, desc = NEW_CARDS[k]
        nc = re.sub(r'(<a class="flip-card flip-card--vertical"[^>]*href=")[^"]*(")', r'\g<1>' + href + r'\g<2>', card, count=1)
        # front title: keep decorative span style of first card form
        nc = re.sub(r'(<h3 class="flip-card__front-title h2">).*?(</h3>)',
                    r'\g<1><span class="tagline tagline--underline">' + front + r'</span>\g<2>', nc, count=1, flags=re.DOTALL)
        nc = re.sub(r'(<h2 class="flip-card__title">)\s*.*?\s*(</h2>)', r'\g<1>' + backtitle + r'\g<2>', nc, count=1, flags=re.DOTALL)
        nc = re.sub(r'(<div class="flip-card__description">\s*<p>)\s*.*?\s*(</p>)', r'\g<1>' + desc + r'\g<2>', nc, count=1, flags=re.DOTALL)
        nc = re.sub(r'(<span href=")[^"]*(" class="btn t-tagline")', r'\g<1>' + href + r'\g<2>', nc, count=1)
        blocks[1] = blocks[1].replace(card, nc, 1)
    else:
        blocks[1] = blocks[1].replace(card, '', 1)

# ── [3]-[7] image blobs ──
blocks[3] = swap_blob(blocks[3], 'Support at home',
    'In-home care that helps you live independently, safely and your way.',
    [('in-home.html','In-home support'), ('personal-care.html','Personal care'),
     ('night-services.html','Night &amp; overnight support'), ('24-hour-care.html','24-hour &amp; complex care'),
     ('funding-options.html','Funding options'), ('ndis-disability-how-to-apply.html','How to apply')], 'blob3')
blocks[4] = swap_blob(blocks[4], 'Empowerment your way',
    'Support to help people with disability live confidently, pursue their goals, and stay connected.',
    [('disability-services.html','Disability support services'), ('disability.html','Who we support'),
     ('specialists-services.html','Specialist &amp; therapy supports'), ('funding-options.html','Funding options'),
     ('disability-ndis-how-it-works.html','How it works'), ('ndis-disability-how-to-apply.html','How to apply')], 'blob4')
blocks[5] = swap_blob(blocks[5], 'Recovery your way',
    'Practical support to help you feel balanced, confident, and connected at your own pace.',
    [('mental-health.html','Mental health support'), ('social-and-community.html','Community participation'),
     ('specialists-services.html','Specialist &amp; therapy supports'), ('ndis-disability-how-to-apply.html','How to apply')], 'blob5')
blocks[6] = swap_blob(blocks[6], 'A place to call home',
    'Supported independent living in homes that feel safe, comfortable and truly yours.',
    [('accommodation.html#sil','Supported Independent Living (SIL)'), ('accommodation.html#sta','Short Term Accommodation &amp; Respite'),
     ('accommodation.html#vacancies','Current vacancies'), ('funding-options.html','Funding options')], 'blob6')
blocks[7] = swap_blob(blocks[7], 'Care for you too',
    'Support to help carers rest, recharge, and continue providing the care that matters most.',
    [('carers-support.html','Respite &amp; carer support'), ('accommodation.html#sta','Short Term Accommodation (STA)'),
     ('funding-options.html','Funding options')], 'blob7')

# ── [8] featured statement: mission ──
blocks[8] = must_replace(blocks[8], 'Supporting Western Australians at home for nearly 60 years.',
    'Our mission: a caring environment where people and families feel heard, supported, and empowered to live life their way.', 'stmt title')
blocks[8], n = re.subn(r'<p>Rehoboth is a registered provider dedicated[^<]*</p>',
    '<p>Rehoboth Comprehensive Care is a registered NDIS provider (Provider Number 4050134271) supporting people across NSW, QLD and NT.</p>', blocks[8], flags=re.DOTALL)
assert n == 1, "stmt p1 not replaced"
blocks[8], n = re.subn(r'<p>Since 1967,[^<]*</p>',
    '<p>Operated by Community Regain Pty Ltd, we provide trusted accommodation, disability and mental health supports, always putting the people we support at the centre of everything we do.</p>', blocks[8], flags=re.DOTALL)
assert n == 1, "stmt p2 not replaced"

# ── [9] dark intro heading ──
blocks[9] = must_replace(blocks[9], 'Find support near you', 'Where we work', 'dark h')
blocks[9] = must_replace(blocks[9], 'We serve 420+ WA suburbs', 'We serve NSW, QLD &amp; the NT', 'dark sub')

# ── [12] why tiles ──
b12 = blocks[12]
for old, new in [
    ('Experience you can trust', 'Personalised NDIS support'),
    ('Trusted by over 55,000 families', 'An experienced, compassionate team'),
]:
    if old in b12: b12 = b12.replace(old, new, 1)
# generic cleanup of any WA/legacy claims in this block's paragraphs
b12 = re.sub(r'For nearly 60 years[^<]*', 'We work alongside individuals, families and carers across NSW, QLD and NT to deliver personalised, high-quality NDIS support. ', b12)
b12 = re.sub(r'Western Australia(ns?)?', 'Australia', b12)
b12 = re.sub(r'(?:more than|over)\s+5[05],000\s+famil\w+', 'families and participants', b12)
b12 = re.sub(r'since\s+1967', 'every day', b12, flags=re.IGNORECASE)
blocks[12] = b12

# ── new sections ──
WHO = '''<section class="section cdb-intro_text sc-lightgrey spt-md spb-md">
<div class="container section-container"><div class="content-container"><div class="section-heading">
<div class="section-heading__title"><div class="title_wrapper intro_text__title title_wrapper--h2"><h2 class="title h2">Who we support</h2></div></div>
<div class="section-heading__description"><p>We provide supports and services for people living with a wide range of disabilities, including:</p>
<ul><li>Intellectual disability</li><li>Acquired brain injury</li><li>Autism</li><li>Spinal injury</li><li>Psychosocial disability</li><li>Physical and sensory disability</li><li>Younger onset dementia</li><li>Degenerative conditions</li></ul>
<div class="btn-row"><a href="disability.html" class="btn dark"><span class="link-text">How we support you</span></a></div></div>
</div></div></div></section>'''
SIL = '''<section class="section cdb-intro_text sc-default spt-md spb-md">
<div class="container section-container"><div class="content-container"><div class="section-heading">
<div class="section-heading__title"><div class="title_wrapper intro_text__title title_wrapper--h2"><h2 class="title h2">Current SIL vacancies</h2></div></div>
<div class="section-heading__description"><p>Find your ideal supported home in one of our welcoming communities &#8212; including Burnside, Blacktown, Werrington, Penrith, Blackheath (Blue Mountains), and our high-physical-support group home in Miranda. SIL properties are currently NSW-only, while our other services extend to QLD and the NT.</p>
<div class="btn-row"><a href="accommodation.html#vacancies" class="btn dark"><span class="link-text">View vacancies</span></a><a href="contact.html" class="btn light"><span class="link-text">Enquire about SIL</span></a></div></div>
</div></div></div></section>'''

# ── assemble: keep 0,1,2,3,4,5,6,7 + WHO + 8 + 9 + SIL + 12 + 18 ──
keep = blocks[:8] + [WHO, blocks[8], blocks[9], SIL, blocks[12], blocks[18]]
new_inner = pre + "\n".join(keep) + post
out = head + new_inner + tail
open(P, "w", encoding="utf-8", errors="surrogateescape").write(out)
print(f"index rebuilt: {len(src)//1024}KB -> {len(out)//1024}KB, sections 19 -> {len(keep)}")
