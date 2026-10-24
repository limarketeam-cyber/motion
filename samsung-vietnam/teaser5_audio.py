"""Mix for teaser v5: speech + SFX cues (from the page) + a synthesized beat bed.
usage: python3 teaser5_audio.py speech.wav sfx.json timings.json out.wav"""
import json, sys, wave, numpy as np
from scipy.signal import butter, sosfilt
src=open('audio.py').read(); exec(src[:src.index('speech_path, sfx_path, out_path')])   # reuse SR + SFX synths
speech_p,sfx_p,tim_p,out_p=sys.argv[1:5]
T=json.load(open(tim_p))
w=wave.open(speech_p); ch=w.getnchannels(); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)/32768
speech=a.reshape(-1,ch).mean(1)
L=int(T['END']*SR)+SR//2; speech=np.pad(speech,(0,max(0,L-len(speech))))[:L]
def put(bus,sig,t,g=1.0):
    i=int(t*SR)
    if i>=len(bus): return
    j=min(len(bus),i+len(sig)); bus[i:j]+=sig[:j-i]*g
# ---- beat bed (A minor, 112 bpm), first downbeat on the friend story
BPM=112; beat=60/BPM; t0=T['S1']
def kick():
    s=.35; f=np.geomspace(150,42,int(s*SR)); return np.sin(2*np.pi*np.cumsum(f)/SR)*env(s,.002,.10)*.9
def hat(): return hp(noise(.05),7000)*env(.05,.0005,.012)*.22
def clap(): return bp(noise(.18),900,4000)*env(.18,.002,.05)*.45
def bassnote(f,s): x=tt(s); return np.tanh(2.2*np.sin(2*np.pi*f*x))*env(s,.005,s*.6)*.32
mus=np.zeros(L)
roots=[55.0,55.0,43.65,49.0]  # A A F G
k=0; t=t0
while t<T['FRZ']-0.01:
    put(mus,kick(),t)
    if k%4 in (1,3): put(mus,clap(),t,0.8)
    put(mus,hat(),t+beat/2)
    if k%2==0: put(mus,bassnote(roots[(k//4)%4],beat*1.8),t)
    k+=1; t=t0+k*beat
# pack shot: music back with a hit
t=T['CTA']; k=0
while t<T['END']:
    put(mus,kick(),t); put(mus,hat(),t+beat/2)
    if k%4 in (1,3): put(mus,clap(),t,0.8)
    if k%2==0: put(mus,bassnote(roots[(k//4)%4],beat*1.8),t)
    k+=1; t=T['CTA']+k*beat
mus=lp(mus,9000)
# duck music under the voice
e=np.abs(speech); win=int(.05*SR); e=np.convolve(e,np.ones(win)/win,'same')
duck=1-0.7*np.clip(e/0.03,0,1); duck=np.convolve(duck,np.ones(int(.08*SR))/int(.08*SR),'same')
mus*=duck
# fade the bed in over the first bar, cut on the freeze, fade out at the very end
fi=np.clip((np.arange(L)/SR-t0)/(beat*2),0,1); mus*=fi
end=np.arange(L)/SR; mus*=np.clip((T['END']-end)/0.6,0,1)
# ---- SFX from the page
bus=np.zeros(L); cache={}
for c in json.load(open(sfx_p)):
    if c['type'] not in cache: cache[c['type']]=SYN[c['type']]()
    put(bus,cache[c['type']],c['t'],c['g'])
put(bus,impact() if 'impact' in globals() else thud(),t0,0.9)
mix=speech+bus*0.35+mus*0.30
mix=mix/max(1e-9,np.abs(mix).max())*0.89
st=np.stack([mix,mix],1)
o=wave.open(out_p,'w'); o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR); o.writeframes((st*32767).astype(np.int16).tobytes()); o.close()
print('mixed', out_p)
