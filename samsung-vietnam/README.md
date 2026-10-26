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

### Teaser v2 (current `samsung-vietnam-teaser.mp4`)
- `teaser2.html` — overlays on the speaker use only white + red (flags excepted);
  full-graphic boards use the Hamahang white→red post gradient with grain and black text.
- Icons near the head sit **behind** the speaker (person cutout masks from rembg
  `u2net_human_seg`, smoothed) with a light depth-of-field blur; masks go in `tmasks/`.
- Chest text is positioned per line from the detected chin (+30px); an automatic
  check over all frames found 0 text/face overlaps.
- Glitch frames from the source's own transitions (colour flashes before B&W shots)
  are replaced with the nearest clean frame; the low opening shot is reframed
  (1.4× zoom, lifted 160px) so the text stays in the sweet spot below the chin.
- Render: `PAGE=teaser2.html node render.mjs out`.

### Teaser v3 — 3D tiles (current `samsung-vietnam-teaser.mp4`)
- Style chosen from `style-options.png` (option 4, 3D tiles); built in `teaser3.html`.
- Speaker shots: white + red only (flags excepted). Boards and pack shot: 60% white,
  30% black, 10% blue, on the Hamahang white→red gradient.
- Tiles sit beside the jaw (fully readable, only the edge tucks behind the speaker).
- Text slabs track the lapel mic (`teaser_mic.js`, smoothed per shot) to cover it.
- Editing fixes: orange flash frames removed, 3-frame soft blend on mid-sentence cuts,
  camera punch-in changes only between sentences.

### Teaser v4 (37.9s)
- `teaser4.html` + `teaser_edl2.json`: natural pauses kept inside sentences (no
  mid-sentence jump cuts); the source's orange light-leak frames removed.
- Chest text: one fixed position for the whole video — centred, at lapel-mic height;
  style = white words + key word in a red pill.
- Tiles sit behind the speaker; each placed so its icon and caption are never covered
  by head/body in any frame it is shown (only ~15% of the tile edge tucks behind).
- SFX cues are remapped to the new cut (`teaser4_sfx_mapped.json`).

### Teaser v5 — tight rhythm (`samsung-vietnam-teaser.mp4`, 28.2s)
- `teaser5_cut.py` → `teaser5_edl.json` (cold open on the money line, pauses removed,
  flash frames auto-replaced, 0.6s freeze on the cliffhanger).
- `teaser5_build.py` → `teaser5.html` (all timings derived from the cut);
  tile positions in `teaser5_tiles.json` (icon + caption never covered by the speaker,
  inside the safe zone at the 112% punch-in).
- `teaser5_audio.py`: speech + SFX + 112 bpm synthesized beat, ducked under the voice,
  cut on the freeze, back on the pack shot.
- Jump cuts alternate 100% / 112% zoom; thin progress bar at the top; board A shows
  point 1 half-revealed, points 2 and 3 locked.

### Teaser v6 — v4 in the Hamahang visual identity (`samsung-vietnam-teaser-v6.mp4`, 37.9s)
- Same cut, timing and audio as v4; `teaser6_build.py` → `teaser6.html` (built from `teaser4.html`).
- Assets from the Hamahang pack in `assets/brand/`: IBM Plex Sans Arabic / IBM Plex Sans
  Regular + Bold, official line icons, native-ratio flags, revised logo.
- Speaker shots: flat white plates (no shadow, volume or gradient) with a red line icon
  that draws on, a red accent bar, red caption tags; still placed behind the speaker.
- Boards and pack shot: brand light gradient, white plates with a thin outline and a blue
  accent bar, blue index tags, ink #262426 text, flat phones and VS tile.
- Transitions: brand layer wipes (T02 diagonal into boards, T01 out, T03 vertical into
  the pack shot), same layer timing as the pack JSON at ~0.5x length.
