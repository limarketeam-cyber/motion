"""Builds teaser6.html: teaser v4 (same cut, same timing, same audio) restyled to the
Hamahang visual-identity pack — flat brand plates, official icons/flags/logo/fonts,
brand layer-wipe transitions.  Run: python3 teaser6_build.py"""
import re

t4 = open('teaser4.html', encoding='utf-8').read()
RED, INK, BLUE, SEC, LINE = '#D32F2F', '#262426', '#002CB0', '#567B9F', '#D5D9DD'


def icon(name, recolor, draw=False):
    """Inline a brand icon (96-unit viewBox). recolor: {old: new}. draw: add pathLength for stroke-draw."""
    s = open(f'assets/brand/icons/{name}.svg', encoding='utf-8').read()
    s = re.sub(r'<title>.*?</title>', '', s)
    s = re.sub(r'<svg[^>]*>', '<svg viewBox="0 0 96 96" xmlns="http://www.w3.org/2000/svg">', s, count=1)
    s = s.replace(' xmlns="http://www.w3.org/2000/svg" d=', ' d=').replace('<rect xmlns="http://www.w3.org/2000/svg" ', '<rect ')
    for a, b in recolor.items():
        s = s.replace(a, b)
    if draw:
        s = re.sub(r'<(path|rect|circle|line|polyline|ellipse)((?:(?!/>)[^>])*fill="none"[^>]*?)/>', r'<\1 pathLength="1"\2/>', s)
    return s


# ---------- tiles on the speaker shot: flat white plate, red line icon, red accent bar
ICON = {'b_ex': 'warning', 'b_shield': 'warranty', 'b_q1': 'faq', 'b_globe': 'globe', 'b_bulb': 'information',
        'b_fac': 'factory', 'b_q4': 'faq', 'b_cart': 'cart', 'b_money': 'price', 'b_bulb2': 'chat',
        'b_scale': 'discount', 'b_q2': 'faq'}
FLAG = {'b_vn': 'VN', 'b_c1': 'VN', 'b_c2': 'CN', 'b_c4': 'KR', 'b_c3': 'IN'}
tile_re = re.compile(r'<div class="t3( capup)?" id="(\w+)" style="([^"]*)"><div class="face( fl)?" style="[^"]*">.*?</div>'
                     r'(<div class="cap"><span>(.*?)</span></div>)?</div>', re.S)


def new_tile(m):
    capup, tid, style, cap = m.group(1) or '', m.group(2), m.group(3), m.group(6)
    if tid in FLAG:
        face = f'<div class="face fl"><img src="assets/brand/flags/{FLAG[tid]}.svg"><i class="acc"></i></div>'
    else:
        face = f'<div class="face">{icon(ICON[tid], {INK: RED}, draw=True)}<i class="acc"></i></div>'
    c = f'<div class="cap"><span>{cap}</span></div>' if cap else ''
    return f'<div class="t3{capup}" id="{tid}" style="{style}">{face}{c}</div>'


html, n = tile_re.subn(new_tile, t4)
assert n == 17, n

# ---------- boards: brand locks + flags
lock_board = icon('lock-color', {SEC: INK, RED: BLUE})
lock_white = icon('lock', {INK: '#FFFFFF'})
html, n1 = re.subn(r'<div class="lk"><svg viewBox="0 0 32 32".*?</svg>', lambda m: '<div class="lk">' + lock_board, html, flags=re.S)
html, n2 = re.subn(r'<span class="f"><svg viewBox="0 0 32 32".*?</svg>', lambda m: '<span class="f">' + lock_white, html, flags=re.S)
assert n1 == 11 and n2 == 1, (n1, n2)
html = re.sub(r'assets/flags/(\w\w)\.svg', lambda m: f'assets/brand/flags/{m.group(1).upper()}.svg', html)
html = html.replace('color:rgba(30,94,255,.45)', '')

# ---------- pack shot: revised logo
html = html.replace('<div class="lg"></div>', '<div class="lg"><img src="assets/brand/logo.svg" alt="گروه هماهنگ"></div>')

# ---------- brand layer wipes (Transitions T01/T02/T03, portrait)
WIPES = '''  <div id="wipe">
    <div class="ws wi"><i style="background:#262426"></i><i style="background:#D32F2F"></i><i style="background:#DFE7ED"></i></div>
    <div class="ws wo"><i style="background:#567B9F"></i><i style="background:#262426"></i><i style="background:#D32F2F"></i></div>
    <div class="ws v"><i style="background:#D32F2F"></i><i style="background:#567B9F"></i><i style="background:#262426"></i></div>
  </div>
</div>
<script src="assets/gsap.min.js"></script>'''
html = html.replace('</div>\n<script src="assets/gsap.min.js"></script>', WIPES, 1)

# ---------- styles
CSS = '''<style>
@font-face{font-family:"HH";src:url(assets/brand/fonts/IBMPlexSansArabic-Regular.ttf);font-weight:400}
@font-face{font-family:"HH";src:url(assets/brand/fonts/IBMPlexSansArabic-Bold.ttf);font-weight:700}
@font-face{font-family:"HH";src:url(assets/brand/fonts/IBMPlexSans-Regular.ttf);font-weight:400;unicode-range:U+0000-00FF,U+2000-206F}
@font-face{font-family:"HH";src:url(assets/brand/fonts/IBMPlexSans-Bold.ttf);font-weight:700;unicode-range:U+0000-00FF,U+2000-206F}
/* Hamahang visual identity: primary #D32F2F, ink #262426, tertiary #002CB0, secondary #567B9F, outline #D5D9DD */
:root{--ink:#262426;--r:#D32F2F;--b:#002CB0;--sec:#567B9F;--line:#D5D9DD;--bg:#FCFBFB;--skel:#E3E8ED}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#000;width:1080px;height:1920px;overflow:hidden}
body{font-family:"HH",sans-serif;font-weight:400}
#stage{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}
#cam{position:absolute;inset:0;transform-origin:540px 700px}
#vid,#vid2{position:absolute;inset:0;width:1080px;height:1920px;display:block}
#actor{position:absolute;inset:0;-webkit-mask-size:1080px 1920px;mask-size:1080px 1920px;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat}
#behind{position:absolute;inset:0;filter:blur(.6px)}
.layer{position:absolute;inset:0;pointer-events:none}
/* speaker shot: flat brand plates (white + red), no shadow / volume / gradient */
.t3{position:absolute;opacity:0}
.t3 .face{position:absolute;inset:0;border-radius:16px;background:#fff;box-shadow:inset 0 0 0 2px var(--line);display:grid;place-items:center}
.t3 .face svg{width:62%;height:62%;overflow:visible}
.t3 .face svg [pathLength]{stroke-dasharray:1 2}
.t3 .face .acc{position:absolute;right:10px;top:24%;bottom:24%;width:5px;border-radius:3px;background:var(--r);transform-origin:50% 0}
.t3 .face.fl{padding:20px 26px 20px 20px}
.t3 .face.fl img{width:100%;height:100%;object-fit:contain}
.t3 .cap{position:absolute;left:50%;top:calc(100% + 10px);transform:translateX(-50%);white-space:nowrap}
.t3.capup .cap{top:auto;bottom:calc(100% + 10px)}
.t3 .cap span{display:inline-block;background:var(--r);color:#fff;font-weight:700;font-size:30px;line-height:1.45;padding:2px 22px 6px;border-radius:10px}
/* chest text: white words + key word on a red plate */
.kt{position:absolute;isolation:isolate;left:0;right:0;text-align:center;opacity:0;font-weight:700;font-size:80px;line-height:1.25;color:#fff;
  text-shadow:0 0 3px rgba(0,0,0,.85),0 6px 22px rgba(0,0,0,.7)}
.kt::before{content:"";position:absolute;left:50%;top:50%;width:980px;height:230px;transform:translate(-50%,-50%);
  background:radial-gradient(closest-side,rgba(0,0,0,.40),transparent);z-index:-1}
.kt .w{display:inline-block;margin:0 10px}
.kt .w.key{background:var(--r);border-radius:14px;padding:0 26px 12px;text-shadow:none}
/* full-graphic boards: brand light gradient background; 60 white / 30 ink / 10 blue */
.postbg{position:absolute;inset:0;overflow:hidden;
  background:radial-gradient(900px 760px at 84% 94%,rgba(211,47,47,.50),transparent 70%),radial-gradient(700px 620px at 8% 80%,rgba(230,149,149,.32),transparent 72%),
  radial-gradient(820px 700px at 6% 2%,rgba(157,175,230,.42),transparent 70%),radial-gradient(700px 640px at 102% 28%,rgba(196,213,230,.55),transparent 70%),var(--bg)}
#board{position:absolute;inset:0;overflow:hidden}
.bignum{position:absolute;width:560px;height:560px;border-radius:50%;border:40px solid #C4D5E6;color:#9DAFE6;opacity:0;display:grid;place-items:center;font-weight:700;font-size:250px;line-height:1;padding-bottom:40px}
.scene{position:absolute;inset:0;opacity:0}
.arrow{position:absolute;overflow:visible;opacity:0}
.dash{fill:none;stroke:var(--sec);stroke-width:5;stroke-linecap:round;stroke-dasharray:18 14}
.head{fill:none;stroke:var(--sec);stroke-width:5;stroke-linecap:round;stroke-linejoin:round}
.acc-b::after,.acc-r::after{content:"";position:absolute;right:12px;top:22px;bottom:22px;width:4px;border-radius:2px;background:var(--b)}
.acc-r::after{background:var(--r)}
.bcard{position:absolute;background:#fff;border-radius:14px;overflow:hidden;opacity:0;border:2px solid var(--line)}
.bcard::after{content:"";position:absolute;right:26px;bottom:0;width:60px;height:4px;background:var(--b)}
.bcard img.shot{display:block;width:100%}
.blurbox{filter:blur(7px)}
.note{position:absolute;color:var(--ink);font-weight:700;font-size:54px;line-height:1.3;opacity:0;text-align:right}
.note b{color:var(--b);font-weight:700}
.stile{position:absolute;width:170px;height:170px;opacity:0}
.stile .f3{position:absolute;inset:0;border-radius:14px;background:#fff;border:2px solid var(--line);display:grid;place-items:center}
.stile svg{width:130px;height:28px;fill:var(--ink)}
.lock{position:absolute;opacity:0;white-space:nowrap}
.lock .f{position:relative;display:flex;align-items:center;gap:14px;background:var(--ink);color:#fff;border-radius:14px;padding:10px 40px 18px 22px;font-size:40px;font-weight:700}
.lock svg{width:52px;height:52px}
.tc{position:absolute;width:280px;height:300px;opacity:0}
.tc .f3{position:absolute;inset:0;border-radius:14px;background:#fff;border:2px solid var(--line);padding:26px 30px 26px 24px}
.tc .n,.ph .row .n{border-radius:10px;background:var(--b);color:#fff;font-weight:700;display:grid;place-items:center}
.tc .n{width:80px;height:80px;font-size:46px}
.tc .sk{height:20px;border-radius:10px;background:var(--skel);margin-top:22px;filter:blur(1.5px)}
.tc .lk{position:absolute;left:50%;bottom:22px;transform:translateX(-50%);width:84px;height:84px} .tc .lk svg{width:100%;height:100%}
.ttlB{position:absolute;left:70px;right:70px;text-align:center;font-weight:700;font-size:66px;color:var(--ink);opacity:0;line-height:1.3}
.ttlB b{color:var(--b);font-weight:700}
.ph{position:absolute;width:420px;height:820px;opacity:0}
.ph .f3{position:absolute;inset:0;border-radius:56px;background:var(--ink);padding:12px}
.ph .scr{position:absolute;inset:12px;border-radius:46px;background:var(--bg);overflow:hidden;padding:28px 20px}
.ph .punch{position:absolute;left:50%;top:22px;width:20px;height:20px;border-radius:50%;background:var(--ink);transform:translateX(-50%)}
.ph .sb{display:flex;justify-content:space-between;direction:ltr;font-size:20px;color:var(--ink);padding:0 16px}
.ph .ttl{text-align:center;direction:ltr;font-size:44px;font-weight:700;color:var(--ink);margin:54px 0 8px}
.ph .ctry{display:flex;justify-content:center;align-items:center;gap:12px;font-size:34px;font-weight:700;color:var(--ink);margin-bottom:30px}
.ph .ctry img{width:60px;height:40px;object-fit:contain}
.ph .grp{position:relative;background:#fff;border-radius:14px;border:2px solid var(--line);padding:6px 10px}
.ph .row{display:flex;align-items:center;gap:14px;padding:22px 8px;border-bottom:2px solid #EEF1F4;opacity:0}
.ph .row:last-child{border-bottom:0}
.ph .row .n{width:48px;height:48px;font-size:28px;border-radius:8px;flex:none}
.ph .row .bar{flex:1;height:20px;border-radius:10px;background:var(--skel);filter:blur(1.5px)}
.ph .row .lk{width:44px;height:44px;flex:none} .ph .row .lk svg{width:100%;height:100%}
.vs{position:absolute;width:140px;height:140px;opacity:0}
.vs .f3{position:absolute;inset:0;border-radius:20px;background:var(--b);color:#fff;font-size:56px;font-weight:700;direction:ltr;display:grid;place-items:center}
/* pack shot: same background, 60/30/10, revised logo */
#cta{position:absolute;inset:0;opacity:0}
#cta .lg{position:absolute;left:50%;top:330px;width:460px;transform:translateX(-50%);opacity:0}
#cta .lg img{display:block;width:100%}
#cta .l1{position:absolute;left:0;right:0;top:540px;text-align:center;color:var(--ink);font-size:60px;font-weight:400;opacity:0}
#cta .l2{position:absolute;left:0;right:0;top:640px;text-align:center;color:var(--ink);font-size:100px;font-weight:700;opacity:0}
#cta .l2 b{color:var(--b);font-weight:700}
#cta .ap{position:absolute;left:120px;right:120px;top:880px;height:250px;opacity:0}
#cta .ap .f3{position:absolute;inset:0;background:#fff;border:2px solid var(--line);border-radius:14px;display:flex;align-items:center;gap:34px;padding:0 50px 0 44px}
#cta .ap .pl{width:150px;height:150px;border-radius:14px;background:var(--r);display:grid;place-items:center;flex:none}
#cta .ap .pl svg{width:96px;height:96px}
#cta .ap .t1{font-size:56px;font-weight:700;color:var(--ink)}
#cta .ap .t2{font-size:36px;font-weight:400;color:var(--sec);margin-top:6px}
#cta .bio{position:absolute;left:50%;top:1230px;transform:translateX(-50%);opacity:0;white-space:nowrap}
#cta .bio .f{position:relative;display:inline-block;background:var(--ink);color:#fff;border-radius:14px;padding:10px 50px 20px 44px;font-size:46px;font-weight:700}
/* brand layer wipes */
#wipe{position:absolute;inset:0;pointer-events:none;z-index:50}
#wipe .ws{position:absolute;inset:0;overflow:hidden}
#wipe i{position:absolute;inset:0}
#wipe .wi i{left:-16%;right:-16%;clip-path:polygon(14% 0,100% 0,86% 100%,0 100%)}
</style>'''
html = re.sub(r'<link rel="stylesheet" href="assets/fonts/plex-\d+\.css">\n', '', html)
html = re.sub(r'<style>.*?</style>', lambda m: CSS, html, count=1, flags=re.S)
html = html.replace('<title>تیزر سامسونگ ویتنام — کاشی سه‌بعدی</title>', '<title>تیزر سامسونگ ویتنام — هویت بصری هماهنگ</title>')
# accent bars on brand plates (boards use blue, dark plates use red)
html = html.replace('<div class="stile" id="aTile" style="left:830px;top:290px"><div class="f3">', '<div class="stile" id="aTile" style="left:830px;top:290px"><div class="f3 acc-b">')
html = html.replace('<div class="tc" id="t1" style="left:720px;top:1020px"><div class="f3">', '<div class="tc" id="t1" style="left:720px;top:1020px"><div class="f3 acc-b">')
html = html.replace('<div class="tc" id="t2" style="left:400px;top:1020px"><div class="f3">', '<div class="tc" id="t2" style="left:400px;top:1020px"><div class="f3 acc-b">')
html = html.replace('<div class="tc" id="t3" style="left:80px;top:1020px"><div class="f3">', '<div class="tc" id="t3" style="left:80px;top:1020px"><div class="f3 acc-b">')
html = html.replace('<div class="ap"><div class="f3">', '<div class="ap"><div class="f3 acc-b">')
html = html.replace('<span class="f">لینک توی بیو</span>', '<span class="f acc-r">لینک توی بیو</span>')
html = html.replace('<div class="lock" id="aLock" style="left:50%;top:140px;transform:translateX(-50%)"><span class="f">',
                    '<div class="lock" id="aLock" style="left:50%;top:140px;transform:translateX(-50%)"><span class="f acc-r">')

# ---------- motion: calm brand entrances (panel in, accent line grows, icon path draws)
def sub1(old, new):
    global html
    assert html.count(old) == 1, old[:60]
    html = html.replace(old, new)

old_pop = html[html.index('function pop(sel,t0,t1,o={}){'):html.index('function kt(sel,t0,t1,o={}){')]
sub1(old_pop, '''function pop(sel,t0,t1,o={}){
  const el=$(sel);
  tl.fromTo(sel,{opacity:0,scale:0.86,y:24},{opacity:1,scale:1,y:0,duration:0.32,ease:'power3.out'},t0);
  const acc=el.querySelector('.acc'); if(acc) tl.fromTo(acc,{scaleY:0},{scaleY:1,duration:0.28,ease:'power2.out'},t0+0.12);
  const ps=el.querySelectorAll('[pathLength]'); if(ps.length) tl.fromTo(ps,{strokeDashoffset:1},{strokeDashoffset:0,duration:0.5,ease:'power2.inOut',stagger:0.06},t0+0.1);
  const cap=el.querySelector('.cap span'); if(cap) tl.fromTo(cap,{opacity:0,y:12},{opacity:1,y:0,duration:0.25,ease:'power3.out'},t0+0.2);
  if(t1!=null) tl.to(sel,{opacity:0,scale:0.92,duration:0.2,ease:'power2.in'},t1-0.2);
  if(o.snd!==false) sfx(t0,o.snd||'pop',o.g??1);
}
''')
old_bi = html[html.index('function boardIn(t){'):html.index('function scene(sel,t0,t1){')]
sub1(old_bi, '''// brand transitions (T01/T02/T03 layer wipes): 3 stacked colour layers, cut while fully covered.
// Same layer timing as the pack JSON, run at 0.55x length to keep the teaser's pace.
const WK=0.55, LAY=[[0,.65,1.3,.6],[.11,.65,1.2,.6],[.22,.65,1.1,.6]];
gsap.set('#wipe .wi i,#wipe .wo i',{xPercent:100}); gsap.set('#wipe .v i',{yPercent:-100});
function wipe(id,tc,k=WK){
  const v=id==='v', P=v?'yPercent':'xPercent', a=v?-100:100, z=v?100:-100, t0=tc-1.0*k;
  document.querySelectorAll('#wipe .'+id+' i').forEach((el,i)=>{ const [es,ed,xs,xd]=LAY[i];
    tl.fromTo(el,{[P]:a},{[P]:0,duration:ed*k,ease:'power3.inOut',immediateRender:false},t0+es*k);
    tl.fromTo(el,{[P]:0},{[P]:z,duration:xd*k,ease:'power3.inOut',immediateRender:false},t0+xs*k); });
}
function boardIn(t){ wipe('wi',t); tl.set('#board',{xPercent:0},t); sfx(t-0.08,'whoosh',1); }
function boardOut(t){ wipe('wo',t,0.42); tl.set('#board',{xPercent:110},t); sfx(t-0.3,'whoosh',0.9); }
''')
sub1("function ring(sel,t0,t1){ tl.fromTo(sel,{opacity:0,scale:0.8,rotation:-20},{opacity:1,scale:1,rotation:0,duration:0.6,ease:'power3.out'},t0);",
     "function ring(sel,t0,t1){ tl.fromTo(sel,{opacity:0,scale:0.85},{opacity:1,scale:1,duration:0.5,ease:'power3.out'},t0);")
sub1("tl.set('#b_vn',{opacity:1,scale:1,rotation:-6},0);\ntl.to('#b_vn',{y:-12,duration:0.9,repeat:2,yoyo:true,ease:'sine.inOut'},0.4);",
     "tl.set('#b_vn',{opacity:1,scale:1},0);")
sub1("tl.to('#b_q1',{rotation:-6,duration:0.12,repeat:5,yoyo:true},6.4);\n", "")
sub1("tl.to('#b_scale',{rotation:6,duration:0.4,repeat:3,yoyo:true,ease:'sine.inOut'},29.5);\n", "")
sub1("tl.fromTo('#aCard',{opacity:0,y:120,rotation:3},{opacity:1,y:0,rotation:0,duration:0.5,ease:'back.out(1.4)'},8.35);",
     "tl.fromTo('#aCard',{opacity:0,y:90},{opacity:1,y:0,duration:0.45,ease:'power3.out'},8.35);")
sub1("tl.fromTo(s,{opacity:0,y:80,scale:0.8},{opacity:1,y:0,scale:1,duration:0.4,ease:'back.out(2)'},11.9+i*0.2);",
     "tl.fromTo(s,{opacity:0,y:60},{opacity:1,y:0,duration:0.35,ease:'power3.out'},11.9+i*0.2);")
sub1("tl.fromTo('#ph2',{opacity:0,x:-120,rotation:-6},{opacity:1,x:0,rotation:-3,duration:0.5,ease:'back.out(1.5)'},18.5);",
     "tl.fromTo('#ph2',{opacity:0,x:-120},{opacity:1,x:0,duration:0.45,ease:'power3.out'},18.5);")
sub1("tl.fromTo('#ph1',{opacity:0,x:120,rotation:6},{opacity:1,x:0,rotation:3,duration:0.5,ease:'back.out(1.5)'},18.7);",
     "tl.fromTo('#ph1',{opacity:0,x:120},{opacity:1,x:0,duration:0.45,ease:'power3.out'},18.7);")
sub1("tl.fromTo('#cta',{opacity:0,scale:1.08},{opacity:1,scale:1,duration:0.35,ease:'power3.out'},31.6);",
     "wipe('v',31.66); tl.set('#cta',{opacity:1},31.66);")
sub1("tl.fromTo('#cta .ap .pl',{scale:1},{scale:1.12,duration:0.35,repeat:7,yoyo:true,ease:'sine.inOut'},33.3);",
     "tl.fromTo('#cta .ap .pl',{scale:1},{scale:1.08,duration:0.35,repeat:7,yoyo:true,ease:'sine.inOut'},33.3);")
assert 'rotation' not in html.split('<script src="teaser4_data.js"></script>')[1], 'leftover rotation'
open('teaser6.html', 'w', encoding='utf-8').write(html)
print('written teaser6.html', len(html))
