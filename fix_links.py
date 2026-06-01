#!/usr/bin/env python3
import glob, os

BASE = "https://www.avivo.org.au"
MAP = {
    "contact.html":        BASE + "/contact-us",
    "/contact":            BASE + "/contact-us",
    "/contact-us":         BASE + "/contact-us",
    "about.html":          BASE + "/about-avivo/about-us",
    "resources.html":      BASE + "/resource-hub",
    "/resource-hub":       BASE + "/resource-hub",
    "/your-journey":       BASE + "/your-journey",
    "/blog":               BASE + "/blog",
    "/veterans":           BASE + "/veterans",
    "/work-with-us":       BASE + "/work-with-us",
    "/refer-to-us":        BASE + "/refer-to-us",
    "/pay-your-invoice":   BASE + "/pay-your-invoice",
    "accommodation.html":  BASE + "/disability/disability-services",
    "forms.html":          BASE + "/resource-hub",
    "/faq":                BASE + "/resource-hub",
}

# longest targets first so "/contact-us" is replaced before "/contact"
targets = sorted(MAP, key=len, reverse=True)
total = 0
for f in glob.glob("/Users/brookw/demorccs/*.html"):
    with open(f, encoding="utf-8", errors="surrogatepass") as fh:
        html = fh.read()
    n = 0
    for t in targets:
        repl = MAP[t]
        for q in ('"', "'"):
            for variant in (t, t + "/"):
                needle = f"href={q}{variant}{q}"
                sub = f"href={q}{repl}{q}"
                c = html.count(needle)
                if c:
                    html = html.replace(needle, sub)
                    n += c
    if n:
        with open(f, "w", encoding="utf-8", errors="surrogatepass") as fh:
            fh.write(html)
        total += n
        print(f"  {os.path.basename(f):40s} {n} links")
print("Total links rewritten:", total)
