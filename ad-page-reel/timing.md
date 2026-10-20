# Ad-page reel — timing map

Source: talking-head video, 720×1280, 75.4 s (speech ends 73.35 s; output cut at 74.6 s).
Sentence starts from pause detection + Whisper per chunk, matched to the script by hand.

| t (s) | spoken | motion |
|---|---|---|
| 0.9 | دو تا کسب‌وکار توی یه پیج تبلیغ می‌کنن | «یه پیج، دو تا نتیجه» + page pill forking to two business tiles |
| 3.6 / 4.85 | یکی از نتیجه راضیه / اون یکی نه | «راضی» / «ناراضی» result badges |
| 5.9 | چرا یه پیج می‌تونه… | «چرا یکی جواب گرفت، یکی نه؟» |
| 9.8–10.3 | (pause) | yellow section wipe |
| 10.3 | چون انتخاب پیج… فقط به تعداد فالوورهاش | criteria card, follower row; strike-through at 13.6 |
| 15.15 / 16.3 | هدف تبلیغ / مخاطب اون پیج | + rows |
| 18.0 | مثلاً اگه می‌خوای… شناخته بشه | goal column «شناخته‌شدن», Reach counter 20.6, «مرتبط» marked 22.7 |
| 24.5 | اما اگه هدفت فروشه… | goal column «فروش», Purchases counter 26.45, «خرید» marked 28.3 |
| 29.9–30.4 | (pause) | section wipe |
| 30.4 | پس قبل از انتخاب پیج، سه تا کار | title, then 3-step bar (32.55) |
| 33.9 | اول: هدفت رو مشخص کن | step 1; chips at 35.9 / 36.35 / 37.7 |
| 38.95 | دوم: از ادمین آمار… بخواه | step 2; asks at 40.35 / 41.5; audience-overlap circles at 43.3 |
| 45.7 | قدم سوم… | step 3; engagement / past results at 48.05 / 49.1; low-budget test at 50.85 |
| 53.85 | اشتباه خیلی‌ها اینه که… | «اشتباه رایج» + comparison table; «هدف تو؟» row at 58.85 |
| 61.2–62.0 | (pause) | section wipe |
| 62.0 | قبل از تبلیغ بعدیت، سه تا پیج… | three page tiles (63.7), criteria ticks (65.1) |
| 66.8 | پیج مناسب لزوماً پرفالوورترین نیست | follower counts (68.6) |
| 71.0 | پیجیه که با هدف تبلیغت هماهنگ باشه | page 2 picked «هماهنگ با هدفت», others dimmed |
| 73.6 | (end) | save CTA + ruby.explains |

## Face-safe layout
Titles: top band, 282–370 px. Cards: bottom-anchored at 1620 px, ≤ 400 px tall.
`check-bands.py` reports how far each band reaches; `check-face.py` runs OpenCV face
detection on the graded footage and fails any frame where overlay pixels touch the face
(only the full-frame section wipes are allowed).

## Rebuild
```
./grade.sh source.mp4 graded.mp4
NODE_PATH=$(npm root -g) node render.mjs frames/ 30 4
python3 check-bands.py frames/ && python3 check-face.py graded.mp4 frames/
ffmpeg -i graded.mp4 -framerate 30 -i frames/f%05d.png \
  -filter_complex "[0:v][1:v]overlay=eof_action=pass,format=yuv420p[v]" \
  -map "[v]" -map 0:a -t 74.6 -af afade=t=out:st=74.3:d=0.3 \
  -c:v libx264 -preset slow -crf 20 -c:a aac -b:a 160k ad-page-reel.mp4
```
