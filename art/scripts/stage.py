import sys, random, math; sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from pix import *
from hero import A
from PIL import Image, ImageDraw
random.seed(7)
VW, VH, T = 427, 240, 16
im = Image.new('RGBA', (VW, VH)); px = im.load()
def hexc(h, a=255): h=h.lstrip('#'); return (int(h[0:2],16),int(h[2:4],16),int(h[4:6],16),a)
def put(x,y,c):
    if 0<=x<VW and 0<=y<VH: px[x,y]=c
def blend(x,y,c,a):
    if 0<=x<VW and 0<=y<VH:
        o=px[x,y]; px[x,y]=tuple(int(o[i]*(1-a)+c[i]*a) for i in range(3))+(255,)
def rect(x,y,w,h,c):
    for j in range(y,y+h):
        for i in range(x,x+w): put(i,j,c)
# ---------- 背景：夜空 ----------
top, bot = hexc('#141b30'), hexc('#2b3a5e')
for y in range(VH):
    t=y/VH; c=tuple(int(top[i]*(1-t)+bot[i]*t) for i in range(3))+(255,)
    for x in range(VW): px[x,y]=c
# 远景：冻结的钟楼群
far=hexc('#22304d'); farL=hexc('#2e3f62')
def tower(cx, w, h, clock=True):
    y0=VH-h
    rect(cx-w//2, y0, w, h, far)
    for k in range(w//2+2):                      # 尖顶
        rect(cx-w//2+k, y0-k*2-2, w-2*k, 2, far)
    if clock:
        r=w//3; cy=y0+r+6
        for j in range(-r,r+1):
            for i in range(-r,r+1):
                if i*i+j*j<=r*r: put(cx+i,cy+j,farL)
        rect(cx, cy-r+2, 1, r-1, far); rect(cx, cy, r-2, 1, far)
    for j in range(y0+6, VH, 9):                 # 窗
        for i in range(cx-w//2+3, cx+w//2-3, 6): rect(i,j,2,3,hexc('#3c5378'))
for cx,w,h in [(40,26,150),(120,34,185),(215,22,130),(300,40,200),(395,28,160)]: tower(cx,w,h)
# 中景：冰冻管道
mid=hexc('#2a3b5c'); midL=hexc('#3d5580')
for y0 in (118, 150):
    rect(0,y0,VW,7,mid); rect(0,y0,VW,1,midL)
    for x in range(10,VW,46): rect(x,y0-2,5,11,hexc('#34496f'))
    for x in range(0,VW,3):                       # 管道下挂的小冰锥
        if random.random()<0.25:
            L=random.randint(1,4)
            for k in range(L): put(x,y0+7+k,hexc('#6f97c4'))
# ---------- 地图 ----------
G=[list(r) for r in [
"###########................",
"###########................",
"##########.................",
"...........................",
"...........................",
"...........................",
".......................####",
"...........................",
"....----...............####",
"...........................",
"...........................",
".......................####",
"#########~~~~~####IIIII####",
"#########~~~~~####IIIII####",
"#########~~~~~####IIIII####",
]]
for r in range(6,15):
    for c in range(23,27): G[r][c]='#'
H_,W_=len(G),len(G[0])
def at(c,r): return G[r][c] if 0<=r<H_ and 0<=c<W_ else '.'
stone=[hexc('#3a4864'),hexc('#44547a'),hexc('#334058')]
for r in range(H_):
    for c in range(W_):
        t=at(c,r); x0,y0=c*T,r*T
        if t=='#':
            for j in range(T):
                for i in range(T):
                    k=0 if (j//4+i//8+(j//8))%2 else 1
                    col=stone[k] if random.random()>0.08 else stone[2]
                    if j%8==7 or (i+(8 if (j//8)%2 else 0))%16==15: col=hexc('#28324a')   # 砖缝
                    put(x0+i,y0+j,col)
            if at(c,r-1) not in '#':                 # 雪顶
                for i in range(T):
                    d=2+(1 if (i*7+c*3)%5==0 else 0)
                    for j in range(d): put(x0+i,y0+j,hexc('#eaf5ff') if j<d-1 else hexc('#b9d6ee'))
                    if (i*5+c)%7==0: put(x0+i,y0+d,hexc('#b9d6ee'))
            if at(c,r+1)=='.' and r<3:              # 天花板下的冰锥
                for i in range(1,T,4):
                    L=3+((i*3+c*5)%6)
                    for k in range(L):
                        w=max(0,2-k*2//L)
                        for q in range(-w//2, w//2+1): put(x0+i+q,y0+T+k,hexc('#a9d8f5') if q<=0 else hexc('#6fa8d6'))
        elif t=='I':                                  # 冰（规则生效后的水）
            for j in range(T):
                for i in range(T):
                    col=hexc('#8fcbea')
                    if (i+j)%11==0 or (i+j)%11==1: col=hexc('#c9ecff')
                    if j>12: col=hexc('#79b5da')
                    put(x0+i,y0+j,col)
            if at(c,r-1)!='I' and at(c,r-1)!='#':
                rect(x0,y0,T,1,hexc('#ffffff')); rect(x0,y0+1,T,1,hexc('#dff4ff'))
        elif t=='-':
            rect(x0,y0,T,3,hexc('#8a96ab')); rect(x0,y0,T,1,hexc('#c4ccd9'))
            for i in (2,7,12): rect(x0+i,y0+3,2,3,hexc('#55607a'))
# 水（半透明，带“规则光”描边提示：这块能被规则改写）
for r in range(H_):
    for c in range(W_):
        if at(c,r)!='~': continue
        x0,y0=c*T,r*T
        surf=at(c,r-1)!='~'
        for j in range(T):
            for i in range(T):
                wave=int(1.2*math.sin((x0+i)*0.35)) if surf else 0
                if surf and j<1+wave: continue
                blend(x0+i,y0+j,hexc('#3a8fd6'),0.55)
                if surf and j==1+wave: blend(x0+i,y0+j,hexc('#d6f0ff'),0.85)
        for j in range(T):
            if at(c-1,r)=='#' or at(c-1,r)=='.': blend(x0,y0+j,hexc('#c58cff'),0.6)
            if at(c+1,r)=='#': blend(x0+T-1,y0+j,hexc('#c58cff'),0.6)
        if r==H_-1 or at(c,r+1)!='~':
            pass
# 规则光：冰块边缘一圈淡紫色
for r in range(H_):
    for c in range(W_):
        if at(c,r)=='I':
            if at(c-1,r)!='I':
                for j in range(T): blend(c*T,r*T+j,hexc('#c58cff'),0.45)
            if at(c+1,r)!='I':
                for j in range(T): blend(c*T+T-1,r*T+j,hexc('#c58cff'),0.45)
# 冰面下冻住的鱼（背景叙事）
fish=[(5,0,'#e08a5a'),(4,1,'#e08a5a'),(5,1,'#e08a5a'),(6,1,'#e08a5a'),(7,1,'#101a2b'),(5,2,'#e08a5a'),(3,1,'#c46a1c'),(2,0,'#c46a1c'),(2,2,'#c46a1c')]
for fx,fy,col in fish:
    for a in range(2):
        for b in range(2): blend(19*T+2+fx*2+a, 13*T+4+fy*2+b, hexc(col), 0.8)
# ---------- 角色 ----------
hero=sprite(A)
im.alpha_composite(hero,(7*T-4, 12*T-32))
# 子弹 + 枪口火光
for (bx,by,r) in [(7*T+26,12*T-13,2),(7*T+70,12*T-13,2)]:
    for j in range(-r-1,r+2):
        for i in range(-r-1,r+2):
            d=i*i+j*j
            if d<=r*r: put(bx+i,by+j,hexc('#ffffff'))
            elif d<=(r+1)**2: put(bx+i,by+j,hexc('#fff59d'))
# 小敌人：冰壳巡逻兵（站在冰面上）
enemy=[
"....KKKKKKKK....",
"...KLLWLLLLLK...",
"..KLLBBBBBBBLK..",
"..KBBBBBBBBBBK..",
".KBBKKKKKKKBBBK.",
".KBBKRRKKRRKBBK.",
".KbBKKKKKKKKBbK.",
".KbbBBBBBBBBbbK.",
"..KbbbbbbbbbbK..",
"...KKKKKKKKKK...",
"...KgK....KgK...",
"..KggK....KggK..",
"..KKKK....KKKK..",
]
pal2=dict(PAL); pal2.update({'B':'#7fb6dc','L':'#cfeaff','b':'#4f86b3'})
im.alpha_composite(sprite(enemy,16,pal2),(20*T, 12*T-13))
# 飘雪
for _ in range(120):
    x=random.randint(0,VW-1); y=random.randint(0,VH-1)
    blend(x,y,hexc('#ffffff'),random.choice([0.35,0.6,0.9]))
# ---------- HUD ----------
rect(8,8,8,68,hexc('#101a2b'))
for i in range(16):
    rect(10, 10+i*4, 4, 3, hexc('#fff59d') if i>=3 else hexc('#3a3d46'))
for k in range(2):
    y=82+k*12; rect(8,y,10,10,hexc('#101a2b'))
    rect(9,y+1,8,8,hexc('#81d4fa') if k==0 else hexc('#262b36'))
    if k==0:
        for (i,j) in [(2,2),(5,2),(3,3),(4,3),(3,4),(4,4),(2,5),(5,5),(3,6),(4,6)]: put(9+i,y+1+j,hexc('#0d2b52'))
im.save('stage_raw.png')
# ---------- 展示板 ----------
S=3
board=Image.new('RGB',(VW*S+80, VH*S+200),'#101218'); d=ImageDraw.Draw(board)
d.text((40,22),'画风样板：霜钟关（427×240 原始分辨率，放大 3 倍）',font=font(28),fill='#e8ecf2')
board.paste(up(im,S).convert('RGB'),(40,80))
notes=['远景：冻结的钟楼群，低饱和蓝灰，不与地形抢眼',
       '可站立地形：砖石 + 雪顶亮边；冰面带白色顶边',
       '淡紫色描边 = “规则光”：这块东西能被芯片改写（左边是水，右边已冻成冰）',
       '冰面下冻住的鱼、管道上的冰锥：用背景交代“断律之夜”的后果']
for i,n in enumerate(notes): d.text((40, VH*S+96+i*24),'· '+n,font=font(18),fill='#aab2c0')
board.save('stage_mockup.png')
print('ok')
