# Samsung «Made in Vietnam» — 1-minute Reels edit

- `samsung-vietnam-1min.mp4` — final video (1080×1920 vertical 9:16, 30fps, 60s incl. 1.4s brand end card)
- `transcript-full.txt` — the full 2:22 original speech (read from burned-in subtitles)
- `edl.json` — kept parts of the original (source start/end → new time)
- `index.html` — all motion graphics (GSAP timeline, seeked frame by frame)

Rebuild: `subs.py` (subtitle timing) → `edl.py` (cut list) → `cut.py` (cut video) →
extract frames to `frames/` at 1080x1920 (the source is 1080x1080 with SAR 9:16, so scale to 1080:1920) → serve this folder on :8765 → `node render.mjs out` →
`python3 audio.py speech.wav sfx.json mix.wav` → encode with ffmpeg.

3D icons: Microsoft Fluent Emoji (MIT). Flags: flag-icons (MIT). Font: IBM Plex Sans Arabic (OFL). Logo: Hamahang (extracted from their own post).

## Instagram teaser (for the full 2-min video on Aparat)
- `samsung-vietnam-teaser.mp4` — 36.5s, 1080×1920, no subtitles
- `teaser.html` + `teaser_edl.json` — teaser motion and cut list
- Burned-in subtitles are removed by a 1.32× zoom anchored at the top of the frame
  (`scale=1426:2534,crop=1080:1920:173:0`), so the head keeps its headroom.
- Safe zone used for all text: x 64–1016, y 250–1500.
- Render: `PAGE=teaser.html node render.mjs out` (frames in `tframes/`).
