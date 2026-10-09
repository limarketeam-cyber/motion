import numpy as np, wave
from scipy.signal import butter, sosfilt, fftconvolve

SR = 44100; T = 48.0; TAIL = 3.0
N = int((T + TAIL) * SR)
rng = np.random.default_rng(11)
BPM = 120; B = 60 / BPM; BAR = 4 * B
CUTS = [5, 15, 27, 37]

def z(sec): return np.zeros(int(sec * SR))
def tt(sec): return np.arange(int(sec * SR)) / SR
def env(sec, a, d): x = tt(sec); return np.minimum(x / max(a, 1e-4), 1) * np.exp(-x / d)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, f1, f2, o=2): return sosfilt(butter(o, [f1, f2], 'band', fs=SR, output='sos'), x)
def noise(sec): return rng.standard_normal(int(sec * SR))
def sweep(f0, f1, sec, curve=1.0):
    x = tt(sec); k = (x / sec) ** curve; f = f0 * (f1 / f0) ** k
    return np.sin(2 * np.pi * np.cumsum(f) / SR)
def mtof(m): return 440 * 2 ** ((m - 69) / 12)
def varbp(x, f0, f1, sec, q=.6):
    out = np.zeros_like(x); C = 1024
    for i in range(0, len(x), C):
        fr = f0 * (f1 / f0) ** (i / len(x)); lo = max(40, fr * (1 - q / 2)); hi = min(SR / 2 - 100, fr * (1 + q / 2))
        out[i:i + C] = bp(x[max(0, i - 2048):i + C], lo, hi)[-len(x[i:i + C]):]
    return out

# ---------- instruments ----------
def kick():
    s = .45; x = tt(s); f = 48 + 130 * np.exp(-x * 30)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x / .16)
    click = hp(noise(s), 2500) * np.exp(-x / .004) * .5
    return np.tanh((body + click) * 1.6) * .95
def clap():
    s = .35; out = np.zeros(int(s * SR))
    for k, o in enumerate([0, .011, .022]):
        i = int(o * SR); n = bp(noise(s - o), 900, 3200) * env(s - o, .0005, .012 if k < 2 else .09); out[i:] += n
    return out * .9
def hat(open_=False):
    s = .3 if open_ else .06; return hp(noise(s), 7000, 4) * env(s, .0005, .09 if open_ else .014) * (.45 if open_ else .35)
def snare():
    s = .2; x = tt(s); return (bp(noise(s), 1200, 6000) * env(s, .0005, .05) * .6 + np.sin(2 * np.pi * 190 * x) * env(s, .001, .04) * .4)
def bass(m, sec):
    x = tt(sec); f = mtof(m); sig = sum(np.sin(2 * np.pi * f * h * x) / h for h in range(1, 7)) * .5 + np.sin(2 * np.pi * f / 2 * x) * .8
    e = np.minimum(x / .005, 1) * (0.55 + .45 * np.exp(-x / .08)); e[-int(.02 * SR):] *= np.linspace(1, 0, int(.02 * SR))
    return lp(sig, 380) * e * .5
def pad(ms, sec):
    x = tt(sec); sig = 0
    for m in ms:
        f = mtof(m)
        for det in (-.12, .12): sig = sig + sum(np.sin(2 * np.pi * f * (1 + det / 100) * h * x + h) / h for h in range(1, 6))
    e = np.minimum(x / .25, 1) * np.minimum((sec - x) / .3, 1)
    return lp(sig, 1100) * e * .05
def pluck(m, sec=.35):
    x = tt(sec); f = mtof(m); return lp(sum(np.sin(2 * np.pi * f * h * x) / h ** 1.2 for h in range(1, 6)), 2600) * env(sec, .002, .09) * .35

# ---------- sfx ----------
def whoosh(sec=.6, up=True, g=1):
    n = noise(sec); y = varbp(n, 400 if up else 4000, 4000 if up else 400, sec)
    return y * np.sin(np.linspace(0, np.pi, len(y))) ** 1.5 * 1.8 * g
def swish(): return whoosh(.22, True, .7)
def riser(sec=1.1):
    n = varbp(noise(sec), 300, 7000, sec, .5) * 1.3; s = sweep(180, 1400, sec, 1.5) * .18
    e = (tt(sec) / sec) ** 2.2; return (n + s) * e
def impact():
    s = 1.6; x = tt(s); boom = np.sin(2 * np.pi * np.cumsum(30 + 60 * np.exp(-x * 9)) / SR) * np.exp(-x / .45) * 1.1
    crash = hp(noise(s), 3500) * env(s, .001, .5) * .35
    return np.tanh((boom + crash) * 1.3)
def pop(m=76, g=1):
    s = .2; x = tt(s); f = mtof(m) * (1 + 1.2 * np.exp(-x * 60))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(s, .001, .05) * .55 * g
def snap(m=84):
    p = pop(m, 1.0); c = hp(noise(.03), 3000) * env(.03, .0003, .004) * .5; p[:len(c)] += c; return p
def zipup(sec=.2): return sweep(500, 2600, sec, .8) * env(sec, .002, sec * .6) * .25
def tick(): return hp(noise(.025), 2500) * env(.025, .0002, .003) * .5 + np.sin(2 * np.pi * 2200 * tt(.025)) * env(.025, .0002, .004) * .15
def thud():
    s = .5; x = tt(s); b = np.sin(2 * np.pi * np.cumsum(40 + 80 * np.exp(-x * 25)) / SR) * np.exp(-x / .12)
    cr = lp(noise(s), 1800) * env(s, .0005, .05) * .6; return np.tanh((b + cr) * 1.8) * .9
def clink(f=900):
    s = .7; x = tt(s); return sum(np.sin(2 * np.pi * f * r * x) * np.exp(-x / d) * a for r, d, a in [(1, .35, .5), (2.76, .2, .3), (5.4, .1, .2)]) * .45
def bell(m, s=1.2):
    x = tt(s); f = mtof(m); return (np.sin(2 * np.pi * f * x) + .35 * np.sin(2 * np.pi * f * 2.0 * x) + .15 * np.sin(2 * np.pi * f * 3.01 * x)) * env(s, .002, .35) * .32
def sparkle(sec=1.2, n=26):
    out = np.zeros(int(sec * SR))
    for i in range(n):
        t0 = rng.uniform(0, sec - .1); f = rng.uniform(2500, 6500); s = .08; i0 = int(t0 * SR)
        out[i0:i0 + int(s * SR)] += np.sin(2 * np.pi * f * tt(s)) * env(s, .001, .02) * .12 * (1 - t0 / sec)
    return out
def tone(f0, f1, sec, g=.12): return sweep(f0, f1, sec) * np.minimum(tt(sec) / .05, 1) * np.minimum((sec - tt(sec)) / .1, 1) * g
def boop(): return np.sin(2 * np.pi * 110 * tt(.4)) * env(.4, .005, .12) * .4

# ---------- buses ----------
drums = np.zeros(N); music = np.zeros(N); sfx = np.zeros(N); duck = np.ones(N)
def put(bus, sig, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(sig)); bus[i:j] += sig[:j - i] * g

prog = [(57, [69, 72, 76]), (53, [65, 69, 72]), (60, [67, 72, 76]), (55, [67, 71, 74])]  # Am F C G
def near_cut(t, w): return any(c - w <= t < c for c in CUTS + [T])
for bar in range(int(T / BAR)):
    t0 = bar * BAR; root, chord = prog[bar % 4]
    put(music, pad(chord, BAR), t0)
    for e in range(8):  # بیس هشتم‌ها
        te = t0 + e * B / 2
        if near_cut(te, B / 2): continue
        m = root - 12 + (12 if e in (3, 6) else 0)
        put(music, bass(m, B / 2 * .9), te)
    for k in range(4):
        tb = t0 + k * B
        if k in (0, 2) and not near_cut(tb, B):
            put(drums, kick(), tb); i = int(tb * SR); L = int(.25 * SR); duck[i:i + L] = np.minimum(duck[i:i + L], 1 - .6 * np.exp(-np.arange(L) / SR / .08))
        if k in (1, 3) and not near_cut(tb, B): put(drums, clap(), tb, .8)
        for h in range(2):
            th = tb + h * B / 2
            if not near_cut(th, B * 1.5): put(drums, hat(open_=(k == 3 and h == 1)), th, .6 if h else .4)
    if bar % 2 == 1 and not near_cut(t0 + 1.75, .3): put(drums, kick(), t0 + 1.75, .7)  # کیک سنکوپ
# رول اسنیر و رایزر قبل از هر برش
for c in CUTS + [T]:
    for i in range(8): put(drums, snare(), c - 1.0 + i * .125, .25 + i * .07)
    put(sfx, riser(1.1), c - 1.1, .55)
# ایمپکت روی برش‌ها (و شروع لوپ)
for c in [0] + CUTS: put(sfx, impact(), c, .9)

# آرپژ پلاک روی قفل انتخاب
LOCK = 43.65
for i, m in enumerate([81, 84, 88, 93, 88, 84, 81, 84, 88, 93, 96, 93]):
    put(music, pluck(m), LOCK + i * .125, .7)

# ---------- SFX timeline (هم‌زمان با نریشن) ----------
E = [(.1, lambda: pop(72, .5)), (.25, swish), (.85, lambda: snap(84)), (1.25, swish), (1.6, zipup), (1.9, lambda: pop(76, .4)),
     (.05, lambda: whoosh(1.4, False, .7)), (2.9, lambda: tone(1800, 400, .45, .1)), (3.4, lambda: clink(980)), (3.45, lambda: pop(88, 1.0)),
     (3.45, lambda: sparkle(.8, 16)), (3.9, lambda: zipup(.35)), (3.65, boop), (4.1, boop), (4.55, boop),
     (5.5, lambda: pop(72, .5)), (5.7, thud), (5.7, swish), (6.2, zipup), (6.75, swish), (11.1, swish)]
for t, f in E: put(sfx, f(), t)
for t, m in [(5.45, 81), (6.75, 84), (9.0, 88), (13.4, 93)]: put(sfx, pop(m), t)
for t in [7.05, 9.3, 13.7]: put(sfx, zipup(.15), t, .6)
for t in [9.6, 11.9, 14.2]: put(sfx, tick(), t, .7)
put(sfx, whoosh(.6, True, .8), 15.1); put(sfx, pop(76, .6), 15.3)
for i in range(6): put(sfx, tick(), 16.4 + i * .32, 1.0)
put(sfx, tone(700, 140, 2.2, .07), 16.4)
put(sfx, thud(), 18.65, 1.1); put(sfx, swish(), 18.95); put(sfx, whoosh(.45, True, .9), 19.1); put(sfx, pop(84, .8), 19.3)
for i in range(4): put(sfx, snap(84 + i * 2), 19.75 + i * .42, .7)
put(sfx, tone(220, 1000, 1.0, .06), 20.5)
for i in range(10): put(sfx, tick(), 20.5 + i * .09 * (1 + i * .08), .5)
put(sfx, pop(88, .8), 21.3)
for i, t in enumerate([22.3, 22.75, 23.1, 24.6, 25.4]): put(sfx, pop([69, 74, 76, 79, 81][i] + 12, .8 if i % 2 == 0 else .5), t)
put(sfx, whoosh(.6, False, .8), 27.1); put(sfx, pop(72, .5), 27.05); put(sfx, swish(), 27.15); put(sfx, snap(84), 27.85); put(sfx, swish(), 28.5); put(sfx, zipup(), 28.8)
for i, t in enumerate([29.9, 31.15, 32.6]): put(sfx, pop(76 + i * 4), t); put(sfx, clink(900 + i * 150), t + .05, .6)
put(sfx, pop(72, .4), 34.0)
for t in [37.5, 37.9, 38.3]: put(sfx, whoosh(.35, True, .7), t)
put(sfx, pop(72, .5), 37.05); put(sfx, pop(74, .4), 37.2); put(sfx, swish(), 40.2)
for i, t in enumerate([40.3, 40.9, 41.5, 42.1, 42.8]): put(sfx, snap(76 + i * 3), t, .7)
put(sfx, impact(), LOCK, .6); put(sfx, snap(88), LOCK - .05)
for i, m in enumerate([81, 84, 88, 93]): put(sfx, bell(m), LOCK + i * .06)
put(sfx, sparkle(1.4, 30), LOCK + .05); put(sfx, swish(), 44.25)
put(sfx, whoosh(.6, True, .7), 47.35)

# ---------- mix ----------
ir = rng.standard_normal(int(.9 * SR)) * np.exp(-np.arange(int(.9 * SR)) / SR / .25); ir = lp(ir, 5000); ir /= np.abs(ir).sum() ** .5 * 6
sfx_w = sfx + fftconvolve(sfx, ir)[:N] * .5
import wave as _w
vw = _w.open('vo/vo_proc.wav'); vo = np.frombuffer(vw.readframes(vw.getnframes()), '<i2').astype(float) / 32768
vo = np.pad(vo, (0, max(0, N - len(vo))))[:N]
ve = lp(np.abs(vo), 6); ve = ve / (np.percentile(ve, 99) + 1e-9); ve = np.clip(ve * 1.6, 0, 1)
vd = 1 - .75 * ve; sd = 1 - .45 * ve
mix = (drums * .38 * vd + music * duck * .4 * vd) + sfx_w * .5 * sd + vo * 1.05
# دمِ صداها بعد از ۴۴ ثانیه به ابتدای فایل برمی‌گرده تا لوپ بی‌درز باشه
L = int(T * SR); mix[:N - L] += mix[L:]; mix = mix[:L]
mix = hp(mix, 30)
mix = np.tanh(mix * 1.1) / np.tanh(1.1)
mix /= np.abs(mix).max() / .93
st = np.stack([mix, mix], 1)
# پهنای استریو کوچک
st[:, 0] = mix; st[:, 1] = np.roll(mix, 12)
w = wave.open('final_vo.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype('<i2').tobytes()); w.close()
print('ok', L / SR)
