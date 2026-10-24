// Render index.html frame by frame (needs a local http server on :8765).
// usage: node render.mjs <outDir> [frame,frame,...]  (no list = all frames, 3 workers)
import { createRequire } from 'module';
const { chromium } = createRequire(import.meta.url)('playwright');
import fs from 'fs';
const out = process.argv[2] || 'out';
const only = process.argv[3] ? process.argv[3].split(',').map(Number) : null;
fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch();
async function worker(list) {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('http://127.0.0.1:8765/index.html');
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  for (const i of list) {
    await page.evaluate(i => window.seekFrame(i), i);
    await page.screenshot({ path: `${out}/${String(i + 1).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 93 });
  }
  if (!only) fs.writeFileSync(`sfx.json`, JSON.stringify(await page.evaluate(() => window.SFX)));
  await page.close();
}
let frames = only;
if (!frames) { const n = 1800; frames = [...Array(n).keys()]; }  // 60s incl. 1.4s end card
const W = only ? 1 : 3, chunk = Math.ceil(frames.length / W);
await Promise.all([...Array(W).keys()].map(w => worker(frames.slice(w * chunk, (w + 1) * chunk))));
await browser.close();
console.log('done', frames.length);
