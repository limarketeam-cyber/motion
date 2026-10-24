"""Builds teaser5.html (tight-rhythm teaser) from teaser4's styles and teaser5_edl.json."""
import re, json
t4=open('teaser4.html').read()
head=t4[:t4.index('</style>')]
defs=re.search(r'<svg width="0" height="0" style="position:absolute"><defs>.*?</defs></svg>',t4,re.S).group(0)
cta=t4[t4.index('  <div id="cta" class="postbg">'):]
cta=cta[:cta.index('\n</div>\n')+1]          # up to the end of #cta (stage closes after it)
E=json.load(open('teaser5_edl.json')); PC=E['pieces']; SPEECH=E['speech_end']; FRZ=E['freeze']
def N(lab,src):
    """new-timeline time of a source time inside segment `lab` (snaps into removed pauses)."""
    ps=[p for p in PC if p[0]==lab]
    for p in ps:
        if src<=p[2]+1e-6: return round(p[3]+max(0,src-p[1]),3)
    p=ps[-1]; return round(p[3]+p[2]-p[1],3)
def ST(lab): return N(lab,[p for p in PC if p[0]==lab][0][1])
def EN(lab): p=[p for p in PC if p[0]==lab][-1]; return round(p[3]+p[2]-p[1],3)
FREEZE0=SPEECH; CTA0=round(SPEECH+FRZ,3); END=round(CTA0+4.3,3)
T=dict(S0=ST('S0'),S1=ST('S1'),S1x=N('S1',28.70),S2a=ST('S2a'),S2b=ST('S2b'),BA=ST('BA'),BAx=N('BA',54.40),
       S3=ST('S3'),S3x=N('S3',82.55),BB=ST('BB'),BBx=N('BB',103.80),S4=ST('S4'),S4x=N('S4',139.50),
       FRZ=FREEZE0,CTA=CTA0,END=END)
print(T)
R='#d0141c'; B='#1e5eff'; K='#111114'
def hc(name,color):
    s=open(f'assets/hc/{name}.svg').read().replace('#212121',color)
    return re.sub(r'<svg[^>]*>','<svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">',s,count=1)
def tile(id,side,inner,cap=None,size=190,flag=False):
    ry=-18 if side=='L' else 18; left=100 if side=='L' else 790
    face=f'<div class="face{" fl" if flag else ""}" style="--ry:{ry}deg">{inner}</div>'
    c=f'<div class="cap"><span>{cap}</span></div>' if cap else ''
    return f'<div class="t3" id="{id}" style="left:{left}px;top:600px;width:{size}px;height:{size}px">{face}{c}</div>'
fl=lambda c:f'<img src="assets/flags/{c}.svg">'
tiles='\n'.join([
 tile('b_q0','L',hc('red_question_mark',R)), tile('b_money','R',hc('money_with_wings',R)),
 tile('b_vn','L',fl('vn'),flag=True), tile('b_ex','R',hc('double_exclamation_mark',R)),
 tile('b_c1','L',fl('vn'),'ویتنام',170,True), tile('b_c2','R',fl('cn'),'چین',170,True),
 tile('b_c4','L',fl('kr'),'کره',170,True), tile('b_c3','R',fl('in'),'هند',170,True),
 tile('b_shield','L',hc('shield',R)), tile('b_q1','R',hc('red_question_mark',R)),
 tile('b_globe','L',hc('globe_showing_asia-australia',R)), tile('b_bulb','R',hc('light_bulb',R)),
 tile('b_fac','L',hc('factory',R)), tile('b_q2','R',hc('red_question_mark',R)),
 tile('b_scale','L',hc('balance_scale',R)), tile('b_q3','R',hc('red_question_mark',R)),
])
KT={'k0':[('۲ تا ۳ میلیون',1),('بیشتر؟',0)],'k1':[('حتماً،',0),('حتماً!',1)],'k2':[('ویتنام',1),('باشه!',0)],
    'k3':[('کشورِ',1),('سازنده',0)],'k4':[('کیفیت',1),('رو تضمین می‌کنه؟',0)],'k5':[('واقعاً',0),('مهمه؟',1)],
    'k6':[('کجا',0),('مونتاژ',1),('شده؟',0)],'k7':[('این',0),('اختلاف قیمت',1)],'k8':[('دقیقاً بابت',0),('چیه؟',1)]}
kts='\n'.join(f'<div class="kt" id="{k}">'+''.join(f'<span class="w{" key" if key else ""}">{w}</span>' for w,key in ws)+'</div>' for k,ws in KT.items())
lockB=hc('locked',B)
def tcard(id,left,n,reveal=False):
    if reveal:
        body=('<div class="rv">همه‌ی کارخونه‌ها</div><div class="rv2">یک استاندارد…</div>')
    else:
        body=f'<div class="sk" style="width:90%"></div><div class="sk" style="width:65%"></div><div class="lk">{lockB}</div>'
    return f'<div class="tc" id="{id}" style="left:{left}px;top:1000px"><div class="f3"><div class="n">{n}</div>{body}</div></div>'
def phone(pid,left,code,name,tilt):
    rows=''.join(f'<div class="row r{i}"><div class="n">{"۱۲۳۴"[i-1]}</div><div class="bar"></div><div class="lk">{lockB}</div></div>' for i in range(1,5))
    return (f'<div class="ph" id="{pid}" style="left:{left}px;top:470px"><div class="f3" style="--rz:{tilt}deg"><div class="scr"><div class="punch"></div><div class="sb"><span>9:41</span><span>85%</span></div>'
            f'<div class="ttl">Galaxy A57</div><div class="ctry"><img src="assets/flags/{code}.svg">{name}</div><div class="grp">{rows}</div></div></div></div>')
extra_css='''
.tc .rv{margin-top:20px;font-size:34px;font-weight:700;color:var(--k);line-height:1.3}
.tc .rv2{margin-top:8px;font-size:34px;font-weight:700;color:var(--k);filter:blur(6px);opacity:.55}
.tc.open .f3{box-shadow:0 0 0 5px var(--b),0 2px 0 #e6e6eb,0 4px 0 #dcdce2,0 6px 0 #d2d2d9,0 8px 0 #c8c8d0,0 34px 50px rgba(30,30,40,.22)}
#prog{position:absolute;left:64px;right:64px;top:252px;height:8px;border-radius:4px;background:rgba(255,255,255,.35);
  box-shadow:0 2px 8px rgba(0,0,0,.25);overflow:hidden}
#prog i{position:absolute;left:0;top:0;bottom:0;width:0;background:var(--r);border-radius:4px}
#frz{position:absolute;inset:0;pointer-events:none;opacity:0;background:radial-gradient(closest-side,transparent 55%,rgba(208,20,28,.22))}
'''
body=f'''{defs}
<div id="stage">
  <div id="cam">
    <img id="vid" alt="">
    <div id="behind">
{tiles}
    </div>
    <div id="actor"><img id="vid2" alt=""></div>
  </div>
  <div id="frz"></div>
  <div class="layer" id="fx">
{kts}
  </div>
  <div id="board" class="postbg">
    <div class="bignum" id="n3" style="left:-210px;top:1060px;color:rgba(30,94,255,.45)">۳</div>
    <div class="bignum" id="n4" style="right:-230px;top:200px;color:rgba(30,94,255,.45)">۴</div>
    <div class="scene" id="sA">
      <div class="stile" id="aTile" style="left:830px;top:340px"><div class="f3"><svg viewBox="0 10 24 4"><use href="#samsung-path"/></svg></div></div>
      <div class="note" id="aNote" style="right:270px;top:360px;width:640px">صفحه‌ی <b>رسمی</b><br>پشتیبانی سامسونگ</div>
      <div class="ttlB" id="aTtl" style="top:640px"><b>۳ نکته</b> گفته</div>
      <svg class="arrow" id="aBr" style="left:0;top:860px;width:1080px;height:120px" viewBox="0 0 1080 120"><path class="dash" d="M540 0 V44 M220 44 H860 M220 44 V110 M540 44 V110 M860 44 V110"/></svg>
      {tcard('t1',720,'۱',True).replace('class="tc"','class="tc open"')}{tcard('t2',400,'۲')}{tcard('t3',80,'۳')}
    </div>
    <div class="scene" id="sB">
      <div class="ttlB" id="bTtl" style="top:300px">موقع مقایسه، <b>۴ چیز</b> مهمه</div>
      {phone('ph1',600,'vn','ویتنام',3)}
      {phone('ph2',60,'in','هند',-3)}
      <div class="vs" id="vs" style="left:470px;top:810px"><div class="f3">VS</div></div>
    </div>
  </div>
  <div id="prog"><i></i></div>
{cta}</div>
'''
js='''
<script src="assets/gsap.min.js"></script>
<script>
const T=__T__, PIECES=__P__;
const FPS=30, VIDEO_FRAMES=__VF__, FRAMES='tf5', MASKS='tmasks5';
const tl=gsap.timeline({paused:true});
gsap.set('#board',{xPercent:110});
const SFX=[]; window.SFX=SFX;
const $=s=>document.querySelector(s);
const sfx=(t,type,g=1)=>SFX.push({t:+Math.max(0,t).toFixed(3),type,g});
function pop(sel,t0,t1,o={}){
  const rot=o.rot??0;
  tl.fromTo(sel,{opacity:0,scale:0.3,rotation:rot-20,y:30},{opacity:1,scale:1,rotation:rot,y:0,duration:0.38,ease:'back.out(2.2)'},t0);
  if(o.float!==false && t1-t0>1.2) tl.to(sel,{y:-10,duration:0.8,ease:'sine.inOut',repeat:Math.max(1,Math.floor((t1-t0-0.4)/0.8)),yoyo:true},t0+0.38);
  if(t1!=null) tl.to(sel,{opacity:0,scale:0.4,duration:0.18,ease:'power2.in'},t1-0.18);
  if(o.snd!==false) sfx(t0,o.snd||'pop',o.g??0.9);
}
function kt(sel,t0,t1,o={}){
  const el=$(sel), words=el.querySelectorAll('.w');
  tl.set(el,{opacity:1},t0);
  tl.fromTo(words,{opacity:0,y:40,scale:1.25},{opacity:1,y:0,scale:1,duration:0.24,ease:'back.out(2)',stagger:0.07},t0);
  if(o.shake){ tl.fromTo(el,{x:-9},{x:9,duration:0.05,repeat:7,yoyo:true,ease:'none'},t0+0.3); tl.set(el,{x:0},t0+0.72); }
  if(t1!=null){ tl.to(el,{opacity:0,y:-18,duration:0.14,ease:'power2.in'},t1-0.14); tl.set(el,{y:0},t1); }
  if(o.snd!==false) sfx(t0,'swish',0.5);
}
function boardIn(t){ tl.fromTo('#board',{xPercent:110,skewX:-6},{xPercent:0,skewX:0,duration:0.32,ease:'power3.out'},t-0.05); sfx(t-0.08,'whoosh',1); }
function boardOut(t){ tl.to('#board',{xPercent:-110,skewX:6,duration:0.28,ease:'power3.in'},t-0.28); tl.set('#board',{xPercent:110,skewX:0},t); sfx(t-0.26,'whoosh',0.9); }
function scene(sel,t0,t1){ tl.set(sel,{opacity:1},t0); tl.set(sel,{opacity:0},t1); }
function ring(sel,t0,t1){ tl.fromTo(sel,{opacity:0,scale:0.8,rotation:-20},{opacity:1,scale:1,rotation:0,duration:0.5,ease:'power3.out'},t0); tl.to(sel,{opacity:0,duration:0.18},t1-0.18); }
function draw(sel,t,d=0.25){ tl.fromTo(sel,{opacity:1,clipPath:'inset(0 0 100% 0)'},{clipPath:'inset(0 0 0% 0)',duration:d,ease:'power2.out'},t); }

// ===== COLD OPEN: the money line
tl.set('#k0',{opacity:1},0); tl.set('#k0 .w',{opacity:1},0);
tl.fromTo('#k0 .key',{scale:1},{scale:1.12,duration:0.14,yoyo:true,repeat:1,ease:'sine.inOut'},0.12);
tl.to('#k0',{opacity:0,y:-18,duration:0.12},T.S1-0.12);
sfx(0.02,'thud',0.9);
tl.set('#b_money',{opacity:1,scale:1,rotation:6},0); tl.to('#b_money',{opacity:0,scale:0.4,duration:0.16},T.S1-0.16);
pop('#b_q0',0.35,T.S1,{rot:-6,float:false});
// ===== FRIEND
kt('#k1',T.S1+0.04,T.S1x,{shake:true}); sfx(T.S1,'thud',1);
pop('#b_vn',T.S1+0.1,T.S2a,{rot:-6}); pop('#b_ex',T.S1+0.5,T.S1x,{rot:8});
kt('#k2',T.S1x,T.S2a);
// ===== QUESTION
kt('#k3',T.S2a+0.04,T.S2b);
pop('#b_c1',T.S2a+0.1,T.S2b,{rot:-6}); pop('#b_c2',T.S2a+0.3,T.S2b,{rot:6,snd:false}); pop('#b_c4',T.S2a+0.5,T.S2b,{rot:5}); pop('#b_c3',T.S2a+0.7,T.S2b,{rot:-4,snd:false});
kt('#k4',T.S2b+0.04,T.BA);
pop('#b_shield',T.S2b+0.1,T.BA,{rot:-8}); pop('#b_q1',T.S2b+0.35,T.BA,{rot:10});
tl.to('#b_q1',{rotation:-6,duration:0.1,repeat:5,yoyo:true},T.S2b+0.9);
// ===== BOARD A: Samsung's official page — point 1 half shown, 2 and 3 locked
boardIn(T.BA); scene('#sA',T.BA-0.1,T.S3+0.02);
pop('#aTile',T.BA+0.15,null,{float:false});
tl.fromTo('#aNote',{opacity:0,x:40},{opacity:1,x:0,duration:0.3,ease:'power3.out'},T.BA+0.25);
tl.fromTo('#aTtl',{opacity:0,y:30},{opacity:1,y:0,duration:0.3,ease:'back.out(2)'},T.BAx-0.15);
ring('#n3',T.BAx-0.2,T.S3); draw('#aBr',T.BAx,0.22);
['#t1','#t2','#t3'].forEach((s,i)=>{ tl.fromTo(s,{opacity:0,y:70,scale:0.8},{opacity:1,y:0,scale:1,duration:0.32,ease:'back.out(2)'},T.BAx+0.12+i*0.14); sfx(T.BAx+0.12+i*0.14,'pop',0.9); });
tl.fromTo('#t1 .rv2',{opacity:0},{opacity:0.55,duration:0.3},T.BAx+0.5);
boardOut(T.S3);
// ===== DOES IT MATTER?
kt('#k5',T.S3+0.04,T.S3x); pop('#b_globe',T.S3+0.1,T.S3x,{rot:-6}); pop('#b_bulb',T.S3+0.3,T.S3x,{rot:6});
kt('#k6',T.S3x,T.BB); pop('#b_fac',T.S3x+0.05,T.BB,{rot:-6}); pop('#b_q2',T.S3x+0.2,T.BB,{rot:10});
// ===== BOARD B: 4 things (locked)
boardIn(T.BB); scene('#sB',T.BB-0.1,T.S4+0.02);
tl.fromTo('#bTtl',{opacity:0,y:30},{opacity:1,y:0,duration:0.32,ease:'power3.out'},T.BB+0.2);
tl.fromTo('#ph2',{opacity:0,x:-120,rotation:-6},{opacity:1,x:0,rotation:-3,duration:0.42,ease:'back.out(1.5)'},T.BB+0.4);
tl.fromTo('#ph1',{opacity:0,x:120,rotation:6},{opacity:1,x:0,rotation:3,duration:0.42,ease:'back.out(1.5)'},T.BB+0.55); sfx(T.BB+0.4,'whoosh',0.7);
pop('#vs',T.BB+1.1,null,{float:false,snd:'thud'});
ring('#n4',T.BBx-0.2,T.S4);
['.r1','.r2','.r3','.r4'].forEach((r,i)=>{ tl.fromTo('#sB '+r,{opacity:0,x:40},{opacity:1,x:0,duration:0.22,ease:'back.out(2)'},T.BBx+i*0.26); sfx(T.BBx+i*0.26,'tick',1); });
boardOut(T.S4);
// ===== CLIFFHANGER
kt('#k7',T.S4+0.04,T.S4x); pop('#b_scale',T.S4+0.08,T.CTA,{rot:-6});
tl.to('#b_scale',{rotation:6,duration:0.36,repeat:3,yoyo:true,ease:'sine.inOut'},T.S4+0.5);
kt('#k8',T.S4x,T.CTA); pop('#b_q3',T.S4x+0.05,T.CTA,{rot:10});
// freeze on the question: hit + red vignette, music drops out
tl.fromTo('#frz',{opacity:0},{opacity:1,duration:0.12},T.FRZ); tl.to('#frz',{opacity:0,duration:0.15},T.CTA);
tl.fromTo('#k8 .key',{scale:1},{scale:1.15,duration:0.12,yoyo:true,repeat:1},T.FRZ);
sfx(T.FRZ,'thud',1.1);
// progress bar
tl.fromTo('#prog i',{width:'0%'},{width:'100%',duration:T.CTA,ease:'none'},0);
tl.to('#prog',{opacity:0,duration:0.2},T.CTA-0.1);
// ===== PACK SHOT
const C=T.CTA;
tl.fromTo('#cta',{opacity:0,scale:1.08},{opacity:1,scale:1,duration:0.3,ease:'power3.out'},C-0.05); sfx(C-0.1,'whoosh',1);
tl.fromTo('#cta .lg',{opacity:0,y:-20},{opacity:1,y:0,duration:0.3},C+0.15);
tl.fromTo('#cta .l1',{opacity:0,y:30},{opacity:1,y:0,duration:0.3,ease:'power3.out'},C+0.3);
tl.fromTo('#cta .l2',{opacity:0,scale:1.4},{opacity:1,scale:1,duration:0.35,ease:'back.out(2)'},C+0.55); sfx(C+0.55,'pop',1);
tl.fromTo('#cta .ap',{opacity:0,y:120},{opacity:1,y:0,duration:0.42,ease:'back.out(1.6)'},C+0.95); sfx(C+0.95,'whoosh',0.7);
tl.fromTo('#cta .ap .pl',{scale:1},{scale:1.12,duration:0.3,repeat:7,yoyo:true,ease:'sine.inOut'},C+1.4);
tl.fromTo('#cta .bio',{opacity:0,y:30},{opacity:1,y:0,duration:0.3},C+1.6); sfx(C+1.6,'ding',0.8);
tl.set({},{},T.END);

// one fixed text position: centred, at lapel-mic height of the style sample frame
const TEXT_CY=1459;
function placeText(){ document.querySelectorAll('#fx .kt').forEach(el=>{ el.style.top=(TEXT_CY-el.offsetHeight/2)+'px'; }); }
// every jump cut gets a clear zoom change so it reads as intentional
function camScale(t){
  if(t>=T.FRZ) return 1.06+Math.min(1,(t-T.FRZ)/0.6)*0.08;
  let i=0; for(let k=0;k<PIECES.length;k++) if(t>=PIECES[k][3]-1e-6) i=k;
  const p=PIECES[i], k=Math.min(1,(t-p[3])/Math.max(0.4,p[2]-p[1]));
  return ((i%2)?1.12:1.0)+0.02*k;
}
function load(img,src){ return new Promise(r=>{ if(img.src.endsWith(src)) return r(); img.onload=()=>r(); img.onerror=()=>r(); img.src=src; }); }
const maskImg=new Image();
window.seekFrame=async function(i){
  const t=i/FPS; tl.seek(Math.max(t,0.001),false); placeText();
  $('#cam').style.transform=`scale(${camScale(t).toFixed(4)})`;
  const n=String(Math.min(i+1,VIDEO_FRAMES)).padStart(5,'0');
  const src=`${FRAMES}/${n}.jpg`, msrc=`${MASKS}/${n}.png`;
  await Promise.all([load($('#vid'),src),load($('#vid2'),src),load(maskImg,msrc)]);
  const a=$('#actor'); a.style.webkitMaskImage=a.style.maskImage=`url(${msrc})`;
  await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
  return t;
};
window.frontRects=function(i){
  const t=i/FPS; tl.seek(Math.max(t,0.001),false); placeText();
  const bx=gsap.getProperty('#board','xPercent'), ctaO=+getComputedStyle($('#cta')).opacity;
  const out=[], s=t>=T.FRZ?1.14:camScale(t);
  if(Math.abs(bx)<100 || ctaO>0.9) return {t,cover:true,s,r:out};
  document.querySelectorAll('#behind .t3').forEach(el=>{ if(+getComputedStyle(el).opacity>0.05){ const r=el.getBoundingClientRect(); out.push(['TILE:'+el.id,r.left,r.top,r.right,r.bottom]); } });
  document.querySelectorAll('#fx .kt .w').forEach(el=>{
    let o=1,e=el; while(e&&e!==document.body){ o*=+getComputedStyle(e).opacity; e=e.parentElement; }
    if(o>0.05){ const r=el.getBoundingClientRect(); out.push([el.closest('[id]').id,r.left,r.top,r.right,r.bottom]); }
  });
  return {t,cover:false,s,r:out};
};
window.DURATION=T.END; window.TOTAL_FRAMES=Math.round(T.END*FPS);
</script>
</body>
</html>
'''
import os
VF=len([f for f in os.listdir('tf5') if f.endswith('.jpg')]) if os.path.exists('tf5') else 721
js=js.replace('__T__',json.dumps(T)).replace('__P__',json.dumps(PC)).replace('__VF__',str(VF))
html=head.replace('<title>تیزر سامسونگ ویتنام — کاشی سه‌بعدی</title>','<title>تیزر سامسونگ ویتنام — ریتم تند</title>')+extra_css+'</style>\n</head>\n<body>\n'+body+js
if os.path.exists('teaser5_tiles.json'):
    for tid,(x,y,sz,up) in json.load(open('teaser5_tiles.json')).items():
        html,n=re.subn(r'<div class="t3" id="%s" style="[^"]*">'%tid,f'<div class="t3{" capup" if up else ""}" id="{tid}" style="left:{x}px;top:{y}px;width:{sz}px;height:{sz}px">',html); assert n==1,tid
open('teaser5.html','w').write(html); print('written',len(html),'VF',VF)
