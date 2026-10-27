// Renders cover.html to cover.png (1080x1920) and cover-grid.png (the 4:5 grid crop, 1080x1350).
import { createRequire } from 'module';
import { fileURLToPath } from 'url';
import path from 'path';
const { chromium } = createRequire(import.meta.url)('playwright');
const here = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
await page.goto('file://' + path.join(here, 'cover.html'));
await page.evaluate(() => document.fonts.ready);
await page.screenshot({ path: path.join(here, 'cover.png') });
await page.screenshot({ path: path.join(here, 'cover-grid.png'), clip: { x: 0, y: 285, width: 1080, height: 1350 } });
await browser.close();
