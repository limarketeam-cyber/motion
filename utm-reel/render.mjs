// Renders overlay.html frame-by-frame to transparent PNGs.
// usage: node render.mjs <outDir> [fps=30] [workers=4] [onlyTimes comma list]
import { createRequire } from 'module';
import { mkdirSync, existsSync, readFileSync } from 'fs';
import http from 'http';
import { fileURLToPath } from 'url';
import path from 'path';
const { chromium } = createRequire(import.meta.url)('playwright'); // resolved via NODE_PATH (global install)
const here = path.dirname(fileURLToPath(import.meta.url));
const [outDir, fpsArg = '30', wArg = '4', only] = process.argv.slice(2);
const fps = +fpsArg, workers = +wArg;
mkdirSync(outDir, { recursive: true });
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || undefined });
// serve over http: CSS mask images (icons) are CORS-fetched and fail on file://
const types = { '.html': 'text/html', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.woff2': 'font/woff2' };
const server = http.createServer((req, res) => {
  const f = path.join(here, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  if (!f.startsWith(here) || !existsSync(f)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': types[path.extname(f)] || 'application/octet-stream' });
  res.end(readFileSync(f));
}).listen(0);
const url = `http://127.0.0.1:${server.address().port}/overlay.html?render=1`;
async function open() {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto(url); await page.waitForFunction(() => window.__ready === true);
  return page;
}
const first = await open();
const total = await first.evaluate(() => window.__total);
const jobs = only ? only.split(',').map(t => ({ t: +t, name: `t${t}.png` }))
  : Array.from({ length: Math.round(total * fps) }, (_, f) => ({ t: f / fps, name: `f${String(f).padStart(5, '0')}.png` }));
const pages = [first, ...await Promise.all(Array.from({ length: Math.max(0, Math.min(workers, jobs.length) - 1) }, open))];
let done = 0;
await Promise.all(pages.map(async page => {
  // each worker takes a contiguous range so its timeline only moves forward
  const per = Math.ceil(jobs.length / pages.length), k = pages.indexOf(page);
  for (const j of jobs.slice(k * per, (k + 1) * per)) {
    await page.evaluate(t => window.__seek(t), j.t);
    await page.screenshot({ path: path.join(outDir, j.name), omitBackground: true });
    if (++done % 300 === 0) console.log(`${done}/${jobs.length}`);
  }
}));
await browser.close(); server.close();
console.log('done', jobs.length);
