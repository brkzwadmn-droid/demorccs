#!/usr/bin/env python3
"""Install workflow drafts into EXISTING pages: replace <main> inner content
and update title/meta, keeping each page's own header/footer shell."""
import json, re, sys

drafts = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "/tmp/drafts2.json"))

def set_head(html, title, desc, fname):
    html = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', html, count=1, flags=re.DOTALL)
    html = re.sub(r'(<link rel="canonical"[^>]*href=")[^"]*(")', r'\g<1>' + fname + r'\g<2>', html)
    if re.search(r'<meta name="description"', html):
        html = re.sub(r'(<meta name="description"[^>]*content=")[^"]*(")', r'\g<1>' + desc + r'\g<2>', html)
    else:
        html = html.replace('</title>', f'</title>\n<meta name="description" content="{desc}">', 1)
    html = re.sub(r'(<meta property="og:title"[^>]*content=")[^"]*(")', r'\g<1>' + title + r'\g<2>', html)
    html = re.sub(r'(<meta property="og:description"[^>]*content=")[^"]*(")', r'\g<1>' + desc + r'\g<2>', html)
    html = re.sub(r'(<meta property="og:url"[^>]*content=")[^"]*(")', r'\g<1>' + fname + r'\g<2>', html)
    return html

ok = fail = 0
for d in drafts:
    fname = d.get('f') or d.get('file')
    path = f"/Users/brookw/demorccs/{fname}"
    try:
        html = open(path, encoding="utf-8", errors="surrogateescape").read()
    except FileNotFoundError:
        print(f"  !! missing {fname}"); fail += 1; continue
    m1 = re.search(r'<main[^>]*>', html); m2 = html.rfind('</main>')
    if not m1 or m2 < 0:
        print(f"  !! no main in {fname}"); fail += 1; continue
    html = html[:m1.end()] + "\n" + d['mainHtml'] + "\n" + html[m2:]
    html = set_head(html, d['title'], d['metaDescription'].replace('"', '&quot;'), fname)
    open(path, "w", encoding="utf-8", errors="surrogateescape").write(html)
    print(f"  installed {fname} (verified={d.get('verified')}, main {len(d['mainHtml'])//1024}KB)")
    ok += 1
print(f"installed {ok}, failed {fail}")
