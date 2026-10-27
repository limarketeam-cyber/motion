"""Builds reel.html — the 1-minute Instagram Reel in the Hamahang visual identity.
Timings come from reel_edl.json (source time -> reel time).  Run: python3 reel_build.py
Rules kept from the teasers: speaker shots use white + red only (flags excepted); graphics near the
head sit BEHIND the speaker; chest text at one fixed spot (centred, on the lapel mic); boards are
60 white / 30 ink / 10 blue on the brand light gradient; everything inside the Instagram safe zone."""
import json, os, re

E = json.load(open('reel_edl.json')); PC = E['pieces']; SPEECH = E['speech_end']
END = round(SPEECH + 3.0, 3)


def N(src):
    """reel time of a source time (a time inside a removed pause snaps to the next kept piece)."""
    for p in PC:
        if src < p[1] - 1e-6: return p[3]
        if src <= p[2] + 1e-6: return round(p[3] + src - p[1], 3)
    return SPEECH


RED, INK, BLUE, SEC = '#D32F2F', '#262426', '#002CB0', '#567B9F'


def icon(name, recolor, draw=False):
    s = open(f'assets/brand/icons/{name}.svg', encoding='utf-8').read()
    s = re.sub(r'<title>.*?</title>', '', s)
    s = re.sub(r'<svg[^>]*>', '<svg viewBox="0 0 96 96" xmlns="http://www.w3.org/2000/svg">', s, count=1)
    s = re.sub(r' xmlns="http://www.w3.org/2000/svg"(?= (d|x|cx|points|x1)=)', '', s)
    for a, b in recolor.items(): s = s.replace(a, b)
    if draw:
        s = re.sub(r'<(path|rect|circle|line|polyline|ellipse)((?:(?!/>)[^>])*fill="none"[^>]*?)/>', r'<\1 pathLength="1"\2/>', s)
    return s


ON_ACTOR = lambda n: icon(n, {INK: RED}, draw=True)                 # red line icon (speaker shots)
ON_BOARD = lambda n: icon(n + '-color', {SEC: INK, RED: BLUE})      # ink structure, blue accent (boards)

# ---------------- big white line icons behind the speaker (layout from the client's reference frames) ----------------
# id: (icon / F:flag, red label or None, size, target x, target y)  — flags are 3:2, icons square
ICONS = {
    'i_vn': ('F:VN', 'ویتنام', 170, 90, 330), 'i_cn': ('F:CN', 'چین', 170, 830, 320),
    'i_kr': ('F:KR', 'کره', 150, 90, 600), 'i_in': ('F:IN', 'هند', 150, 850, 600),
    'i_shield': ('warranty', None, 300, 50, 380), 'i_q1': ('faq', None, 260, 770, 330),
    'i_call': ('call-center', 'دوستم', 230, 800, 320), 'i_phone': ('phone-rear', 'A57', 240, 790, 320),
    'i_ex': ('warning', None, 300, 50, 380), 'i_vn2': ('F:VN', None, 220, 60, 380), 'i_mute': ('mute', None, 280, 770, 330),
    'i_gear1': ('gear', None, 300, 40, 440), 'i_fac': ('factory', None, 330, 690, 290), 'i_gear2': ('gear', None, 240, 720, 620),
    'i_model': ('phone-front', 'مدل دقیق', 210, 830, 300), 'i_ram': ('ram', 'رم', 230, 790, 600), 'i_sto': ('storage', 'حافظه', 210, 60, 420),
    'i_cart': ('cart', None, 300, 50, 370), 'i_price': ('price', None, 280, 770, 340), 'i_pay': ('payment', None, 240, 60, 400),
    'i_disc': ('discount', None, 300, 50, 380), 'i_q2': ('faq', None, 280, 760, 320), 'i_q3': ('faq', None, 200, 80, 650),
}
POS = json.load(open('reel_icons.json')) if os.path.exists('reel_icons.json') else {}
WHITE = lambda n: icon(n, {INK: '#FFFFFF'}, draw=True)


def icon_html(iid):
    kind, lab, sz, x, y = ICONS[iid]; up = False
    if iid in POS: x, y, sz, up = POS[iid]
    fl = kind.startswith('F:'); h = round(sz * 2 / 3) if fl else sz
    inner = f'<img src="assets/brand/flags/{kind[2:]}.svg">' if fl else WHITE(kind)
    lb = f'<div class="lb{" ltr" if lab[0].isascii() else ""}">{lab}</div>' if lab else ''
    return f'<div class="ic{" fl" if fl else ""}{" up" if up else ""}" id="{iid}" style="left:{x}px;top:{y}px;width:{sz}px;height:{h}px">{inner}{lb}</div>'


icons = '\n'.join(icon_html(i) for i in ICONS)
# chapter bar (reference frame 1) and the big red shield over the chest (reference frame 2) — front layer
chapter = '<div class="chap" id="ch2"><i class="bar"></i><b>تکنولوژی تولید</b><span class="no">02</span></div>'
shield = f'<div id="fsh">{icon("warranty", {INK: RED}, draw=True)}</div>'

# ---------------- subtitles (brand subtitle plate) ----------------
LINES = [(0.10, 2.30, 'واقعاً کشور تولیدکننده'), (2.30, 4.33, 'کیفیت گوشی‌های سامسونگ رو تضمین می‌کنه؟'),
         (22.10, 23.90, 'امروز دوستم با من تماس گرفت'), (24.10, 26.00, 'گفت یه دونه A57 سامسونگ می‌خوام'),
         (26.20, 28.70, 'خیلی تأکید داشت که حتماً، حتماً'), (28.70, 29.44, 'ویتنام باشه'),
         (34.95, 36.22, 'اما گوشش بدهکار نبود'),
         (52.44, 54.40, 'سامسونگ توی صفحه‌ی پشتیبانی'), (54.40, 55.37, 'سه تا نکته رو گفته'),
         (55.37, 58.64, 'یک: محصولاتی که توی کارخونه‌ها تولید می‌شن'), (60.77, 63.46, 'همگی از نظر کیفیت یکسان هستن'),
         (63.46, 67.30, 'دو: تکنولوژی تولید توی تمام این کارخونه‌ها'), (67.41, 68.68, 'با همدیگه برابره'),
         (68.68, 73.50, 'سه: تمام محصولات قبل از عرضه چندین مرحله'), (73.63, 76.90, 'از نظر اینکه با استانداردهای رسمی سامسونگ'),
         (76.90, 78.72, 'یکی باشن چک می‌شن'),
         (103.75, 105.50, 'باید چهارتا چیز رو در نظر بگیریم'), (105.50, 107.45, 'یک: مدل دقیق دستگاه'),
         (107.66, 109.30, 'دو: رم اون دستگاه'), (109.30, 111.35, 'سه: حافظه‌ی اون دستگاه'),
         (111.47, 114.48, 'چهار و مهم‌ترینشون: گارانتی اون دستگاه'),
         (128.95, 131.40, 'توی سایت هماهنگ که همه‌شون یک قیمتن'), (131.60, 133.90, 'اما اگه خواستی از جای دیگه بخری'),
         (134.05, 135.94, 'دو، سه میلیون و بیشتر هزینه کنی'), (138.22, 139.40, 'این اختلاف قیمت'),
         (139.57, 141.41, 'دقیقاً بابت چه تفاوتیه؟')]
SUBS = []
for a_, b_, txt in LINES:
    ra, rb = N(a_), N(b_ - 0.01)
    if rb - ra > 0.25: SUBS.append([round(ra, 3), round(rb, 3), txt])
for k in range(len(SUBS) - 1): SUBS[k][1] = min(SUBS[k][1], SUBS[k + 1][0])
subs = '<div id="sub"><div class="sp"><span></span><i></i></div></div>'

# ---------------- chest text (white words, key word on a red plate) ----------------
KT = {'k1': [('کشورِ', 1), ('سازنده', 0)], 'k2': [('کیفیت', 1), ('رو تضمین می‌کنه؟', 0)],
      'k3': [('دوستم', 0), ('زنگ زد', 1)], 'k4': [('Galaxy', 0), ('A57', 1)], 'k5': [('حتماً،', 0), ('حتماً!', 1)],
      'k6': [('ویتنام', 1), ('باشه!', 0)], 'k7': [('گوشش', 0), ('بدهکار نبود', 1)],
      'k8': [('توی', 0), ('همه‌ی', 1), ('کارخونه‌ها', 0)], 'k9': [('همه‌جا', 0), ('یکسان', 1)],
      'k10': [('۴', 1), ('تا چیز رو چک کن', 0)], 'k11': [('مهم‌ترین:', 0), ('گارانتی', 1)],
      'k12': [('جای دیگه', 1), ('بخری؟', 0)], 'k13': [('۲ تا ۳ میلیون', 1), ('بیشتر؟', 0)],
      'k14': [('این', 0), ('اختلاف قیمت', 1)], 'k15': [('دقیقاً بابت', 0), ('چه تفاوتیه؟', 1)]}
kts = '\n'.join(f'<div class="kt{" ltr" if k == "k4" else ""}" id="{k}">' + ''.join(
    f'<span class="w{" key" if key else ""}">{w}</span>' for w, key in ws) + '</div>' for k, ws in KT.items())

# ---------------- boards ----------------
fac = ON_BOARD('factory'); chk = icon('check', {INK: BLUE}); chk_w = icon('check', {INK: '#FFFFFF'})
board = f'''
<div id="board" class="postbg">
  <div id="dbg"></div>
  <div class="bignum" id="n1" style="right:-200px;top:960px">۱</div>
  <div class="bignum" id="n3" style="left:-200px;top:1000px">۳</div>
  <!-- A: Samsung support page, 3 points -->
  <div class="scene" id="sA">
    <div class="stile" id="aTile" style="left:820px;top:300px"><div class="f3 acc-b"><svg viewBox="0 10 24 4"><use href="#samsung-path"/></svg></div></div>
    <div class="note" id="aNote" style="right:280px;top:316px;width:600px">صفحه‌ی <b>رسمی</b><br>پشتیبانی سامسونگ</div>
    <svg class="arrow" id="aArr" style="left:740px;top:470px;width:150px;height:100px" viewBox="0 0 150 100"><path class="dash" d="M120 4 C 120 56, 80 84, 20 90"/><path class="head" d="M34 74 L16 91 L38 100"/></svg>
    <div class="bcard" id="aCard" style="left:70px;top:590px;width:940px;padding:0 0 22px">
      <img class="shot" src="assets/ev/community_url.jpg" style="border-bottom:2px solid #eee">
      <div style="position:relative;margin:18px 28px 0"><img class="shot" src="assets/ev/community_par.jpg">
        <div class="hl" id="aH1" style="left:51.3%;top:70.6%;width:44.5%;height:11.7%"></div>
        <div class="hl" id="aH2" style="left:1.6%;top:86.9%;width:55%;height:11.7%"></div></div>
      <div class="fa" id="aFa">«گوشی‌ای که توی کارخونه‌ی ویتنام ساخته شده، ذاتاً از نمونه‌ی ساخت اندونزی بهتر نیست.»</div>
    </div>
    <div class="tags" id="aTags" style="top:1210px"><span class="ix b">۱</span><span class="ix b">۲</span><span class="ix b">۳</span><b>نکته</b></div>
  </div>
  <!-- B: point 1 — factories -->
  <div class="scene" id="sB">
    <div class="hdr" id="bHdr" style="top:320px"><span class="ix b">۱</span>کارخونه‌ها</div>
    {''.join(f'<div class="bico" id="bF{i}" style="left:{x}px;top:520px">{fac}</div>' for i, x in ((1, 90), (2, 430), (3, 770)))}
    {''.join(f'<div class="bflag" id="bG{i}" style="left:{x}px;top:770px"><img src="assets/brand/flags/{c}.svg"><span>{n}</span></div>' for i, x, c, n in ((1, 120, 'CN', 'چین'), (2, 460, 'IN', 'هند'), (3, 800, 'VN', 'ویتنام')))}
    <div class="eq" id="bE1" style="left:332px;top:560px">=</div><div class="eq" id="bE2" style="left:672px;top:560px">=</div>
    <div class="pill" id="bPill" style="top:1010px">{chk_w}کیفیت یکسان</div>
  </div>
  <!-- C: point 3 — quality control + official report -->
  <div class="scene" id="sC">
    <div class="hdr" id="cHdr" style="top:320px"><span class="ix b">۳</span>کنترل کیفیت قبل از عرضه</div>
    <div class="bico big" id="cPhone" style="left:80px;top:500px">{ON_BOARD('phone-front')}</div>
    <div class="bico" id="cMag" style="left:200px;top:600px;width:200px;height:200px">{ON_BOARD('search')}</div>
    <div class="bcard steps" id="cList" style="left:470px;top:520px;width:530px">
      <div class="stp">{chk}مرحله‌ی اول</div><div class="stp">{chk}مرحله‌ی دوم</div><div class="stp">{chk}مرحله‌ی سوم</div></div>
    <div class="stamp" id="cStamp" style="top:1010px">استاندارد رسمی سامسونگ</div>
    <div class="stile" id="cTile" style="left:820px;top:300px"><div class="f3 acc-b"><svg viewBox="0 10 24 4"><use href="#samsung-path"/></svg></div></div>
    <div class="note" id="cNote" style="right:280px;top:316px;width:600px">گزارش <b>رسمی</b><br>سامسونگ ـ ۲۰۲۴</div>
    <div class="quote" id="cQ" style="left:70px;top:590px;width:940px">
      <div class="en">“…the highest quality products that satisfy customers are produced <mark>uniformly no matter where they are produced.</mark>”</div>
      <div class="fa2">«محصولات، هر جا که تولید بشن، با یک کیفیت یکسان ساخته می‌شن.»</div>
      <div class="src">— Samsung Electronics Sustainability Report 2024</div></div>
  </div>
  <!-- D: same price on Hamahang -->
  <div class="scene" id="sD">
    <div class="headline" id="dHead" style="top:330px">توی سایت هماهنگ<br><b>همه یک قیمتن</b></div>
    <div class="bcard shop" id="dCard" style="left:90px;top:640px;width:900px">
      <div class="hd"><span>www.hamahang.shop</span><img src="assets/brand/logo-white.svg" alt="گروه هماهنگ"></div>
      {''.join(f'<div class="r" id="dR{i}"><img class="f" src="assets/brand/flags/{c}.svg"><div class="m">Galaxy A57</div><div class="p">یک قیمت</div></div>' for i, c in ((1, 'VN'), (2, 'IN'), (3, 'CN')))}
    </div>
  </div>
</div>'''
endc = '''
<div id="endc"><i class="panel"></i><i class="bar"></i>
  <div class="in"><img class="lg" src="assets/brand/logo-white.svg" alt="گروه هماهنگ">
  <div class="site">www.hamahang.shop</div><div class="ig">@hamahang_shop</div></div></div>'''
WIPES = '''
<div id="wipe">
  <div class="ws wi"><i style="background:#262426"></i><i style="background:#D32F2F"></i><i style="background:#DFE7ED"></i></div>
  <div class="ws wo"><i style="background:#567B9F"></i><i style="background:#262426"></i><i style="background:#D32F2F"></i></div>
  <div class="ws v"><i style="background:#D32F2F"></i><i style="background:#567B9F"></i><i style="background:#262426"></i></div>
</div>'''
defs = re.search(r'<svg width="0" height="0" style="position:absolute"><defs>.*?</defs></svg>', open('teaser4.html', encoding='utf-8').read(), re.S).group(0)

CSS = open('reel.css', encoding='utf-8').read()
html = f'''<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<title>ریل سامسونگ ویتنام — هماهنگ</title>
<style>
{CSS}
</style>
</head>
<body>
{defs}
<div id="stage">
  <div id="cam">
    <img id="vid" alt="">
    <div id="behind">
{icons}
    </div>
    <div id="actor"><img id="vid2" alt=""></div>
  </div>
  <div class="layer" id="fx">
{kts}
{chapter}
{shield}
  </div>
{board}
{subs}
{endc}
{WIPES}
</div>
<script src="assets/gsap.min.js"></script>
<script>
const PIECES={json.dumps(PC)}, SPEECH={SPEECH}, END={END}, SUBS={json.dumps(SUBS, ensure_ascii=False)};
const FPS=30, FRAMES='rf', MASKS='rmasks', VIDEO_FRAMES={len([f for f in os.listdir('rf') if f.endswith('.jpg')]) if os.path.exists('rf') else 1711};
{open('reel_timeline.js', encoding='utf-8').read()}
</script>
</body>
</html>'''
# reel times of the source cue points used in the timeline
T = {k: N(v) for k, v in dict(
    k1=0.0, k2=2.3, call=22.1, k4=24.1, k5=26.2, k6=28.7, k7=34.93,
    BA=52.44, aThree=54.4, P1=55.37, P1eq=58.3, P1same=60.9, P2=63.46, P2b=67.41,
    P3=68.68, P3s1=69.36, P3s2=70.63, P3s3=71.94, P3std=73.63, P3ev=75.6,
    L=103.75, r1=105.5, r2=107.66, r3=109.35, r4=111.47,
    D=128.95, D2=131.6, M=134.05, X1=138.22, X2=139.57).items()}
T['SPEECH'] = SPEECH; T['END'] = END
html = html.replace('const PIECES=', 'const T=' + json.dumps(T) + ';\nconst PIECES=', 1)
open('reel.html', 'w', encoding='utf-8').write(html)
print('written reel.html', len(html)); print(T)
