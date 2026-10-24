import subprocess, numpy as np, json, sys
from PIL import Image
src=sys.argv[1]; out=sys.argv[2]
W,H=1080,80; Y0=815; FPS=10
p=subprocess.Popen(['ffmpeg','-v','error','-i',src,'-vf',f'fps={FPS},crop={W}:{H}:0:{Y0},format=gray','-f','rawvideo','-'],stdout=subprocess.PIPE)
frames=[]
while True:
    b=p.stdout.read(W*H)
    if len(b)<W*H: break
    frames.append(np.frombuffer(b,np.uint8).reshape(H,W))
F=np.array(frames); print(F.shape)
mask=(F>200)
cnt=mask.reshape(len(F),-1).sum(1)
segs=[]; cur=None
for i in range(len(F)):
    has=cnt[i]>300
    if cur is not None:
        d=np.logical_xor(mask[i],mask[cur['ref']]).sum()
        if (not has) or d>0.35*max(mask[cur['ref']].sum(),1):
            cur['e']=i/FPS; segs.append(cur); cur=None
    if cur is None and has:
        cur={'s':i/FPS,'ref':i}
if cur: cur['e']=len(F)/FPS; segs.append(cur)
segs=[s for s in segs if s['e']-s['s']>=0.25]
for k,s in enumerate(segs):
    mid=int((s['s']+s['e'])/2*FPS)
    Image.fromarray(F[mid]).save(f'{out}/sub{k:03d}.png'); s['ref']=mid
json.dump(segs,open(f'{out}/subs.json','w'))
print(len(segs))
for k,s in enumerate(segs): print(k,s['s'],s['e'])
