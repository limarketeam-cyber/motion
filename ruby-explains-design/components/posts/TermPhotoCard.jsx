import React from 'react';
import { CategoryTag } from '../primitives/CategoryTag.jsx';
import { TermLabel } from '../primitives/TermLabel.jsx';
import { InfoBox } from '../primitives/InfoBox.jsx';
import { PostFooter } from '../primitives/PostFooter.jsx';
import { PhotoSlot } from '../primitives/PhotoSlot.jsx';
export function TermPhotoCard({ category, number, termEn, termFa, definition, photoSrc, photoLabel = 'عکس واقعی', note = 'بفرست برای اون دوستت که کسب‌وکار داره', icon = 'send' }) {
  return (
    <div dir="rtl" style={{ width:1080, height:1350, boxSizing:'border-box', display:'flex', flexDirection:'column', background:'var(--paper)', fontFamily:'var(--font-fa)', color:'var(--ink)' }}>
      <PhotoSlot src={photoSrc} label={photoLabel} />
      <div style={{ flex:1, padding:'64px var(--pad-post) var(--pad-post)', display:'flex', flexDirection:'column', gap:24 }}>
        <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', fontFamily:'var(--font-mono)', fontSize:'var(--type-label)' }}>
        <CategoryTag>{category}</CategoryTag><span dir="ltr">{number}</span>
      </div>
        <div style={{ marginTop:20 }}><TermLabel size="sm">{termEn}</TermLabel></div>
        <div style={{ fontSize:'var(--type-display-s)', fontWeight:900, lineHeight:1.1 }}>{termFa}</div>
        <div style={{ fontSize:36, lineHeight:1.85, color:'var(--text-body)', textWrap:'pretty' }}>{definition}</div>
        <div style={{ marginTop:'auto' }}><PostFooter note={note} icon={icon} /></div>
      </div>
    </div>
  );
}
