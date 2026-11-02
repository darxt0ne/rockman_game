"""Boss 2：磁暴裁缝（40×48，三帧：站立 / 张剪 / 投针）"""
import sys, math; sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from enemies2 import C, hx, RAMP, OUT, EYE, EYE2, WHITE, YEL, YEL2, BLK
from pix import font, up
from PIL import Image, ImageDraw
RAMP['copper']=['#4a1e0a','#86391a','#c4622c','#f09050','#ffc89a']
RAMP['blade']=['#2a1640','#4a2a78','#7a4ab8','#b48ae8','#ece0ff']
def blade(c, x0,y0, x1,y1, width, light):
    """一片剪刀刃：沿 (x0,y0)->(x1,y1) 的楔形，受光边更亮"""
    L=math.hypot(x1-x0,y1-y0); ux,uy=(x1-x0)/L,(y1-y0)/L; nx,ny=-uy,ux
    for y in range(c.h):
        for x in range(c.w):
            qx,qy=x+0.5-x0,y+0.5-y0; t=qx*ux+qy*uy; d=qx*nx+qy*ny
            if 0<=t<=L:
                wd=width*(1-t/L*0.85)
                if abs(d)<=wd:
                    k = 4 if (d*light)>wd*0.45 else (3 if (d*light)>0 else (1 if abs(d)>wd*0.6 else 2))
                    c.px(x,y,c.r('blade',k))
def tailor(pose):
    c=C(44,50)
    open_ = pose=='open'
    # 腿
    for (x,sh) in ((17,0),(23,1)):
        for y in range(36,47):
            c.px(x,y,c.r('blade',2+sh)); c.px(x+1,y,c.r('blade',1+sh))
        c.box(x-2,46,x+3,49,'metal')
    # 后臂 + U 型磁铁
    for k in range(9): c.px(13-k//2,22+k,c.r('copper',1)); c.px(14-k//2,22+k,c.r('copper',2))
    mx,my=6,31
    for y in range(my,my+9):
        for x in range(mx,mx+9):
            dx,dy=(x+0.5-(mx+4.5))/4.5,(y+0.5-(my+3))/4.5
            if dy>0 and dx*dx+dy*dy<=1 and dx*dx+dy*dy>=0.3: c.px(x,y,c.r('metal',3 if dx<0 else 2))
            if dy<=0 and 0.55<=abs(dx)<=1: c.px(x,y,c.r('metal',3 if dx<0 else 2))
    for x in (mx,mx+1): c.px(x,my-1,hx('#ff5a5a')); c.px(x,my,hx('#c92a36'))
    for x in (mx+7,mx+8): c.px(x,my-1,hx('#5aa0ff')); c.px(x,my,hx('#2a5ac9'))
    # 躯干（裁缝马甲）
    for y in range(18,37):
        half=6+(y-18)//6
        for x in range(21-half,22+half):
            k=2
            if x==21-half: k=3
            elif x==21+half: k=1
            elif y==36: k=0
            if x<21-half+3 and y<24: k=4
            c.px(x,y,c.r('copper',k))
    for y in range(20,36,4): c.px(21,y,c.r('metal',4)); c.px(22,y,c.r('metal',2))       # 纽扣
    for y in range(18,37): c.px(20,y,c.r('copper',1)) if y%2 else None                     # 缝线
    # 软尺围巾
    for x in range(14,30):
        c.px(x,17,YEL if x%3 else BLK); c.px(x,18,YEL2)
    for y in range(18,28): c.px(28,y,YEL if y%3 else BLK); c.px(29,y,YEL2)
    # 前臂 + 大针
    if pose=='throw':
        for k in range(10): c.px(29+k,20-k//2,c.r('copper',2)); c.px(29+k,21-k//2,c.r('copper',1))
        for k in range(14): c.px(36+k//3*0+k%1,0,0) if False else None
        for k in range(12): c.px(38,4+k,c.r('metal',4) if k<10 else c.r('metal',2))
        c.px(38,3,WHITE)
    else:
        for k in range(9): c.px(29+k//3,21+k,c.r('copper',2)); c.px(30+k//3,21+k,c.r('copper',1))
        for k in range(16): c.px(33+k//4,14+k,c.r('metal',4) if k<14 else c.r('metal',2))
        c.px(33,13,WHITE)
        for k in range(8): c.px(34+k,28+(k%3),hx('#ff9ad0'))   # 线
    # 剪刀头：两片刀刃 + 中轴眼睛
    spread = 9 if open_ else 4
    blade(c, 21,15, 21-spread,1, 3.2, 1)
    blade(c, 22,15, 22+spread,1, 3.2, -1)
    blade(c, 21,15, 16,22, 2.0, 1)
    blade(c, 22,15, 27,22, 2.0, -1)
    c.disc(21.5,14.5,3.4,'metal')
    c.px(21,14,EYE); c.px(22,14,EYE); c.px(21,15,EYE2); c.px(22,13,WHITE)
    # 两个握环（剪刀柄）
    for (cx,cy) in ((15,23),(28,23)):
        for y in range(cy-2,cy+3):
            for x in range(cx-2,cx+3):
                d=(x-cx)**2+(y-cy)**2
                if 2<d<=6: c.px(x,y,c.r('blade',3))
    return c.outline().im
frames=[tailor('idle'),tailor('open'),tailor('throw')]
st=Image.new('RGBA',(44*3,50),(0,0,0,0))
for i,f in enumerate(frames): st.paste(f,(i*44,0))
st.save('sp_tailor.png')
# 芯片图标在 HUD 用文字，不需要精灵
b=Image.new('RGB',(44*3*6+60,50*6+60),'#14161d'); d=ImageDraw.Draw(b)
big=up(st,6); b.paste(big,(30,30),big); b.save('tailor_board.png'); print('ok')
