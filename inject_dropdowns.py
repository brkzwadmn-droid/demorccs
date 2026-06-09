#!/usr/bin/env python3
"""Two header fixes, injected before the real (last) </body> of every page:
1. Desktop mega-menu dropdowns: theme JS is dead, so menus never open.
   Add hover + touch toggle that forces the .dropdown-menu visible.
2. Mobile menu: below 1200px the theme shows no menu at all. Append a
   burger button + slide-down panel (CSS-only details groups) to the header.
"""
import glob

PAYLOAD = r"""<style id="rcc-nav-fixes">
/* mobile menu (only shown when the theme menu is hidden) */
.rcc-mburger{display:none;position:absolute;top:14px;right:64px;z-index:1002;background:#004851;color:#fff;border:none;border-radius:8px;width:42px;height:42px;font-size:21px;line-height:1;cursor:pointer}
.rcc-mpanel{display:none;position:absolute;top:70px;left:0;right:0;z-index:1001;background:#fff;box-shadow:0 14px 30px rgba(0,0,0,.25);max-height:calc(100vh - 80px);overflow:auto;padding:10px 16px 18px;font-family:Montserrat,Arial,sans-serif}
.rcc-mpanel.rcc-open{display:block}
.rcc-mpanel a{display:block;padding:9px 10px;color:#143b41;text-decoration:none;border-radius:6px;font-size:15px}
.rcc-mpanel a:hover{background:#eef3e0}
.rcc-mpanel details{border-bottom:1px solid #eee}
.rcc-mpanel summary{cursor:pointer;padding:11px 10px;font-weight:700;color:#004851;font-size:15px;list-style:none}
.rcc-mpanel summary::-webkit-details-marker{display:none}
.rcc-mpanel summary:after{content:"\25BE";float:right;opacity:.7}
.rcc-mpanel .rcc-mtop{font-weight:700;color:#004851;border-bottom:1px solid #eee}
.rcc-mpanel .rcc-mphone{background:#c4d600;color:#004851;text-align:center;font-weight:700;border-radius:999px;margin-top:12px}
@media (max-width:1199px){.rcc-mburger{display:block}}
</style>
<script id="rcc-nav-fixes-js">
(function(){
  function show(m,on){
    if(on){m.style.setProperty('visibility','visible','important');m.style.setProperty('opacity','1','important');
      m.style.setProperty('transform','none','important');m.style.setProperty('pointer-events','auto','important');}
    else{m.style.setProperty('visibility','hidden','important');m.style.setProperty('opacity','0','important');
      m.style.setProperty('pointer-events','none','important');}
    m.setAttribute('aria-hidden', on?'false':'true');
  }
  function initDropdowns(){
    document.querySelectorAll('.navbar-nav > li.dropdown').forEach(function(li){
      var menu=li.querySelector(':scope > .dropdown-menu'); var tog=li.querySelector(':scope > a.dropdown-toggle');
      if(!menu||!tog||li.dataset.rccDd) return; li.dataset.rccDd='1';
      var hideT=null;
      li.addEventListener('mouseenter',function(){clearTimeout(hideT);closeAll(li);show(menu,true);tog.setAttribute('aria-expanded','true');});
      li.addEventListener('mouseleave',function(){hideT=setTimeout(function(){show(menu,false);tog.setAttribute('aria-expanded','false');},220);});
      tog.addEventListener('click',function(e){
        var open=menu.getAttribute('aria-hidden')==='false';
        if(!open){e.preventDefault();closeAll(li);show(menu,true);tog.setAttribute('aria-expanded','true');}
      });
    });
    document.addEventListener('keydown',function(e){if(e.key==='Escape')closeAll(null);});
  }
  function closeAll(except){
    document.querySelectorAll('.navbar-nav > li.dropdown').forEach(function(li){
      if(li===except)return;
      var m=li.querySelector(':scope > .dropdown-menu');var t=li.querySelector(':scope > a.dropdown-toggle');
      if(m){show(m,false);} if(t){t.setAttribute('aria-expanded','false');}
    });
  }
  function initMobile(){
    var host=document.querySelector('.mn-light .main-nav-wrapper .container');
    if(!host||document.querySelector('.rcc-mburger'))return;
    var b=document.createElement('button');b.className='rcc-mburger';b.setAttribute('aria-label','Menu');b.innerHTML='&#9776;';
    var p=document.createElement('div');p.className='rcc-mpanel';
    p.innerHTML='<a class="rcc-mtop" href="index.html">Home</a>'
      +'<details><summary>Accommodation</summary><a href="accommodation.html">Accommodation overview</a><a href="accommodation.html#sil">Supported Independent Living (SIL)</a><a href="accommodation.html#sda">Specialist Disability Accommodation (SDA)</a><a href="accommodation.html#sta">Short Term Accommodation (STA)</a><a href="accommodation.html#mta">Medium Term Accommodation (MTA)</a><a href="accommodation.html#ilo">Individualised Living Options (ILO)</a></details>'
      +'<details><summary>Disability</summary><a href="disability.html">Disability overview</a><a href="disability-services.html">Disability services</a><a href="in-home.html">In-home support</a><a href="personal-care.html">Personal care</a><a href="social-and-community.html">Social &amp; community</a><a href="transport-services.html">Transport services</a><a href="night-services.html">Night services</a><a href="24-hour-care.html">24-hour care</a><a href="specialists-services.html">Specialist services</a><a href="disability-nursing.html">Disability nursing</a></details>'
      +'<details><summary>NDIS</summary><a href="disability-ndis-how-it-works.html">How it works</a><a href="ndis-disability-how-to-apply.html">How to apply</a><a href="funding-options.html">Funding options</a><a href="ndis-pricelist.html">Pricelist</a><a href="agency-managed-ndis.html">Agency-managed</a><a href="plan-management-ndis.html">Plan-managed</a><a href="self-management-ndis.html">Self-managed</a></details>'
      +'<details><summary>Care &amp; support</summary><a href="care-management-services.html">Care management</a><a href="carers-support.html">Carers support</a><a href="aged-care.html">Aged care</a><a href="mental-health.html">Mental health</a><a href="veterans.html">Veterans</a></details>'
      +'<details><summary>About &amp; resources</summary><a href="about.html">About Rehoboth</a><a href="resource-hub.html">Resource hub</a><a href="forms.html">Forms</a><a href="blog.html">News &amp; stories</a><a href="work-with-us.html">Work with us</a><a href="refer-to-us.html">Refer to us</a><a href="pay-your-invoice.html">Pay your invoice</a></details>'
      +'<a href="contact.html">Contact us</a>'
      +'<a class="rcc-mphone" href="tel:1300853095">Call 1300 853 095</a>';
    b.addEventListener('click',function(e){e.stopPropagation();p.classList.toggle('rcc-open');});
    document.addEventListener('click',function(e){if(!p.contains(e.target)&&e.target!==b)p.classList.remove('rcc-open');});
    host.style.position='relative';host.appendChild(b);host.appendChild(p);
  }
  function init(){initDropdowns();initMobile();}
  if(document.readyState!=='loading')init();else document.addEventListener('DOMContentLoaded',init);
})();
</script>"""

count = 0
for f in glob.glob("/Users/brookw/demorccs/*.html"):
    with open(f, encoding="utf-8", errors="surrogatepass") as fh:
        html = fh.read()
    if 'rcc-nav-fixes' in html:
        continue
    pos = max(html.rfind('</body>'), html.rfind('</BODY>'))
    if pos == -1:
        pos = len(html)
    html = html[:pos] + PAYLOAD + html[pos:]
    with open(f, "w", encoding="utf-8", errors="surrogatepass") as fh:
        fh.write(html)
    count += 1
print("Patched:", count, "files")
