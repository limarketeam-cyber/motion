"""1-minute Instagram Reel cut from the clean (no burned-in subtitles) source.
Tight pacing: pauses inside sentences are removed; every jump cut gets a zoom change in the page.
usage: python3 -I reel_cut.py <scratch dir>   (writes reel_edl.json here, frames to <scratch>/rf, speech to <scratch>/reel/speech.wav)"""
import json, subprocess, glob, sys, os, numpy as np
from PIL import Image
S = sys.argv[1]; P = os.path.dirname(os.path.abspath(__file__))
SRC = glob.glob('/root/.claude/uploads/042058c6-22a1-50c5-89b1-6e542c5bd208/7275f3aa*.mp4')[0]
db = np.load(f'{S}/reel/db.npy'); dbs = np.convolve(db, np.ones(5) / 5, 'same')
# label, source start, source end
SEGS = [('H', 0.00, 4.33),      # واقعاً کشور تولیدکننده کیفیت ... رو تضمین می‌کنه؟
        ('ST', 21.86, 29.44),   # دوستم زنگ زد ... A57 ... حتماً، حتماً ویتنام باشه
        ('DF', 34.93, 36.22),   # اما گوشش بدهکار نبود
        ('G', 52.44, 55.37),    # سامسونگ توی صفحه‌ی پشتیبانی سه تا نکته رو گفته
        ('P1', 55.37, 58.64), ('P1', 60.77, 63.46),   # یک: ... همگی از نظر کیفیت یکسان
        ('P2', 63.46, 68.68),   # دو: تکنولوژی تولید ... برابره
        ('P3', 68.68, 78.72),   # سه: ... با استانداردهای رسمی سامسونگ چک می‌شن
        ('L', 103.75, 114.48),  # ۴ چیز: مدل، رم، حافظه، گارانتی
        ('N', 128.95, 135.94),  # توی سایت هماهنگ یک قیمت ... جای دیگه ... دو سه میلیون بیشتر
        ('N2', 138.22, 141.41)]  # این اختلاف قیمت دقیقاً بابت چه تفاوتیه؟ (kept whole: the dramatic pause stays)
TH, MINP, PAD = -36, 0.40, 0.08
pieces = []
for lab, s, e in SEGS:
    a, b = int(round(s * 100)), int(round(e * 100)); q = dbs[a:b] < TH; cur = s; i = 0
    if lab == 'N2': q[:] = False
    while i < len(q):
        if q[i]:
            j = i
            while j < len(q) and q[j]: j += 1
            if (j - i) / 100 >= MINP and i > 0 and j < len(q):
                pieces.append([lab, round(cur, 3), round((a + i) / 100 + PAD, 3)]); cur = (a + j) / 100 - PAD
            i = j
        else: i += 1
    pieces.append([lab, round(cur, 3), e])
t = 0
for p in pieces: p.append(round(t, 3)); t += p[2] - p[1]
json.dump({'pieces': pieces, 'speech_end': round(t, 3)}, open(f'{P}/reel_edl.json', 'w'), indent=1)
for p in pieces: print(p)
print('speech', round(t, 2))
if '--plan' in sys.argv: sys.exit()

fc = []; v = []; au = []
for i, (lab, s, e, o) in enumerate(pieces):
    d = e - s; f = 0.012
    fc.append(f"[0:v]trim={s:.3f}:{e:.3f},setpts=PTS-STARTPTS,fps=30,scale=1080:1920:flags=lanczos,setsar=1[v{i}]"); v.append(f"[v{i}]")
    fc.append(f"[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS,afade=t=in:d={f},afade=t=out:st={d - f:.3f}:d={f}[a{i}]"); au.append(f"[a{i}]")
fc.append(''.join(v) + f"concat=n={len(pieces)}:v=1:a=0[vo]"); fc.append(''.join(au) + f"concat=n={len(pieces)}:v=0:a=1[ao]")
open(f'{S}/reel/fc.txt', 'w').write(';\n'.join(fc))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', SRC, '-filter_complex_script', f'{S}/reel/fc.txt', '-map', '[vo]', '-map', '[ao]',
                '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', '-ar', '48000', f'{S}/reel/cut.mov'], check=True)
os.makedirs(f'{S}/rf', exist_ok=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{S}/reel/cut.mov', '-q:v', '2', f'{S}/rf/%05d.jpg'], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{S}/reel/cut.mov', '-vn', '-c:a', 'pcm_s16le', f'{S}/reel/speech.wav'], check=True)
N = len(os.listdir(f'{S}/rf'))
# remove light-leak/flash residue: inside each piece, a frame that does not match the piece's look
# (orange flash, or a colour frame inside a B&W shot) is replaced with the nearest clean frame
sat = [np.array(Image.open(f'{S}/rf/{i:05d}.jpg').resize((90, 160)).convert('HSV'))[..., 1].mean() for i in range(1, N + 1)]
fixed = []
for lab, s, e, o in pieces:
    f0 = int(round(o * 30)) + 1; f1 = min(int(round((o + e - s) * 30)), N)
    rng = list(range(f0, f1 + 1)); gray = np.median([sat[i - 1] for i in rng]) < 25
    bad = [i for i in rng if sat[i - 1] > 100 or (gray and sat[i - 1] >= 25)]
    good = [i for i in rng if i not in bad]
    for b in bad:
        g = min(good, key=lambda k: abs(k - b)); Image.open(f'{S}/rf/{g:05d}.jpg').save(f'{S}/rf/{b:05d}.jpg', quality=95); fixed.append(b)
print('frames', N, 'fixed', fixed)
