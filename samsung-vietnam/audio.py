"""Mix the edited speech with synthesized SFX cues exported by the page (sfx.json)."""
import json, sys, wave
import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000
rng = np.random.default_rng(7)
def tt(s): return np.arange(int(s * SR)) / SR
def env(s, a, d): x = tt(s); return np.minimum(x / max(a, 1e-4), 1) * np.exp(-x / d)
def lp(x, f): return sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)
def hp(x, f): return sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)
def bp(x, a, b): return sosfilt(butter(2, [a, b], 'band', fs=SR, output='sos'), x)
def noise(s): return rng.standard_normal(int(s * SR))
def sweep(f0, f1, s):
    f = np.geomspace(f0, f1, int(s * SR)); return np.sin(2 * np.pi * np.cumsum(f) / SR)

def whoosh(s=0.45):
    n = noise(s); x = tt(s); e = np.sin(np.pi * x / s) ** 2
    out = np.zeros_like(n); k = 8; seg = len(n) // k
    for i in range(k):  # moving band-pass = airy sweep
        f = 400 + 2600 * i / k
        out[i*seg:(i+1)*seg] = bp(n, f, f * 1.8)[i*seg:(i+1)*seg]
    return out * e * 0.35
def swish(): return whoosh(0.22) * 0.6
def pop():
    s = 0.12; return (np.sin(2 * np.pi * np.cumsum(np.geomspace(900, 260, int(s*SR))) / SR) * env(s, .002, .035)) * 0.45
def tick(): return hp(noise(.03), 2500) * env(.03, .0003, .004) * .5 + np.sin(2*np.pi*2400*tt(.03)) * env(.03, .0003, .006) * .25
def ding():
    s = 0.9; x = tt(s); return (np.sin(2*np.pi*1318*x) + .5*np.sin(2*np.pi*1975*x) + .25*np.sin(2*np.pi*2637*x)) * env(s, .002, .22) * .22
def thud():
    s = .35; return (sweep(160, 45, s) * env(s, .002, .09) * .9 + lp(noise(s), 900) * env(s, .001, .03) * .4) * .7
def marker():
    s = .5; n = bp(noise(s), 1800, 6000); m = 0.6 + 0.4 * np.sin(2*np.pi*11*tt(s))
    return n * m * np.sin(np.pi * tt(s) / s) * .12
def ring():
    s = 1.3; x = tt(s); tone = np.sin(2*np.pi*1400*x) + np.sin(2*np.pi*1750*x)
    gate = ((x % 0.18) < 0.1).astype(float); gate[int(0.75*SR):] = 0
    return lp(tone * gate, 3500) * .09
def cash():
    s = .7; x = tt(s); return (np.sin(2*np.pi*2093*x) + np.sin(2*np.pi*2637*x)) * env(s, .001, .18) * .18
SYN = dict(whoosh=whoosh, swish=swish, pop=pop, tick=tick, ding=ding, thud=thud, marker=marker, ring=ring, cash=cash)

speech_path, sfx_path, out_path = sys.argv[1:4]
w = wave.open(speech_path); assert w.getframerate() == SR
ch = w.getnchannels(); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
speech = a.reshape(-1, ch).mean(1)
bus = np.zeros(len(speech) + SR)
cache = {}
for c in json.load(open(sfx_path)):
    if c['type'] not in cache: cache[c['type']] = SYN[c['type']]()
    sig = cache[c['type']] * c['g']; i = int(c['t'] * SR)
    if i < 0: sig = sig[-i:]; i = 0
    j = min(len(bus), i + len(sig)); bus[i:j] += sig[:j - i]
bus = bus[:len(speech)]
mix = speech + bus * 0.35
mix = mix / max(1e-9, np.abs(mix).max()) * 0.89
st = np.stack([mix, mix], 1)
o = wave.open(out_path, 'w'); o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR)
o.writeframes((st * 32767).astype(np.int16).tobytes()); o.close()
print('mixed', len(json.load(open(sfx_path))), 'cues')
