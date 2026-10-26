"""Mix for the reel: speech + SFX cues (from the page) + a synthesized beat bed ducked under the voice.
usage: python3 reel_audio.py speech.wav reel_sfx.json out.wav <beat_start> <speech_end> <end>"""
import json, sys, wave, numpy as np
src = open('audio.py').read(); exec(src[:src.index('speech_path, sfx_path, out_path')])   # SR, env, noise, hp/bp/lp, SYN synths
speech_p, sfx_p, out_p = sys.argv[1:4]; T0, SPEECH, END = map(float, sys.argv[4:7])
w = wave.open(speech_p); ch = w.getnchannels(); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
speech = a.reshape(-1, ch).mean(1)
L = int(END * SR) + SR // 4; speech = np.pad(speech, (0, max(0, L - len(speech))))[:L]
def put(bus, sig, t, g=1.0):
    i = int(t * SR)
    if i >= len(bus) or i < 0: return
    j = min(len(bus), i + len(sig)); bus[i:j] += sig[:j - i] * g
# ---- beat bed (A minor, 112 bpm): first downbeat on the story, steady to the end card
BPM = 112; beat = 60 / BPM
def kick(): s = .35; f = np.geomspace(150, 42, int(s * SR)); return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(s, .002, .10) * .9
def hat(): return hp(noise(.05), 7000) * env(.05, .0005, .012) * .22
def clap(): return bp(noise(.18), 900, 4000) * env(.18, .002, .05) * .45
def bassnote(f, s): x = tt(s); return np.tanh(2.2 * np.sin(2 * np.pi * f * x)) * env(s, .005, s * .6) * .32
mus = np.zeros(L); roots = [55.0, 55.0, 43.65, 49.0]
k = 0; t = T0
while t < END - 0.05:
    put(mus, kick(), t); put(mus, hat(), t + beat / 2)
    if k % 4 in (1, 3): put(mus, clap(), t, 0.8)
    if k % 2 == 0: put(mus, bassnote(roots[(k // 4) % 4], beat * 1.8), t)
    k += 1; t = T0 + k * beat
mus = lp(mus, 9000)
e = np.abs(speech); win = int(.05 * SR); e = np.convolve(e, np.ones(win) / win, 'same')
duck = 1 - 0.72 * np.clip(e / 0.03, 0, 1); duck = np.convolve(duck, np.ones(int(.08 * SR)) / int(.08 * SR), 'same')
mus *= duck
tt_ = np.arange(L) / SR
mus *= np.clip((tt_ - T0) / (beat * 2), 0, 1) * np.clip((END - tt_) / 0.8, 0, 1)
mus *= np.where(tt_ > SPEECH, 1.35, 1.0)          # bed comes up on the end card
bus = np.zeros(L); cache = {}
for c in json.load(open(sfx_p)):
    if c['type'] not in cache: cache[c['type']] = SYN[c['type']]()
    put(bus, cache[c['type']], c['t'], c['g'])
put(bus, thud(), T0, 0.9)
mix = speech + bus * 0.33 + mus * 0.26
mix = mix / max(1e-9, np.abs(mix).max()) * 0.89
st = np.stack([mix, mix], 1)
o = wave.open(out_p, 'w'); o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR); o.writeframes((st * 32767).astype(np.int16).tobytes()); o.close()
print('mixed', out_p)
