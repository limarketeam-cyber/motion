#!/usr/bin/env bash
# Reframe + relight the low-angle talking-head source (720x1280) to 1080x1920 30fps.
#  - "raise the camera": mild keystone (top edge widened 3.5% per side) so the walls stop
#    converging, then a 1.10x zoom shifted down (crop starts 13% from the top) so less
#    ceiling/downlight shows and the face sits higher in frame
#  - white balance toward neutral, lift mids/shadows, roll off highlights
#  - fill light on face + torso through soft masks (fillmask.png, eyemask.png)
#  - light denoise + sharpen (extra unsharp to offset the zoom)
# usage: ./grade.sh source.mp4 graded.mp4
set -e
cd "$(dirname "$0")"
IN="$1"; OUT="$2"
K=0.035; Z=1.10; Y0=0.13
RF="perspective=x0=W*$K:y0=0:x1=W*(1-$K):y1=0:x2=0:y2=H:x3=W:y3=H:interpolation=cubic,crop=iw/$Z:ih/$Z:(iw-iw/$Z)/2:ih*$Y0"
WB="colorchannelmixer=rr=0.98:gg=0.975:bb=1.08"
G="$RF,scale=1080:1920:flags=lanczos,hqdn3d=1.5:1.5:4:4,$WB,curves=master='0/0.02 0.25/0.30 0.5/0.57 0.75/0.80 1/0.96',eq=saturation=1.04"
F="[0:v]$G,split=3[a][b][c];[b]curves=master='0/0 0.3/0.42 0.6/0.72 1/1'[br];[1:v]format=gray,scale=1080:1920[m];[br][m]alphamerge[bm];[a][bm]overlay[a2];[c]curves=master='0/0 0.25/0.40 0.5/0.64 1/1'[cr];[2:v]format=gray,scale=1080:1920[m2];[cr][m2]alphamerge[cm];[a2][cm]overlay,unsharp=5:5:0.6:5:5:0,format=yuv420p,fps=30[v]"
ffmpeg -y -i "$IN" -loop 1 -i fillmask.png -loop 1 -i eyemask.png -filter_complex "$F" \
  -map "[v]" -map 0:a -c:v libx264 -preset medium -crf 16 -c:a copy -shortest "$OUT"
