"""Verify no overlay pixel lands on the face.
Detects the face (OpenCV Haar) on the graded footage every STEP seconds, pads the box,
and measures overlay alpha inside it from the rendered overlay frames.
usage: python3 check-face.py graded.mp4 overlay_frames_dir [fps=30]"""
import sys, cv2, numpy as np
from PIL import Image
vid, ov = sys.argv[1], sys.argv[2]; fps = int(sys.argv[3]) if len(sys.argv) > 3 else 30
STEP, PAD = 0.2, 0.04
cas = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(vid); n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
bad, wipes, checked, last = [], [], 0, None
for f in range(0, n, int(STEP * fps)):
    cap.set(cv2.CAP_PROP_POS_FRAMES, f); ok, img = cap.read()
    if not ok: break
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = cas.detectMultiScale(g, 1.1, 6, minSize=(200, 200))
    if len(faces): last = max(faces, key=lambda r: r[2] * r[3])
    if last is None: continue
    x, y, w, h = last; px, py = int(w * PAD), int(h * PAD)
    x0, y0, x1, y1 = max(0, x - px), max(0, y - py), x + w + px, y + h + py  # Haar box already spans forehead→chin
    try: im = np.asarray(Image.open(f"{ov}/f{f:05d}.png"))
    except FileNotFoundError: continue
    checked += 1
    if im.ndim < 3 or im.shape[2] < 4: wipes.append(f / fps); continue  # fully opaque frame = section wipe (by design)
    cov = (im[..., 3][y0:y1, x0:x1] > 20).mean()
    if cov > 0.002: bad.append((f / fps, round(cov * 100, 2), (x0, y0, x1, y1)))
print(f"checked {checked} samples; text/card on face at {len(bad)} samples; full-frame wipe at {len(wipes)} samples {[round(w,1) for w in wipes]}")
for b in bad: print(f"  t={b[0]:.1f}s  covered={b[1]}%  box={b[2]}")
