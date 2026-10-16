# ruby.explains — Design System ("خط‌کش" / Ruler)

Instagram page that teaches marketing terms in friendly Persian, with the English term alongside. Audience: beginners & students, small-business owners, professional marketers, freelancers/content creators.

Sources: none supplied (no logo, codebase or Figma). Built from scratch from the "1a خط‌کش" direction in `ruby.explains Directions.dc.html`.

Surfaces: single-term post (1080×1350), reels cover (1080×1920), highlight covers.

## CONTENT FUNDAMENTALS
- Language: Persian, RTL. English term always shown next to the Persian term (mono, LTR). Digits are Persian (۱۲۳), except the post number `No.012` and the handle.
- Voice: friendly and spoken (محاوره‌ای). Address the reader as **تو**, never شما. Use spoken forms: «میشه»، «رو»، «میگه»، «بفرست».
- Definitions: 1–2 sentences, start with «یعنی…», tie to the reader's own page or shop. No textbook phrasing («عبارت است از…»).
- One idea per post. Formula/example box only when it adds something.
- Footer CTAs (rotate): «ذخیره‌ش کن، بعداً لازمت میشه» · «بفرست برای اون دوستت که کسب‌وکار داره» · «تو کامنت بگو تا حالا شنیده بودی؟»
- No emoji. No exclamation stacks. Casing for English terms: Title Case (Conversion Rate), acronyms upper (CTA, SEO, ROI).
- Category names: مبانی، دیجیتال، تبلیغات، برندینگ، سئو، آمار.

## VISUAL FOUNDATIONS
- Colors: cool paper `--paper #F5F6F8`, ink `--ink #15171C`, single accent yellow `--yellow #ECFF52` (sampled from the Month 1 recap carousel). Neutrals ink-2 (body), ink-3 (muted), line, grid. Approx. 75% paper / 20% ink / 5% yellow. Yellow appears once per post (the English term block or the reels circle) plus the tiny category square.
- Type: Vazirmatn (900 display, 700 strong, 500 meta, 400 body) + IBM Plex Mono (English terms, numbers, handle, labels). Display terms are huge (160px on 1080) with tight leading 1.05 and −2px tracking; body is 38px at leading 1.85.
- Backgrounds: flat paper with a 2px grid every 54px (1080÷20) on text posts and reels. Photo posts use plain paper. No gradients, no textures, no blur.
- Shapes: only circle, square, stacked bars (e.g. funnel). Flat fills. A big yellow circle bleeding off the left edge is the reels signature.
- Corners: sharp (0) everywhere. Circles only for highlight covers and shapes.
- Borders: 3px ink on boxes, 2px ink footer rule, 3px ink rule under photos. No shadows on content.
- Imagery: real photos, natural, slightly cool, people using phones/laptops, shops. Full-bleed top area on photo posts.
- Layout: 72px outer margin on posts; top row = category + number, bottom row = handle + CTA. Reels: all text inside the centred 4:5 crop (285–1635px from top).
- Transparency, blur, hover/press states: not used (static social media). Motion: see MOTION below.

## MOTION
Tokens: `tokens/motion.css`. Reference piece: `Motion Sample - Reels 29.dc.html` (+ `motion-reel.jsx`). Canvas 1080×1920, 30fps.
- Character: calm and precise, like a ruler. Things slide, wipe and grow in straight lines. Never bounce, overshoot, rotate, shake, blur, glow or go 3D.
- Easing: enter = `--ease-enter` (easeOutQuart), exit = `--ease-exit` (easeInCubic), move/wipe = `--ease-move` (easeInOutCubic). Linear only for ambient drift.
- Durations: 120ms captions · 240ms exits & chips · 400ms text and each half of a wipe · 700ms shapes · 800ms full section wipe. Stagger 80ms between lines, 150ms between list chips/steps.
- Enter = rise 48px + fade in. Exit = rise 24px upward + fade out (shorter and faster than enter). Exits run in reverse order of entrances.
- Reading direction: Persian text and the category chip reveal with a clip wipe from right to left; English terms, links and code wipe from left to right. Rules (footer line) draw from the right.
- Cover build (first 2.2s, order fixed): category shape → category chip → No. → English term box → Persian title → subtitle → footer rule → handle/day. The video's settled frame must equal the static cover, so the cover image and the first seconds match.
- Shapes per category: دیجیتال circle scales 0.6→1 from its centre · برندینگ square slides in from the left edge · فروش و رشد bars grow from the left, staggered 80ms. Between sections the shape may shrink/move to a corner (700ms, `--ease-move`), never disappears mid-video.
- Emphasis: a yellow marker grows left→right behind a key word or the English term (400ms). One emphasis on screen at a time. No color flashes, no scale pops beyond 1.02.
- Section change (hook → definition → when → steps → mistake → CTA): full-frame yellow panel sweeps right→left (400ms cover, cut content while covered, 400ms reveal). Inside a section, use rises only.
- Steps (قدم ۱/۲/۳) and list chips enter one by one with 150ms stagger; the step number is mono and appears 80ms before its text.
- Ambient: the background grid drifts down exactly one cell (54px) per loop, linear, so the loop is seamless. Something should always move: drift, or a 1.00→1.02 slow push on the title during holds.
- Holds: a title stays still ≥1.8s; body text gets ≥250ms per word before anything replaces it.
- Burned-in captions: Vazirmatn 700 52px, ink on a white box with 3px ink border, inside y 1380–1560, max ~28 characters per line, 120ms fade, no word-by-word bouncing.
- Loop/end: settle to the empty grid (same as frame 0). Keep all text inside the 4:5 crop (285–1635px) and away from the right 160px and bottom 320px where Instagram's buttons and caption sit.

## ICONOGRAPHY
- Lucide (CDN, `lucide-static@0.460.0`), 2px stroke, rendered single-color via CSS mask (`Icon` component). Ink on paper, or yellow on ink for highlight covers.
- Core set: bookmark, send, arrow-left (footer); book-open, smartphone, megaphone, gem, search, bar-chart-3 (highlights).
- No emoji, no unicode glyphs as icons, no hand-drawn SVG.
- Logo: none supplied — the handle `ruby.explains` is set in IBM Plex Mono 500 wherever a mark would go.

## Fonts
Vazirmatn and IBM Plex Mono load from Google Fonts (`tokens/fonts.css`). Yekan Bakh (mentioned as a reference) is commercial and not included; send the files to swap it in.

## Index
- `styles.css` — entry point (imports only) → `tokens/` colors, typography, spacing, effects, fonts
- `guidelines/` — foundation specimen cards (Colors, Type, Spacing, Brand)
- `components/primitives/` — Icon, CategoryTag, TermLabel, InfoBox, PostFooter, PhotoSlot
- `components/covers/` — HighlightCover
- `components/posts/` — TermCard, TermPhotoCard, ReelsCover
- `ui_kits/instagram/` — full-size templates: term-card, term-card-photo, reels-cover, highlight-covers
- `tokens/motion.css` + `guidelines/motion-*.html` — motion tokens and demos
- `Motion Sample - Reels 29.dc.html` — animated reference reel (UTM), built on `animations-v3.jsx` + `motion-reel.jsx`
- `Reels Covers - Month 2.dc.html` — 30 reels covers for No.029–058
- `ruby.explains Directions.dc.html` — original two-direction exploration

## Intentional additions
- `Icon` — wrapper so Lucide icons can take token colors.
