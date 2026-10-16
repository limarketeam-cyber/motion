import React from 'react';
const grid = { backgroundColor:'var(--paper)', backgroundImage:'var(--grid-bg)', backgroundSize:'var(--grid-cell) var(--grid-cell)' };
const Funnel = () => (
  <div style={{ display:'flex', flexDirection:'column', alignItems:'center', gap:16, marginTop:48 }}>
    {['100%','68%','36%'].map(w => <div key={w} style={{ width:w, height:56, background:'var(--ink)' }} />)}
  </div>
);
export function ReelsCover({ tag = 'ریلز · ۶۰ ثانیه', termEn, termFa, graphic = 'none', showSafeZone = false, handle = 'ruby.explains' }) {
  return (
    <div dir="rtl" style={{ width:1080, height:1920, position:'relative', overflow:'hidden', boxSizing:'border-box', fontFamily:'var(--font-fa)', color:'var(--ink)', ...grid }}>
      <div style={{ position:'absolute', width:940, height:940, borderRadius:'50%', background:'var(--lime)', top:170, left:-370 }} />
      {showSafeZone && <div style={{ position:'absolute', top:285, left:0, right:0, height:1350, borderTop:'2px dashed var(--ink-3)', borderBottom:'2px dashed var(--ink-3)' }} />}
      <div style={{ position:'absolute', top:285, left:0, right:0, height:1350, padding:'110px 84px', boxSizing:'border-box', display:'flex', flexDirection:'column', justifyContent:'center', gap:32 }}>
        <div style={{ display:'flex' }}><span style={{ fontFamily:'var(--font-mono)', fontSize:32, fontWeight:600, background:'var(--ink)', color:'var(--white)', padding:'10px 28px' }}>{tag}</span></div>
        <div dir="ltr" style={{ fontFamily:'var(--font-mono)', fontSize:56, fontWeight:500, textAlign:'right' }}>{termEn}</div>
        <div style={{ fontSize:192, fontWeight:900, lineHeight:1.05, letterSpacing:-3 }}>{termFa}</div>
        {graphic === 'funnel' && <Funnel />}
      </div>
      <div dir="ltr" style={{ position:'absolute', bottom:64, right:84, fontFamily:'var(--font-mono)', fontSize:32 }}>{handle}</div>
    </div>
  );
}
