# Build the vector replica of the poster as an animated SVG page
import json, numpy as np
L = np.array([(435.39,527),(415.95,535),(392.8,545),(368.4,555),(344.62,565),(321.2,575),(308.44,580)])
Rr = np.array([(479.06,527),(467.84,535),(454.32,545),(441.04,555),(427.56,565),(415.34,575),(407.88,580)])
aL, bL = np.polyfit(L[:, 1], L[:, 0], 1); aR, bR = np.polyfit(Rr[:, 1], Rr[:, 0], 1)
DB, FLOOR = 523.7, 582.6
beam = dict(LT=aL * DB + bL, RT=aR * DB + bR, LB=aL * FLOOR + bL, RB=aR * FLOOR + bR, top=DB, bot=FLOOR)
logo = json.load(open('logo_paths.json'))
P = dict(
  BEAM=json.dumps(beam),
  LOGO_GRAY=logo['gray'],
)
html = open('scene_template.html').read()
for k, v in P.items(): html = html.replace('%%' + k + '%%', str(v))
open('scene.html', 'w').write(html)
print(beam)
