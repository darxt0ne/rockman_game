import sys; sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from pix import *
A = [
"........................",
"..........KKKK..........",
"........KKBBBBKK........",
".......KBBLLBBBBK.......",
"......KBLLBBBBBBBK......",
".....KBLBBBBBBBBBBK.....",
".....KBBBBBBBBBBBBK.....",
"....KBBBBBBBBBBBBBBK....",
"....KBBBBBBBKKKKKKKKK...",
"....KbBBBBBKdDDDYYYWK...",
"....KbBBBBBKdDDYYYYYK...",
"....KbbBBBBKddDDyYYyK...",
".....KbbBBBBKKKKKKKK....",
"......KKbbbbbbbbbK......",
".......KKKKKKKKKK.......",
".......KDDDDDDDDK.......",
"......KBBBBBBBBBBK......",
".....KBLLBBBBBBBBBKKKKK.",
".....KBLDDDDDDDDBKGGGGGK",
".....KBBDCDDCDDDBKGLWWGK",
".....KbBDDDDDDDDBKgGGGGK",
".....KbbBBBBBBBBbKKggggK",
"......KbbbbbbbbbK..KKKK.",
"......KDDDDDDDDDK.......",
"......KdKDDDDDDKdK......",
"......KBBK...KBBK.......",
"......KbBK...KbBK.......",
".....KOOOOK.KOOOOK......",
"....KOOWOOOKOOWOOOK.....",
"....KOOOOOOOKOOOOOOK....",
"....KoooooooKoooooooK...",
".....KKKKKKKKKKKKKKK....",
]
B = [
"..............KK........",
".............KLBK.......",
".........KKKKBBK........",
".......KKBBBBBBKK.......",
"......KBBLLLBBBBBK......",
".....KBBLBBBBBBBBBK.....",
".....KBBBBBBBBBBBBK.....",
"....KBBBBBKKKKKKKKKK....",
"....KBBBBKWWdDDDWWdK....",
"....KbBBBKWYdDDDWYdK....",
"....KbBBBKddDDDDDddK....",
"....KbbBBBKKKKKKKKK.....",
".....KbbbBBBBBBBbK......",
"......KKbbbbbbbbK.......",
".......KKKKKKKKK........",
".......KGGGGGGGK........",
"......KDDDDDDDDDK.......",
".....KDBBBBBBBBDKKKKKK..",
".....KDBLLBBBBBDKGGGGGK.",
".....KDBLCCBBBBDKGLWWGGK",
".....KDBBCCBBBBDKgGGGGGK",
".....KDbBBBBBBbDKKgggggK",
"......KDbbbbbbbDK.KKKKK.",
"......KgggggggggK.......",
"......KGKGGGGGKGK.......",
"......KDDK...KDDK.......",
"......KdDK...KdDK.......",
".....KGGGGK.KGGGGK......",
"....KGGWGGGKGGWGGGK.....",
"....KGGGGGGGKGGGGGGK....",
"....KgggggggKgggggggK...",
".....KKKKKKKKKKKKKKK....",
]
C = [
"........................",
"........................",
"..........KKKKK.........",
"........KKBBBBBKK.......",
".......KBLLBBBBBBK......",
"......KBLBBBBBBBBBK.....",
"......KBBBBBBBBBBBK.....",
".....KBBBBBBKKKKKKKK....",
".....KbBBBBKdDYYDYYK....",
".....KbBBBBKdDYWDYWK....",
".....KbbBBBKddDDDDDK....",
"......KbbBBBKKKKKKK.....",
"..KK...KKbbbbbbbK.......",
".KRRKKKRRRRRRRRRK.......",
"KRRrRRRRRRRRRRRRK.......",
"KRrKKKRRrrrrrRRK........",
".KK..KDBBBBBBBBDK.......",
".....KBLLBBBBBBBBKKKKK..",
".....KBLBBBBBBBBKGGGGGK.",
".....KBBBCBBCBBBKGLWWGK.",
".....KbBBBBBBBBBKgGGGGK.",
".....KbbBBBBBBBbKKggggK.",
"......KbbbbbbbbK..KKKK..",
"......KDDDDDDDDK........",
"......KdDDDDDDdK........",
"......KBBK..KBBK........",
"......KbBK..KbBK........",
".....KOOOOKKOOOOK.......",
"....KOOWOOOKOWOOOK......",
"....KOOOOOOKOOOOOOK.....",
"....KooooooKoooooooK....",
".....KKKKKKKKKKKKKK.....",
]
def main():
    designs=[('A 工作头盔 · 独眼探照灯', '最贴近原型，一眼看出朝向', A),
             ('B 机甲护目 · 天线鳍', '更硬派，偏“战斗机器人”', B),
             ('C 圆头 · 红围巾', '更可爱，围巾在跑动时能表现速度', C)]
    S=8
    W_=1500; H_=560
    board=Image.new('RGB',(W_,H_),'#181a21'); d=ImageDraw.Draw(board)
    d.text((40,24),'主角「残响」概念：三个方向（24×32 像素，放大 8 倍）',font=font(30),fill='#e8ecf2')
    for i,(t,sub,g) in enumerate(designs):
        sp=sprite(g); x0=60+i*480; y0=100
        d.rectangle([x0-20,y0-16,x0+420,y0+350],fill='#262b37')
        big=up(sp,S); board.paste(big,(x0,y0),big)
        # 实际游戏尺寸（放大 2 倍）与镜像
        small=up(sp,2); board.paste(small,(x0+230,y0+190),small); board.paste(up(flip(sp),2),(x0+290,y0+190),up(flip(sp),2))
        d.text((x0+230,y0+165),'游戏内 2×',font=font(16),fill='#7a8090')
        d.text((x0,y0+275),t,font=font(24),fill='#e8ecf2')
        d.text((x0,y0+310),sub,font=font(18),fill='#9aa0aa')
    # 调色板
    d.text((60,470),'主角调色板',font=font(20),fill='#9aa0aa')
    for i,k in enumerate('KdDbBLWYyOoGgCR'):
        d.rectangle([200+i*44,462,236+i*44,498],fill=PAL[k],outline='#30343e')
    board.save('hero_concepts.png')
    print('saved')
if __name__=="__main__": main()
