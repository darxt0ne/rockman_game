"""主角 A 精修版：逐像素手绘"""
import sys; sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from pix import font, up
from PIL import Image, ImageDraw
PAL = {
 'K':'#0a101c','N':'#16376a',
 '1':'#1d64a3','2':'#3aa8e8','3':'#86d6ff','4':'#dcf5ff',
 'v':'#0b1526','V':'#1c3256','u':'#4a73ab',
 'm':'#262c3b','n':'#465064','M':'#7a869c','H':'#b4bfd2','h':'#eef3fa',
 'd':'#0d182c','D':'#1c3358','E':'#2c4f82',
 'Y':'#fff07a','y':'#f0b02e','W':'#ffffff',
 'O':'#9a4512','P':'#de7628','Q':'#ffaa58','o':'#55250b',
 't':'#14a88a','T':'#3df0c8',
 'R':'#ff5a5a','r':'#b32e3a',
}
LEGS = {
 'idle': [
    ".KKK.KDEDDDK............",
    "....NEDK.NEEDK..........",
    "....NEDK.NMHMK..........",
    "....NDdK.NEDDK..........",
    "....NDdK.NDDdK..........",
    "...NQPPOKNQPPOK.........",
    "..NQQPPPPNQQPPPPOK......",
    "..NPPPPPPOKPPPPPPPPOK...",
    "..NOOOOOOOKOOOOOOOOOOK..",
    "...KKKKKKKKKKKKKKKKKK...",
 ],
 'run1': [
    ".KKK.KDEDDDK............",
    "...NEDK..NEEDK..........",
    "..NEDK....NMHMK.........",
    ".NQPOK.....NEDDK........",
    "NQPPPOK....NEDdK........",
    "NOOOOK....NQPPPOK.......",
    ".KKKK....NQQPPPPOK......",
    ".........NPPPPPPPPOK....",
    ".........NOOOOOOOOOK....",
    "..........KKKKKKKKKK....",
 ],
 'run2': [
    ".KKK.KDEDDDK............",
    "....NEDKNEEDK...........",
    "....NEDKNMHMK...........",
    "....NDdNQPPPOK..........",
    "....NDdKNOOOOOK.........",
    "...NQPPOKKKKKK..........",
    "..NQQPPPPOK.............",
    "..NPPPPPPPPOK...........",
    "..NOOOOOOOOOK...........",
    "...KKKKKKKKK............",
 ],
 'jump': [
    ".KKK.KDEDDDK............",
    "....NEDKNEEDK...........",
    "...NEDK.NMHMNQPPOK......",
    "..NEDK..NEDNQPPPPOK.....",
    ".NQPPOK..KKNOOOOOOK.....",
    "NQPPPPOK....KKKKKK......",
    "NOOOOOOK................",
    ".KKKKKK.................",
    "........................",
    "........................",
 ],
}

LEGS.update({
 'run3': [
    ".KKK.KDEDDDK............",
    "...NEEK..NDDK...........",
    "..NMHMK...NDdK..........",
    ".NQPPOK....NDdK.........",
    "NQPPPPOK...NDddK........",
    "NOOOOOK...NOPPPOK.......",
    ".KKKKK...NOPPPPPOK......",
    ".........NOPPPPPPPOK....",
    ".........NOOOOOOOOOK....",
    "..........KKKKKKKKKK....",
 ],
 'run4': [
    ".KKK.KDEDDDK............",
    ".....NEEDKDK............",
    ".....NMHMKDdK...........",
    ".....NEDDNOPPOK.........",
    ".....NEDDKOOOOOK........",
    "....NQPPOKKKKKK.........",
    "...NQQPPPPOK............",
    "...NPPPPPPPPOK..........",
    "...NOOOOOOOOOK..........",
    "....KKKKKKKKKK..........",
 ],
 'fall': [
    ".KKK.KDEDDDK............",
    "....NEDK.NEEDK..........",
    "....NEDK.NMHMK..........",
    "...NEDK...NEDDK.........",
    "...NQPPOK.NQPPOK........",
    "..NQPPPPOKNPPPPPOK......",
    "..NOOOOOOKNOOOOOOK......",
    "...KKKKKK..KKKKKK.......",
    "........................",
    "........................",
 ],
 'dash': [
    ".KKKKKDEDDDK............",
    "..NEEDK..NEEDDK.........",
    ".NMHMK.....NMHMK........",
    "NEDK........NEDDK.......",
    "NQPPOK......NQPPPOK.....",
    "NPPPPPOK....NQQPPPPPOK..",
    "NOOOOOOK....NOOOOOOOOOK.",
    ".KKKKKK......KKKKKKKKK..",
 ],
 'wall': [
    ".KKK.KDEDDDK............",
    ".NQPEDK.NEEDK...........",
    "NQPPOK..NMHMK...........",
    "NPPOK...NEDDK...........",
    "NOOK....NEDDK...........",
    ".KK.....NQPPOK..........",
    "........NQQPPPOK........",
    "........NPPPPPPOK.......",
    "........NOOOOOOOK.......",
    ".........KKKKKKKK.......",
 ],
 'hurt': [
    ".KKK.KDEDDDK............",
    "...NEDK...NEEDK.........",
    "..NEDK.....NMHMK........",
    ".NQPOK......NEDDK.......",
    "NQPPPOK....NQPPPOK......",
    "NOOOOOK...NQPPPPPOK.....",
    ".KKKKK....NOOOOOOOK.....",
    "...........KKKKKKKK.....",
    "........................",
    "........................",
 ],
})
def legs_bob(pose, bob):
    L = list(LEGS[pose])
    if bob > 0: L = L[bob:]                 # 身体下沉：去掉髋部行
    elif bob < 0: L = [L[0]] + [L[1]]*(1-bob) + L[2:]   # 身体抬起：拉长大腿
    return L

def body_rows(pose='idle'):
    return BODY + LEGS[pose]
BODY_ = [
    "..NN3322222N3443K.......",
    ".NDE32DDDD2233221K......",
    ".NDE2DDDDD2122211K......",
    ".NDE2DDTTD2KNHhHHHHMMnK.",
    ".NDE2DDDDD1KNHMHMHMMnmK.",
    ".NDD1222221KNMMMMMMnntK.",
    ".KHMKnMMMMnKKmnnnnnmmmK.",
    ".KMnKmnmnmnK.KKKKKKKKK..",
    ]
_unused = [
    "....NEDK.NEEDK..........",
    "....NEDK.NMHMK..........",
    "....NDdK.NEDDK..........",
    "....NDdK.NDDdK..........",
    "...NQPPOKNQPPOK.........",
    "..NQQPPPPNQQPPPPOK......",
    "..NPPPPPPOKPPPPPPPPOK...",
    "..NOOOOOOOKOOOOOOOOOOK..",
    "...KKKKKKKKKKKKKKKKKK...",
    ]
HEAD = [
 "."*32,
 "."*12+"NNNNKK"+"."*14,
 "."*10+"NN344322KK"+"."*12,
 "."*9+"N3444322221K"+"."*11,
 "."*8+"N344322222221K"+"."*10,
 "."*7+"N3432222222221K"+"."*10,
 "."*7+"N33"+"2"*11+"1K"+"."*9,
 "."*6+"N3222222"+"K"*9+"."*9,
 "."*6+"N3nHM221"+"KuuVVvMyYyK"+"."*7,
 "."*6+"N2HTM221"+"KVuVvvMYWYK"+"."*7,
 "."*6+"N2nMn211"+"KvVvvvMyYyK"+"."*7,
 "."*7+"N122111"+"K"*9+"."*9,
 "."*8+"K11111"+"KMHHMnK"+"."*11,
 "."*11+"KnMMnK"+"."*15,
]
BODY = BODY_
def grid(pose='idle', bob=0):
    head = [r.replace('Y','R').replace('W','R').replace('y','r') for r in HEAD] if pose=='hurt' else HEAD
    rows = head + ["."*6 + r + "."*(26-len(r)) for r in BODY + legs_bob(pose, bob)]
    while len(rows) < 32: rows.insert(0, "."*32)
    while len(rows) > 32:
        assert set(rows[0]) == {'.'}, 'top row not empty'
        rows.pop(0)
    for i,r in enumerate(rows): assert len(r)==32, (i,len(r),r)
    assert len(rows)==32, len(rows)
    return rows
def img(rows):
    im=Image.new('RGBA',(32,32),(0,0,0,0)); p=im.load()
    for y,r in enumerate(rows):
        for x,c in enumerate(r):
            if c!='.': h=PAL[c].lstrip('#'); p[x,y]=(int(h[0:2],16),int(h[2:4],16),int(h[4:6],16),255)
    return im
FRAMES=[('idle',0),('idle',1),('run1',0),('run1',1),('run2',-1),('run3',0),('run3',1),('run4',-1),
        ('jump',0),('fall',0),('dash',0),('wall',0),('hurt',-1)]
NAMES=['站立','呼吸','跑1','跑2','跑3','跑4','跑5','跑6','上升','下落','冲刺','滑墙','受伤']
def strip():
    st=Image.new('RGBA',(32*len(FRAMES),32),(0,0,0,0))
    for i,(p,b) in enumerate(FRAMES): st.paste(img(grid(p,b)),(i*32,0))
    return st
if __name__=='__main__':
    st=strip(); st.save('hero_A_strip.png')
    Z=6; cw=32*Z+12
    b2=Image.new('RGB',(cw*7+20,(32*Z+50)*2+20),'#14161d'); dd=ImageDraw.Draw(b2)
    for i,(p,_) in enumerate(FRAMES):
        fr=st.crop((i*32,0,i*32+32,32)); x0=10+(i%7)*cw; y0=10+(i//7)*(32*Z+50)
        dd.rectangle([x0,y0,x0+32*Z,y0+32*Z],fill='#262b37'); big=up(fr,Z); b2.paste(big,(x0,y0),big)
        dd.text((x0,y0+32*Z+8),NAMES[i],font=font(20),fill='#e8ecf2')
    b2.save('hero_A_frames.png')
    sp=img(grid())
    sp.save('hero_A_idle.png')
    board=Image.new('RGB',(900,420),'#14161d'); d=ImageDraw.Draw(board)
    d.rectangle([30,30,350,350],fill='#262b37'); big=up(sp,10); board.paste(big,(30,30),big)
    for k,bg in enumerate(['#181a21','#3a4864','#8fcbea']):
        d.rectangle([400,30+k*110,860,130+k*110],fill=bg)
        for s,x in ((1,420),(2,480),(3,580)):
            sm=up(sp,s); board.paste(sm,(x,40+k*110+(96-32*s)//2 if s<3 else 34+k*110),sm)
    board.save('hero_A_v3_preview.png'); print('ok')
