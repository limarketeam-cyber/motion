import React from 'react';
export function CategoryTag({ children }) {
  return (
    <div style={{ display:'flex', alignItems:'center', gap:16, fontFamily:'var(--font-fa)', fontWeight:700, fontSize:'var(--type-label)', color:'var(--ink)' }}>
      <span style={{ width:20, height:20, background:'var(--lime)', border:'3px solid var(--ink)' }} />
      <span>{children}</span>
    </div>
  );
}
