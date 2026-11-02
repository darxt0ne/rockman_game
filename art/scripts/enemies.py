"""小敌人与霜钟守卫的像素精灵"""
import sys, math; sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from pix import font, up
from PIL import Image, ImageDraw
PAL = {
 'K':'#0a101c','k':'#101a2b','W':'#ffffff','Y':'#fff07a',
 'o':'#7a3410','O':'#c9611c','P':'#f08a2e','Q':'#ffc070',
 'g':'#2c5a1e','G':'#4f9a2e','h':'#8fd14a','j':'#d4f59a',
 'u':'#3e1f5c','U':'#6e3aa0','V':'#a66ad8','w':'#dcb8ff',
 'e':'#6a1520','E':'#b52a36','F':'#ee4a52','f':'#ff9a9a',
 'm':'#262c3b','n':'#465064','M':'#7a869c','H':'#b4bfd2',
 'i':'#6fa8d6','I':'#a6d8f5','J':'#e2f5ff',
}
def hx(c): c=c.lstrip('#'); return (int(c[0:2],16),int(c[2:4],16),int(c[4:6],16),255)
def grid_img(rows, w, h):
    im=Image.new('RGBA',(w,h),(0,0,0,0)); p=im.load()
    off=h-len(rows)                       # 底部对齐
    for y,r in enumerate(rows):
        assert len(r)<=w, (r,len(r),w)
        for x,c in enumerate(r):
            if c!='.': p[x,y+off]=hx(PAL[c])
    return im
def sheet(frames, w, h):
    st=Image.new('RGBA',(w*len(frames),h),(0,0,0,0))
    for i,f in enumerate(frames): st.paste(grid_img(f,w,h),(i*w,0))
    return st
WALK_TOP = [
"....KKKKKKKKK.....",
"...KJJIJJJIJJK....",
"..KJIIJJIIJJIJK...",
"..KPQQPPPPPKKKKK..",
"..KPQPPPPPKkkkkK..",
"..KPPPPPPPKkYWkK..",
"..KOPPPPPPKkYYkK..",
"..KOPPPPPPPKKKKKK.",
"..KOOPPPPPPPPPKHK.",
"..KoOOOOOOOOOOKMHK",
"...KoooooooooKKMHK",
"...KKKKKKKKKKKMMMK",
]
walker = sheet([WALK_TOP+["...KnMnK..KnMnKKK.","..KnMMnK.KnMMnK...","..KKKKKK.KKKKKK..."],
                WALK_TOP+["....KnMnK.KnMnKKK.","...KnMMnKKnMMnK...","...KKKKKKKKKKKK..."]], 18, 16)
HOP_TOP = [
"..KKK.....KKK...",
".KJWkK...KJWkK..",
".KWYkKKKKKWYkK..",
"..KKhhhhhhhKK...",
".KhhjjhhhhhhhK..",
".KhjhhhhhhhhGK..",
".KhhhhhhKKKKGK..",
".KGhhhhhhhhGGK..",
"..KGGGGGGGGGK...",
"..KgKgggggKgK...",
]
hopper = sheet([HOP_TOP+[".KMHK.....KMHK..",".KnMK.....KnMK..",".KKKK.....KKKK.."],
                HOP_TOP+["..KMK.....KMK...","..KHK.....KHK...","..KMK.....KMK...",".KnMnK...KnMnK..",".KKKKK...KKKKK.."]], 16, 16)
FLY_BODY = [
".......KKKKKK.......",
"......KVVwVVVK......",
".....KVwVVVVVUK.....",
".....KVVKKKKVUK.....",
".....KVKWYYkKUK.....",
".....KUKYYYkKuK.....",
"......KUKKKKuK......",
".......KuuuuK.......",
"........KKKK........",
]
def wings(rows, up_):
    rows=[list(r) for r in rows]
    L = [(0,0),(1,0),(0,1),(1,1),(2,1),(1,2),(2,2),(3,2),(2,3),(3,3),(4,3),(4,4),(5,4)] if up_ else \
        [(5,3),(4,4),(3,4),(4,5),(2,5),(3,5),(1,6),(2,6),(3,6),(0,7),(1,7),(2,7),(1,8)]
    for (x,y) in L:
        c = 'J' if (x+y)%3==0 else 'I'
        for X in (x, 19-x):
            if rows[y][X]=='.': rows[y][X]=c
    # 翅膀描边
    out=[r[:] for r in rows]
    for y in range(len(rows)):
        for x in range(20):
            if rows[y][x]=='.' and any(0<=x+dx<20 and 0<=y+dy<len(rows) and rows[y+dy][x+dx] in 'IJ' for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))):
                out[y][x]='K'
    return [''.join(r) for r in out]
flyer = sheet([wings(FLY_BODY, True), wings(FLY_BODY, False)], 20, 11)
turret = sheet([[
"......KKKKKK......",
"....KKJJIJJJKK....",
"...KFJIFFFFFFEK...",
"..KFfFFFFFFFFEEK..",
"..KFFFFFFFFFFEEK..",
"..KEFFFFFFFFEEeK..",
".KKKKKKKKKKKKKKKK.",
".KHHMMMMMMMMMMMnK.",
".KMHYMMMMMMMMMnnK.",
".KMMMMMMMMMMMMnnK.",
".KnnnnnnnnnnnnnmK.",
"KKKKKKKKKKKKKKKKKK",
]], 18, 12)
barrel = sheet([[
"KKKKKKKKKKK.",
"KnMHHHHHMnKK",
"KnMMMMMMMnkK",
"KmnnnnnnnmKK",
"KKKKKKKKKKK.",
]], 12, 5)
# ---- 霜钟守卫：按钟的曲面计算明暗 ----
def bell(phase2=False):
    Wd,Hd=56,56; cx=28
    ramp=[hx(c) for c in (['#1d3f66','#2d5e8f','#4a86bd','#79b3e0','#a9d6f5','#e3f5ff'] if not phase2 else
                          ['#18264a','#25416f','#365f99','#5689c4','#86b6e6','#cfe6ff'])]
    def r_of(y):
        if y<6: return None
        if y<16: t=(y-6)/10; return 6+9*math.sqrt(1-(1-t)**2)
        if y<40: return 15+4*((y-16)/24)**1.5
        if y<=49: return 19+7*((y-40)/9)**1.2
        return None
    im=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); p=im.load()
    L=(-0.55,-0.45,0.70); n=math.sqrt(sum(v*v for v in L)); L=[v/n for v in L]
    for y in range(Hd):
        r=r_of(y+0.5)
        if r is None: continue
        r1=r_of(min(49,y+1.5)) or r; r0=r_of(max(6,y-0.5)) or r; slope=(r1-r0)/2
        for x in range(Wd):
            dx=(x+0.5-cx)/r
            if abs(dx)>1: continue
            nz=math.sqrt(max(0,1-dx*dx)); nx=dx; ny=-slope*0.6
            ln=math.sqrt(nx*nx+ny*ny+nz*nz); v=(nx*L[0]+ny*L[1]+nz*L[2])/ln
            k=int(max(0,min(5,(v+0.05)/1.25*6)))
            p[x,y]=ramp[k]
    # 钟口边缘（金属带）
    rimc=[hx('#2a4a6e'),hx('#3f6b92'),hx('#8fb8dc')]
    for y in range(45,50):
        for x in range(Wd):
            if p[x,y][3]:
                p[x,y]=rimc[2] if y==45 else (rimc[1] if (x-cx)<8 else rimc[0])
    # 护目镜带（眼睛由代码画）
    for y in range(24,31):
        r=r_of(y+0.5)
        for x in range(int(cx-r+2),int(cx+r-1)):
            p[x,y]=hx('#0b1a30') if 24<y<30 else hx('#061020')
    # 顶部吊环
    for y in range(1,7):
        for x in range(cx-5,cx+5):
            ring=(x-cx+0.5)**2/25+(y-4)**2/9
            if 0.45<ring<=1.05: p[x,y]=hx('#3f6b92') if x<cx else hx('#2a4a6e')
    # 冰霜与高光
    for (x,y) in [(18,10),(19,9),(20,9),(17,12),(16,14),(15,17),(15,18),(22,8)]: p[x,y]=hx('#ffffff')
    for x in range(10,46,3):
        if p[x,50-1][3]:
            Ln = 1+((x*7)%4)
            for k in range(Ln): p[x,50+k]=hx('#e2f5ff') if k<Ln-1 else hx('#6fa8d6')
    if phase2:   # 二阶段：红色裂纹
        crack=[(33,12),(34,13),(34,14),(35,15),(36,16),(35,17),(36,18),(37,19),(37,20),(38,21),(38,22),
               (21,34),(22,35),(22,36),(23,37),(24,38),(24,39),(25,40),(40,33),(41,34),(41,35),(42,36)]
        for (x,y) in crack: p[x,y]=hx('#ff5a5a')
        for (x,y) in crack[::3]: p[x+1,y]=hx('#ffb0b0')
    # 描边
    out=im.copy(); po=out.load()
    for y in range(Hd):
        for x in range(Wd):
            if p[x,y][3]: continue
            nb=[(X,Y) for X,Y in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)) if 0<=X<Wd and 0<=Y<Hd and p[X,Y][3]]
            if nb: po[x,y]= ramp[0] if any(X>x or Y>y for X,Y in nb) else hx('#0a101c')
    return out
bell_sheet=Image.new('RGBA',(112,56),(0,0,0,0)); bell_sheet.paste(bell(False),(0,0)); bell_sheet.paste(bell(True),(56,0))
clapper=Image.new('RGBA',(10,24),(0,0,0,0)); cp=clapper.load()
for y in range(0,15):
    cp[4,y]=hx('#e2f5ff'); cp[5,y]=hx('#6fa8d6'); cp[3,y]=hx('#0a101c'); cp[6,y]=hx('#0a101c')
for y in range(14,24):
    for x in range(10):
        d=(x-4.5)**2+(y-18.5)**2
        if d<=16: cp[x,y]=hx('#e2f5ff') if d<5 and x<5 else (hx('#a6d8f5') if x<6 else hx('#6fa8d6'))
        elif d<=22: cp[x,y]=hx('#0a101c')
SHEETS={'walker':walker,'hopper':hopper,'flyer':flyer,'turret':turret,'barrel':barrel,'bell':bell_sheet,'clapper':clapper}
if __name__=='__main__':
    for k,v in SHEETS.items(): v.save(f'sp_{k}.png')
    board=Image.new('RGB',(1300,620),'#14161d'); d=ImageDraw.Draw(board)
    d.text((30,16),'敌人与 Boss 像素精灵（放大 6 倍）',font=font(26),fill='#e8ecf2')
    x=30
    for k,lab in [('walker','巡逻兵 ×2帧'),('hopper','跳跳怪 ×2帧'),('flyer','飞行怪 ×2帧'),('turret','炮台')]:
        sp=up(SHEETS[k],6); d.rectangle([x-6,64,x+sp.width+6,70+sp.height+6],fill='#262b37'); board.paste(sp,(x,70),sp)
        if k=='turret':
            b=up(barrel,6); board.paste(b,(x+60,70-10),b)
        d.text((x,70+max(sp.height,100)+14),lab,font=font(18),fill='#aab2c0'); x+=sp.width+40
    bs=up(bell_sheet,4); d.rectangle([24,254,30+bs.width+6,260+bs.height+6],fill='#262b37'); board.paste(bs,(30,260),bs)
    c=up(clapper,4); board.paste(c,(30+bs.width+30,300),c)
    d.text((30,260+bs.height+14),'霜钟守卫：一阶段 / 二阶段（裂纹）+ 钟锤',font=font(18),fill='#aab2c0')
    board.save('enemies_board.png'); print('ok')
