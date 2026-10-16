import React from 'react';
export function InfoBox({ label = 'فرمول', children }) {
  return (
    <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', gap:24, background:'var(--surface-box)', border:'var(--stroke) solid var(--border-strong)', padding:'28px 36px', fontFamily:'var(--font-fa)', color:'var(--ink)' }}>
      <span style={{ fontFamily:'var(--font-mono)', fontSize:24, color:'var(--text-muted)' }}>{label}</span>
      <span style={{ fontSize:'var(--type-box)', fontWeight:700 }}>{children}</span>
    </div>
  );
}
