import sys; sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from pix import *
from PIL import Image, ImageDraw
N=64
def canvas(): im=Image.new('RGBA',(N,N),(0,0,0,0)); return im, ImageDraw.Draw(im)
def outline(im, col='#101a2b'):
    px=im.load(); out=im.copy(); po=out.load()
    for y in range(N):
        for x in range(N):
            if px[x,y][3]==0:
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    X,Y=x+dx,y+dy
                    if 0<=X<N and 0<=Y<N and px[X,Y][3]>0: po[x,y]=Image.new('RGB',(1,1),col).getpixel((0,0))+(255,); break
    return out
def ghost(im, a=0.35):
    g=im.copy(); px=g.load()
    for y in range(N):
        for x in range(N):
            r,gg,b,al=px[x,y]
            if al: px[x,y]=(r,gg,b,int(al*a))
    return g
B={}
# 1 霜钟守卫
im,d=canvas()
d.polygon([(10,56),(14,40),(16,24),(22,14),(32,11),(42,14),(48,24),(50,40),(54,56)],fill='#9cc9e8')
d.polygon([(34,12),(42,14),(48,24),(50,40),(54,56),(44,56),(42,34),(38,18)],fill='#79aed6')
d.polygon([(18,22),(24,15),(30,13),(26,18),(22,30)],fill='#e1f5fe')
d.rectangle([7,54,57,58],fill='#4f7fa6'); d.rectangle([28,6,36,11],fill='#4f7fa6')
d.rectangle([18,30,46,37],fill='#0d2b52'); d.rectangle([34,32,42,35],fill='#e1f5fe')
d.line([(32,58),(32,61)],fill='#d6f0ff',width=3); d.ellipse([28,58,36,63],fill='#d6f0ff')
B['霜钟守卫']=(im,'温度','巨钟身体 · 冰锤钟摆')
# 2 磁暴裁缝
im,d=canvas()
d.polygon([(20,8),(32,22),(26,24)],fill='#b388ff'); d.polygon([(44,8),(32,22),(38,24)],fill='#8e5fe0')
d.ellipse([29,19,35,25],fill='#e0c3ff')
d.polygon([(25,26),(39,26),(36,44),(28,44)],fill='#e0884a'); d.polygon([(33,26),(39,26),(36,44),(33,44)],fill='#b8642a')
d.line([(26,28),(14,36),(8,30)],fill='#e0884a',width=3)
d.arc([0,18,14,32],200,340,fill='#9aa6b8',width=4)   # U 型磁铁
d.rectangle([0,24,3,27],fill='#ff6b6b'); d.rectangle([11,24,14,27],fill='#ff6b6b')
d.line([(38,28),(52,38),(58,30)],fill='#e0884a',width=3); d.line([(58,30),(62,12)],fill='#e1e5ec',width=1)
d.line([(62,12),(48,4),(40,10)],fill='#b388ff',width=1)
d.line([(29,44),(26,60)],fill='#8e5fe0',width=3); d.line([(35,44),(38,60)],fill='#8e5fe0',width=3)
d.rectangle([22,59,29,62],fill='#3a2a55'); d.rectangle([36,59,43,62],fill='#3a2a55')
B['磁暴裁缝']=(im,'磁力','剪刀头 · 细长手臂 · 磁力线')
# 3 回溯钟摆
im,d=canvas()
def clock(d,ox,fill,shade):
    d.polygon([(ox+22,10),(ox+32,4),(ox+42,10)],fill=shade)
    d.rectangle([ox+22,10,ox+42,48],fill=fill); d.rectangle([ox+36,10,ox+42,48],fill=shade)
    d.ellipse([ox+24,13,ox+40,29],fill='#fff3c4'); d.line([(ox+32,21),(ox+32,15)],fill='#5a3a1a'); d.line([(ox+32,21),(ox+37,21)],fill='#5a3a1a')
    d.line([(ox+32,48),(ox+26,58)],fill='#d4a017',width=2); d.ellipse([ox+21,55,ox+30,63],fill='#ffd54f')
    d.line([(ox+22,30),(ox+12,40)],fill=fill,width=3); d.line([(ox+42,30),(ox+52,40)],fill=fill,width=3)
g,gd=canvas(); clock(gd,-12,'#c9a227','#8d6e1d')
im.alpha_composite(ghost(outline(g),0.35))
c,cd=canvas(); clock(cd,0,'#c9a227','#8d6e1d'); im.alpha_composite(c)
B['回溯钟摆']=(im,'时间','落地钟身体 · 拖着自己的残影',True)
# 4 倒影猎手
im,d=canvas()
d.polygon([(32,10),(22,20),(18,46),(24,60),(32,60)],fill='#2b2d3a')
d.polygon([(32,10),(42,20),(46,46),(40,60),(32,60)],fill='#c9d1dc')
d.line([(36,22),(40,34)],fill='#ffffff'); d.line([(38,40),(42,50)],fill='#ffffff')
d.ellipse([26,12,38,24],fill='#3a3d4e'); d.pieslice([26,12,38,24],270,90,fill='#e6ebf2')
d.rectangle([27,16,30,18],fill='#ff6b6b'); d.rectangle([34,16,37,18],fill='#2b8fc9')
d.arc([44,14,62,46],-80,80,fill='#9aa6b8',width=2); d.line([(55,15),(55,45)],fill='#e1e5ec')
d.line([(22,28),(10,36)],fill='#2b2d3a',width=3)
B['倒影猎手']=(im,'镜像','左右不对称 · 半边是镜子',True)
# 5 熔炉园丁
im,d=canvas()
d.polygon([(14,30),(50,30),(44,60),(20,60)],fill='#3f6b3a'); d.polygon([(36,30),(50,30),(44,60),(36,60)],fill='#2e5029')
d.rectangle([12,27,52,32],fill='#4f8a48')
d.rectangle([22,40,42,52],fill='#1a1a1a'); 
for x in (25,30,35,40): d.line([(x,40),(x,52)],fill='#ff6a1a')
d.rectangle([23,47,41,51],fill='#ff9f43')
for (x,h,c) in [(22,14,'#ff6b3a'),(32,20,'#ffb03a'),(42,12,'#ff6b3a')]:
    d.line([(x,27),(x,27-h)],fill='#4f8a48',width=2)
    d.polygon([(x,27-h-8),(x-4,27-h),(x+4,27-h)],fill=c); d.polygon([(x,27-h-4),(x-2,27-h),(x+2,27-h)],fill='#fff59d')
d.line([(50,36),(60,30)],fill='#4f8a48',width=3); d.polygon([(58,27),(63,26),(62,32)],fill='#9aa6b8')
B['熔炉园丁']=(im,'生长','花盆 + 高炉身体 · 头顶火焰花')
# 6 重力邮差
im,d=canvas()
d.line([(28,4),(26,20)],fill='#2f7d4f',width=4); d.line([(36,4),(38,20)],fill='#2f7d4f',width=4)
d.rectangle([22,1,30,5],fill='#3a2a1a'); d.rectangle([34,1,42,5],fill='#3a2a1a')
d.rectangle([22,20,42,40],fill='#2f9e5f'); d.rectangle([35,20,42,40],fill='#237a48')
d.ellipse([24,40,40,54],fill='#ffe0b2'); d.rectangle([28,46,31,48],fill='#101a2b'); d.rectangle([34,46,37,48],fill='#101a2b')
d.polygon([(20,54),(44,54),(40,60),(24,60)],fill='#2f9e5f'); d.rectangle([30,58,34,63],fill='#f5e6b8')
d.ellipse([42,18,62,40],fill='#f5e6b8'); d.ellipse([50,22,62,40],fill='#d8c48f'); d.line([(42,22),(30,22)],fill='#8d6e3a',width=2)
d.rectangle([47,24,55,30],fill='#ffffff'); d.line([(47,24),(51,27),(55,24)],fill='#ff6b6b')
B['重力邮差']=(im,'重力','身体倒立 · 帽子朝下 · 巨大邮包')
# 7 频律歌手
im,d=canvas()
for i,(x,h) in enumerate([(24,10),(30,16),(36,12),(42,8)]):
    d.line([(x,18),(x-2,18-h//2),(x+2,18-h)],fill='#2de0c8',width=1)
d.ellipse([22,12,42,26],fill='#e0408a'); d.rectangle([26,17,38,20],fill='#101a2b'); d.rectangle([29,18,35,19],fill='#2de0c8')
d.rectangle([18,26,46,50],fill='#e0408a'); d.rectangle([36,26,46,50],fill='#b02a6a')
d.ellipse([22,28,40,46],fill='#2b1a2e'); d.ellipse([26,32,36,42],fill='#5a3a60'); d.ellipse([29,35,33,39],fill='#2de0c8')
for k,h in enumerate([3,6,9,5]): d.rectangle([42+k*0, 0,0,0],fill=None) if False else None
for k,h in enumerate([4,8,12,6,10]): d.rectangle([48+k*3,50-h,49+k*3,50],fill='#2de0c8')
d.line([(18,30),(8,22)],fill='#e0408a',width=3); d.ellipse([3,16,11,24],fill='#9aa6b8')
d.line([(26,50),(24,62)],fill='#b02a6a',width=3); d.line([(38,50),(40,62)],fill='#b02a6a',width=3)
B['频律歌手']=(im,'节奏','喇叭胸口 · 天线头发 · 音量条')
# 8 雾锁典狱长
im,d=canvas()
d.polygon([(30,2),(18,16),(14,62),(46,62),(42,16)],fill='#4a4560'); d.polygon([(34,2),(42,16),(46,62),(36,62)],fill='#38334b')
d.ellipse([22,8,38,22],fill='#2a2638'); d.rectangle([25,14,28,16],fill='#ffd54f'); d.rectangle([32,14,35,16],fill='#ffd54f')
d.line([(42,24),(54,30)],fill='#4a4560',width=3); d.line([(54,30),(54,36)],fill='#5d6880')
d.ellipse([46,32,62,48],fill='#ffd54f'); d.rectangle([50,36,58,46],fill='#fff59d'); d.rectangle([49,35,59,36],fill='#5d6880')
for (x,y) in [(18,34),(24,46),(16,52)]:
    d.arc([x-3,y-6,x+3,y],180,360,fill='#9aa6b8'); d.rectangle([x-4,y-1,x+4,y+5],fill='#c9a227')
d.line([(20,30),(26,42),(18,50)],fill='#9aa6b8')
B['雾锁典狱长']=(im,'可见性','提灯的高大影子 · 身上挂满锁')

S=4; cell=300
CH=370
board=Image.new('RGB',(cell*4+40, CH*2+110),'#101218'); dd=ImageDraw.Draw(board)
dd.text((30,20),'八个守律者 · 概念剪影（64×64 像素，放大 4 倍）',font=font(28),fill='#e8ecf2')
for i,(name,v) in enumerate(B.items()):
    im=v[0]; pre_outlined=len(v)>3 and name=='回溯钟摆'
    sp=im if name=='回溯钟摆' else outline(im)
    if name=='回溯钟摆':
        c2=Image.new('RGBA',(N,N)); c2.alpha_composite(sp); sp=c2
    x0=20+(i%4)*cell; y0=80+(i//4)*CH
    dd.rectangle([x0+10,y0,x0+cell-10,y0+CH-20],fill='#1f2330')
    big=up(sp,S); board.paste(big,(x0+(cell-big.width)//2,y0+12),big)
    dd.text((x0+22,y0+CH-90),f'{name}',font=font(22),fill='#e8ecf2')
    dd.text((x0+22+len(name)*24,y0+CH-88),f'「{v[1]}」',font=font(18),fill='#81d4fa')
    dd.text((x0+22,y0+CH-56),v[2],font=font(15),fill='#9aa0aa')
board.save('bosses_concepts.png'); print('ok')
