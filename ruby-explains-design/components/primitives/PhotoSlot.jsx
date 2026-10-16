import React from 'react';
export function PhotoSlot({ src, label = 'عکس واقعی', height = 580, alt = '' }) {
  const base = { height, flexShrink:0, borderBottom:'var(--stroke) solid var(--ink)', boxSizing:'border-box' };
  if (src) return <img src={src} alt={alt} style={{ ...base, width:'100%', objectFit:'cover', display:'block' }} />;
  return (
    <div style={{ ...base, display:'flex', alignItems:'center', justifyContent:'center', background:'var(--stripe-bg)' }}>
      <span style={{ fontFamily:'var(--font-mono)', fontSize:24, color:'var(--text-muted)', background:'var(--paper)', padding:'8px 20px' }}>{label}</span>
    </div>
  );
}
