#!/usr/bin/env python3
"""Generate the new flagship homepage (self-contained index.html).
Design: modern, warm, professional NDIS provider. SIL-prominent.
Photos hot-linked from avivo.org.au as approved placeholders."""

LOGO = open('/tmp/rehoboth_logo.txt').read().strip()
FAVICON = open('/tmp/rehoboth_favicon.txt').read().strip()
NDIS_BADGE = open('/tmp/indis_badge.txt').read().strip()

IMG = {
 'hero':      'https://www.avivo.org.au/wp-content/uploads/2025/11/EDITED-RiftPhotography-AvivoDay1and2-144_min.webp',
 'sil_main':  'https://www.avivo.org.au/wp-content/uploads/2025/10/avivo-images-disability-paul-kenny-at-home-perth5.jpg',
 'sil_small': 'https://www.avivo.org.au/wp-content/uploads/2025/11/home-about-avivo_min.webp',
 'who':       'https://www.avivo.org.au/wp-content/uploads/2025/10/avivo-images-disability-becky-and-horses.jpg',
 'mission':   'https://www.avivo.org.au/wp-content/uploads/2026/02/RiftPhotography-AvivoDay3-2-scaled.jpg',
 'nurse':     'https://www.avivo.org.au/wp-content/uploads/2025/09/specialist-services-nursing_min.webp',
 'workforce': 'https://www.avivo.org.au/wp-content/uploads/2025/11/avivo-images-disability-jess-jas-at-the-office-perth2.jpg',
 'p1':        'https://www.avivo.org.au/wp-content/uploads/2025/11/iStock-1367774041-scaled.jpg',
 'p2':        'https://www.avivo.org.au/wp-content/uploads/2025/11/iStock-2190214515-scaled.jpg',
 'p3':        'https://www.avivo.org.au/wp-content/uploads/2025/10/avivo_2019-07_090.jpg',
}

def icon(inner, stroke='#0e3a40'):
    return ('<svg aria-hidden="true" focusable="false" viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.9" '
            'stroke-linecap="round" stroke-linejoin="round">' + inner + '</svg>')

IC = {
 'home':  '<path d="M3 9.5 12 3l9 6.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
 'person':'<circle cx="12" cy="8" r="4"/><path d="M5.5 21a6.5 6.5 0 0 1 13 0"/>',
 'users': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
 'heart': '<path d="M19 14c1.5-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
 'car':   '<path d="M5 13 6.5 8.5A2 2 0 0 1 8.4 7h7.2a2 2 0 0 1 1.9 1.5L19 13"/><path d="M5 13h14v4a1 1 0 0 1-1 1h-1a1 1 0 0 1-1-1v-1H8v1a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1z"/><circle cx="7.5" cy="15.5" r=".6"/><circle cx="16.5" cy="15.5" r=".6"/>',
 'compass':'<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88"/>',
 'moon':  '<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>',
 'pulse': '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
 'shield':'<path d="M12 22s8-3.5 8-10V5l-8-3-8 3v7c0 6.5 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
 'phone': '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
 'mail':  '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/>',
 'pin':   '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
 'clock': '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
 'sun':   '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
 'chat':  '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
 'check': '<path d="M20 6 9 17l-5-5"/>',
 'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
 'star':  '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
 'brief': '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/>',
 'building':'<rect x="5" y="3" width="14" height="18" rx="1.5"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M10 21v-4h4v4"/>',
}

def chk(t):
    return f'<li><span class="tick">{icon(IC["check"], "#7a9a0e")}</span>{t}</li>'

SERVICES = [
 ('accommodation.html', 'home', 'Supported Independent Living', 'Safe, welcoming SIL homes with 24/7 trained support, helping you live independently, your way.'),
 ('in-home.html', 'sun', 'In-home support', 'Help with daily routines, personal care, meals, medication and household tasks, at home.'),
 ('carers-support.html', 'moon', 'Short Term Accommodation (STA)', 'Short stays and respite that give you new experiences, and give families and carers a break.'),
 ('social-and-community.html', 'users', 'Community participation', 'Get out, get involved and stay connected to the people and activities you love.'),
 ('disability-nursing.html', 'heart', 'Community nursing', 'Registered nurses delivering clinical care at home, from wound care to complex health needs.'),
 ('24-hour-care.html', 'pulse', 'Complex &amp; high-intensity care', 'Around-the-clock support from staff trained in high-intensity daily personal activities.'),
 ('mental-health.html', 'chat', 'Psychosocial support', 'Recovery-oriented, person-centred support for psychosocial disability, at your pace.'),
 ('transport-services.html', 'car', 'Travel &amp; transport', 'Our own fleet gets you safely to appointments, work, study and community activities.'),
 ('care-management-services.html', 'compass', 'Support coordination', 'We help you understand your plan, connect with providers and get the most from your funding.'),
]

svc_cards = "".join(
 f'<a class="svc reveal" style="--d:{i*0.05:.2f}s" href="{href}">'
 f'<span class="svc-ic">{icon(IC[ic])}</span><h3>{t}</h3><p>{d}</p>'
 f'<span class="more">Learn more {icon(IC["arrow"], "currentColor")}</span></a>'
 for i, (href, ic, t, d) in enumerate(SERVICES))

HOMES = [
 (IMG['p1'], 'Werrington', 'Wheelchair accessible · Private garden · Quiet neighbourhood'),
 (IMG['p2'], 'Blacktown', '4 bedrooms · Secure garage · Near Blacktown Hospital'),
 (IMG['p3'], 'Blackheath', 'Fully accessible · Modern double-storey · Blue Mountains'),
]
home_cards = "".join(
 f'<a class="hcard reveal" style="--d:{i*0.08:.2f}s" href="accommodation.html#vacancies">'
 f'<div class="himg"><img src="{src}" alt="" loading="lazy">'
 f'<span class="badge-vac">Enquire about vacancies</span></div>'
 f'<div class="hbody"><h3>{name} Home</h3><p>{feat}</p>'
 f'<span class="more">View this home {icon(IC["arrow"], "currentColor")}</span></div></a>'
 for i, (src, name, feat) in enumerate(HOMES))

WHO = ['Complex care needs', 'Psychosocial disability', 'Physical disability', 'Behaviour support needs',
       'Autism', 'Intellectual disability', 'Acquired brain injury', 'Spinal cord injury',
       'Younger onset dementia', 'Degenerative conditions', 'Sensory disability', 'Co-occurring mental health needs']
who_pills = "".join(f'<span class="pill reveal" style="--d:{i*0.03:.2f}s">{w}</span>' for i, w in enumerate(WHO))

WHY = [
 ('shield', 'Registered &amp; audited', 'A registered NDIS provider, independently audited against the NDIS Practice Standards.'),
 ('star', '10+ years of experience', 'More than a decade walking alongside participants and families across VIC, NSW and QLD.'),
 ('heart', 'Clinical expertise', 'Registered nurses lead our clinical care, with access to medical practitioners for complex needs.'),
 ('users', 'Complex-care trained team', 'Support workers trained in high-intensity supports, positive behaviour support and manual handling.'),
 ('car', 'Our own fleet', 'A fleet of our own vehicles, so transport never holds you back.'),
 ('clock', '24/7 on-call response', 'Real people answer around the clock, because support needs don’t keep office hours.'),
]
why_cards = "".join(
 f'<div class="why reveal" style="--d:{i*0.06:.2f}s"><span class="why-ic">{icon(IC[ic], "#dff066")}</span>'
 f'<h3>{t}</h3><p>{d}</p></div>' for i, (ic, t, d) in enumerate(WHY))

STEPS = [
 ('Say hello', 'Call 1300 853 095 or send an enquiry. A real person listens to your story; no obligation.'),
 ('Visit &amp; plan', 'We visit you, understand your goals and NDIS plan, and design supports around your life.'),
 ('Meet your team', 'We carefully match support workers to your needs, personality and culture.'),
 ('Grow together', 'We review regularly, adjust as life changes, and celebrate every win with you.'),
]
steps_html = "".join(
 f'<div class="step reveal" style="--d:{i*0.08:.2f}s"><span class="stepnum">{i+1}</span>'
 f'<h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(STEPS))

page = f'''<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rehoboth | Registered NDIS Provider | SIL, Complex Care &amp; Disability Support in VIC, NSW &amp; QLD</title>
<meta name="description" content="Rehoboth is a registered NDIS provider with over 10 years of experience. Supported Independent Living homes, complex care, community nursing and disability support across Victoria, New South Wales and Queensland. Call 1300 853 095.">
<link rel="icon" href="{FAVICON}">
<link rel="canonical" href="index.html">
<meta property="og:title" content="Rehoboth | Registered NDIS Provider | VIC, NSW &amp; QLD">
<meta property="og:description" content="Supported Independent Living, complex care and disability support from a registered NDIS provider with 10+ years of experience.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&family=Caveat:wght@600;700&display=swap" rel="stylesheet">
<style>
:root {{
  --teal:#0e3a40; --teal-deep:#092b30; --teal-soft:#11464d;
  --lime:#a9c81e; --lime-bright:#c4d600; --lime-pale:#eef3da; --lime-glow:#dff066; --olive:#5d7610;
  --cream:#faf8f2; --sand:#f3efe4; --ink:#15333a; --mut:#5c6f6d; --white:#fff;
  --r-lg:22px; --r-md:16px; --shadow:0 20px 50px rgba(14,58,64,.12);
  --max:1180px;
}}
* {{ margin:0; padding:0; box-sizing:border-box; }}
.skip-link {{ position:absolute; left:-9999px; top:0; background:var(--teal); color:#fff; padding:12px 22px; z-index:2000; border-radius:0 0 10px 0; font-weight:700; }}
.skip-link:focus {{ left:0; }}
html {{ scroll-behavior:smooth; }}
body {{ font-family:'Montserrat',system-ui,sans-serif; color:var(--ink); background:var(--cream); line-height:1.65; font-size:16.5px; }}
img {{ max-width:100%; display:block; }}
a {{ color:inherit; text-decoration:none; }}
ul {{ list-style:none; }}
.wrap {{ max-width:var(--max); margin:0 auto; padding:0 24px; }}
h1,h2,h3 {{ line-height:1.18; color:var(--teal); font-weight:800; letter-spacing:-.01em; }}
.eyebrow {{ display:inline-flex; align-items:center; gap:10px; font-size:13px; font-weight:700; letter-spacing:.16em; text-transform:uppercase; color:var(--olive); margin-bottom:14px; }}
.eyebrow::before {{ content:""; width:34px; height:3px; border-radius:2px; background:var(--lime-bright); }}
.hand {{ font-family:'Caveat',cursive; font-size:30px; color:var(--olive); font-weight:700; display:block; margin-bottom:6px; }}
.lead {{ color:var(--mut); font-size:18px; max-width:640px; }}
section {{ padding:96px 0; }}
.center {{ text-align:center; }}
.center .lead {{ margin:0 auto; }}

/* buttons */
.btn {{ display:inline-flex; align-items:center; gap:10px; font-weight:700; font-size:16px; border-radius:999px; padding:16px 30px; transition:.25s; cursor:pointer; border:2px solid transparent; }}
.btn svg {{ width:19px; height:19px; transition:transform .25s; }}
.btn:hover svg {{ transform:translateX(4px); }}
.btn-lime {{ background:var(--lime-bright); color:var(--teal); box-shadow:0 10px 26px rgba(169,200,30,.4); }}
.btn-lime:hover {{ background:var(--lime); transform:translateY(-2px); }}
.btn-ghost {{ border-color:rgba(14,58,64,.25); color:var(--teal); }}
.btn-ghost:hover {{ border-color:var(--teal); background:var(--teal); color:#fff; }}
.btn-white {{ background:#fff; color:var(--teal); }}
.btn-white:hover {{ transform:translateY(-2px); }}
.btn-teal {{ background:var(--teal); color:#fff; }}
.btn-teal:hover {{ background:var(--teal-soft); transform:translateY(-2px); }}

/* top bar */
.topbar {{ background:var(--teal-deep); color:#cfe0d8; font-size:13.5px; font-weight:600; }}
.topbar .wrap {{ display:flex; justify-content:space-between; align-items:center; min-height:42px; gap:14px; }}
.topbar a {{ color:#fff; display:inline-flex; align-items:center; gap:7px; white-space:nowrap; }}
.topbar svg {{ width:15px; height:15px; }}
.topbar .tb-l span em {{ color:var(--lime-glow); font-style:normal; }}
.topbar .tb-r {{ display:flex; gap:22px; }}
@media (max-width:760px) {{ .topbar .tb-r .hide-s {{ display:none; }} .topbar .tb-l {{ font-size:12px; }} }}

/* nav */
.nav {{ position:sticky; top:0; z-index:900; background:rgba(250,248,242,.92); backdrop-filter:blur(14px); border-bottom:1px solid rgba(14,58,64,.07); transition:box-shadow .3s; }}
.nav.scrolled {{ box-shadow:0 6px 30px rgba(14,58,64,.1); }}
.nav .wrap {{ display:flex; align-items:center; gap:34px; min-height:84px; }}
.nav .logo img {{ height:40px; width:auto; }}
.nav nav.primary {{ display:flex; gap:28px; margin-left:auto; }}
.nav nav.primary a {{ font-weight:600; font-size:15.5px; color:var(--ink); position:relative; padding:6px 0; }}
.nav nav.primary a::after {{ content:""; position:absolute; left:0; bottom:0; width:0; height:2.5px; border-radius:2px; background:var(--lime-bright); transition:width .25s; }}
.nav nav.primary a:hover::after {{ width:100%; }}
.nav .nav-cta {{ display:flex; gap:12px; align-items:center; }}
.nav .nav-cta .btn {{ padding:12px 22px; font-size:15px; }}
.burger {{ display:none; margin-left:auto; background:var(--teal); color:#fff; border:0; border-radius:10px; width:46px; height:46px; font-size:22px; cursor:pointer; }}
.nav nav.mobile-menu {{ display:none; background:#fff; border-bottom:1px solid #eee; }}
.nav nav.mobile-menu.open {{ display:block; }}
.mobile-menu a {{ display:block; padding:15px 26px; font-weight:600; border-top:1px solid #f1efe8; }}
.mobile-menu .mcall {{ background:var(--lime-bright); text-align:center; font-weight:800; }}
@media (max-width:1020px) {{ .nav nav.primary, .nav .nav-cta {{ display:none; }} .burger {{ display:block; }} }}

/* hero */
.hero {{ position:relative; overflow:hidden; padding:84px 0 110px; }}
.hero::before {{ content:""; position:absolute; right:-340px; top:-280px; width:880px; height:880px; border-radius:50%;
  background:radial-gradient(circle at 35% 35%, rgba(196,214,0,.20), rgba(196,214,0,0) 60%); animation:floaty 9s ease-in-out infinite; }}
.hero .wrap {{ display:grid; grid-template-columns:1.05fr .95fr; gap:60px; align-items:center; position:relative; }}
.hero h1 {{ font-size:clamp(38px,4.6vw,58px); margin:6px 0 22px; }}
.hero h1 em {{ font-style:normal; color:var(--olive); position:relative; white-space:nowrap; }}
.hero h1 em svg {{ position:absolute; left:0; bottom:-7px; width:100%; height:12px; }}
.hero .lead {{ margin-bottom:34px; }}
.hero-cta {{ display:flex; gap:16px; flex-wrap:wrap; margin-bottom:38px; }}
.hero-trust {{ display:flex; gap:26px; flex-wrap:wrap; align-items:center; color:var(--mut); font-size:14px; font-weight:600; }}
.hero-trust span {{ display:inline-flex; gap:8px; align-items:center; }}
.hero-trust svg {{ width:17px; height:17px; }}
.hero-visual {{ position:relative; }}
.hero-blob {{ position:relative; width:100%; aspect-ratio:.94; }}
.hero-blob .ph {{ position:absolute; inset:0; clip-path:url(#blobclip); overflow:hidden; }}
.hero-blob .ph img {{ width:100%; height:100%; object-fit:cover; animation:kenburns 18s ease-in-out infinite alternate; }}
.hero-blob .accent {{ position:absolute; width:120px; height:120px; border-radius:46% 54% 60% 40%/50% 45% 55% 50%; background:var(--lime-bright); right:-16px; bottom:34px; z-index:-1; animation:floaty 7s ease-in-out infinite; }}
.hero-blob .accent2 {{ position:absolute; width:74px; height:74px; border-radius:50% 50% 44% 56%/48% 56% 44% 52%; background:var(--teal); left:-10px; top:48px; z-index:-1; animation:floaty 8s 1s ease-in-out infinite; }}
.float-card {{ position:absolute; background:#fff; border-radius:16px; box-shadow:var(--shadow); padding:14px 20px; display:flex; gap:12px; align-items:center; font-size:14px; font-weight:700; color:var(--teal); animation:floaty 6s ease-in-out infinite; }}
.float-card svg {{ width:22px; height:22px; flex:none; }}
.float-card small {{ display:block; font-weight:600; color:var(--mut); font-size:12px; }}
.fc1 {{ left:-26px; bottom:14%; }}
.fc2 {{ right:-8px; top:8%; animation-delay:1.4s; }}
@keyframes floaty {{ 0%,100% {{ transform:translateY(0); }} 50% {{ transform:translateY(-13px); }} }}
@keyframes kenburns {{ from {{ transform:scale(1); }} to {{ transform:scale(1.09); }} }}
@media (max-width:920px) {{ .hero .wrap {{ grid-template-columns:1fr; }} .hero-visual {{ max-width:520px; margin:0 auto; }} }}

/* stats band */
.stats {{ background:var(--teal); color:#fff; padding:54px 0; position:relative; overflow:hidden; }}
.stats::after {{ content:""; position:absolute; left:-120px; bottom:-180px; width:420px; height:420px; border-radius:50%; background:rgba(196,214,0,.10); }}
.stats .wrap {{ display:grid; grid-template-columns:repeat(4,1fr); gap:30px; text-align:center; position:relative; }}
.stat b {{ font-size:clamp(34px,3.4vw,46px); font-weight:800; color:var(--lime-glow); display:block; line-height:1; }}
.stat span {{ font-size:14.5px; font-weight:600; color:#cfe0d8; display:block; margin-top:9px; }}
@media (max-width:760px) {{ .stats .wrap {{ grid-template-columns:repeat(2,1fr); }} }}

/* SIL flagship */
.sil {{ background:var(--cream); }}
.sil-top {{ display:grid; grid-template-columns:1.02fr .98fr; gap:64px; align-items:center; margin-bottom:74px; }}
.sil-top h2 {{ font-size:clamp(30px,3.4vw,44px); margin-bottom:20px; }}
.sil-list {{ margin:26px 0 32px; display:grid; gap:13px; }}
.sil-list li {{ display:flex; gap:12px; align-items:flex-start; font-weight:600; color:var(--ink); }}
.sil-list .tick {{ flex:none; width:24px; height:24px; border-radius:50%; background:var(--lime-pale); display:flex; align-items:center; justify-content:center; margin-top:2px; }}
.sil-list .tick svg {{ width:13px; height:13px; }}
.sil-visual {{ position:relative; }}
.sil-visual .main {{ border-radius:var(--r-lg); overflow:hidden; box-shadow:var(--shadow); aspect-ratio:1.08; }}
.sil-visual .main img {{ width:100%; height:100%; object-fit:cover; transition:transform .6s; }}
.sil-visual:hover .main img {{ transform:scale(1.05); }}
.sil-visual .mini {{ position:absolute; left:-40px; bottom:-40px; width:46%; border-radius:18px; overflow:hidden; border:6px solid var(--cream); box-shadow:var(--shadow); aspect-ratio:1.25; }}
.sil-visual .mini img {{ width:100%; height:100%; object-fit:cover; }}
.sil-visual .chip {{ position:absolute; top:18px; right:18px; background:var(--lime-bright); color:var(--teal); font-weight:800; font-size:13.5px; border-radius:999px; padding:9px 17px; box-shadow:0 8px 20px rgba(0,0,0,.18); }}
.hgrid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:26px; }}
.hcard {{ background:#fff; border-radius:var(--r-lg); overflow:hidden; box-shadow:0 8px 26px rgba(14,58,64,.08); transition:transform .25s, box-shadow .25s; display:flex; flex-direction:column; }}
.hcard:hover {{ transform:translateY(-7px); box-shadow:var(--shadow); }}
.himg {{ position:relative; aspect-ratio:1.5; overflow:hidden; }}
.himg img {{ width:100%; height:100%; object-fit:cover; transition:transform .5s; }}
.hcard:hover .himg img {{ transform:scale(1.07); }}
.badge-vac {{ position:absolute; top:14px; left:14px; background:var(--lime-bright); color:var(--teal); font-size:12.5px; font-weight:800; padding:7px 13px; border-radius:999px; }}
.hbody {{ padding:24px 26px 26px; display:flex; flex-direction:column; gap:8px; flex:1; }}
.hbody h3 {{ font-size:20px; }}
.hbody p {{ color:var(--mut); font-size:14.5px; }}
.more {{ display:inline-flex; align-items:center; gap:8px; font-weight:700; color:var(--teal); font-size:15px; margin-top:auto; padding-top:8px; }}
.more svg {{ width:17px; height:17px; transition:transform .25s; }}
.hcard:hover .more svg, .svc:hover .more svg {{ transform:translateX(5px); }}
.hcard:hover .more, .svc:hover .more {{ color:var(--olive); }}
.sil-ctas {{ display:flex; gap:16px; flex-wrap:wrap; justify-content:center; margin-top:44px; }}
@media (max-width:920px) {{ .sil-top {{ grid-template-columns:1fr; }} .sil-visual {{ max-width:540px; margin:0 auto; }} .sil-visual .mini {{ left:-8px; }} .hgrid {{ grid-template-columns:1fr; max-width:480px; margin:0 auto; }} }}

/* services */
.services {{ background:var(--sand); border-radius:60px 60px 0 0; }}
.svc-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:24px; margin-top:54px; }}
.svc {{ background:#fff; border-radius:var(--r-md); padding:32px 30px; display:flex; flex-direction:column; gap:10px; border:1px solid rgba(14,58,64,.05); transition:transform .25s, box-shadow .25s; }}
.svc:hover {{ transform:translateY(-6px); box-shadow:var(--shadow); }}
.svc-ic {{ width:56px; height:56px; border-radius:15px; background:var(--lime-pale); display:flex; align-items:center; justify-content:center; margin-bottom:8px; }}
.svc-ic svg {{ width:28px; height:28px; }}
.svc h3 {{ font-size:19px; }}
.svc p {{ color:var(--mut); font-size:14.5px; flex:1; }}
@media (max-width:920px) {{ .svc-grid {{ grid-template-columns:repeat(2,1fr); }} }}
@media (max-width:620px) {{ .svc-grid {{ grid-template-columns:1fr; }} }}

/* who we support */
.who .wrap {{ display:grid; grid-template-columns:1fr .9fr; gap:64px; align-items:center; }}
.who-img {{ border-radius:var(--r-lg); overflow:hidden; box-shadow:var(--shadow); aspect-ratio:.92; position:relative; }}
.who-img img {{ width:100%; height:100%; object-fit:cover; }}
.who-img::after {{ content:""; position:absolute; inset:0; background:linear-gradient(to top, rgba(9,43,48,.35), transparent 45%); }}
.pills {{ display:flex; flex-wrap:wrap; gap:11px; margin-top:26px; }}
.pill {{ background:#fff; border:1.5px solid #e3e7d2; border-radius:999px; padding:10px 19px; font-weight:600; font-size:14.5px; color:var(--ink); transition:.25s; }}
.pill:hover {{ border-color:var(--lime); background:var(--lime-pale); }}
@media (max-width:920px) {{ .who .wrap {{ grid-template-columns:1fr; }} .who-img {{ max-width:520px; margin:0 auto; order:2; }} }}

/* why us */
.why-s {{ background:var(--teal); color:#fff; border-radius:60px; margin:0 18px; }}
.why-s .eyebrow {{ color:var(--lime-glow); }}
.why-s h2, .why-s h3 {{ color:#fff; }}
.why-s .lead {{ color:#b9cfc6; }}
.why-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:26px; margin-top:54px; }}
.why {{ background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.1); border-radius:var(--r-md); padding:32px 30px; transition:.25s; }}
.why:hover {{ background:rgba(255,255,255,.09); transform:translateY(-5px); }}
.why-ic {{ width:54px; height:54px; border-radius:14px; background:rgba(196,214,0,.15); display:flex; align-items:center; justify-content:center; margin-bottom:18px; }}
.why-ic svg {{ width:27px; height:27px; }}
.why h3 {{ font-size:18.5px; margin-bottom:9px; }}
.why p {{ color:#b9cfc6; font-size:14.5px; }}
@media (max-width:920px) {{ .why-grid {{ grid-template-columns:1fr; }} .why-s {{ margin:0; border-radius:0; }} }}

/* steps */
.steps-grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:26px; margin-top:58px; counter-reset:s; position:relative; }}
.step {{ background:#fff; border-radius:var(--r-md); padding:34px 28px; box-shadow:0 8px 26px rgba(14,58,64,.07); position:relative; }}
.stepnum {{ width:46px; height:46px; border-radius:50%; background:var(--lime-bright); color:var(--teal); font-weight:800; font-size:19px; display:flex; align-items:center; justify-content:center; margin-bottom:18px; }}
.step h3 {{ font-size:19px; margin-bottom:9px; }}
.step p {{ color:var(--mut); font-size:14.5px; }}
@media (max-width:920px) {{ .steps-grid {{ grid-template-columns:repeat(2,1fr); }} }}
@media (max-width:620px) {{ .steps-grid {{ grid-template-columns:1fr; }} }}

/* workforce */
.work {{ background:var(--sand); }}
.work-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:26px; margin-top:54px; }}
.wcard {{ border-radius:var(--r-lg); padding:44px 42px; position:relative; overflow:hidden; display:flex; flex-direction:column; gap:14px; min-height:330px; }}
.wcard h3 {{ font-size:25px; }}
.wcard p {{ font-size:15.5px; flex:1; }}
.wcard .btn {{ align-self:flex-start; }}
.wc1 {{ background:#fff; box-shadow:0 8px 26px rgba(14,58,64,.07); }}
.wc1 p {{ color:var(--mut); }}
.wc2 {{ background:var(--teal); color:#fff; }}
.wc2 h3 {{ color:#fff; }}
.wc2 p {{ color:#b9cfc6; }}
.wc-ic {{ width:56px; height:56px; border-radius:15px; display:flex; align-items:center; justify-content:center; }}
.wc1 .wc-ic {{ background:var(--lime-pale); }}
.wc2 .wc-ic {{ background:rgba(196,214,0,.16); }}
.wc-ic svg {{ width:28px; height:28px; }}
@media (max-width:880px) {{ .work-grid {{ grid-template-columns:1fr; }} }}

/* mission band */
.mission {{ position:relative; min-height:520px; display:flex; align-items:center; overflow:hidden; }}
.mission .bg {{ position:absolute; inset:0; }}
.mission .bg img {{ width:100%; height:100%; object-fit:cover; }}
.mission .bg::after {{ content:""; position:absolute; inset:0; background:linear-gradient(100deg, rgba(9,43,48,.88) 18%, rgba(9,43,48,.55) 55%, rgba(9,43,48,.25)); }}
.mission .wrap {{ position:relative; color:#fff; max-width:var(--max); width:100%; }}
.mission .hand {{ color:var(--lime-glow); }}
.mission h2 {{ color:#fff; font-size:clamp(28px,3.4vw,44px); max-width:660px; margin-bottom:18px; }}
.mission p {{ color:#d6e4dd; max-width:560px; font-size:17px; margin-bottom:32px; }}

/* cta */
.cta {{ padding:96px 0; }}
.cta-box {{ background:linear-gradient(115deg, var(--lime-bright), var(--lime)); border-radius:var(--r-lg); padding:64px 56px; display:grid; grid-template-columns:1.2fr .8fr; gap:40px; align-items:center; position:relative; overflow:hidden; }}
.cta-box::after {{ content:""; position:absolute; right:-90px; top:-90px; width:300px; height:300px; border-radius:50%; background:rgba(255,255,255,.22); }}
.cta-box h2 {{ font-size:clamp(26px,3vw,38px); }}
.cta-box p {{ color:#3c4d10; font-weight:600; margin-top:10px; }}
.cta-actions {{ display:flex; gap:14px; flex-wrap:wrap; justify-content:flex-end; position:relative; }}
@media (max-width:880px) {{ .cta-box {{ grid-template-columns:1fr; text-align:center; }} .cta-actions {{ justify-content:center; }} }}

/* footer */
footer {{ background:var(--teal-deep); color:#bdd2c9; font-size:14.5px; }}
.f-main {{ display:grid; grid-template-columns:1.3fr 1fr 1fr 1fr; gap:44px; padding:76px 0 50px; }}
.f-main .logo img {{ height:38px; width:auto; margin-bottom:18px; filter:brightness(1.15); }}
.f-main .fh {{ color:#fff; font-size:15.5px; font-weight:700; margin-bottom:18px; }}
.f-main li {{ margin-bottom:11px; }}
.f-main a:hover {{ color:var(--lime-glow); }}
.f-contact li {{ display:flex; gap:11px; align-items:flex-start; }}
.f-contact svg {{ width:17px; height:17px; flex:none; margin-top:3px; }}
.f-badge {{ display:flex; align-items:center; gap:14px; margin-top:22px; background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.1); padding:13px 17px; border-radius:13px; max-width:330px; }}
.f-badge img {{ width:52px; height:52px; }}
.f-badge span {{ font-size:13px; line-height:1.45; }}
.ack {{ border-top:1px solid rgba(255,255,255,.1); padding:38px 0; display:flex; gap:22px; align-items:flex-start; }}
.ack-flags {{ display:flex; gap:8px; flex:none; margin-top:4px; }}
.ack-flags svg {{ width:42px; height:27px; border-radius:4px; }}
.ack p {{ font-size:13.5px; line-height:1.7; max-width:880px; }}
.f-bottom {{ border-top:1px solid rgba(255,255,255,.1); padding:24px 0 30px; display:flex; justify-content:space-between; gap:14px; flex-wrap:wrap; font-size:13px; }}
.f-bottom a {{ text-decoration:underline; text-underline-offset:3px; }}
@media (max-width:920px) {{ .f-main {{ grid-template-columns:1fr 1fr; }} }}
@media (max-width:560px) {{ .f-main {{ grid-template-columns:1fr; }} .ack {{ flex-direction:column; }} }}

/* reveal animation */
.js .reveal {{ opacity:0; transform:translateY(28px); transition:opacity .7s ease var(--d,0s), transform .7s ease var(--d,0s); }}
.js .reveal.in {{ opacity:1; transform:none; }}
@media (prefers-reduced-motion:reduce) {{
  *, *::before, *::after {{ animation:none !important; transition:none !important; }}
  html {{ scroll-behavior:auto; }}
  .js .reveal {{ opacity:1; transform:none; }}
}}
</style>
</head>
<body>

<svg width="0" height="0" style="position:absolute"><defs>
<clipPath id="blobclip" clipPathUnits="objectBoundingBox">
<path d="M.512.012C.65.005.787.05.873.143c.084.09.115.222.112.353-.003.13-.04.258-.12.345C.785.93.664.974.54.99.41 1.006.266.99.17.906.075.823.03.69.013.557-.004.42.01.276.09.18.17.083.375.02.512.012Z"/>
</clipPath></defs></svg>

<a class="skip-link" href="#main">Skip to content</a>
<div class="topbar">
  <div class="wrap">
    <div class="tb-l"><span>Registered NDIS Provider · <em>10+ years of experience</em> · VIC · NSW · QLD</span></div>
    <div class="tb-r">
      <a class="hide-s" href="mailto:info@rehoboth.com.au">{icon(IC['mail'], '#dff066')} info@rehoboth.com.au</a>
      <a href="tel:1300853095">{icon(IC['phone'], '#dff066')} 1300 853 095</a>
    </div>
  </div>
</div>

<header class="nav" id="nav">
  <div class="wrap">
    <a class="logo" href="index.html"><img src="{LOGO}" alt="Rehoboth"></a>
    <nav class="primary" aria-label="Main">
      <a href="accommodation.html">SIL homes</a>
      <a href="disability-services.html">Services</a>
      <a href="disability-ndis-how-it-works.html">NDIS</a>
      <a href="about.html">About us</a>
      <a href="work-with-us.html">Careers</a>
      <a href="resource-hub.html">Resources</a>
    </nav>
    <div class="nav-cta">
      <a class="btn btn-teal" href="contact.html">Start your journey</a>
    </div>
    <button class="burger" id="burger" aria-label="Menu" aria-expanded="false" aria-controls="mmenu">&#9776;</button>
  </div>
  <nav class="mobile-menu" id="mmenu" aria-label="Mobile">
    <a href="accommodation.html">SIL homes &amp; vacancies</a>
    <a href="disability-services.html">Our services</a>
    <a href="disability-ndis-how-it-works.html">Understanding the NDIS</a>
    <a href="about.html">About us</a>
    <a href="work-with-us.html">Careers</a>
    <a href="resource-hub.html">Resources</a>
    <a href="contact.html">Contact us</a>
    <a class="mcall" href="tel:1300853095">Call 1300 853 095</a>
  </nav>
</header>

<main id="main">
<section class="hero">
  <div class="wrap">
    <div class="hero-copy">
      <span class="hand">Support that feels like family.</span>
      <h1>Live life <em>your way<svg viewBox="0 0 200 12" preserveAspectRatio="none"><path d="M3 9 C60 2 140 2 197 8" fill="none" stroke="#c4d600" stroke-width="5" stroke-linecap="round"/></svg></em>, with a team that truly cares.</h1>
      <p class="lead">Rehoboth is a registered NDIS provider whose team brings more than 10 years of experience, supporting people with disability across Victoria, New South Wales and Queensland; at home, in the community and in our supported independent living homes across Sydney and the Blue Mountains.</p>
      <div class="hero-cta">
        <a class="btn btn-lime" href="accommodation.html#vacancies">Explore SIL homes {icon(IC['arrow'], 'currentColor')}</a>
        <a class="btn btn-ghost" href="contact.html">Talk to our team</a>
      </div>
      <div class="hero-trust">
        <span>{icon(IC['shield'], '#5d7610')} Registered NDIS provider</span>
        <span>{icon(IC['clock'], '#5d7610')} 24/7 on-call</span>
        <span>{icon(IC['heart'], '#5d7610')} Nurse-led clinical care</span>
      </div>
    </div>
    <div class="hero-visual">
      <div class="hero-blob">
        <span class="ph"><img src="{IMG['hero']}" alt="A support worker and participant sharing a laugh at home" fetchpriority="high"></span>
        <span class="accent"></span><span class="accent2"></span>
      </div>
      <div class="float-card fc1">{icon(IC['home'], '#5d7610')}<span>SIL homes<small>Call for current vacancies</small></span></div>
      <div class="float-card fc2">{icon(IC['shield'], '#5d7610')}<span>Registered provider<small>Independently audited</small></span></div>
    </div>
  </div>
</section>

<div class="stats">
  <div class="wrap">
    <div class="stat reveal"><b><span data-count="10">10</span>+</b><span>Years of team experience</span></div>
    <div class="stat reveal" style="--d:.1s"><b><span data-count="7">7</span></b><span>SIL homes across NSW</span></div>
    <div class="stat reveal" style="--d:.2s"><b>24/7</b><span>On-call response</span></div>
    <div class="stat reveal" style="--d:.3s"><b><span data-count="3">3</span></b><span>States: VIC, NSW &amp; QLD</span></div>
  </div>
</div>

<section class="sil" id="sil">
  <div class="wrap">
    <div class="sil-top">
      <div class="reveal">
        <span class="eyebrow">Supported Independent Living</span>
        <h2>More than a house. <br>A place to call home.</h2>
        <p class="lead">Our SIL homes are warm, modern and welcoming, with experienced support teams on site, backed by 24/7 on-call response. Whether you&#8217;re moving out for the first time or looking for a provider who really listens, we&#8217;ll help you make the move with confidence.</p>
        <ul class="sil-list">
          {chk('Support staff trained in high-intensity and complex care')}
          {chk('Support workers trained in positive behaviour support; strategies implemented with dignity and respect')}
          {chk('Thoughtful housemate matching; your home should feel right')}
          {chk('Family and friends welcome, always')}
        </ul>
        <div class="hero-cta">
          <a class="btn btn-lime" href="accommodation.html#vacancies">View current vacancies {icon(IC['arrow'], 'currentColor')}</a>
          <a class="btn btn-ghost" href="accommodation.html#sil">How SIL works</a>
        </div>
      </div>
      <div class="sil-visual reveal" style="--d:.15s">
        <span class="chip">Ask about availability</span>
        <div class="main"><img src="{IMG['sil_main']}" alt="A participant relaxing in his supported independent living home" loading="lazy"></div>
        <div class="mini"><img src="{IMG['sil_small']}" alt="Support worker and participant cooking together" loading="lazy"></div>
      </div>
    </div>
    <div class="center reveal">
      <span class="eyebrow" style="justify-content:center">Featured homes</span>
      <h2 style="font-size:clamp(26px,3vw,38px)">Find your new home</h2>
    </div>
    <div class="hgrid" style="margin-top:44px">{home_cards}</div>
    <div class="sil-ctas reveal">
      <a class="btn btn-teal" href="accommodation.html#vacancies">See all 7 homes {icon(IC['arrow'], 'currentColor')}</a>
      <a class="btn btn-ghost" href="refer-to-us.html">Make a referral</a>
    </div>
  </div>
</section>

<section class="services" id="services">
  <div class="wrap">
    <div class="center reveal">
      <span class="eyebrow" style="justify-content:center">Our services</span>
      <h2 style="font-size:clamp(28px,3.2vw,42px)">Whatever your goals, <br>there&#8217;s support for that</h2>
      <p class="lead" style="margin-top:16px">From a few hours of help each week to around-the-clock complex care, our supports flex around your life, your plan and your goals.</p>
    </div>
    <div class="svc-grid">{svc_cards}</div>
  </div>
</section>

<section class="who">
  <div class="wrap">
    <div class="who-img reveal"><img src="{IMG['who']}" alt="A participant smiling while patting a horse" loading="lazy"></div>
    <div class="reveal" style="--d:.12s">
      <span class="eyebrow">Who we support</span>
      <h2 style="font-size:clamp(28px,3.2vw,40px)">Every person. Every need. <br>Genuinely welcome.</h2>
      <p class="lead" style="margin-top:16px">No two people are the same, and neither are our supports. Our teams are trained and experienced across a wide range of disability support needs, including complex and high-intensity supports; and people whose needs other providers have found hard to meet are genuinely welcome here.</p>
      <div class="pills">{who_pills}</div>
    </div>
  </div>
</section>

<section class="why-s">
  <div class="wrap">
    <div class="center reveal">
      <span class="eyebrow" style="justify-content:center">The Rehoboth difference</span>
      <h2 style="font-size:clamp(28px,3.2vw,42px)">Why participants and families trust us</h2>
      <p class="lead" style="margin-top:16px">Choosing a provider is a big decision. Here&#8217;s what you can count on from day one.</p>
    </div>
    <div class="why-grid">{why_cards}</div>
  </div>
</section>

<section class="steps">
  <div class="wrap">
    <div class="center reveal">
      <span class="eyebrow" style="justify-content:center">Getting started</span>
      <h2 style="font-size:clamp(28px,3.2vw,42px)">Four simple steps</h2>
      <p class="lead" style="margin-top:16px">Starting with a new provider shouldn&#8217;t be hard. We make it simple, and we move at your pace.</p>
    </div>
    <div class="steps-grid">{steps_html}</div>
  </div>
</section>

<section class="work" id="workforce">
  <div class="wrap">
    <div class="center reveal">
      <span class="eyebrow" style="justify-content:center">Workforce</span>
      <h2 style="font-size:clamp(28px,3.2vw,42px)">A trained team, ready when you need them</h2>
    </div>
    <div class="work-grid">
      <div class="wcard wc1 reveal">
        <span class="wc-ic">{icon(IC['brief'])}</span>
        <h3>For providers: need qualified staff?</h3>
        <p>We supply screened, trained and fully credentialed support workers and nurses to other providers, for one-off shifts, emergency cover or ongoing rosters. Workers we supply hold current NDIS Worker Screening clearances and the credentials required for their roles, backed by our 24/7 on-call team.</p>
        <a class="btn btn-teal" href="contact.html">Request staff {icon(IC['arrow'], 'currentColor')}</a>
      </div>
      <div class="wcard wc2 reveal" style="--d:.12s">
        <span class="wc-ic">{icon(IC['users'], '#dff066')}</span>
        <h3>For support workers: join our on-call team</h3>
        <p>Love the flexibility of choosing your shifts? Put your hand up to join our on-call workforce. We&#8217;ll support you with training, credentialing and a team that has your back, then match you with shifts that suit your life.</p>
        <a class="btn btn-lime" href="work-with-us.html#oncall">Register your interest {icon(IC['arrow'], 'currentColor')}</a>
      </div>
    </div>
  </div>
</section>

<section class="mission">
  <div class="bg"><img src="{IMG['mission']}" alt="" loading="lazy"></div>
  <div class="wrap">
    <span class="hand reveal">Our promise to you</span>
    <h2 class="reveal" style="--d:.1s">A caring environment where people and families feel heard, supported and empowered to live life their way.</h2>
    <p class="reveal" style="--d:.2s">That&#8217;s not a slogan; it&#8217;s how our team has worked for more than ten years. Person-centred, culturally safe and always on your side.</p>
    <a class="btn btn-lime reveal" style="--d:.3s" href="about.html">Our story {icon(IC['arrow'], 'currentColor')}</a>
  </div>
</section>

<section class="cta" id="contact">
  <div class="wrap">
    <div class="cta-box reveal">
      <div>
        <h2>Ready when you are.</h2>
        <p>Call us for a friendly, no-obligation chat about your needs and how we can help. We welcome self-managed, plan-managed and NDIA-managed participants.</p>
      </div>
      <div class="cta-actions">
        <a class="btn btn-white" href="tel:1300853095">{icon(IC['phone'], 'currentColor')} 1300 853 095</a>
        <a class="btn btn-teal" href="contact.html">Send an enquiry</a>
      </div>
    </div>
  </div>
</section>

</main>
<footer>
  <div class="wrap">
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
      <div>
        <h3 class="fh">Supports</h3>
        <ul>
          <li><a href="accommodation.html">SIL &amp; accommodation</a></li>
          <li><a href="in-home.html">In-home support</a></li>
          <li><a href="24-hour-care.html">Complex &amp; 24/7 care</a></li>
          <li><a href="disability-nursing.html">Community nursing</a></li>
          <li><a href="mental-health.html">Psychosocial support</a></li>
          <li><a href="disability-services.html">All services</a></li>
        </ul>
      </div>
      <div>
        <h3 class="fh">NDIS</h3>
        <ul>
          <li><a href="disability-ndis-how-it-works.html">How the NDIS works</a></li>
          <li><a href="ndis-disability-how-to-apply.html">How to apply</a></li>
          <li><a href="funding-options.html">Funding options</a></li>
          <li><a href="ndis-pricelist.html">Pricing</a></li>
          <li><a href="refer-to-us.html">Make a referral</a></li>
        </ul>
      </div>
      <div>
        <h3 class="fh">Company</h3>
        <ul>
          <li><a href="about.html">About us</a></li>
          <li><a href="work-with-us.html">Careers</a></li>
          <li><a href="work-with-us.html#oncall">Join our on-call team</a></li>
          <li><a href="resource-hub.html">Resources &amp; FAQs</a></li>
          <li><a href="blog.html">News &amp; stories</a></li>
          <li><a href="contact.html">Contact us</a></li>
        </ul>
      </div>
    </div>
    <div class="ack">
      <div class="ack-flags">
        <svg role="img" focusable="false" viewBox="0 0 60 40" aria-label="Aboriginal flag"><rect width="60" height="20" fill="#000"/><rect y="20" width="60" height="20" fill="#cc0000"/><circle cx="30" cy="20" r="9" fill="#ffce00"/></svg>
        <svg role="img" focusable="false" viewBox="0 0 60 40" aria-label="Torres Strait Islander flag"><rect width="60" height="40" fill="#0052b4"/><rect y="7" width="60" height="5" fill="#000"/><rect y="28" width="60" height="5" fill="#000"/><rect y="12" width="60" height="16" fill="#009543"/><path d="M30 13l1.8 3.6 4 .6-2.9 2.8.7 4-3.6-1.9-3.6 1.9.7-4-2.9-2.8 4-.6z" fill="#fff"/></svg>
      </div>
      <p>Rehoboth acknowledges the Traditional Custodians of the lands on which we live and work across Australia, and pays its respects to Elders past and present. We celebrate the diversity of all people, and welcome every participant, family member and team member regardless of culture, faith, sexuality, gender identity or ability.</p>
    </div>
    <div class="f-bottom">
      <span>&copy; 2026 Rehoboth Comprehensive Care Services &middot; Community Regain Pty Ltd &middot; ABN 12 657 939 896</span>
      <span><a href="privacy-policy.html">Privacy policy</a> &nbsp;&middot;&nbsp; <a href="resource-hub.html">Feedback &amp; complaints</a></span>
    </div>
  </div>
</footer>

<script>
(function() {{
  document.documentElement.classList.add('js');
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  // sticky nav shadow
  var nav = document.getElementById('nav');
  addEventListener('scroll', function() {{ nav.classList.toggle('scrolled', scrollY > 8); }}, {{passive:true}});
  // mobile menu
  var b = document.getElementById('burger'), m = document.getElementById('mmenu');
  b.addEventListener('click', function() {{ var open = m.classList.toggle('open'); b.setAttribute('aria-expanded', open); }});
  addEventListener('keydown', function(e) {{ if (e.key === 'Escape' && m.classList.contains('open')) {{ m.classList.remove('open'); b.setAttribute('aria-expanded', 'false'); b.focus(); }} }});
  // reveal on scroll
  var io = new IntersectionObserver(function(es) {{
    es.forEach(function(e) {{ if (e.isIntersecting) {{ e.target.classList.add('in'); io.unobserve(e.target); }} }});
  }}, {{threshold:.14}});
  document.querySelectorAll('.reveal').forEach(function(el) {{ io.observe(el); }});
  // counters
  var cio = new IntersectionObserver(function(es) {{
    es.forEach(function(e) {{
      if (!e.isIntersecting) return;
      if (reduce) {{ cio.unobserve(e.target); return; }}
      var el = e.target, end = +el.dataset.count, t0 = null;
      el.textContent = '0';
      function tick(t) {{
        if (!t0) t0 = t;
        var p = Math.min((t - t0) / 1400, 1);
        el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3)));
        if (p < 1) requestAnimationFrame(tick);
      }}
      requestAnimationFrame(tick);
      cio.unobserve(el);
    }});
  }}, {{threshold:.6}});
  document.querySelectorAll('[data-count]').forEach(function(el) {{ cio.observe(el); }});
}})();
</script>
</body>
</html>'''

open('/Users/brookw/demorccs/index.html', 'w', encoding='utf-8').write(page)
print(f"index.html written: {len(page)//1024} KB")
