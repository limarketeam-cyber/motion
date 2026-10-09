import numpy as np, wave
from scipy.signal import butter, sosfilt, fftconvolve

SR = 44100; T = 44.0; TAIL = 4.0
N = int((T + TAIL) * SR)
rng = np.random.default_rng(5)
T3 = 24.58; T4 = T3 + 8.7

def tt(s): return np.arange(int(s * SR)) / SR
def env(s, a, d): x = tt(s); return np.minimum(x / max(a, 1e-4), 1) * np.exp(-x / d)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, a, b, o=2): return sosfilt(butter(o, [a, b], 'band', fs=SR, output='sos'), x)
def noise(s): return rng.standard_normal(int(s * SR))
def mtof(m): return 440 * 2 ** ((m - 69) / 12)
def sweep(f0, f1, s, c=1.0):
    x = tt(s); f = f0 * (f1 / f0) ** ((x / s) ** c); return np.sin(2 * np.pi * np.cumsum(f) / SR)
def varbp(x, f0, f1, q=.7):
    out = np.zeros_like(x); C = 1024
    for i in range(0, len(x), C):
        fr = f0 * (f1 / f0) ** (i / len(x)); lo = max(40, fr * (1 - q / 2)); hi = min(SR / 2 - 100, fr * (1 + q / 2))
        out[i:i + C] = bp(x[max(0, i - 2048):i + C], lo, hi)[-len(x[i:i + C]):]
    return out

# ---------- صداها (نرم و مینیمال) ----------
def air(s=.5, up=True, g=1.0):
    y = varbp(noise(s), 500 if up else 5000, 5000 if up else 500)
    return y * np.sin(np.linspace(0, np.pi, len(y))) ** 2 * g
def bell(m, s=1.6, g=1.0):
    x = tt(s); f = mtof(m)
    return (np.sin(2 * np.pi * f * x) + .3 * np.sin(2 * np.pi * f * 2.0 * x) * np.exp(-x / .3) + .12 * np.sin(2 * np.pi * f * 3.0 * x) * np.exp(-x / .15)) * env(s, .003, .55) * .22 * g
def pluck(m, g=1.0):
    s = .9; x = tt(s); f = mtof(m)
    return lp(sum(np.sin(2 * np.pi * f * h * x) * np.exp(-x * h * 2.2) / h for h in range(1, 6)), 3000) * env(s, .002, .35) * .3 * g
def tink(g=1.0): return bell(96, .9, .7 * g)
def click(g=1.0):
    s = .03; return (bp(noise(s), 1800, 6000) * env(s, .0003, .004) * .25 + np.sin(2 * np.pi * 3200 * tt(s)) * env(s, .0003, .003) * .05) * g
def clack():
    s = .12; x = tt(s)
    return (bp(noise(s), 2000, 7000) * env(s, .0002, .006) * .7 + np.sin(2 * np.pi * 2400 * x) * env(s, .0005, .025) * .35 + np.sin(2 * np.pi * 3900 * x) * env(s, .0005, .015) * .2)
def thump(g=1.0):
    s = .4; x = tt(s); return np.sin(2 * np.pi * np.cumsum(55 + 70 * np.exp(-x * 30)) / SR) * env(s, .002, .09) * .6 * g
def bloop(f0=300, f1=700, s=.22, g=1.0): return sweep(f0, f1, s, .6) * env(s, .004, s * .5) * .3 * g
def zipd(): return sweep(1600, 260, .55, .7) * env(.55, .01, .2) * .08 + air(.55, False, .5)
def swell(s=.7): return lp(noise(s), 900) * (tt(s) / s) ** 2 * .25
def snore(s=2.0):
    x = tt(s); e = (np.sin(2 * np.pi * x / 1.0 - np.pi / 2) * .5 + .5) ** 2
    return lp(noise(s), 500) * e * .12 + np.sin(2 * np.pi * 95 * x) * e * .03
def boing(): return sweep(260, 900, .35, .5) * np.sin(2 * np.pi * 18 * tt(.35)) * env(.35, .003, .15) * .15

sfx = np.zeros(N); mus = np.zeros(N)
def put(bus, sig, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(sig)); bus[i:j] += sig[:j - i] * g

# تایپ
for t0, d in [(.95, .9), (2.85, 1.2), (4.9, .7), (7.2, 1.2), (10.7, 1.3), (13.9, .9), (14.7, 1.1), (17.8, .3), (18.1, 1.0), (20.4, 1.0),
              (T3 + 1.3, 1.0), (T3 + 4.7, 1.5), (T4 + .2, .9), (T4 + 1.3, 1.1), (T4 + 1.75, 1.1), (T4 + 2.2, 1.1), (T4 + 3.3, .9), (T4 + 7.2, .9)]:
    n = int(d * 11);
    for k in range(n): put(sfx, click(.7 + .3 * rng.random()), t0 + k * d / n + rng.uniform(0, .02))

ev = [
 (0.0, air(1.0, True, .9)), (0.0, sweep(180, 640, .9, .6) * env(.9, .3, .5) * .05), (.9, tink()),
 (1.6, zipd()), (2.0, pluck(76, .6)), (2.45, bell(100, .6, .4)), (2.6, bloop(240, 360)), (3.4, bloop(240, 360)),
 (4.3, air(.7, True, 1.3)), (4.4, air(.9, False, .8)), (5.3, tink()),
 (5.9, pluck(79)), (6.0, pluck(84)), (6.4, air(.6, True, .4)),
 (8.3, air(.6, False, .7)), (8.9, bloop(300, 900, .3)), (9.0, bell(88, 1.8, .7)), (11.0, click(2)), (11.6, pluck(81)),
 (12.9, air(.5, True, .8)), (13.3, air(.4, False, .6)), (13.7, thump()),
 (15.0, swell(.6)), (15.4, snore(2.1)), (18.0, bloop(400, 1200, .18, 1.2)), (18.0, boing()),
 (19.3, air(.4, False, .6)), (19.65, zipd()), (19.8, zipd() * .6),
 (24.2, air(.5, True, .9)), (T3, air(1.0, False, .9)),
 (T3 + .4, air(.9, True, .35)), (T3 + 1.0, tink()), (T3 + 1.3, pluck(79)),
 (T3 + 2.6, air(.6, True, .5)), (T3 + 3.3, pluck(83)), (T3 + 4.2, air(.5, True, .5)), (T3 + 4.75, pluck(86)),
 (T3 + 7.6, air(.5, False, .5)), (T3 + 8.0, air(.6, True, .9)), (T4, thump(.8)), (T4, tink(.6)),
 (T4 + .9, pluck(76)), (T4 + 1.05, pluck(79)), (T4 + 1.2, pluck(84)),
 (T4 + 4.4, click(2.5)), (T4 + 4.9, click(2.5)), (T4 + 5.4, click(2.5)), (T4 + 5.9, click(2.5)), (T4 + 6.4, click(2.5)),
 (T4 + 6.8, bell(84, 2, .8)), (T4 + 6.86, bell(88, 2, .7)), (T4 + 6.92, bell(91, 2, .6)), (T4 + 6.98, bell(96, 2, .5)),
 (T - 2.2, air(.6, True, .5)), (T - 1.6, tink()), (T - .95, sweep(640, 160, .8, .8) * env(.8, .05, .4) * .05), (T - .95, air(.8, False, .9)),
]
for t, s in ev: put(sfx, s, t)
for t in [2.55, 6.9, 10.4, 17.5, 20.0, T3 + 4.4, T4 + 3.0, T4 + 6.9, 12.9, T3 + 8.0, T - 2.4]: put(sfx, air(.45, False, .45), t)
# برخورد گوی‌ها
for k in range(5): put(sfx, clack(), 20.4 + .76 * (k + 1))
put(sfx, clack() * .5, 20.4)

# ---------- بستر آمبینت ----------
chords = [[48, 55, 64, 71, 74], [45, 52, 60, 67, 71], [41, 48, 57, 64, 67], [43, 50, 59, 62, 69]] * 2  # Cmaj9 Am9 Fmaj9 G6/9
seg = T / len(chords)
for i, ch in enumerate(chords):
    s = seg + 2.5; x = tt(s); sig = 0
    for m in ch:
        f = mtof(m)
        for det in (-.15, .15): sig = sig + np.sin(2 * np.pi * f * (1 + det / 100) * x + rng.uniform(0, 6)) + .25 * np.sin(2 * np.pi * 2 * f * x)
    e = np.minimum(x / 1.2, 1) * np.minimum(np.maximum(s - x, 0) / 2.4, 1)
    put(mus, lp(sig, 1400) * e * .025, i * seg - 1.2 if i else 0)
    put(mus, lp(sig, 1400) * e * .025, T + i * seg - 1.2) if i == 0 else None
# نت‌های پیانویی پراکنده (پنتاتونیک)
for t, m in [(.9, 76), (4.6, 79), (9.0, 81), (13.7, 74), (18.0, 84), (24.6, 79), (28.9, 81), (33.3, 76), (40.1, 84), (42.4, 79)]:
    put(mus, pluck(m, .55), t)
sub = np.sin(2 * np.pi * 65.4 * np.arange(N) / SR) * .0  # بدون ساب

# ---------- میکس ----------
ir = rng.standard_normal(int(2.2 * SR)) * np.exp(-np.arange(int(2.2 * SR)) / SR / .6); ir = lp(ir, 4500); ir /= np.sqrt((ir ** 2).sum()) * 9
wet = fftconvolve(sfx + mus * .6, ir)[:N]
mix = sfx * .9 + mus + wet * .9
L = int(T * SR); mix[:N - L] += mix[L:]; mix = mix[:L]
mix = hp(mix, 35)
mix = np.tanh(mix * 1.2) / np.tanh(1.2)
mix /= np.abs(mix).max() / .9
st = np.stack([mix, np.roll(mix, 9)], 1)
w = wave.open('minimal.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype('<i2').tobytes()); w.close()
print('ok')
