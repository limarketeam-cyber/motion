import numpy as np, json
db=np.load('main/db.npy')  # 10ms frames
def fr(t): return int(round(t*100))
def sm(x,k=5): return np.convolve(x,np.ones(k)/k,'same')
dbs=sm(db)
def quiet(t,win=0.22):
    a,b=fr(t-win),fr(t+win); i=a+int(np.argmin(dbs[a:b])); return i/100
# approximate keep ranges (source seconds) with labels
KEEP=[
 ('A',0.0,4.65),
 ('C',22.0,29.45),
 ('D',34.9,36.35),
 ('G',52.35,55.5),
 ('H1a',55.5,58.55),
 ('H1b',60.85,63.55),
 ('H2',63.55,68.6),
 ('H3',68.75,78.65),
 ('L',103.75,114.55),
 ('N',128.9,141.25),
]
FIX={('A','e'):4.33,('C','s'):21.86,('D','e'):36.22}
out=[]
for lab,s,e in KEEP:
    s2 = 0.0 if s==0 else quiet(s); e2=quiet(e)
    s2=FIX.get((lab,'s'),s2); e2=FIX.get((lab,'e'),e2)
    out.append([lab,s2,e2])
# tighten long internal pauses
TH=-36; MINP=0.30; KEEPPAD=0.09
pieces=[]
for lab,s,e in out:
    a,b=fr(s),fr(e); q=dbs[a:b]<TH
    cur=s; i=0
    while i<len(q):
        if q[i]:
            j=i
            while j<len(q) and q[j]: j+=1
            if (j-i)/100>=MINP and i>0 and j<len(q):
                ps=(a+i)/100+KEEPPAD; pe=(a+j)/100-KEEPPAD
                pieces.append([lab,cur,ps]); cur=pe
            i=j
        else: i+=1
    pieces.append([lab,cur,e])
tot=0; t=0
for p in pieces: p.append(t); t+=p[2]-p[1]
print('pieces',len(pieces),'total',round(t,2))
for p in pieces: print(p[0],round(p[1],2),round(p[2],2),'->',round(p[3],2))
json.dump(pieces,open('main/edl.json','w'))
