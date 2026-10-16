import React from 'react';
import { Icon } from './Icon.jsx';
export function PostFooter({ handle = 'ruby.explains', note, icon }) {
  return (
    <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', borderTop:'var(--stroke-hair) solid var(--ink)', paddingTop:28, fontFamily:'var(--font-fa)', fontSize:'var(--type-meta)', color:'var(--ink)' }}>
      <span dir="ltr" style={{ fontFamily:'var(--font-mono)' }}>{handle}</span>
      <div style={{ display:'flex', alignItems:'center', gap:16 }}>
        {note && <span style={{ fontWeight:500 }}>{note}</span>}
        {icon && <Icon name={icon} size={36} />}
      </div>
    </div>
  );
}
