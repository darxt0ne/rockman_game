"""敌人精灵 v2：机械结构 + 分层明暗 + 手工细节"""
import sys, math; sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from pix import font, up
from PIL import Image, ImageDraw
def hx(c): c=c.lstrip('#'); return (int(c[0:2],16),int(c[2:4],16),int(c[4:6],16),255)
RAMP = {
 'orange':['#5e240a','#9c4016','#d96a24','#ff9c45','#ffd08a'],
 'metal': ['#1c212b','#353d4d','#5b6579','#939fb4','#d3dbe8'],
 'dark':  ['#0e1118','#1a1e27','#262c38','#363e4e','#4a5468'],
 'ice':   ['#3d6c9c','#5a8fc0','#93c9ec','#c8ebff','#ffffff'],
 'stone': ['#2e323c','#4a4f5c','#6c7282','#9aa0ae','#cdd2dc'],
 'green': ['#16351f','#24603a','#35924f','#5ec47a','#a8eab6'],
 'red':   ['#4a0d14','#8a1a26','#d0343e','#ff6a6a','#ffb4b4'],
 'purple':['#24143c','#432570','#6a3fa8','#9a6ad8','#d2b4f5'],
 'glass': ['#06101c','#0b1a2c','#12283f','#1d3b5a','#2f5a80'],
}
OUT=hx('#0a101c'); EYE=hx('#48f0d8'); EYE2=hx('#0f8a7a'); WHITE=hx('#ffffff')
YEL=hx('#ffe066'); YEL2=hx('#c98a10'); BLK=hx('#16181e')
class C:
    def __init__(s,w,h): s.w,s.h=w,h; s.im=Image.new('RGBA',(w,h),(0,0,0,0)); s.p=s.im.load()
    def px(s,x,y,c):
        if 0<=x<s.w and 0<=y<s.h: s.p[x,y]=c
    def r(s,ramp,i): return hx(RAMP[ramp][i])
    def box(s,x0,y0,x1,y1,ramp,round_=True):
        """分层明暗的圆角方块：顶/左受光，底/右背光"""
        R=RAMP[ramp]
        for y in range(y0,y1+1):
            for x in range(x0,x1+1):
                if round_ and (x in (x0,x1)) and (y in (y0,y1)): continue
                c=2
                if y==y0: c=4 if x<(x0+x1)//2 else 3
                elif x==x0: c=3
                elif y==y1: c=0
                elif x==x1: c=1
                elif y==y1-1: c=1
                s.px(x,y,hx(R[c]))
    def disc(s,cx,cy,r,ramp,lo=0):
        R=RAMP[ramp]
        for y in range(int(cy-r-1),int(cy+r+2)):
            for x in range(int(cx-r-1),int(cx+r+2)):
                dx,dy=x+0.5-cx,y+0.5-cy
                if dx*dx+dy*dy<=r*r:
                    v=-(dx*0.6+dy*0.8)/r              # 左上受光
                    k=2+round(v*1.6); k=max(lo,min(4,k))
                    s.px(x,y,hx(R[k]))
    def ellipse(s,cx,cy,rx,ry,ramp):
        R=RAMP[ramp]
        for y in range(int(cy-ry-1),int(cy+ry+2)):
            for x in range(int(cx-rx-1),int(cx+rx+2)):
                dx,dy=(x+0.5-cx)/rx,(y+0.5-cy)/ry
                if dx*dx+dy*dy<=1:
                    v=-(dx*0.55+dy*0.85); k=max(0,min(4,2+round(v*1.7)))
                    s.px(x,y,hx(R[k]))
    def outline(s):
        p=s.p; out=s.im.copy(); po=out.load()
        for y in range(s.h):
            for x in range(s.w):
                if p[x,y][3]: continue
                if any(0<=x+dx<s.w and 0<=y+dy<s.h and p[x+dx,y+dy][3] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))): po[x,y]=OUT
        s.im=out; s.p=out.load(); return s

def plow_truck(f):
    c=C(28,20)
    # 履带
    c.box(1,13,20,19,'dark')
    for i,x in enumerate(range(2,20,2)):
        c.px(x+(f%2),13,c.r('metal',2)); c.px(x+1-(f%2),19,c.r('metal',1))
    for wx in (4.5,9,13.5,18):
        c.disc(wx,16.5,2.0,'metal')
        c.px(int(wx),16+(f%2),c.r('metal',0))           # 轮毂转动
    # 车身
    c.box(2,7,19,13,'orange')
    for x in range(3,19):                                 # 警示条纹
        on=((x+(12))//2)%2==0
        c.px(x,11,YEL if on else BLK); c.px(x,12,YEL2 if on else BLK)
    c.px(17,9,YEL); c.px(18,9,YEL); c.px(18,8,WHITE)      # 车灯
    for x in (5,9,13): c.px(x,9,c.r('orange',1))          # 铆钉
    # 驾驶舱 + 玻璃 + 眼睛
    c.box(5,1,14,7,'orange')
    c.box(9,2,14,6,'glass',round_=False)
    c.px(9,2,c.r('glass',4)); c.px(10,2,c.r('glass',3))
    for (x,y) in ((12,3),(13,3),(12,4),(13,4)): c.px(x,y,EYE)
    c.px(13,3,WHITE); c.px(11,4,EYE2); c.px(12,5,EYE2)
    # 舱顶积冰
    for x in range(5,15):
        c.px(x,0,c.r('ice',4) if x%3 else c.r('ice',3)); c.px(x,1,c.r('ice',3) if x%2 else c.r('ice',2))
    c.px(7,2,c.r('ice',2)); c.px(11,2,c.r('ice',2))
    # 排气管 + 天线
    c.box(1,2,3,8,'metal'); c.px(2,1,c.r('metal',1))
    c.px(16,0,c.r('metal',3)); c.px(16,1,c.r('metal',2)); c.px(16,2,c.r('metal',2))
    c.px(17,0,hx('#ff5a5a') if f==0 else hx('#8a1a26'))
    # 铲雪板（弯曲金属板 + 警示条纹）
    for y in range(6,19):
        t=(y-6)/12; x0=21+round(3*math.sin(t*math.pi*0.9)-1)
        for k in range(3):
            col=c.r('metal',[4,3,1][k]) if y<17 else c.r('metal',[3,2,0][k])
            if 7<=y<=9: col=(YEL if (y+k)%2 else BLK)
            c.px(x0+k,y,col)
    for y in range(9,16): c.px(20,y,c.r('metal',1))      # 支架
    return c.outline().im

def curling(f):
    c=C(22,24)
    jump = f==1
    by = 0 if jump else 3            # 弹簧压缩时身体下沉
    # 弹簧
    top=15+by; bot=23
    n=(bot-top)//2
    for i in range(n+1):
        y=top+i*2
        for x in range(7,15):
            c.px(x,y,c.r('metal',3) if (x+i)%5 else c.r('metal',4))
        if y+1<=bot:
            for x in range(7,15): c.px(x,y+1,c.r('metal',1))
    c.box(5,22,16,23,'metal')
    # 冰壶石身
    c.ellipse(10.5,9.5+by,9.5,6.5,'stone')
    for x in range(1,21):                                 # 绿色腰带
        for y in (9+by,10+by,11+by):
            if c.p[x,y][3]: c.px(x,y,c.r('green',[4,2,1][y-9-by]))
    for x in range(12,18): c.px(x,10+by,c.r('glass',1))   # 眼缝
    c.px(15,10+by,EYE); c.px(16,10+by,EYE); c.px(16,9+by,WHITE)
    # 花岗岩斑点
    for (x,y) in ((5,6),(8,13),(14,6),(17,13),(4,12),(11,5)): c.px(x,y+by,c.r('stone',1))
    for (x,y) in ((6,5),(12,13),(16,7)): c.px(x,y+by,c.r('stone',4))
    # 顶部手柄（红色握把）
    for y in range(1,5):
        for x in (8,14): c.px(x,y+by,c.r('metal',3)); c.px(x+1,y+by,c.r('metal',1))
    for x in range(7,17): c.px(x,0+by,c.r('red',3) if x<11 else c.r('red',2)); c.px(x,1+by,c.r('red',1))
    # 积霜
    for x in range(4,17,2): c.px(x,3+by,c.r('ice',4))
    return c.outline().im

def drone(f):
    c=C(28,18)
    # 旋翼
    if f==0:
        for x in range(2,26):
            if x not in (12,13,14): c.px(x,1,c.r('metal',3) if (x%3) else c.r('metal',4))
    else:
        for x in range(9,18): c.px(x,1,c.r('metal',4) if x%2 else c.r('metal',2))
    c.box(12,1,14,3,'metal'); 
    # 机身
    c.box(7,4,20,10,'purple')
    for x in range(8,20): c.px(x,4,c.r('ice',3) if x%3 else c.r('ice',4))   # 积冰
    c.px(9,5,c.r('ice',2)); c.px(15,5,c.r('ice',2))
    for x in range(8,20,3): c.px(x,8,c.r('purple',1))     # 散热格栅
    # 侧臂 + 航行灯
    for x in range(3,7): c.px(x,7,c.r('metal',2)); c.px(x,8,c.r('metal',1))
    for x in range(21,25): c.px(x,7,c.r('metal',2)); c.px(x,8,c.r('metal',1))
    c.px(2,7,hx('#ff5a5a')); c.px(2,8,hx('#a3202c')); c.px(25,7,hx('#5aff8a')); c.px(25,8,hx('#1f8a4a'))
    # 腹部摄像头
    c.disc(13.5,12.0,3.6,'metal')
    c.disc(13.5,12.3,2.2,'glass')
    c.px(13,12,EYE); c.px(14,12,EYE); c.px(13,13,EYE2); c.px(12,11,WHITE)
    # 天线
    c.px(18,2,c.r('metal',3)); c.px(18,3,c.r('metal',2)); c.px(19,2,hx('#ff5a5a') if f==0 else hx('#8a1a26'))
    return c.outline().im

def turret_base():
    c=C(26,20)
    # 装甲底座
    for y in range(11,20):
        inset=max(0,(14-y)) if y<14 else 0
        for x in range(1+inset,25-inset):
            k=2
            if y==11: k=4 if x<13 else 3
            elif x==1+inset: k=3
            elif y==19: k=0
            elif x==24-inset: k=1
            c.px(x,y,c.r('metal',k))
    for x in range(2,24):                                  # 警示条纹
        on=((x+3)//2)%2==0
        c.px(x,15,YEL if on else BLK); c.px(x,16,YEL2 if on else BLK)
    for x in (4,21): c.px(x,13,c.r('metal',4)); c.px(x,18,c.r('metal',4))   # 螺栓
    # 背后的冰锥弹仓
    c.box(2,4,7,11,'metal')
    for (x,y) in ((3,5),(4,5),(3,6),(5,6),(4,7),(6,7),(3,8),(5,8),(4,9),(6,9)): c.px(x,y,c.r('ice',[4,3,2][(x+y)%3]))
    # 炮塔圆顶
    for y in range(3,12):
        for x in range(7,22):
            dx,dy=(x+0.5-14.5)/7.5,(y+0.5-11.5)/8.0
            if dx*dx+dy*dy<=1:
                v=-(dx*0.55+dy*0.85); k=max(0,min(4,2+round(v*1.7)))
                c.px(x,y,c.r('red',k))
    for x in range(8,21): c.px(x,10,c.r('red',0)); c.px(x,11,c.r('metal',2))
    for x in range(10,19,2): c.px(x,4,c.r('ice',4))        # 积霜
    c.px(11,3,c.r('ice',3)); c.px(15,3,c.r('ice',3))
    # 警示灯
    c.px(14,1,YEL); c.px(15,1,YEL); c.px(14,2,YEL2); c.px(15,2,YEL2); c.px(14,0,WHITE)
    # 炮塔观察窗
    c.box(15,6,19,8,'glass',round_=False); c.px(18,7,EYE); c.px(17,7,EYE2)
    return c.outline().im
def turret_barrel():
    c=C(16,7)
    c.box(0,1,12,5,'metal')
    for x in range(2,11,2): c.px(x,3,c.r('metal',1))
    c.box(12,0,15,6,'metal')                               # 炮口
    c.px(15,2,c.r('ice',4)); c.px(15,3,c.r('ice',3)); c.px(15,4,c.r('ice',2))
    return c.outline().im

def strip(frames):
    w,h=frames[0].size; st=Image.new('RGBA',(w*len(frames),h),(0,0,0,0))
    for i,f in enumerate(frames): st.paste(f,(i*w,0))
    return st
SHEETS={'walker':strip([plow_truck(0),plow_truck(1)]),'hopper':strip([curling(0),curling(1)]),
        'flyer':strip([drone(0),drone(1)]),'turret':turret_base(),'barrel':turret_barrel()}
if __name__=='__main__':
    for k,v in SHEETS.items(): v.save(f'sp2_{k}.png')
    Z=8
    board=Image.new('RGB',(1560,520),'#14161d'); d=ImageDraw.Draw(board)
    d.text((30,16),'敌人 v2（放大 8 倍，右侧为游戏内 2 倍）',font=font(26),fill='#e8ecf2')
    x=30
    for k,lab in [('walker','铲雪清道车'),('hopper','冰壶弹簧机'),('flyer','侦察无人机'),('turret','冰锥炮台')]:
        sp=SHEETS[k]; w,h=sp.size
        if k=='turret':
            comp=Image.new('RGBA',(w+10,h),(0,0,0,0)); comp.alpha_composite(SHEETS['barrel'],(14,4)); comp.alpha_composite(sp,(0,0)); sp=comp
        big=up(sp,Z if k!='flyer' and k!='walker' else 6)
        d.rectangle([x-6,64,x+big.width+6,70+big.height+6],fill='#262b37'); board.paste(big,(x,70),big)
        d.text((x,80+big.height+10),lab,font=font(20),fill='#e8ecf2')
        sm=up(sp,2); board.paste(sm,(x,80+big.height+44),sm)
        x+=big.width+40
    board.save('enemies_v2_board.png'); print('ok')
