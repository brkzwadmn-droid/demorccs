#!/usr/bin/env python3
"""Re-render all 32 subpages in the new design language (same shell as the
flagship homepage): topbar, sticky nav, curved dividers, check-list styling,
lime CTA box, footer with Acknowledgement of Country. Ports each page's
existing (compliance-reviewed) content; preserves section ids/anchors.
Replaces the old captured-theme shells entirely (no more savepage scripts)."""
import re, glob, os, html as H

LOGO = open('/tmp/rehoboth_logo.txt').read().strip()
FAVICON = open('/tmp/rehoboth_favicon.txt').read().strip()
NDIS_BADGE = open('/tmp/indis_badge.txt').read().strip()

def icon(inner, stroke='#0e3a40'):
    return ('<svg aria-hidden="true" focusable="false" viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.9" '
            'stroke-linecap="round" stroke-linejoin="round">' + inner + '</svg>')
IC = {
 'phone': '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
 'mail':  '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/>',
 'pin':   '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
 'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
}
SQUIG = '<svg aria-hidden="true" focusable="false" viewBox="0 0 96 24" fill="none"><path d="M3 12 C11 4 19 4 27 12 C35 20 43 20 51 12 C59 4 67 4 75 12 C83 20 91 20 93 12" stroke="currentColor" stroke-width="4" stroke-linecap="round"/></svg>'
SPARK = '<svg aria-hidden="true" focusable="false" class="spark" viewBox="0 0 24 24"><path d="M12 1c.8 6.2 4.8 10.2 11 11-6.2.8-10.2 4.8-11 11-.8-6.2-4.8-10.2-11-11C7.2 11.2 11.2 7.2 12 1Z" fill="currentColor"/></svg>'

NAV_ITEMS = [
 ('accommodation.html', 'SIL homes'), ('disability-services.html', 'Services'),
 ('disability-ndis-how-it-works.html', 'NDIS'), ('about.html', 'About us'),
 ('work-with-us.html', 'Careers'), ('resource-hub.html', 'Resources'),
]

CSS = '''
:root { --teal:#0e3a40; --teal-deep:#092b30; --teal-soft:#11464d; --lime:#a9c81e; --lime-bright:#c4d600;
 --lime-pale:#eef3da; --lime-glow:#dff066; --olive:#5d7610; --cream:#faf8f2; --sand:#f3efe4; --ink:#15333a;
 --mut:#5c6f6d; --r-lg:22px; --r-md:16px; --shadow:0 20px 50px rgba(14,58,64,.13); --max:1100px; }
* { margin:0; padding:0; box-sizing:border-box; }
.skip-link { position:absolute; left:-9999px; top:0; background:var(--teal); color:#fff; padding:12px 22px; z-index:2000; border-radius:0 0 10px 0; font-weight:700; }
.skip-link:focus { left:0; }
html { scroll-behavior:smooth; }
body { font-family:'Montserrat',system-ui,sans-serif; color:var(--ink); background:var(--cream); line-height:1.7; font-size:16.5px; overflow-x:hidden; }
img { max-width:100%; display:block; } a { color:inherit; text-decoration:none; } ul { list-style:none; }
.wrap { max-width:var(--max); margin:0 auto; padding:0 24px; position:relative; }
h1,h2,h3 { line-height:1.2; color:var(--teal); font-weight:800; letter-spacing:-.01em; }
.eyebrow { display:inline-flex; align-items:center; gap:10px; font-size:13px; font-weight:700; letter-spacing:.16em; text-transform:uppercase; color:var(--olive); margin-bottom:14px; }
.eyebrow::before { content:""; width:34px; height:3px; border-radius:2px; background:var(--lime-bright); }
.curve { line-height:0; margin-bottom:-1px; } .curve svg { width:100%; height:64px; display:block; }
@media (max-width:700px){ .curve svg{ height:38px; } }
.deco { position:absolute; pointer-events:none; color:var(--lime); z-index:0; }
.spark { width:24px; height:24px; animation:twinkle 3.2s ease-in-out infinite; display:block; }
@keyframes twinkle { 0%,100%{ transform:scale(.55) rotate(0); opacity:.45; } 50%{ transform:scale(1) rotate(18deg); opacity:1; } }
.btn { display:inline-flex; align-items:center; gap:10px; font-weight:700; font-size:16px; border-radius:999px; padding:15px 28px; transition:.25s; cursor:pointer; border:2px solid transparent; }
.btn svg { width:18px; height:18px; transition:transform .25s; } .btn:hover svg { transform:translateX(4px); }
.btn-lime { background:var(--lime-bright); color:var(--teal); box-shadow:0 10px 26px rgba(169,200,30,.4); }
.btn-lime:hover { background:var(--lime); transform:translateY(-2px); }
.btn-ghost { border-color:rgba(14,58,64,.25); color:var(--teal); }
.btn-ghost:hover { border-color:var(--teal); background:var(--teal); color:#fff; }
.btn-teal { background:var(--teal); color:#fff; } .btn-teal:hover { background:var(--teal-soft); transform:translateY(-2px); }
.btn-white { background:#fff; color:var(--teal); } .btn-white:hover { transform:translateY(-2px); }
.btns { display:flex; gap:14px; flex-wrap:wrap; margin-top:22px; }
.topbar { background:var(--teal-deep); color:#cfe0d8; font-size:13.5px; font-weight:600; position:relative; z-index:901; }
.topbar .wrap { display:flex; justify-content:space-between; align-items:center; min-height:42px; gap:14px; max-width:1180px; }
.topbar a { color:#fff; display:inline-flex; align-items:center; gap:7px; white-space:nowrap; }
.topbar svg { width:15px; height:15px; } .topbar em { color:var(--lime-glow); font-style:normal; }
.topbar .tb-r { display:flex; gap:22px; }
@media (max-width:760px){ .topbar .tb-r .hide-s{ display:none; } .topbar .tb-l{ font-size:12px; } }
.nav { position:sticky; top:0; z-index:900; background:rgba(250,248,242,.92); backdrop-filter:blur(14px); border-bottom:1px solid rgba(14,58,64,.07); transition:box-shadow .3s; }
.nav.scrolled { box-shadow:0 6px 30px rgba(14,58,64,.1); }
.nav .wrap { display:flex; align-items:center; gap:34px; min-height:84px; max-width:1180px; }
.nav .logo img { height:40px; width:auto; }
.nav nav.primary { display:flex; gap:28px; margin-left:auto; }
.nav nav.primary a { font-weight:600; font-size:15.5px; color:var(--ink); position:relative; padding:6px 0; }
.nav nav.primary a::after { content:""; position:absolute; left:0; bottom:0; width:0; height:2.5px; border-radius:2px; background:var(--lime-bright); transition:width .25s; }
.nav nav.primary a:hover::after, .nav nav.primary a.on::after { width:100%; }
.nav .nav-cta .btn { padding:12px 22px; font-size:15px; }
.burger { display:none; margin-left:auto; background:var(--teal); color:#fff; border:0; border-radius:10px; width:46px; height:46px; font-size:22px; cursor:pointer; }
.nav nav.mobile-menu { display:none; background:#fff; border-bottom:1px solid #eee; }
.nav nav.mobile-menu.open { display:block; }
.mobile-menu a { display:block; padding:15px 26px; font-weight:600; border-top:1px solid #f1efe8; }
.mobile-menu .mcall { background:var(--lime-bright); text-align:center; font-weight:800; }
@media (max-width:1020px){ .nav nav.primary, .nav .nav-cta{ display:none; } .burger{ display:block; } }
/* page hero */
.phero { padding:64px 0 56px; position:relative; }
.phero .crumb { font-size:14px; font-weight:600; color:var(--mut); margin-bottom:18px; display:flex; gap:8px; align-items:center; flex-wrap:wrap; }
.phero .crumb a { color:var(--olive); } .phero .crumb a:hover { text-decoration:underline; }
.phero h1 { font-size:clamp(34px,4.2vw,52px); max-width:820px; margin-bottom:18px; }
.phero .lede { color:var(--mut); font-size:18.5px; max-width:680px; }
.phero .deco-squig { right:6%; top:30px; width:80px; transform:rotate(8deg); }
.phero .deco-spark { right:12%; top:108px; color:var(--lime-bright); }
/* content sections */
.sect { padding:64px 0; position:relative; }
.sect.alt { background:var(--sand); }
.sect h2 { font-size:clamp(24px,2.8vw,34px); margin-bottom:20px; max-width:760px; }
.prose { max-width:820px; color:#42555312; }
.prose p { color:#4a5e5c; margin:0 0 16px; }
.prose p:last-child { margin-bottom:0; }
.prose strong { color:var(--teal); }
.prose a { color:var(--olive); font-weight:600; text-decoration:underline; text-decoration-color:rgba(169,200,30,.6); text-underline-offset:3px; }
.prose a:hover { text-decoration-color:var(--olive); }
.prose a.btn { text-decoration:none; color:inherit; }
.prose a.btn.btn-teal { color:#fff; }
.prose h3 { font-size:19.5px; margin:26px 0 10px; padding-left:16px; border-left:4px solid var(--lime-bright); }
.prose ul { margin:6px 0 18px; display:grid; gap:11px; padding:0; }
.prose ul li { position:relative; padding-left:30px; color:#4a5e5c; font-weight:500; list-style:none; }
.prose ul li::before { content:""; position:absolute; left:0; top:.32em; width:17px; height:17px; border-radius:50%;
 background:var(--lime-pale) url('data:image/svg+xml;utf8,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke=%22%235d7610%22 stroke-width=%223.4%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22><path d=%22M20 6 9 17l-5-5%22/></svg>') no-repeat center/10px; }
.prose ol { margin:6px 0 18px 22px; display:grid; gap:10px; color:#4a5e5c; }
/* CTA box */
.ctabox-wrap { padding:72px 0 88px; }
.ctabox { background:linear-gradient(115deg, var(--lime-bright), var(--lime)); border-radius:var(--r-lg); padding:52px 50px; display:grid; grid-template-columns:1.25fr .75fr; gap:36px; align-items:center; position:relative; overflow:hidden; }
.ctabox::after { content:""; position:absolute; right:-90px; top:-90px; width:280px; height:280px; border-radius:50%; background:rgba(255,255,255,.22); }
.ctabox h2 { font-size:clamp(24px,2.8vw,34px); }
.ctabox .acts { display:flex; gap:14px; flex-wrap:wrap; justify-content:flex-end; position:relative; z-index:1; }
@media (max-width:860px){ .ctabox{ grid-template-columns:1fr; text-align:center; } .ctabox .acts{ justify-content:center; } }
/* footer */
footer { background:var(--teal-deep); color:#bdd2c9; font-size:14.5px; }
.f-main { display:grid; grid-template-columns:1.3fr 1fr 1fr 1fr; gap:44px; padding:70px 0 46px; max-width:1180px; margin:0 auto; padding-left:24px; padding-right:24px; }
.f-main .logo img { height:38px; width:auto; margin-bottom:18px; filter:brightness(1.15); }
.f-main .fh { color:#fff; font-size:15.5px; font-weight:700; margin-bottom:18px; }
.f-main li { margin-bottom:11px; } .f-main a:hover { color:var(--lime-glow); }
.f-contact li { display:flex; gap:11px; align-items:flex-start; }
.f-contact svg { width:17px; height:17px; flex:none; margin-top:3px; }
.f-badge { display:flex; align-items:center; gap:14px; margin-top:22px; background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.1); padding:13px 17px; border-radius:13px; max-width:330px; }
.f-badge img { width:52px; height:52px; } .f-badge span { font-size:13px; line-height:1.45; }
.ack { border-top:1px solid rgba(255,255,255,.1); padding:34px 24px; display:flex; gap:22px; align-items:flex-start; max-width:1180px; margin:0 auto; }
.ack-flags { display:flex; gap:8px; flex:none; margin-top:4px; }
.ack-flags svg { width:42px; height:27px; border-radius:4px; }
.ack p { font-size:13.5px; line-height:1.7; max-width:880px; }
.f-bottom { border-top:1px solid rgba(255,255,255,.1); padding:22px 24px 28px; display:flex; justify-content:space-between; gap:14px; flex-wrap:wrap; font-size:13px; max-width:1180px; margin:0 auto; }
.f-bottom a { text-decoration:underline; text-underline-offset:3px; }
@media (max-width:920px){ .f-main{ grid-template-columns:1fr 1fr; } }
@media (max-width:560px){ .f-main{ grid-template-columns:1fr; } .ack{ flex-direction:column; } }
/* svc grid (services overview page) */
.svc-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:24px; margin-top:44px; }
.svc { border-radius:var(--r-md); padding:30px 28px; display:flex; flex-direction:column; gap:10px; border:1px solid rgba(14,58,64,.05); background:#fff; transition:transform .3s, box-shadow .3s; }
.svc:hover { transform:translateY(-7px); box-shadow:var(--shadow); }
.svc-ic { width:62px; height:62px; border-radius:18px; background:linear-gradient(140deg,#f4f8e4,#ffffff 70%); border:1px solid #e6ecd2; display:flex; align-items:center; justify-content:center; margin-bottom:8px; box-shadow:0 10px 22px rgba(14,58,64,.08); }
.svc-ic svg { width:34px; height:34px; }
.svc h3 { font-size:18.5px; border:none; padding:0; margin:0; }
.svc p { color:var(--mut); font-size:14.5px; flex:1; margin:0; }
.more { display:inline-flex; align-items:center; gap:8px; font-weight:700; color:var(--teal); font-size:15px; margin-top:auto; padding-top:6px; }
.more svg { width:17px; height:17px; transition:transform .25s; }
.svc:hover .more svg { transform:translateX(5px); } .svc:hover .more { color:var(--olive); }
@media (max-width:920px){ .svc-grid{ grid-template-columns:repeat(2,1fr); } }
@media (max-width:620px){ .svc-grid{ grid-template-columns:1fr; } }
/* reveal */
.js .reveal { opacity:0; transform:translateY(24px); transition:opacity .65s ease var(--d,0s), transform .65s ease var(--d,0s); }
.js .reveal.in { opacity:1; transform:none; }
@media (prefers-reduced-motion:reduce){ *,*::before,*::after{ animation:none !important; transition:none !important; } html{ scroll-behavior:auto; } .js .reveal{ opacity:1; transform:none; } }
'''

def curve(prev_bg, next_fill, variant=1):
    paths = {1:'M0,64 C240,96 480,8 760,40 C1040,72 1280,88 1440,40 L1440,96 L0,96 Z',
             2:'M0,48 C320,96 640,0 900,48 C1160,92 1320,72 1440,48 L1440,96 L0,96 Z'}
    return (f'<div class="curve" aria-hidden="true" style="background:{prev_bg}"><svg viewBox="0 0 1440 96" preserveAspectRatio="none">'
            f'<path d="{paths[variant]}" fill="{next_fill}"/></svg></div>')

FLAGS = ('<div class="ack-flags">'
 '<svg role="img" focusable="false" viewBox="0 0 60 40" aria-label="Aboriginal flag"><rect width="60" height="20" fill="#000"/><rect y="20" width="60" height="20" fill="#cc0000"/><circle cx="30" cy="20" r="9" fill="#ffce00"/></svg>'
 '<svg role="img" focusable="false" viewBox="0 0 60 40" aria-label="Torres Strait Islander flag"><rect width="60" height="40" fill="#0052b4"/><rect y="7" width="60" height="5" fill="#000"/><rect y="28" width="60" height="5" fill="#000"/><rect y="12" width="60" height="16" fill="#009543"/><path d="M30 13l1.8 3.6 4 .6-2.9 2.8.7 4-3.6-1.9-3.6 1.9.7-4-2.9-2.8 4-.6z" fill="#fff"/></svg></div>')

def shell(fname, title, desc, crumb, body):
    ON = ' class="on"'
    navlinks = ''.join(f'<a href="{h}"{ON if h==fname else ""}>{t}</a>' for h, t in NAV_ITEMS)
    return f'''<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="{FAVICON}">
<link rel="canonical" href="{fname}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&family=Caveat:wght@600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap">
  <div class="tb-l"><span>Registered NDIS Provider · <em>10+ years of experience</em> · VIC · NSW · QLD</span></div>
  <div class="tb-r">
    <a class="hide-s" href="mailto:info@rehoboth.com.au">{icon(IC['mail'], '#dff066')} info@rehoboth.com.au</a>
    <a href="tel:1300853095">{icon(IC['phone'], '#dff066')} 1300 853 095</a>
  </div>
</div></div>
<header class="nav" id="nav"><div class="wrap">
  <a class="logo" href="index.html"><img src="{LOGO}" alt="Rehoboth"></a>
  <nav class="primary" aria-label="Main">{navlinks}</nav>
  <div class="nav-cta"><a class="btn btn-teal" href="contact.html">Start your journey</a></div>
  <button class="burger" id="burger" aria-label="Menu" aria-expanded="false" aria-controls="mmenu">&#9776;</button>
</div>
<nav class="mobile-menu" id="mmenu" aria-label="Mobile">
  <a href="accommodation.html">SIL homes &amp; vacancies</a><a href="disability-services.html">Our services</a>
  <a href="disability-ndis-how-it-works.html">Understanding the NDIS</a><a href="about.html">About us</a>
  <a href="work-with-us.html">Careers</a><a href="resource-hub.html">Resources</a><a href="contact.html">Contact us</a>
  <a class="mcall" href="tel:1300853095">Call 1300 853 095</a>
</nav></header>
<main id="main">
{body}
</main>
{curve('#faf8f2', '#092b30', 1)}
<footer>
  <div class="f-main">
    <div>
      <a class="logo" href="index.html"><img src="{LOGO}" alt="Rehoboth"></a>
      <ul class="f-contact">
        <li>{icon(IC['phone'], '#a9c81e')} <a href="tel:1300853095">1300 853 095</a></li>
        <li>{icon(IC['mail'], '#a9c81e')} <a href="mailto:info@rehoboth.com.au">info@rehoboth.com.au</a></li>
        <li>{icon(IC['pin'], '#a9c81e')} <span>Head office: 78 William St,<br>Werrington NSW 2747</span></li>
      </ul>
      <div class="f-badge"><img src="{NDIS_BADGE}" alt=""><span>Registered NDIS Provider<br>Supporting VIC, NSW &amp; QLD</span></div>
    </div>
    <div><h3 class="fh">Supports</h3><ul>
      <li><a href="accommodation.html">SIL &amp; accommodation</a></li><li><a href="in-home.html">In-home support</a></li>
      <li><a href="24-hour-care.html">Complex &amp; 24/7 care</a></li><li><a href="disability-nursing.html">Community nursing</a></li>
      <li><a href="mental-health.html">Psychosocial support</a></li><li><a href="disability-services.html">All services</a></li>
    </ul></div>
    <div><h3 class="fh">NDIS</h3><ul>
      <li><a href="disability-ndis-how-it-works.html">How the NDIS works</a></li><li><a href="ndis-disability-how-to-apply.html">How to apply</a></li>
      <li><a href="funding-options.html">Funding options</a></li><li><a href="ndis-pricelist.html">Pricing</a></li>
      <li><a href="refer-to-us.html">Make a referral</a></li>
    </ul></div>
    <div><h3 class="fh">Company</h3><ul>
      <li><a href="about.html">About us</a></li><li><a href="work-with-us.html">Careers</a></li>
      <li><a href="work-with-us.html#oncall">Join our on-call team</a></li><li><a href="resource-hub.html">Resources &amp; FAQs</a></li>
      <li><a href="blog.html">News &amp; stories</a></li><li><a href="contact.html">Contact us</a></li>
    </ul></div>
  </div>
  <div class="ack">{FLAGS}<p>Rehoboth acknowledges the Traditional Custodians of the lands on which we live and work across Australia, and pays its respects to Elders past and present. We celebrate the diversity of all people, and welcome every participant, family member and team member regardless of culture, faith, sexuality, gender identity or disability.</p></div>
  <div class="f-bottom">
    <span>&copy; 2026 Rehoboth Comprehensive Care Services &middot; Community Regain Pty Ltd &middot; ABN 12 657 939 896</span>
    <span><a href="privacy-policy.html">Privacy policy</a> &nbsp;&middot;&nbsp; <a href="resource-hub.html">Feedback &amp; complaints</a></span>
  </div>
</footer>
<script>
(function() {{
  document.documentElement.classList.add('js');
  var nav = document.getElementById('nav');
  addEventListener('scroll', function() {{ nav.classList.toggle('scrolled', scrollY > 8); }}, {{passive:true}});
  var b = document.getElementById('burger'), m = document.getElementById('mmenu');
  b.addEventListener('click', function() {{ var o = m.classList.toggle('open'); b.setAttribute('aria-expanded', o); }});
  addEventListener('keydown', function(e) {{ if (e.key === 'Escape' && m.classList.contains('open')) {{ m.classList.remove('open'); b.setAttribute('aria-expanded','false'); b.focus(); }} }});
  var io = new IntersectionObserver(function(es) {{ es.forEach(function(e) {{ if (e.isIntersecting) {{ e.target.classList.add('in'); io.unobserve(e.target); }} }}); }}, {{threshold:.12}});
  document.querySelectorAll('.reveal').forEach(function(el) {{ io.observe(el); }});
}})();
</script>
</body>
</html>'''

# ───────── content port helpers ─────────
def map_desc(d):
    d = d.replace('class="btn secondary"', 'class="btn btn-lime"')
    d = d.replace('class="btn dark cdb-icon sw-left"', 'class="btn btn-teal"')
    d = d.replace('class="btn light cdb-icon sw-left"', 'class="btn btn-ghost"')
    d = d.replace('class="btn dark"', 'class="btn btn-teal"')
    d = d.replace('class="btn light"', 'class="btn btn-ghost"')
    d = d.replace('class="btn h-dark cdb-icon sw-left"', 'class="btn btn-ghost"')
    d = re.sub(r'<i class="ic-[^"]*">\s*</i>', '', d)
    d = re.sub(r'<div class="btn-row[^"]*">', '<div class="btns">', d)
    return d.strip()

import subprocess
def parse_page(path):
    fname = os.path.basename(path)
    h = subprocess.run(['git','-C','/Users/brookw/demorccs','show',f'HEAD:{fname}'],
                       capture_output=True).stdout.decode('utf-8','surrogateescape')
    title = re.search(r'<title>(.*?)</title>', h, re.DOTALL).group(1).strip()
    md = re.search(r'<meta name="description"[^>]*content="([^"]*)"', h)
    desc = md.group(1) if md else ''
    m1 = re.search(r'<main[^>]*>', h); m2 = h.rfind('</main>')
    inner = h[m1.end():m2]
    crumb = re.search(r'<nav class="breadcrumbs">.*?<span>(.*?)</span>', inner, re.DOTALL)
    crumb = re.sub(r'\s+', ' ', crumb.group(1)).strip() if crumb else ''
    h1 = re.search(r'<h1 class="title">(.*?)</h1>', inner, re.DOTALL)
    h1 = re.sub(r'\s+', ' ', h1.group(1)).strip() if h1 else crumb
    lede = re.search(r'</div>\s*<p>(.*?)</p>\s*<div class="btn-row hero_animation__cta"', inner, re.DOTALL)
    lede = re.sub(r'\s+', ' ', lede.group(1)).strip() if lede else ''
    hero_btns = re.search(r'<div class="btn-row hero_animation__cta">(.*?)</div>', inner, re.DOTALL)
    hero_btns = map_desc(hero_btns.group(1)) if hero_btns else ''
    secs = []
    for m in re.finditer(r'<section([^>]*class="section cdb-intro_text([^"]*)"[^>]*)>.*?(?:<h2 class="title h2">(.*?)</h2>|<div class="title h2">(.*?)</div>).*?<div class="section-heading__description">(.*?)</div>\s*</div></div></div></section>', inner, re.DOTALL):
        attrs, cls, h2a, h2b, d = m.groups()
        sid = re.search(r'id="([^"]+)"', attrs)
        secs.append({'id': sid.group(1) if sid else None,
                     'h2': re.sub(r'\s+', ' ', (h2a or h2b or '')).strip(),
                     'desc': map_desc(d), 'is_cta': 'intro-text-cta' in cls})
    return {'title': title, 'desc': desc, 'crumb': crumb, 'h1': h1, 'lede': lede,
            'hero_btns': hero_btns, 'secs': secs}

def render(fname, p):
    body = []
    body.append(f'''<section class="phero">
  <span class="deco deco-squig">{SQUIG}</span>
  <span class="deco deco-spark">{SPARK}</span>
  <div class="wrap">
    <div class="crumb"><a href="index.html">Home</a> <span>/</span> <span>{p['crumb']}</span></div>
    <h1>{p['h1']}</h1>
    <p class="lede">{p['lede']}</p>
    <div class="btns">{p['hero_btns']}</div>
  </div>
</section>''')
    content = [x for x in p['secs'] if not x['is_cta']]
    cta = next((x for x in p['secs'] if x['is_cta']), None)
    for i, sec in enumerate(content):
        alt = ' alt' if i % 2 == 1 else ''
        sid = f' id="{sec["id"]}"' if sec['id'] else ''
        body.append(f'''<section class="sect{alt}"{sid}><div class="wrap">
  <div class="reveal"><span class="eyebrow">{p['crumb']}</span><h2>{sec['h2']}</h2>
  <div class="prose">{sec['desc']}</div></div>
</div></section>''')
    cta_h = cta['h2'] if cta else 'Ready when you are.'
    cta_btns = cta['desc'] if cta else ''
    btns = re.findall(r'<a [^>]*href="([^"]+)"[^>]*>.*?<span class="link-text">(.*?)</span>', cta_btns, re.DOTALL)
    acts = ''.join(
        (f'<a class="btn btn-white" href="{h}">{icon(IC["phone"], "currentColor")} {re.sub(chr(10), " ", t).strip()}</a>' if h.startswith('tel:')
         else f'<a class="btn btn-teal" href="{h}">{re.sub(chr(10), " ", t).strip()}</a>')
        for h, t in btns) or f'<a class="btn btn-white" href="tel:1300853095">{icon(IC["phone"], "currentColor")} 1300 853 095</a><a class="btn btn-teal" href="contact.html">Send an enquiry</a>'
    body.append(f'''<div class="ctabox-wrap"><div class="wrap">
  <div class="ctabox reveal"><div><h2>{cta_h}</h2></div><div class="acts">{acts}</div></div>
</div></div>''')
    return shell(fname, p['title'], p['desc'].replace('"','&quot;'), p['crumb'], '\n'.join(body))

# ───────── page-specific content fixes ─────────
def fix_specialists(p):
    p['h1'] = 'Specialist &amp; complex supports'
    p['lede'] = 'Tailored, specialised support for people with higher or changing needs, delivered by a team trained in complex care.'
    p['title'] = 'Specialist &amp; complex supports | Rehoboth'
    p['desc'] = 'Specialist and complex disability supports from Rehoboth: high-intensity care, domestic and daily living support, and close coordination with your clinical team. Call 1300 853 095.'
    p['secs'] = [
     {'id': None, 'h2': 'Complex and high-intensity support', 'is_cta': False, 'desc':
      '<p>Some people need more than standard supports. Our support workers are trained in high-intensity daily personal activities and complex care, and they are backed by registered nurses and our 24/7 on-call team.</p>'
      '<ul><li>Support for participants with high physical support needs</li>'
      '<li>Staff trained in manual handling and high-intensity supports</li>'
      '<li>Around-the-clock rosters where your plan funds them; see our <a href="24-hour-care.html">24/7 and complex care</a> page</li>'
      '<li>Close work with your treating health professionals</li></ul>'},
     {'id': None, 'h2': 'Domestic and daily living support', 'is_cta': False, 'desc':
      '<p>Practical help that keeps your home running and your week on track: cleaning, laundry, meal preparation, shopping and errands, alongside <a href="personal-care.html">personal care</a> and <a href="in-home.html">in-home support</a>.</p>'},
     {'id': None, 'h2': 'Working with your clinical team', 'is_cta': False, 'desc':
      '<p>We do not replace your treating professionals; we work alongside them. Our <a href="disability-nursing.html">community nurses</a> liaise with your doctors and specialists, implement clinical care plans at home, and keep your family and team informed.</p>'},
    ]
    return p

def fix_workwithus(p):
    for sec in p['secs']:
        sec['desc'] = re.sub(r'<h3>Therapy and allied health</h3>\s*<p>.*?</p>', '', sec['desc'], flags=re.DOTALL)
    return p

DUO_GRID_PAGE = None  # disability-services special-cased below

def build_services_grid(p):
    SERVICES = [
     ('accommodation.html', 'Supported Independent Living', 'Safe, welcoming SIL homes with 24/7 trained support, helping you live independently, your way.'),
     ('in-home.html', 'In-home support', 'Help with daily routines, personal care, meals, medication and household tasks, at home.'),
     ('carers-support.html', 'Short Term Accommodation (STA)', 'Short stays and respite that give you new experiences, and give families and carers a break.'),
     ('social-and-community.html', 'Community participation', 'Get out, get involved and stay connected to the people and activities you love.'),
     ('disability-nursing.html', 'Community nursing', 'Registered nurses delivering clinical care at home, from wound care to complex health needs.'),
     ('24-hour-care.html', 'Complex &amp; high-intensity care', 'Around-the-clock support from staff trained in high-intensity daily personal activities.'),
     ('mental-health.html', 'Psychosocial support', 'Recovery-oriented, person-centred support for psychosocial disability, at your pace.'),
     ('transport-services.html', 'Travel &amp; transport', 'Our own fleet gets you safely to appointments, work, study and community activities.'),
     ('care-management-services.html', 'Support coordination', 'We help you understand your plan, connect with providers and get the most from your funding.'),
    ]
    ARROW = icon(IC['arrow'], 'currentColor')
    cards = ''.join(
     f'<a class="svc reveal" style="--d:{i*0.05:.2f}s" href="{h}"><h3>{t}</h3><p>{d}</p>'
     f'<span class="more">Learn more {ARROW}</span></a>' for i, (h, t, d) in enumerate(SERVICES))
    intro = next((s for s in p['secs'] if not s['is_cta']), None)
    body = f'''<section class="phero">
  <span class="deco deco-squig">{SQUIG}</span><span class="deco deco-spark">{SPARK}</span>
  <div class="wrap">
    <div class="crumb"><a href="index.html">Home</a> <span>/</span> <span>Our services</span></div>
    <h1>{p['h1']}</h1><p class="lede">{p['lede']}</p>
    <div class="btns">{p['hero_btns']}</div>
  </div>
</section>
<section class="sect alt"><div class="wrap">
  <div class="reveal"><span class="eyebrow">Our services</span><h2>{intro['h2'] if intro else 'You are always at the centre of what we do'}</h2>
  <div class="prose">{intro['desc'] if intro else ''}</div></div>
  <div class="svc-grid">{cards}</div>
</div></section>
<div class="ctabox-wrap"><div class="wrap">
  <div class="ctabox reveal"><div><h2>Not sure where to start?</h2></div>
  <div class="acts"><a class="btn btn-white" href="tel:1300853095">{icon(IC['phone'], 'currentColor')} 1300 853 095</a><a class="btn btn-teal" href="contact.html">Send an enquiry</a></div></div>
</div></div>'''
    return shell('disability-services.html', p['title'], p['desc'].replace('"','&quot;'), 'Our services', body)

# ───────── run ─────────
SKIP = {'index.html'}
done = 0
for path in sorted(glob.glob('/Users/brookw/demorccs/*.html')):
    fname = os.path.basename(path)
    if fname in SKIP or fname.startswith('_'): continue
    p = parse_page(path)
    if not p['secs']:
        print(f'  !! no sections parsed: {fname} — left untouched'); continue
    if fname == 'specialists-services.html': p = fix_specialists(p)
    if fname == 'work-with-us.html': p = fix_workwithus(p)
    out = build_services_grid(p) if fname == 'disability-services.html' else render(fname, p)
    open(path, 'w', encoding='utf-8').write(out)
    done += 1
print(f'rebuilt {done} subpages in the new design')
