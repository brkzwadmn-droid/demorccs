#!/usr/bin/env python3
"""Build new pages from drafts.json (workflow output) using an existing page
as the shell: everything outside <main> is reused verbatim (header, footer,
theme CSS, all fix scripts), only the main content + title/meta change."""
import json, re, sys

TEMPLATE = "/Users/brookw/demorccs/funding-options.html"
src = open(TEMPLATE, encoding="utf-8", errors="surrogatepass").read()
m1 = re.search(r'<main[^>]*>', src)
m2 = src.rfind('</main>')
prefix, suffix = src[:m1.end()], src[m2:]

drafts = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "/tmp/drafts.json"))

def set_head(head, title, desc, fname):
    head = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', head, count=1, flags=re.DOTALL)
    # canonical
    head = re.sub(r'(<link rel="canonical"[^>]*href=")[^"]*(")', r'\g<1>' + fname + r'\g<2>', head)
    # meta description (replace or insert)
    if re.search(r'<meta name="description"', head):
        head = re.sub(r'(<meta name="description"[^>]*content=")[^"]*(")', r'\g<1>' + desc + r'\g<2>', head)
    else:
        head = head.replace('</title>', f'</title>\n<meta name="description" content="{desc}">', 1)
    # og/twitter
    head = re.sub(r'(<meta property="og:title"[^>]*content=")[^"]*(")', r'\g<1>' + title + r'\g<2>', head)
    head = re.sub(r'(<meta property="og:description"[^>]*content=")[^"]*(")', r'\g<1>' + desc + r'\g<2>', head)
    head = re.sub(r'(<meta property="og:url"[^>]*content=")[^"]*(")', r'\g<1>' + fname + r'\g<2>', head)
    return head

for d in drafts:
    fname, title, desc, main = d["file"], d["title"], d["metaDescription"], d["mainHtml"]
    page = set_head(prefix, title, desc.replace('"', '&quot;'), fname) + "\n" + main + "\n" + suffix
    out = f"/Users/brookw/demorccs/{fname}"
    with open(out, "w", encoding="utf-8", errors="surrogatepass") as fh:
        fh.write(page)
    print(f"  built {fname}  ({len(page)//1024} KB, main {len(main)//1024} KB, verified={d.get('verified')})")
print("Done:", len(drafts), "pages")
