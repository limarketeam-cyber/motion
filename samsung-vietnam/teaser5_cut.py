"""Teaser v5 cut: cold open on the money line, tight pacing (pauses inside sentences removed;
each jump cut gets a clear zoom change in the page), freeze on the cliffhanger."""
import json, subprocess, glob, sys, os, numpy as np
from PIL import Image
S=sys.argv[1]; P=os.path.dirname(os.path.abspath(__file__))
db=np.load(f'{S}/main/db.npy'); dbs=np.convolve(db,np.ones(5)/5,'same')
# label, src start, src end, [(src split time, text id) ...]
SEGS=[('S0',134.10,135.90),('S1',26.20,29.44),('S2a',0.00,2.24),('S2b',2.40,4.33),
      ('BA',52.44,55.37),('S3',80.20,84.32),('BB',100.80,105.53),('S4',138.28,141.41)]
TH,MINP,PAD=-36,0.18,0.06
pieces=[]
for lab,s,e in SEGS:
    a,b=int(round(s*100)),int(round(e*100)); q=dbs[a:b]<TH; cur=s; i=0
    while i<len(q):
        if q[i]:
            j=i
            while j<len(q) and q[j]: j+=1
            if (j-i)/100>=MINP and i>0 and j<len(q):
                pieces.append([lab,cur,(a+i)/100+PAD]); cur=(a+j)/100-PAD
            i=j
        else: i+=1
    pieces.append([lab,cur,e])
t=0
for p in pieces: p.append(round(t,3)); t+=p[2]-p[1]
FREEZE=0.6
json.dump({'pieces':pieces,'speech_end':round(t,3),'freeze':FREEZE},open(f'{P}/teaser5_edl.json','w'),indent=1)
for p in pieces: print(p)
print('speech',round(t,2))
src=glob.glob('/root/.claude/uploads/042058c6-22a1-50c5-89b1-6e542c5bd208/a6191b5a*.mp4')[0]
fc=[];v=[];au=[]
for i,(lab,s,e,o) in enumerate(pieces):
    sc="scale=1512:2688:flags=lanczos,setsar=1,crop=1080:1920:216:160" if lab.startswith('S2') else "scale=1426:2534:flags=lanczos,setsar=1,crop=1080:1920:173:0"
    d=e-s; f=0.012
    fc.append(f"[0:v]trim={s:.3f}:{e:.3f},setpts=PTS-STARTPTS,fps=30,{sc}[v{i}]"); v.append(f"[v{i}]")
    fc.append(f"[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS,afade=t=in:d={f},afade=t=out:st={d-f:.3f}:d={f}[a{i}]"); au.append(f"[a{i}]")
fc.append(''.join(v)+f"concat=n={len(pieces)}:v=1:a=0[vo]"); fc.append(''.join(au)+f"concat=n={len(pieces)}:v=0:a=1[ao]")
open(f'{S}/main/fc_t5.txt','w').write(';\n'.join(fc))
subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-filter_complex_script',f'{S}/main/fc_t5.txt','-map','[vo]','-map','[ao]','-c:v','libx264','-crf','12','-preset','fast','-pix_fmt','yuv420p','-c:a','pcm_s16le','-ar','48000',f'{S}/main/teaser_cut5.mov'],check=True)
os.makedirs(f'{S}/tf5',exist_ok=True)
subprocess.run(['ffmpeg','-v','error','-y','-i',f'{S}/main/teaser_cut5.mov','-q:v','2',f'{S}/tf5/%05d.jpg'],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-i',f'{S}/main/teaser_cut5.mov','-vn','-c:a','pcm_s16le',f'{S}/tspeech5_raw.wav'],check=True)
N=len(os.listdir(f'{S}/tf5'))
# remove light-leak/flash residue: inside each piece, a frame that does not match the piece's look
# (orange flash, or a colour frame inside a B&W shot) is replaced with the nearest clean frame
sat=[np.array(Image.open(f'{S}/tf5/{i:05d}.jpg').resize((90,160)).convert('HSV'))[...,1].mean() for i in range(1,N+1)]
fixed=[]
for lab,s,e,o in pieces:
    f0=int(round(o*30))+1; f1=min(int(round((o+e-s)*30)),N)
    rng=list(range(f0,f1+1)); gray=np.median([sat[i-1] for i in rng])<25
    bad=[i for i in rng if sat[i-1]>100 or (gray and sat[i-1]>=25)]
    good=[i for i in rng if i not in bad]
    for b in bad:
        g=min(good,key=lambda k:abs(k-b)); Image.open(f'{S}/tf5/{g:05d}.jpg').save(f'{S}/tf5/{b:05d}.jpg',quality=95); fixed.append(b)
# freeze frame on the cliffhanger
last=N
for k in range(1,int(round(FREEZE*30))+1):
    Image.open(f'{S}/tf5/{last:05d}.jpg').save(f'{S}/tf5/{last+k:05d}.jpg',quality=95)
print('frames',N,'+freeze',int(round(FREEZE*30)),'fixed',fixed)
