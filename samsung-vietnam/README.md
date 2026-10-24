# Samsung «Made in Vietnam» — 1-minute Reels edit

- `samsung-vietnam-1min.mp4` — final video (1080×1080, 30fps, 58.6s)
- `transcript-full.txt` — the full 2:22 original speech (read from burned-in subtitles)
- `edl.json` — kept parts of the original (source start/end → new time)
- `index.html` — all motion graphics (GSAP timeline, seeked frame by frame)

Rebuild: `subs.py` (subtitle timing) → `edl.py` (cut list) → `cut.py` (cut video) →
extract frames to `frames/` → serve this folder on :8765 → `node render.mjs out` →
`python3 audio.py speech.wav sfx.json mix.wav` → encode with ffmpeg.

3D icons: Microsoft Fluent Emoji (MIT). Flags: flag-icons (MIT). Font: Vazirmatn (OFL).
