import json, subprocess, glob
S='/tmp/claude-0/-home-user-motion/042058c6-22a1-50c5-89b1-6e542c5bd208/scratchpad'
src=glob.glob('/root/.claude/uploads/042058c6-22a1-50c5-89b1-6e542c5bd208/a6191b5a*.mp4')[0]
P=json.load(open(f'{S}/main/edl.json'))
fc=[];v=[];a=[]
for i,(lab,s,e,o) in enumerate(P):
    d=e-s; f=0.012
    fc.append(f"[0:v]trim={s:.3f}:{e:.3f},setpts=PTS-STARTPTS,fps=30[v{i}]")
    fc.append(f"[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS,afade=t=in:d={f},afade=t=out:st={d-f:.3f}:d={f}[a{i}]")
    v.append(f"[v{i}]"); a.append(f"[a{i}]")
fc.append(''.join(v)+f"concat=n={len(P)}:v=1:a=0[vo]")
fc.append(''.join(a)+f"concat=n={len(P)}:v=0:a=1[ao]")
open(f'{S}/main/fc.txt','w').write(';\n'.join(fc))
subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-filter_complex_script',f'{S}/main/fc.txt','-map','[vo]','-map','[ao]','-c:v','libx264','-crf','12','-preset','fast','-pix_fmt','yuv420p','-c:a','pcm_s16le','-ar','48000',f'{S}/main/cut.mov'],check=True)
