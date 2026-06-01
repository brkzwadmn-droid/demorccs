#!/usr/bin/env python3
import glob, re, sys

SNIPPET = """<script data-css-rehydrate="1">
(function(){
  function run(){
    var seen={};
    function add(href){
      if(!href) return;
      href = href.replace(/&amp;/g,'&').replace(/['"\\s]+$/,'').trim();
      if(!/\\.css(\\?|$)/.test(href)) return;
      var key = href.split('?')[0];
      if(seen[key]) return; seen[key]=1;
      var l=document.createElement('link');
      l.rel='stylesheet'; l.href=href;
      document.head.appendChild(l);
    }
    var ns=document.querySelectorAll('noscript');
    for(var i=0;i<ns.length;i++){
      var html=ns[i].textContent||'';
      var re=/(?:data-savepage-href|href)\\s*=\\s*['"]([^'"]*\\.css[^'"\\s]*)['"]/g, m;
      while((m=re.exec(html))){ add(m[1]); }
    }
  }
  if(document.readyState!=='loading'){run();}
  else{document.addEventListener('DOMContentLoaded',run);}
})();
</script>
"""

count = 0
for f in glob.glob("/Users/brookw/demorccs/*.html"):
    with open(f, "r", encoding="utf-8", errors="surrogatepass") as fh:
        html = fh.read()
    if 'data-css-rehydrate' in html:
        continue
    idx = html.lower().find("</head>")
    if idx == -1:
        print("  no </head> in", f)
        continue
    html = html[:idx] + SNIPPET + html[idx:]
    with open(f, "w", encoding="utf-8", errors="surrogatepass") as fh:
        fh.write(html)
    count += 1
    print("  injected:", f.split("/")[-1])

print("Total files patched:", count)
