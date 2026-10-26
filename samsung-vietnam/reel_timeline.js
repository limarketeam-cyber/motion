// Reel timeline — one paused GSAP timeline seeked per frame by render.mjs.  T = reel times of cue points.
const tl=gsap.timeline({paused:true});
gsap.set('#board',{xPercent:110});
const SFX=[]; window.SFX=SFX;
const $=s=>document.querySelector(s);
const sfx=(t,type,g=1)=>SFX.push({t:+Math.max(0,t).toFixed(3),type,g});
// brand entrance: panel in, accent line grows, icon path draws, caption tag slides in
function pop(sel,t0,t1,o={}){
  const el=$(sel);
  tl.fromTo(sel,{opacity:0,scale:0.86,y:24},{opacity:1,scale:1,y:0,duration:0.32,ease:'power3.out'},t0);
  const acc=el.querySelector('.acc'); if(acc) tl.fromTo(acc,{scaleY:0},{scaleY:1,duration:0.28,ease:'power2.out'},t0+0.12);
  const ps=el.querySelectorAll('[pathLength]'); if(ps.length) tl.fromTo(ps,{strokeDashoffset:1},{strokeDashoffset:0,duration:0.5,ease:'power2.inOut',stagger:0.06},t0+0.1);
  const cap=el.querySelector('.cap span'); if(cap) tl.fromTo(cap,{opacity:0,y:12},{opacity:1,y:0,duration:0.25,ease:'power3.out'},t0+0.2);
  if(t1!=null) tl.to(sel,{opacity:0,scale:0.92,duration:0.2,ease:'power2.in'},t1-0.2);
  if(o.snd!==false) sfx(t0,o.snd||'pop',o.g??0.9);
}
function kt(sel,t0,t1,o={}){
  const el=$(sel), words=el.querySelectorAll('.w');
  tl.set(el,{opacity:1},t0);
  if(o.instant) tl.set(words,{opacity:1},t0);
  else tl.fromTo(words,{opacity:0,y:40,scale:1.25},{opacity:1,y:0,scale:1,duration:0.26,ease:'back.out(2)',stagger:0.08},t0);
  if(o.shake){ tl.fromTo(el,{x:-9},{x:9,duration:0.05,repeat:7,yoyo:true,ease:'none'},t0+0.3); tl.set(el,{x:0},t0+0.72); }
  tl.to(el,{opacity:0,y:-18,duration:0.14,ease:'power2.in'},t1-0.14); tl.set(el,{y:0},t1);
  if(o.snd!==false) sfx(t0,'swish',0.5);
}
function fadeIn(sel,t,from={y:30},d=0.35){ tl.fromTo(sel,{opacity:0,...from},{opacity:1,x:0,y:0,duration:d,ease:'power3.out'},t); }
// brand transitions (pack T01/T02/T03): 3 stacked colour layers, the cut happens while fully covered
const WK=0.55, LAY=[[0,.65,1.3,.6],[.11,.65,1.2,.6],[.22,.65,1.1,.6]];
gsap.set('#wipe .wi i,#wipe .wo i',{xPercent:100}); gsap.set('#wipe .v i',{yPercent:-100});
function wipe(id,tc,k=WK,hold=0){
  const v=id==='v', P=v?'yPercent':'xPercent', a=v?-100:100, z=v?100:-100, t0=tc-1.0*k;
  document.querySelectorAll('#wipe .'+id+' i').forEach((el,i)=>{ const [es,ed,xs,xd]=LAY[i];
    tl.fromTo(el,{[P]:a},{[P]:0,duration:ed*k,ease:'power3.inOut',immediateRender:false},t0+es*k);
    tl.fromTo(el,{[P]:0},{[P]:z,duration:xd*k,ease:'power3.inOut',immediateRender:false},t0+xs*k+hold); });
  sfx(t0+0.1,'whoosh',0.9);
}
function boardIn(t,k){ wipe('wi',t,k); tl.set('#board',{xPercent:0},t); }
function boardOut(t,k=0.42){ wipe('wo',t,k); tl.set('#board',{xPercent:110},t); }
function scene(sel,t0,t1){ tl.set(sel,{opacity:1},t0); tl.set(sel,{opacity:0},t1); }
function ring(sel,t0,t1){ tl.fromTo(sel,{opacity:0,scale:0.85},{opacity:1,scale:1,duration:0.5,ease:'power3.out'},t0); tl.to(sel,{opacity:0,duration:0.2},t1-0.2); }
function draw(sel,t,d=0.35){ tl.fromTo(sel,{opacity:1,clipPath:'inset(0 0 100% 0)'},{clipPath:'inset(0 0 0% 0)',duration:d,ease:'power2.out'},t); }
function hl(sel,t,d=0.45){ tl.to(sel,{scaleX:1,duration:d,ease:'power2.out'},t); sfx(t,'marker',0.6); }
function mark(sel,t,d=0.9){ tl.to(sel,{backgroundSize:'100% 100%',duration:d,ease:'power1.inOut'},t); sfx(t,'marker',0.6); }

// ===== HOOK: country vs quality (first frame already carries the text)
kt('#k1',0,T.k2,{instant:true}); sfx(0.02,'thud',0.9);
pop('#t_vn',0.12,T.k2,{snd:false}); pop('#t_cn',0.35,T.k2); pop('#t_kr',0.6,T.k2,{snd:false}); pop('#t_in',0.85,T.k2);
kt('#k2',T.k2,T.call-0.24);
pop('#t_shield',T.k2+0.1,T.call-0.24); pop('#t_q1',T.k2+0.35,T.call-0.24);
// ===== STORY: the friend who wants a Vietnam A57 — a held brand wipe covers the source's zoom-blur (frames 131–144)
const ST0=PIECES[1][3], STC=ST0+0.07, STR=4.84;
wipe('v',STC,0.42,STR-STC-0.04); sfx(ST0,'thud',1);
kt('#k3',STR,T.k4); pop('#call',STR+0.05,T.k4,{snd:'ring',g:0.6});
kt('#k4',T.k4,T.k5); pop('#t_phone',T.k4+0.06,T.k5);
kt('#k5',T.k5,T.k6,{shake:true}); pop('#t_ex',T.k5+0.1,T.k6); sfx(T.k5+0.3,'thud',0.8);
kt('#k6',T.k6,T.k7); pop('#t_vn2',T.k6+0.04,T.k7,{snd:'tick'});
kt('#k7',T.k7,T.BA); pop('#t_mute',T.k7+0.06,T.BA);
// ===== BOARD A: Samsung's support page — 3 points
boardIn(T.BA); scene('#sA',T.BA,T.P1);
pop('#aTile',T.BA+0.15,null);
fadeIn('#aNote',T.BA+0.25,{x:40}); draw('#aArr',T.BA+0.45);
fadeIn('#aCard',T.BA+0.55,{y:90},0.45); sfx(T.BA+0.55,'whoosh',0.5);
hl('#aH1',T.BA+1.05); hl('#aH2',T.BA+1.35); fadeIn('#aFa',T.BA+1.55,{y:14});
fadeIn('#aTags',T.aThree,{y:30}); tl.fromTo('#aTags .ix',{scale:0.4},{scale:1,duration:0.3,ease:'back.out(2.4)',stagger:0.12},T.aThree); [0,.12,.24].forEach(d=>sfx(T.aThree+d,'tick',0.9));
// ===== BOARD B: point 1 — every factory, same quality
wipe('wi',T.P1,0.42); scene('#sB',T.P1,T.P2); ring('#n1',T.P1+0.1,T.P2);
fadeIn('#bHdr',T.P1+0.1,{x:50});
[1,2,3].forEach(i=>{ pop('#bF'+i,T.P1+0.3+i*0.18,null,{snd:i===1?'pop':false}); fadeIn('#bG'+i,T.P1+0.5+i*0.18,{y:16},0.25); });
pop('#bE1',T.P1eq,null,{snd:'ding'}); pop('#bE2',T.P1eq+0.15,null,{snd:false});
tl.fromTo('#bPill',{opacity:0,scale:0.7},{opacity:1,scale:1,duration:0.35,ease:'back.out(2)'},T.P1same); sfx(T.P1same,'ding',0.8);
boardOut(T.P2);
// ===== SPEAKER: point 2 — same technology everywhere
pop('#p2tag',T.P2+0.05,T.P3,{snd:'tick'});
kt('#k8',T.P2+0.05,T.P2b); kt('#k9',T.P2b,T.P3);
pop('#t_gear1',T.P2+0.25,T.P3); pop('#t_gear2',T.P2+0.45,T.P3,{snd:false}); pop('#t_fac',T.P2+1.0,T.P3);
tl.fromTo('#t_gear1 svg',{rotation:0},{rotation:120,duration:T.P3-T.P2,ease:'none'},T.P2+0.25);
tl.fromTo('#t_gear2 svg',{rotation:0},{rotation:-150,duration:T.P3-T.P2,ease:'none'},T.P2+0.45);
// ===== BOARD C: point 3 — quality control, then the official report
boardIn(T.P3); scene('#sC',T.P3,T.L); ring('#n3',T.P3+0.1,T.P3ev);
fadeIn('#cHdr',T.P3+0.15,{x:50});
pop('#cPhone',T.P3+0.3,null); fadeIn('#cMag',T.P3+0.5,{x:-60,y:-40},0.4);
tl.to('#cMag',{x:-90,y:-120,duration:0.8,ease:'sine.inOut',repeat:Math.max(1,Math.floor((T.P3ev-T.P3-1)/0.8)),yoyo:true},T.P3+0.9);
fadeIn('#cList',T.P3+0.6,{x:80});
[T.P3s1,T.P3s2,T.P3s3].forEach((t,i)=>{ tl.fromTo(`#cList .stp:nth-child(${i+1})`,{opacity:0,x:30},{opacity:1,x:0,duration:0.25,ease:'power3.out'},t); sfx(t,'tick',1); });
tl.fromTo('#cStamp',{opacity:0,scale:1.5},{opacity:1,scale:1,duration:0.26,ease:'power3.in'},T.P3std); sfx(T.P3std+0.24,'thud',1);
tl.to(['#cHdr','#cPhone','#cMag','#cList','#cStamp'],{opacity:0,y:-30,duration:0.22,ease:'power2.in'},T.P3ev-0.25);
pop('#cTile',T.P3ev,null); fadeIn('#cNote',T.P3ev+0.12,{x:40});
fadeIn('#cQ',T.P3ev+0.3,{y:90},0.45); sfx(T.P3ev+0.3,'whoosh',0.5); mark('#cQ mark',T.P3ev+0.85,1.0);
boardOut(T.L);
// ===== SPEAKER: the 4 things to compare
kt('#k10',T.L+0.04,T.r1); pop('#spec',T.L+0.15,T.D-0.05,{snd:'whoosh'});
[['#r1',T.r1],['#r2',T.r2],['#r3',T.r3],['#r4',T.r4]].forEach(([s,t])=>{ tl.fromTo(s,{opacity:0,x:40},{opacity:1,x:0,duration:0.26,ease:'back.out(2)'},t); sfx(t,'tick',1); });
kt('#k11',T.r4,T.D-0.05); pop('#t_shield2',T.r4+0.1,T.D-0.05,{snd:'ding',g:0.7});
// ===== BOARD D: one price on Hamahang (brand blue→red gradient)
boardIn(T.D,0.42); scene('#sD',T.D,T.D2); tl.set('#dbg',{opacity:1},T.D); tl.set('#dbg',{opacity:0},T.D2);
fadeIn('#dHead',T.D+0.12,{y:30}); fadeIn('#dCard',T.D+0.32,{y:80},0.4);
[1,2,3].forEach(i=>{ fadeIn('#dR'+i,T.D+0.55+i*0.18,{x:50},0.25); sfx(T.D+0.55+i*0.18,'tick',0.8); });
boardOut(T.D2);
// ===== SPEAKER: the price question
kt('#k12',T.D2,T.M); pop('#t_cart',T.D2+0.06,T.M);
kt('#k13',T.M,T.X1); pop('#t_price',T.M+0.06,T.X1,{snd:'cash'}); pop('#t_pay',T.M+0.3,T.X1,{snd:false});
kt('#k14',T.X1,T.X2); pop('#t_disc',T.X1+0.06,T.SPEECH);
kt('#k15',T.X2,T.SPEECH); pop('#t_q2',T.X2+0.06,T.SPEECH); pop('#t_q3',T.X2+0.3,T.SPEECH,{snd:false});
// ===== END CARD (brand only)
wipe('v',T.SPEECH,0.55); tl.set('#endc',{opacity:1},T.SPEECH);
tl.fromTo('#endc .lg',{opacity:0,y:30},{opacity:1,y:0,duration:0.45,ease:'power3.out'},T.SPEECH+0.3);
tl.fromTo('#endc .bar',{scaleY:0,transformOrigin:'50% 0'},{scaleY:1,duration:0.5,ease:'power2.out'},T.SPEECH+0.2);
tl.fromTo(['#endc .site','#endc .ig'],{opacity:0,y:20},{opacity:1,y:0,duration:0.35,stagger:0.15,ease:'power3.out'},T.SPEECH+0.6);
sfx(T.SPEECH+0.35,'ding',0.7);
tl.set({},{},T.END);

// chest text: one fixed spot — centred, on the lapel mic
const TEXT_CY=1150;
function placeText(){ document.querySelectorAll('#fx .kt').forEach(el=>{ el.style.top=(TEXT_CY-el.offsetHeight/2)+'px'; }); }
// every cut gets a clear zoom change (100% / 110%) plus a slow push
function camScale(t){
  if(t>=2.3 && t<PIECES[1][3]) return 1.10+0.02*(t-2.3)/2;     // hard cut colour→B&W inside the hook gets a zoom change
  let i=0; for(let k=0;k<PIECES.length;k++) if(t>=PIECES[k][3]-1e-6) i=k;
  const p=PIECES[i], k=Math.min(1,(t-p[3])/Math.max(0.4,p[2]-p[1]));
  const amp=p[0]==='L'?0.04:0.10;   // the 4-item card needs the right-hand column: gentler punch-in there
  return ((i%2)?1+amp:1.0)+0.02*k;
}
function load(img,src){ return new Promise(r=>{ if(img.src.endsWith(src)) return r(); img.onload=()=>r(); img.onerror=()=>r(); img.src=src; }); }
const maskImg=new Image();
window.seekFrame=async function(i){
  const t=i/FPS; tl.seek(Math.max(t,0.001),false); placeText();
  $('#cam').style.transform=`scale(${camScale(Math.min(t,SPEECH-0.01)).toFixed(4)})`;
  const n=String(Math.min(i+1,VIDEO_FRAMES)).padStart(5,'0');
  const src=`${FRAMES}/${n}.jpg`, msrc=`${MASKS}/${n}.png`;
  await Promise.all([load($('#vid'),src),load($('#vid2'),src),load(maskImg,msrc)]);
  const a=$('#actor'); a.style.webkitMaskImage=a.style.maskImage=`url(${msrc})`;
  await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
  return t;
};
window.frontRects=function(i){
  const t=i/FPS; tl.seek(Math.max(t,0.001),false); placeText();
  const bx=gsap.getProperty('#board','xPercent'), endO=+getComputedStyle($('#endc')).opacity;
  const out=[], s=camScale(Math.min(t,SPEECH-0.01));
  if(Math.abs(bx)<100 || endO>0.5) return {t,cover:true,s,r:out};
  document.querySelectorAll('#behind .t3,#behind .pc').forEach(el=>{ if(+getComputedStyle(el).opacity>0.05){ const r=el.getBoundingClientRect();
    out.push([(el.classList.contains('t3')?'TILE:':'CARD:')+el.id,r.left,r.top,r.right,r.bottom]); } });
  document.querySelectorAll('#fx .kt .w').forEach(el=>{
    let o=1,e=el; while(e&&e!==document.body){ o*=+getComputedStyle(e).opacity; e=e.parentElement; }
    if(o>0.05){ const r=el.getBoundingClientRect(); out.push([el.closest('[id]').id,r.left,r.top,r.right,r.bottom]); }
  });
  return {t,cover:false,s,r:out};
};
window.DURATION=END; window.TOTAL_FRAMES=Math.round(END*FPS);
