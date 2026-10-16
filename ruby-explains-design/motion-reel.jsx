const { CompositionStage, useComposition, Shot, Easing, clamp, useTweaks, TweaksPanel, TweakSection, TweakToggle } = window;

const C = { paper:'#F5F6F8', ink:'#15171C', ink2:'#3A3E48', ink3:'#6B7080', grid:'#E4E6EA', lime:'#ECFF52', white:'#FFFFFF' };
const FA = "'Vazirmatn', sans-serif", MONO = "'IBM Plex Mono', monospace";
const DUR = { s:0.24, m:0.4, l:0.7 };
const prog = (T, at, d) => clamp((T - at) / d, 0, 1);

// The only three motion helpers (tokens/motion.css)
const MOTION = {
  rise(T, inAt, outAt = Infinity) {
    const i = Easing.easeOutQuart(prog(T, inAt, DUR.m));
    const o = Easing.easeInCubic(prog(T, outAt, DUR.s));
    return { opacity: i * (1 - o), transform: `translateY(${(1 - i) * 48 - o * 24}px)` };
  },
  wipe(T, inAt, outAt = Infinity, dir = 'rtl') {
    const i = Easing.easeInOutCubic(prog(T, inAt, DUR.m));
    const o = Easing.easeInCubic(prog(T, outAt, DUR.s));
    const h = (1 - i) * 100;
    return { clipPath: dir === 'rtl' ? `inset(0 0 0 ${h}%)` : `inset(0 ${h}% 0 0)`, opacity: 1 - o };
  },
  grow(T, inAt, d = DUR.l, outAt = Infinity, outD = DUR.s) {
    return Easing.easeOutQuart(prog(T, inAt, d)) * (1 - Easing.easeInCubic(prog(T, outAt, outD)));
  }
};

function Chip({ style, children }) {
  return <div style={{ position:'absolute', top:0, right:0, fontFamily:FA, fontSize:34, fontWeight:700, background:C.ink, color:C.white, padding:'12px 28px', whiteSpace:'nowrap', ...style }}>{children}</div>;
}

function Panel({ T, at }) {
  const a = MOTION.grow(T, at, DUR.m), b = MOTION.grow(T, at + DUR.m, DUR.m);
  const left = (1 - a) * 1080, right = (1 - b) * 1080;
  return <div style={{ position:'absolute', top:0, bottom:0, left, width:Math.max(0, right - left), background:C.lime }} />;
}

function Piece({ safe }) {
  const { T, CUES, authoredTotal } = useComposition();
  const W1 = CUES.Wipe1, W2 = CUES.Wipe2, O = CUES.Outro, H = CUES.Hook, D = CUES.Definition;
  const cut1 = W1 + DUR.m, cut2 = W2 + DUR.m;

  const k = MOTION.grow(T, 0.1, DUR.l, O + 0.5, 0.4);
  const mv = MOTION.grow(T, W1 + 0.1, DUR.l);
  const size = 940 + (420 - 940) * mv, cl = -370 + (-150 + 370) * mv, ct = 170 + (150 - 170) * mv;
  const fill = MOTION.grow(T, CUES.Hold + 0.2, DUR.m);
  const push = 1 + 0.02 * MOTION.grow(T, CUES.Hold, 1.8);
  const mark = MOTION.grow(T, H + 1.3, DUR.m);
  const drift = (T / authoredTotal) * 54;

  return (
    <div dir="rtl" data-screen-label={`t=${Math.floor(T)}s`} style={{ position:'absolute', inset:0, overflow:'hidden', fontFamily:FA, color:C.ink, backgroundColor:C.paper,
      backgroundImage:`linear-gradient(${C.grid} 2px,transparent 2px),linear-gradient(90deg,${C.grid} 2px,transparent 2px)`, backgroundSize:'54px 54px', backgroundPosition:`0 ${drift}px` }}>

      <div style={{ position:'absolute', width:size, height:size, left:cl, top:ct, borderRadius:'50%', background:C.lime, opacity:k, transform:`scale(${0.6 + 0.4 * k})` }} />

      {safe && <div style={{ position:'absolute', top:285, left:0, right:0, height:1350, borderTop:`3px dashed ${C.ink3}`, borderBottom:`3px dashed ${C.ink3}` }} />}

      <div style={{ position:'absolute', top:285, left:0, right:0, height:1350, padding:'96px 84px', boxSizing:'border-box', display:'flex', flexDirection:'column' }}>
        <div style={{ position:'relative', height:70 }}>
          <Shot from={0} to={cut1}><Chip style={MOTION.wipe(T, 0.45)}>ریلز · دیجیتال مارکتینگ</Chip></Shot>
          <Shot from={cut1} to={cut2}><Chip style={MOTION.wipe(T, cut1 + 0.1)}>۱ · قلاب</Chip></Shot>
          <Shot from={cut2} to={authoredTotal + 1}><Chip style={MOTION.wipe(T, cut2 + 0.1, O + 0.2)}>۲ · تعریف</Chip></Shot>
          <div dir="ltr" style={{ position:'absolute', top:10, left:0, fontFamily:MONO, fontSize:34, fontWeight:500, ...MOTION.rise(T, 0.5, O + 0.25) }}>No.029</div>
        </div>

        <div style={{ flex:1, position:'relative' }}>
          <Shot from={0} to={cut1}>
            <div style={{ position:'absolute', inset:0, display:'flex', flexDirection:'column', justifyContent:'center', gap:36 }}>
              <div style={{ display:'flex', ...MOTION.wipe(T, 0.7, Infinity, 'ltr') }}>
                <div dir="ltr" style={{ position:'relative', fontFamily:MONO, fontSize:48, fontWeight:500, lineHeight:1.3, background:C.white, border:`3px solid ${C.ink}`, padding:'6px 22px' }}>
                  <div style={{ position:'absolute', inset:0, background:C.lime, transformOrigin:'left', transform:`scaleX(${fill})` }} />
                  <span style={{ position:'relative' }}>UTM Parameters</span>
                </div>
              </div>
              <div style={{ ...MOTION.rise(T, 0.9) }}>
                <div style={{ fontSize:168, fontWeight:900, lineHeight:1.12, letterSpacing:-2, transformOrigin:'right center', transform:`scale(${push})` }}>پارامترهای UTM</div>
              </div>
              <div style={{ fontSize:56, fontWeight:700, color:C.ink2, ...MOTION.rise(T, 1.2) }}>ردیابی دقیق منبع فروش</div>
            </div>
          </Shot>

          <Shot from={cut1} to={cut2}>
            <div style={{ position:'absolute', inset:0, display:'flex', flexDirection:'column', justifyContent:'center', gap:48 }}>
              <div style={{ fontSize:72, fontWeight:800, lineHeight:1.5, textWrap:'balance', ...MOTION.rise(T, H + 0.1) }}>اون علامت سوال و حروف عجیب‌غریبی که بعضی وقتا آخر یه لینک می‌بینی رو یادته؟</div>
              <div dir="ltr" style={{ display:'flex', fontFamily:MONO, fontSize:40, fontWeight:500, background:C.white, border:`3px solid ${C.ink}`, padding:'22px 28px', ...MOTION.rise(T, H + 0.7) }}>
                <span>shop.ir/product</span>
                <span style={{ position:'relative' }}>
                  <span style={{ position:'absolute', inset:'-4px -2px', background:C.lime, transformOrigin:'left', transform:`scaleX(${mark})` }} />
                  <span style={{ position:'relative' }}>?utm_source=story</span>
                </span>
              </div>
              <div style={{ fontSize:46, lineHeight:1.75, color:C.ink2, textWrap:'pretty', ...MOTION.rise(T, H + 1.9) }}>همون چیزی که اکثرا نادیده‌ش می‌گیرن، دقیقاً بهت می‌گه مشتریت از کجا اومده.</div>
            </div>
          </Shot>

          <Shot from={cut2} to={authoredTotal + 1}>
            <div style={{ position:'absolute', inset:0, display:'flex', flexDirection:'column', justifyContent:'center', gap:36 }}>
              <div style={{ display:'flex', ...MOTION.wipe(T, D + 0.1, O + 0.18, 'ltr') }}>
                <div dir="ltr" style={{ fontFamily:MONO, fontSize:48, fontWeight:500, lineHeight:1.3, background:C.lime, padding:'6px 22px' }}>UTM Parameters</div>
              </div>
              <div style={{ fontSize:120, fontWeight:900, lineHeight:1.12, letterSpacing:-2, ...MOTION.rise(T, D + 0.25, O + 0.12) }}>پارامتر UTM</div>
              <div style={{ fontSize:46, lineHeight:1.75, color:C.ink2, textWrap:'pretty', ...MOTION.rise(T, D + 0.6, O + 0.06) }}>چند کلمه‌ی کوچیک که به آخر لینک اضافه می‌شه تا وقتی یکی روش کلیک کرد، بشه فهمید این کلیک از کجا اومده:</div>
              <div style={{ display:'flex', gap:20 }}>
                {['استوری', 'بیو', 'تبلیغ'].map((t, i) => (
                  <div key={t} style={{ fontSize:44, fontWeight:700, background:C.ink, color:C.white, padding:'14px 32px', ...MOTION.rise(T, D + 1.4 + i * 0.15, O) }}>{t}</div>
                ))}
              </div>
            </div>
          </Shot>
        </div>

        <div style={{ position:'relative', paddingTop:32 }}>
          <div style={{ position:'absolute', top:0, left:0, right:0, height:3, background:C.ink, transformOrigin:'right', transform:`scaleX(${MOTION.grow(T, 1.4, 0.5, O + 0.35)})` }} />
          <div style={{ display:'flex', justifyContent:'space-between', fontSize:34 }}>
            <div style={{ fontWeight:500, ...MOTION.rise(T, 1.7, O + 0.3) }}>دوشنبه</div>
            <div dir="ltr" style={{ fontFamily:MONO, ...MOTION.rise(T, 1.6, O + 0.3) }}>ruby.explains</div>
          </div>
        </div>
      </div>

      <Panel T={T} at={W1} />
      <Panel T={T} at={W2} />
    </div>
  );
}

function MotionReel() {
  const [t, setTweak] = useTweaks(window.TWEAK_DEFAULTS);
  return (
    <>
      <CompositionStage width={1080} height={1920} scenes={window.OM_SCENES} playback={window.OM_PLAYBACK} bg={C.paper}>
        <Piece safe={t.safeZone} />
      </CompositionStage>
      <TweaksPanel>
        <TweakSection label="Motion" />
        <TweakToggle label="Motion editor" value={t.motionEditor} onChange={v => setTweak('motionEditor', v)} />
        <TweakToggle label="خط‌چین محدوده‌ی گرید" value={t.safeZone} onChange={v => setTweak('safeZone', v)} />
      </TweaksPanel>
    </>
  );
}

window.MotionReel = MotionReel;
