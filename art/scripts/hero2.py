"""主角 A 精修版：按部件建模 + 光照着色 + 选择性描边"""
import sys, math; sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from pix import font, up
from PIL import Image, ImageDraw
def hx(h): h=h.lstrip('#'); return (int(h[0:2],16),int(h[2:4],16),int(h[4:6],16),255)
R = {
 'blue':  [hx(c) for c in ['#123058','#1d64a3','#3aa8e8','#86d6ff','#dcf5ff']],
 'navy':  [hx(c) for c in ['#0d182c','#172a4a','#243f6b','#35598e']],
 'metal': [hx(c) for c in ['#262c3b','#465064','#7a869c','#b4bfd2','#eef3fa']],
 'boot':  [hx(c) for c in ['#55250b','#9a4512','#de7628','#ffaa58','#ffe2b8']],
 'lamp':  [hx(c) for c in ['#a35d0c','#f0b02e','#fff07a','#ffffff']],
 'visor': [hx(c) for c in ['#070d18','#0e1a2e','#1a2d4c','#2f4d7c']],
 'teal':  [hx(c) for c in ['#0a5a4c','#14a88a','#3df0c8','#c8fff0']],
}
OUT = hx('#0a101c')
L = (-0.55, -0.72, 0.42); n_ = math.sqrt(sum(v*v for v in L)); L = tuple(v/n_ for v in L)

class Fig:
    def __init__(s, w=32, h=32):
        s.w, s.h = w, h
        s.col = [[None]*w for _ in range(h)]; s.z = [[-1]*w for _ in range(h)]; s.ramp = [[None]*w for _ in range(h)]
    def set(s, x, y, ramp, idx, z):
        if 0<=x<s.w and 0<=y<s.h and z>=s.z[y][x]:
            r=R[ramp]; s.col[y][x]=r[max(0,min(len(r)-1,idx))]; s.z[y][x]=z; s.ramp[y][x]=ramp
    def shade(s, nx, ny, ramp, bias=0.0):
        nz=math.sqrt(max(0.0,1-nx*nx-ny*ny)); v=nx*L[0]+ny*L[1]+nz*L[2]+bias
        k=len(R[ramp]); t=(v+0.35)/1.15
        return int(max(0,min(k-1, math.floor(t*k))))
    def ellipse(s, cx, cy, rx, ry, ramp, z, bias=0.0, clip=None):
        for y in range(s.h):
            for x in range(s.w):
                dx=(x+0.5-cx)/rx; dy=(y+0.5-cy)/ry
                if dx*dx+dy*dy<=1 and (clip is None or clip(x,y)):
                    s.set(x,y,ramp,s.shade(dx*0.9,dy*0.9,ramp,bias),z)
    def box(s, x0, y0, x1, y1, ramp, z, bias=0.0, round_=1.6):
        cx=(x0+x1+1)/2; cy=(y0+y1+1)/2; rx=(x1-x0+1)/2; ry=(y1-y0+1)/2
        for y in range(y0,y1+1):
            for x in range(x0,x1+1):
                dx=(x+0.5-cx)/rx; dy=(y+0.5-cy)/ry
                if abs(dx)**4+abs(dy)**4>1.0 and round_>0 and (abs(dx)>0.8 and abs(dy)>0.8): continue
                nx=math.copysign(abs(dx)**3,dx)*0.85; ny=math.copysign(abs(dy)**3,dy)*0.85
                s.set(x,y,ramp,s.shade(nx,ny,ramp,bias),z)
    def limb(s, x0, y0, x1, y1, r, ramp, z, bias=0.0):
        ax,ay=x1-x0,y1-y0; ln=math.hypot(ax,ay) or 1; ux,uy=ax/ln,ay/ln; px_,py_=-uy,ux
        for y in range(s.h):
            for x in range(s.w):
                qx,qy=x+0.5-x0,y+0.5-y0; t=max(0,min(ln,qx*ux+qy*uy)); d=(qx-ux*t)*px_+(qy-uy*t)*py_
                dd=math.hypot(qx-ux*t,qy-uy*t)
                if dd<=r: s.set(x,y,ramp,s.shade(px_*d/r*0.95,py_*d/r*0.95,ramp,bias),z)
    def px(s, x, y, ramp, idx, z=99): s.set(x,y,ramp,idx,z)
    def render(s):
        im=Image.new('RGBA',(s.w,s.h),(0,0,0,0)); p=im.load()
        for y in range(s.h):
            for x in range(s.w):
                c=s.col[y][x]
                if c is None: continue
                # 部件交界：被遮挡的一侧画深色
                dark=False
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    X,Y=x+dx,y+dy
                    if 0<=X<s.w and 0<=Y<s.h and s.z[Y][X]>s.z[y][x]+0 and s.ramp[Y][X]!=s.ramp[y][x] and s.z[Y][X]<90: dark=True
                p[x,y]=R[s.ramp[y][x]][0] if dark else c
        out=im.copy(); po=out.load()
        for y in range(s.h):
            for x in range(s.w):
                if p[x,y][3]: continue
                nb=[(X,Y) for X,Y in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)) if 0<=X<s.w and 0<=Y<s.h and p[X,Y][3]]
                if not nb: continue
                # 选择性描边：受光的左上方用部件自身最深色，背光处用纯深色
                X,Y=nb[0]; rp=s.ramp[Y][X]
                lit = any(X2>x or Y2>y for X2,Y2 in nb)   # 邻居在右/下 → 本像素位于左/上边缘（受光侧）
                po[x,y]= R[rp][0] if lit else OUT
        return out

def hero(pose='idle'):
    f=Fig()
    # 根据姿势设定关键点（面朝右）
    if pose=='idle':
        backLeg=((13,22),(12,26)); frontLeg=((18,22),(19,26)); backBoot=(8,27); frontBoot=(16,27); bodyDy=0; armDy=0
    elif pose=='run':
        backLeg=((13,22),(9,25)); frontLeg=((18,22),(21,24)); backBoot=(4,25); frontBoot=(18,24); bodyDy=-1; armDy=0
    else:  # jump
        backLeg=((13,21),(10,24)); frontLeg=((18,21),(20,23)); backBoot=(6,23); frontBoot=(17,22); bodyDy=-2; armDy=-1
    by=bodyDy
    # 后臂（被身体挡住一部分）
    f.limb(12,16+by,10,20+by,1.6,'navy',1, bias=-0.15)
    f.ellipse(9.8,21.2+by,1.9,1.9,'metal',2, bias=-0.1)
    # 后腿 + 后靴
    (a,b)=backLeg; f.limb(a[0],a[1]+by,b[0],b[1],1.7,'navy',2, bias=-0.15)
    bx,byy=backBoot
    f.box(bx,byy,bx+6,byy+3,'boot',3, bias=-0.15); f.box(bx,byy+3,bx+7,byy+4,'boot',3, bias=-0.35)
    # 躯干
    f.box(10,14+by,19,21+by,'blue',5)
    f.box(12,16+by,18,19+by,'navy',6, bias=0.1)              # 胸甲内衬
    f.box(10,20+by,19,22+by,'metal',6)                       # 腰带
    # 前腿 + 前靴
    (a,b)=frontLeg; f.limb(a[0],a[1]+by,b[0],b[1],1.8,'navy',7)
    f.ellipse(b[0]+0.5,b[1]-0.5,1.5,1.5,'metal',8)          # 膝关节
    bx,byy=frontBoot
    f.box(bx,byy,bx+6,byy+3,'boot',8); f.box(bx,byy+3,bx+8,byy+4,'boot',8, bias=-0.25)
    # 头盔
    hy=by
    f.ellipse(14.5,8.0+hy,7.6,7.0,'blue',10)
    f.box(14,12+hy,20,13+hy,'metal',11)                       # 下颌护罩
    f.ellipse(9.6,9.5+hy,2.4,2.6,'metal',12)                  # 耳盘
    # 护目镜（深色带）+ 独眼探照灯
    f.box(14,7+hy,22,11+hy,'visor',13, round_=1)
    f.ellipse(21.0,9.0+hy,2.6,2.6,'metal',14)                 # 灯座
    f.ellipse(21.2,9.0+hy,1.8,1.8,'lamp',15, bias=0.25)       # 灯
    # 肩甲 + 炮臂
    ay=armDy+by
    f.ellipse(19.5,16.5+ay,3.0,2.6,'blue',16)
    f.box(20,17+ay,27,21+ay,'metal',17)
    f.box(26,17+ay,28,21+ay,'metal',18, bias=-0.3)            # 炮口环
    img=f.render(); p=img.load()
    def P(x,y,c):
        if 0<=x<32 and 0<=y<32: p[x,y]=c
    # ---- 手工细节 ----
    for x in range(10,17): 
        if p[x,3+hy][3] and x in (11,12,13): P(x,3+hy,R['blue'][4])   # 头盔高光
    P(11,4+hy,R['blue'][4]); P(10,5+hy,R['blue'][3])
    for x in range(13,19): P(x,2+hy,R['blue'][3]) if p[x,2+hy][3] and p[x,1+hy][3] else None
    P(9,9+hy,R['teal'][2]); P(10,10+hy,R['teal'][1])            # 耳盘指示灯
    for x in range(15,19): P(x,8+hy,R['visor'][3])              # 护目镜反光
    P(16,9+hy,R['visor'][2])
    P(21,8+hy,R['lamp'][3]); P(22,8+hy,R['lamp'][3])            # 灯芯
    P(23,9+hy,R['lamp'][2]); P(24,9+hy,R['lamp'][1])            # 灯光外溢
    P(13,17+by,R['teal'][2]); P(16,17+by,R['teal'][2])          # 胸口两个芯片插槽
    P(13,18+by,R['teal'][1]); P(16,18+by,R['teal'][1])
    for x in range(21,26): P(x,18+ay,R['metal'][4]) if x%2 else None   # 炮管散热纹
    P(28,19+ay,OUT); P(28,18+ay,R['metal'][1]); P(27,19+ay,R['teal'][2])  # 炮口
    for x in range(11,19,2): P(x,21+by,R['metal'][1])            # 腰带纹
    return img

def main():
    poses=[('idle','站立'),('run','跑动'),('jump','起跳')]
    S=10; W_=1400; H_=520
    board=Image.new('RGB',(W_,H_),'#14161d'); d=ImageDraw.Draw(board)
    d.text((40,20),'主角「残响」A 精修版（32×32 画布，放大 10 倍）',font=font(28),fill='#e8ecf2')
    for i,(p,name) in enumerate(poses):
        sp=hero(p); x0=40+i*350; y0=80
        d.rectangle([x0,y0,x0+330,y0+330],fill='#262b37')
        big=up(sp,S); board.paste(big,(x0+5,y0+5),big)
        d.text((x0,y0+340),name,font=font(22),fill='#e8ecf2')
    # 游戏内尺寸预览：深色与浅色背景
    x0=1090; d.text((x0,80),'游戏内 2×',font=font(18),fill='#9aa0aa')
    for k,bg in enumerate(['#181a21','#3a4864','#8fcbea']):
        d.rectangle([x0,110+k*120,x0+260,110+k*120+100],fill=bg)
        for i,(p,_) in enumerate(poses):
            sm=up(hero(p),2); board.paste(sm,(x0+10+i*82,120+k*120),sm)
    board.save('hero_A_refined.png'); print('ok')
if __name__=='__main__': main()
