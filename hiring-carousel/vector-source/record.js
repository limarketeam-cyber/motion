// node record.js out_base  -> out_base-2160.mp4 and out_base-1080.mp4
const { chromium } = require('playwright');
const { spawn } = require('child_process');
(async () => {
  const base = process.argv[2], FPS = 30, DUR = 6.0;
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1080, height: 1080 }, deviceScaleFactor: 2 });
  const p = await ctx.newPage();
  await p.goto('file://' + __dirname + '/scene.html');
  await p.evaluate(() => document.fonts.ready);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-',
    '-filter_complex', '[0:v]split=2[a][b];[a]scale=1080:1080:flags=lanczos[s]',
    '-map', '[s]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', base + '-1080.mp4',
    '-map', '[b]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', base + '-2160.mp4'],
    { stdio: ['pipe', 'inherit', 'inherit'] });
  const N = Math.round(FPS * DUR);
  for (let i = 0; i < N; i++) {
    await p.evaluate(t => setT(t), i / FPS);
    const buf = await p.screenshot({ type: 'png' });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await b.close();
})();
