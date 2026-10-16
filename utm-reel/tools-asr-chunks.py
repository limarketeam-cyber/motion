import sys, json, numpy as np, soundfile as sf, sherpa_onnx
d=sys.argv[1]; m=d+"/sherpa-onnx-whisper-small/"
a,sr=sf.read(d+"/audio16k.wav",dtype="float32")
hop=160; n=len(a)//hop
rms=np.sqrt((a[:n*hop].reshape(n,hop)**2).mean(1)+1e-12); db=20*np.log10(rms)
sm=np.convolve(db,np.ones(5)/5,'same')
floor=np.percentile(sm,10); speech=np.percentile(sm,80); thr=floor+0.35*(speech-floor)
print("floor",floor,"speech",speech,"thr",thr)
quiet=sm<thr
# pauses >= 12 frames (120ms)
pauses=[];i=0
while i<n:
    if quiet[i]:
        j=i
        while j<n and quiet[j]: j+=1
        if j-i>=12: pauses.append((i,j))
        i=j
    else: i+=1
# chunks between pauses
chunks=[];prev=0
for p0,p1 in pauses:
    if p0>prev: chunks.append([prev,p0])
    prev=p1
if prev<n: chunks.append([prev,n])
# merge chunks shorter than 0.8s with next
merged=[]
for c in chunks:
    if merged and (merged[-1][1]-merged[-1][0]<80): merged[-1][1]=c[1]
    else: merged.append(c)
rec=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=m+"small-encoder.int8.onnx",decoder=m+"small-decoder.int8.onnx",tokens=m+"small-tokens.txt",language="fa",task="transcribe",num_threads=4)
out=[]
for c0,c1 in merged:
    s0=max(0,c0*hop-1600); s1=min(len(a),c1*hop+1600)
    st=rec.create_stream(); st.accept_waveform(sr,a[s0:s1]); rec.decode_stream(st)
    out.append(dict(t0=round(c0/100,2),t1=round(c1/100,2),text=st.result.text.strip()))
    print(f"{c0/100:6.2f}-{c1/100:6.2f} {out[-1]['text']}",flush=True)
json.dump(dict(chunks=out,pauses=[(p0/100,p1/100) for p0,p1 in pauses]),open(d+"/asr2.json","w"),ensure_ascii=False,indent=1)
