// node snap.js t1 t2 ... -> snap_<t>.png at 1080 (scale 2 -> 2160)
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1080, height: 1080 }, deviceScaleFactor: +(process.env.DSF || 1) });
  const p = await ctx.newPage();
  await p.goto('file://' + __dirname + '/scene.html');
  await p.evaluate(() => document.fonts.ready);
  for (const t of process.argv.slice(2)) {
    await p.evaluate(t => setT(t), +t);
    await p.screenshot({ path: __dirname + `/snap_${t}.png` });
  }
  await b.close();
})();
