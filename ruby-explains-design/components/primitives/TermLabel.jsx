import React from 'react';
export function TermLabel({ children, size = 'lg' }) {
  const fs = size === 'sm' ? 'var(--type-term-en-s)' : 'var(--type-term-en)';
  return (
    <div style={{ display:'flex' }}>
      <span dir="ltr" style={{ fontFamily:'var(--font-mono)', fontWeight:500, fontSize:fs, lineHeight:1.3, background:'var(--accent)', color:'var(--text-on-accent)', padding:'4px 20px' }}>{children}</span>
    </div>
  );
}
