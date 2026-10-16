#!/usr/bin/env bash
# Relight + color-grade the talking-head source (720x1280) to 1080x1920 30fps.
#  - white balance: pull the warm/yellow cast of the overhead tungsten light toward neutral
#  - lift mids/shadows, roll off highlights (wall hotspot under the downlight)
#  - "fill light": brighten face + upper torso through soft masks (fillmask.png, eyemask.png)
#    to soften the dark eye sockets from the top-down light
#  - light denoise + sharpen
# usage: ./grade.sh source.mp4 graded.mp4
set -e
cd "$(dirname "$0")"
IN="$1"; OUT="$2"
WB="colorchannelmixer=rr=0.98:gg=0.975:bb=1.07"
G="scale=1080:1920:flags=lanczos,hqdn3d=1.5:1.5:4:4,$WB,curves=master='0/0.02 0.25/0.30 0.5/0.57 0.75/0.80 1/0.97',eq=saturation=1.04"
F="[0:v]$G,split=3[a][b][c];[b]curves=master='0/0 0.3/0.42 0.6/0.72 1/1'[br];[1:v]format=gray,scale=1080:1920[m];[br][m]alphamerge[bm];[a][bm]overlay[a2];[c]curves=master='0/0 0.25/0.40 0.5/0.64 1/1'[cr];[2:v]format=gray,scale=1080:1920[m2];[cr][m2]alphamerge[cm];[a2][cm]overlay,unsharp=5:5:0.45:5:5:0,format=yuv420p,fps=30[v]"
ffmpeg -y -i "$IN" -loop 1 -i fillmask.png -loop 1 -i eyemask.png -filter_complex "$F" \
  -map "[v]" -map 0:a -c:v libx264 -preset medium -crf 16 -c:a copy -shortest "$OUT"
