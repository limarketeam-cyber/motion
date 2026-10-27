#!/usr/bin/env bash
# Relight + reframe the second take (720x1280 @60fps) to 1080x1920 30fps.
#  - camera was already near eye level: no keystone; 1.08x zoom with the crop pushed fully
#    down (7.4% off the top) so the face sits as high as the source allows and the
#    downlight hotspot leaves the frame
#  - white balance: wall had a green cast → pull green, nudge blue
#  - lift mids/shadows + face/eye fill through soft masks (fillmask.png, eyemask.png)
# usage: ./grade.sh source.mp4 graded.mp4
set -e
cd "$(dirname "$0")"
IN="$1"; OUT="$2"
Z=1.08; Y0=0.074
RF="crop=iw/$Z:ih/$Z:(iw-iw/$Z)/2:ih*$Y0"
WB="colorchannelmixer=rr=1.0:gg=0.955:bb=1.02"
G="$RF,scale=1080:1920:flags=lanczos,hqdn3d=1.5:1.5:4:4,$WB,curves=master='0/0.02 0.25/0.30 0.5/0.57 0.75/0.80 1/0.96',eq=saturation=1.05"
F="[0:v]$G,split=3[a][b][c];[b]curves=master='0/0 0.3/0.42 0.6/0.72 1/1'[br];[1:v]format=gray,scale=1080:1920[m];[br][m]alphamerge[bm];[a][bm]overlay[a2];[c]curves=master='0/0 0.25/0.40 0.5/0.64 1/1'[cr];[2:v]format=gray,scale=1080:1920[m2];[cr][m2]alphamerge[cm];[a2][cm]overlay,unsharp=5:5:0.5:5:5:0,format=yuv420p,fps=30[v]"
ffmpeg -y -i "$IN" -loop 1 -i fillmask.png -loop 1 -i eyemask.png -filter_complex "$F" \
  -map "[v]" -map 0:a -c:v libx264 -preset medium -crf 16 -c:a aac -b:a 192k -shortest "$OUT"
