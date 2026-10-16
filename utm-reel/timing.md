# UTM reel — timing map

Source: talking-head video, 720×1280, 107.15 s. Sentence starts were taken from
pause detection on the audio + Whisper (small) per chunk (`tools-asr-chunks.py`),
then matched to the script by hand. All times are seconds in the source.

| t (s) | spoken | motion |
|---|---|---|
| 0.5 | تا حالا دقت کردی آخر بعضی لینک‌ها… | title «این حروف عجیب ته لینک چیه؟» + browser bar, URL types |
| 4.1 | …یه علامت سؤال، کلی حرف و عدد عجیب | `?` marked yellow, query string types out |
| 7.1 / 8.7 | شاید به نظرت بی‌اهمیت بیاد / ولی همون چندتا کاراکتر… | whole query marked; title «چندتا کاراکتر، کلی اطلاعات» |
| 10.9 | اطلاعات مهمی درباره بازدیدکننده‌ها | 3 question chips |
| 14.0–14.8 | (pause) | yellow section wipe |
| 14.8 | بهشون می‌گن پارامترهای UTM | term card (Persian wipes R→L, English L→R) |
| 17.3 | اطلاعاتی که به انتهای لینک اضافه می‌شن… | utm_source / medium / campaign rows; source marked at 19.5 |
| 23.8 / 25.2 / 26.4 | استوری اینستاگرام / کمپین تبلیغاتی / کانال‌های دیگه | three source tiles |
| 27.8 | البته به شرطی که ابزار تحلیل… | info box + Google Analytics check (30.4) |
| 31.6–32.4 | (pause) | section wipe |
| 32.5–36.5 | فرض کن لینک فروشگاهت رو… بیو / استوری / تبلیغ | link pill forks into 3 tiles (34.2 / 35.4 / 36.5) |
| 37.7 | از کجا می‌فهمی کدومشون… | «؟» badges |
| 41.5 | اینجاست که UTM به کارت میاد | UTM marked, utm_content tags |
| 43.2–43.8 | (pause) | section wipe |
| 43.8 / 45.4 | ساختنش پیچیده نیست / فقط سه مرحله | title + 3-step bar |
| 46.8 | قدم اول… مثلاً استوری، بیو یا تبلیغات | step 1 card, chips at 50.6 / 51.6 / 52.2 |
| 53.4 | قدم دوم: Campaign URL Builder | builder form; fields type at 58.6 / 60.7 / 61.9; Content marked 65.9, story/bio 66.6–67.5 |
| 69.0 | قدم سوم: لینک‌های جدید رو بردار… | two tagged links, copy → check (71.2), destinations (72.6 / 73.0) |
| 75.0 | حالا می‌تونی توی گوگل آنالیتیکس… | example GA bars + counters (77.6) |
| 79.6–80.4 | (pause) | section wipe |
| 80.4 | اشتباه خیلی‌ها اینه… | «اشتباه رایج» + same link in 3 tiles (82.6+), «؟» at 86.3 |
| 88.8 | درحالی‌که بدون ردیابی درست… | traffic bar goes 72% «نامعلوم» (90.6) |
| 93.75–94.45 | (pause) | section wipe |
| 94.5 / 98.8 / 100.6 | CTA lines | checklist, ticks at 97.3 / 100.45 / 103.55 |
| 104.4 | (end) | save CTA + ruby.explains handle |

## Rebuild
```
./grade.sh source.mp4 graded.mp4
NODE_PATH=$(npm root -g) node render.mjs frames/ 30 4
ffmpeg -i graded.mp4 -framerate 30 -i frames/f%05d.png \
  -filter_complex "[0:v][1:v]overlay=eof_action=pass,format=yuv420p[v]" \
  -map "[v]" -map 0:a -c:v libx264 -preset slow -crf 20 -c:a aac -b:a 160k -shortest utm-reel.mp4
```
