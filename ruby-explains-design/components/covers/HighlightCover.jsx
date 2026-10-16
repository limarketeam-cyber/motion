import React from 'react';
import { Icon } from '../primitives/Icon.jsx';
export function HighlightCover({ icon, label, size = 240 }) {
  return (
    <div style={{ display:'flex', flexDirection:'column', alignItems:'center', gap:size*0.11, fontFamily:'var(--font-fa)', color:'var(--ink)' }}>
      <div style={{ width:size, height:size, borderRadius:'50%', background:'var(--ink)', display:'flex', alignItems:'center', justifyContent:'center' }}>
        <Icon name={icon} size={size*0.36} color="var(--lime)" />
      </div>
      {label && <span style={{ fontSize:size*0.16, fontWeight:500 }}>{label}</span>}
    </div>
  );
}
