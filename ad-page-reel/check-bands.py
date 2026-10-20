"""Report the vertical extent of overlay content per frame: lowest pixel of the top band
(titles) and highest pixel of the bottom band (cards). Fully opaque frames (section wipes)
are skipped. usage: python3 check-bands.py overlay_frames_dir"""
import sys, glob, numpy as np
from PIL import Image
top_max, bot_min = (0, None), (1920, None)
for p in sorted(glob.glob(sys.argv[1] + '/f*.png'))[::3]:
    im = np.asarray(Image.open(p))
    if im.ndim < 3 or im.shape[2] < 4: continue
    if (im[960, :, 3] > 20).any(): continue  # section wipe passing through (nothing else lives at mid-frame)
    rows = np.where((im[..., 3] > 20).any(1))[0]
    if not len(rows): continue
    t, b = rows[rows < 800], rows[rows >= 800]
    if len(t) and t.max() > top_max[0]: top_max = (int(t.max()), p)
    if len(b) and b.min() < bot_min[0]: bot_min = (int(b.min()), p)
print('titles reach down to y =', top_max); print('cards reach up to y =', bot_min)
