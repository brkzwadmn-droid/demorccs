#!/usr/bin/env python3
"""Make the header 'More' hamburger (.cd-dropdown) open/close its menu.
The theme's toggle JS is dead, so bind our own click handler that forces the
panel visible/hidden via inline !important styles. Insert before the LAST
</body> (real document, not the decoy Grammarly artifact)."""
import glob

SCRIPT = """<script id="rcc-more-toggle">
(function(){
  function setOpen(dd, open){
    var m=dd.querySelector('.cd-dropdown__menu'); if(!m) return;
    var b=dd.querySelector('.cd-dropdown__toggle');
    if(open){
      m.style.setProperty('visibility','visible','important');
      m.style.setProperty('opacity','1','important');
      m.style.setProperty('transform','none','important');
      m.style.setProperty('pointer-events','auto','important');
    } else {
      m.style.setProperty('visibility','hidden','important');
      m.style.setProperty('opacity','0','important');
      m.style.setProperty('pointer-events','none','important');
    }
    dd.setAttribute('data-rcc-open', open ? '1' : '0');
    if(b) b.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  function init(){
    document.querySelectorAll('.cd-dropdown').forEach(function(dd){
      var b=dd.querySelector('.cd-dropdown__toggle');
      if(!b || b.dataset.rccBound) return;
      b.dataset.rccBound='1';
      b.addEventListener('click', function(e){
        e.preventDefault(); e.stopPropagation();
        setOpen(dd, dd.getAttribute('data-rcc-open') !== '1');
      }, true);
    });
    document.addEventListener('click', function(e){
      document.querySelectorAll('.cd-dropdown[data-rcc-open="1"]').forEach(function(dd){
        if(!dd.contains(e.target)) setOpen(dd, false);
      });
    });
    document.addEventListener('keydown', function(e){
      if(e.key==='Escape') document.querySelectorAll('.cd-dropdown[data-rcc-open="1"]').forEach(function(dd){ setOpen(dd, false); });
    });
  }
  if(document.readyState!=='loading') init();
  else document.addEventListener('DOMContentLoaded', init);
})();
</script>"""

count = 0
for f in glob.glob("/Users/brookw/demorccs/*.html"):
    with open(f, encoding="utf-8", errors="surrogatepass") as fh:
        html = fh.read()
    if 'rcc-more-toggle' in html:
        continue
    pos = max(html.rfind('</body>'), html.rfind('</BODY>'))
    if pos == -1:
        pos = len(html)
    html = html[:pos] + SCRIPT + html[pos:]
    with open(f, "w", encoding="utf-8", errors="surrogatepass") as fh:
        fh.write(html)
    count += 1
print("Patched:", count, "files")
