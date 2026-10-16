import React from 'react';
import { CategoryTag } from '../primitives/CategoryTag.jsx';
import { TermLabel } from '../primitives/TermLabel.jsx';
import { InfoBox } from '../primitives/InfoBox.jsx';
import { PostFooter } from '../primitives/PostFooter.jsx';
import { PhotoSlot } from '../primitives/PhotoSlot.jsx';
const grid = { backgroundColor:'var(--paper)', backgroundImage:'var(--grid-bg)', backgroundSize:'var(--grid-cell) var(--grid-cell)' };
export function TermCard({ category, number, termEn, termFa, definition, boxLabel = 'فرمول', boxValue, note = 'ذخیره‌ش کن، بعداً لازمت میشه', icon = 'bookmark' }) {
  return (
    <div dir="rtl" style={{ width:1080, height:1350, boxSizing:'border-box', padding:'var(--pad-post)', display:'flex', flexDirection:'column', fontFamily:'var(--font-fa)', color:'var(--ink)', ...grid }}>
      <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', fontFamily:'var(--font-mono)', fontSize:'var(--type-label)' }}>
        <CategoryTag>{category}</CategoryTag><span dir="ltr">{number}</span>
      </div>
      <div style={{ flex:1, display:'flex', flexDirection:'column', justifyContent:'center', gap:28 }}>
        <TermLabel>{termEn}</TermLabel>
        <div style={{ fontSize:'var(--type-display)', fontWeight:900, lineHeight:1.05, letterSpacing:-2 }}>{termFa}</div>
        <div style={{ fontSize:'var(--type-body)', lineHeight:1.85, color:'var(--text-body)', maxWidth:880, textWrap:'pretty' }}>{definition}</div>
      </div>
      {boxValue && <div style={{ marginBottom:48 }}><InfoBox label={boxLabel}>{boxValue}</InfoBox></div>}
      <PostFooter note={note} icon={icon} />
    </div>
  );
}
