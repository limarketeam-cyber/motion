import React from 'react';
const BASE='https://unpkg.com/lucide-static@0.460.0/icons/';
export function Icon({ name, size = 36, color = 'var(--ink)', style }) {
  const m = `url(${BASE}${name}.svg) center/contain no-repeat`;
  return <span aria-hidden="true" style={{ display:'inline-block', flexShrink:0, width:size, height:size, background:color, WebkitMask:m, mask:m, ...style }} />;
}
