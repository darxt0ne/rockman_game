"""第二关敌人：拟人化的数学文具（尺寸与第一关敌人一致，可直接替换）"""
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from enemies2 import C, hx, RAMP, OUT, WHITE
from pix import up, font
from PIL import Image, ImageDraw
RAMP['chalk'] = ['#0f2a22', '#1c4436', '#2b6150', '#3f8a72', '#7fc8b0']
RAMP['wood']  = ['#3a220e', '#62391a', '#8e5a2c', '#b98250', '#e0b88a']
RAMP['paper'] = ['#6a5a38', '#a8946a', '#d8c79a', '#f2e6c8', '#fffaf0']
RAMP['brass'] = ['#4a3410', '#7a5a1c', '#b8892e', '#e8bc52', '#fff0b0']
RAMP['ink']   = ['#141826', '#232a3e', '#363f5c', '#525d82', '#8a94b8']
RAMP['plume'] = ['#4a0d14', '#8a1a26', '#d0343e', '#ff6a6a', '#ffb4b4']
CH = hx('#f4f4ec'); CHD = hx('#b8c8c0'); EYE = hx('#48f0d8'); RED = hx('#ff5a5a'); LCD = hx('#9be8a0'); LCDD = hx('#2f5a34')
def P(c, x, y, col): c.px(int(x), int(y), col)
def seg(c, x0, y0, x1, y1, col, w=1):
    n = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 1
    for s in range(n + 1):
        x = x0 + (x1 - x0) * s / n; y = y0 + (y1 - y0) * s / n
        for dx in range(w): P(c, x + dx, y, col)

def knight(f):
    """量角器骑士（28×20，面朝右）"""
    c = C(28, 20)
    # 铅笔长矛（身后，笔尖朝上）
    for y in range(3, 18):
        P(c, 6, y, c.r('brass', 3)); P(c, 7, y, c.r('brass', 2))
    P(c, 6, 2, c.r('wood', 3)); P(c, 7, 2, c.r('wood', 2)); P(c, 6, 1, c.r('wood', 3)); P(c, 7, 1, c.r('ink', 1)); P(c, 6, 0, c.r('ink', 1))
    P(c, 6, 18, hx('#ff9ad0')); P(c, 7, 18, hx('#d06a9a'))
    # 腿（两帧交替）
    lx = [(10, 13), (11, 12)][f]
    for i, x in enumerate(lx):
        for y in range(15, 18): P(c, x, y, c.r('ink', 2 + (i == 0))); P(c, x + 1, y, c.r('ink', 1))
        P(c, x - (1 if i == 0 else 0), 18, c.r('metal', 3)); P(c, x + 1, 18, c.r('metal', 3)); P(c, x + 2, 18, c.r('metal', 2))
    # 盔甲 + 罩袍
    c.box(9, 8, 17, 15, 'metal')
    for y in range(10, 15):
        for x in range(11, 16): P(c, x, y, c.r('purple', 2 if x < 14 else 1))
    P(c, 13, 11, c.r('brass', 4)); P(c, 13, 12, c.r('brass', 3))         # 胸前小徽记
    # 头盔
    c.box(9, 1, 17, 8, 'metal')
    for x in range(12, 18): P(c, x, 4, c.r('ink', 0)); P(c, x, 5, c.r('ink', 1))   # 面甲缝
    P(c, 15, 4, EYE); P(c, 16, 4, EYE); P(c, 16, 5, hx('#1fa898'))
    for x in range(10, 14): P(c, x, 2, c.r('metal', 4))
    for (x, y) in [(11, 0), (12, 0), (10, 0), (9, 1), (12, -1)]: P(c, x, y, c.r('plume', 3))
    P(c, 8, 1, c.r('plume', 2)); P(c, 8, 2, c.r('plume', 1)); P(c, 7, 3, c.r('plume', 1))
    # 量角器盾（半圆，刻度）
    sx, sy, R = 21, 15, 6.5
    for y in range(int(sy - R), int(sy) + 1):
        for x in range(int(sx - R), int(sx + R) + 1):
            d = math.hypot(x + 0.5 - sx, y + 0.5 - sy)
            if d <= R:
                col = c.r('paper', 3 if x < sx else 2)
                if d > R - 1.2: col = c.r('paper', 1)
                ang = math.atan2(sy - (y + 0.5), x + 0.5 - sx)
                if d > R - 2.6 and int(math.degrees(ang)) % 30 < 7: col = c.r('ink', 1)   # 刻度
                if d < 1.5: col = c.r('ink', 0)                                         # 中心孔
                P(c, x, y, col)
    for x in range(int(sx - R), int(sx + R) + 1): P(c, x, sy + 1, c.r('paper', 1))
    seg(c, 17, 11, 19, 13, c.r('metal', 2))                                           # 握盾的手臂
    return c.outline().im

def compass(f):
    """圆规跳跳（22×24）：f=0 蹲着（腿张开），f=1 跳起（腿并拢）"""
    c = C(22, 24)
    hx0, hy0 = 11, 8 if f == 0 else 6
    # 圆规腿：左针脚、右笔脚
    if f == 0:
        seg(c, hx0 - 1, hy0 + 7, 3, 22, c.r('metal', 4), 2); P(c, 3, 23, WHITE)
        seg(c, hx0 + 1, hy0 + 7, 18, 21, c.r('metal', 2), 2)
        P(c, 18, 22, c.r('brass', 3)); P(c, 19, 22, c.r('ink', 1)); P(c, 19, 23, c.r('ink', 0))
    else:
        seg(c, hx0 - 1, hy0 + 7, 8, 23, c.r('metal', 4), 2)
        seg(c, hx0 + 1, hy0 + 7, 13, 22, c.r('metal', 2), 2)
        P(c, 13, 23, c.r('brass', 3)); P(c, 14, 23, c.r('ink', 0))
    c.disc(hx0 + 0.5, hy0 + 7.5, 2, 'brass')                             # 铰链
    # 圆脸：平涂浅色 + 右下阴影，五官才看得清
    for y in range(hy0 - 7, hy0 + 8):
        for x in range(hx0 - 7, hx0 + 8):
            d = math.hypot(x + 0.5 - (hx0 + 0.5), y + 0.5 - (hy0 + 0.5))
            if d <= 7:
                col = c.r('paper', 3)
                if (x - hx0) + (y - hy0) > 6: col = c.r('paper', 2)
                if d > 6.2 and (x - hx0) + (y - hy0) > 2: col = c.r('paper', 1)
                if (x - hx0) + (y - hy0) < -7: col = c.r('paper', 4)
                P(c, x, y, col)
    # 头发
    for x in range(hx0 - 4, hx0 + 4): P(c, x, hy0 - 7, c.r('wood', 1)); P(c, x, hy0 - 6, c.r('wood', 2) if x % 2 else c.r('wood', 1))
    P(c, hx0 + 1, hy0 - 8, c.r('wood', 2)); P(c, hx0 + 2, hy0 - 9, c.r('wood', 2))
    # 粗框圆眼镜
    for ex in (hx0 - 3, hx0 + 4):
        for (dx, dy) in [(-1,-2),(0,-2),(1,-2),(-2,-1),(2,-1),(-2,0),(2,0),(-2,1),(2,1),(-1,2),(0,2),(1,2)]:
            P(c, ex + dx, hy0 - 1 + dy, c.r('ink', 0))
        for (dx, dy) in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]: P(c, ex + dx, hy0 - 1 + dy, hx('#e8f6ff'))
        P(c, ex, hy0 - 1, c.r('ink', 0)); P(c, ex + 1, hy0 - 1 + (0 if f == 0 else -1), c.r('ink', 0)); P(c, ex - 1, hy0 - 2, WHITE)
    P(c, hx0, hy0 - 1, c.r('ink', 0)); P(c, hx0 + 1, hy0 - 1, c.r('ink', 0))         # 镜梁
    # 嘴：张嘴大笑（跳起时）或咧嘴笑
    if f == 1:
        for x in range(hx0 - 1, hx0 + 3): P(c, x, hy0 + 3, c.r('wood', 0)); P(c, x, hy0 + 4, hx('#d04a5a'))
    else:
        for k in range(-2, 4): P(c, hx0 + k, hy0 + 3 + (1 if 0 <= k <= 1 else 0), c.r('wood', 0))
    P(c, hx0 - 4, hy0 + 2, hx('#f0a0a0')); P(c, hx0 + 5, hy0 + 2, hx('#f0a0a0'))     # 腮红
    # 小手
    P(c, hx0 - 8, hy0 + 2 - f * 3, c.r('paper', 2)); P(c, hx0 - 7, hy0 + 3 - f * 2, c.r('paper', 2))
    P(c, hx0 + 9, hy0 + 2 - f * 3, c.r('paper', 2)); P(c, hx0 + 8, hy0 + 3 - f * 2, c.r('paper', 2))
    return c.outline().im

def board(f):
    """黑板飞贼（28×18）：蝙蝠翅膀 + 粉笔画的脸"""
    c = C(28, 18)
    # 翅膀
    up_ = f == 0
    for side in (-1, 1):
        bx = 14 + side * 7
        pts = [(bx, 6), (bx + side * 6, 1 if up_ else 9), (bx + side * 9, 3 if up_ else 12), (bx + side * 7, 7 if up_ else 13), (bx + side * 4, 6 if up_ else 11), (bx, 9)]
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        for y in range(min(ys), max(ys) + 1):
            for x in range(min(xs), max(xs) + 1):
                # 简单的点在多边形内判断
                inside = False; j = len(pts) - 1
                for i in range(len(pts)):
                    xi, yi = pts[i]; xj, yj = pts[j]
                    if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi + 1e-9) + xi: inside = not inside
                    j = i
                if inside: P(c, x, y, c.r('purple', 2 if (x + y) % 5 else 1))
        seg(c, bx, 6, pts[1][0], pts[1][1], c.r('purple', 4))
    # 黑板（木框 + 绿板）
    c.box(7, 3, 20, 14, 'wood')
    for y in range(5, 13):
        for x in range(9, 19): P(c, x, y, c.r('chalk', 2 if (x * 3 + y) % 7 else 1))
    # 粉笔画的脸：斜眉、眼睛、坏笑
    for (x, y) in [(10, 6), (11, 7), (17, 6), (16, 7)]: P(c, x, y, CH)
    P(c, 11, 8, CH); P(c, 16, 8, CH); P(c, 12, 8, CHD); P(c, 15, 8, CHD)
    for k, x in enumerate(range(11, 17)): P(c, x, 11 - (1 if x in (11, 16) else 0), CH)
    P(c, 13, 11, WHITE); P(c, 14, 12, CHD)
    # 拿着粉笔的小手
    seg(c, 20, 11, 23, 13, c.r('wood', 3)); P(c, 24, 13, CH); P(c, 25, 14, CH); P(c, 24, 14, CHD)
    P(c, 13, 15, c.r('wood', 2)); P(c, 14, 15, c.r('wood', 2))            # 粉笔槽
    return c.outline().im

def calculator():
    """计算器炮兵（26×20）：液晶屏上是一张怒脸"""
    c = C(26, 20)
    c.box(6, 0, 19, 18, 'ink')
    # 液晶屏
    for y in range(2, 8):
        for x in range(8, 18): P(c, x, y, LCDD if y in (2, 7) else hx('#3f7a46'))
    for (x, y) in [(9, 3), (10, 4), (11, 4), (16, 3), (15, 4), (14, 4)]: P(c, x, y, LCD)           # 怒眉
    for (x, y) in [(10, 5), (11, 5), (14, 5), (15, 5)]: P(c, x, y, hx('#d8ffd8'))                   # 眼
    for x in range(11, 15): P(c, x, 7 if x in (11, 14) else 6, LCD)                                  # 嘴（撇下）
    # 按键
    keys = ['#c9d2e0', '#c9d2e0', '#c9d2e0', '#ff9c45']
    for r in range(3):
        for k in range(4):
            x, y = 8 + k * 3, 10 + r * 3
            col = hx(keys[k] if r < 2 else ('#c9d2e0' if k < 3 else '#ff5a5a'))
            P(c, x, y, col); P(c, x + 1, y, col); P(c, x, y + 1, c.r('ink', 1)); P(c, x + 1, y + 1, c.r('ink', 1))
    # 太阳能板
    for x in range(14, 18): P(c, x, 9, hx('#4a3a6a'))
    # 小脚
    for x in (8, 9, 16, 17): P(c, x, 19, c.r('metal', 2))
    P(c, 7, 1, c.r('ink', 4)); P(c, 8, 1, c.r('ink', 4))
    return c.outline().im
def cbarrel():
    c = C(16, 7)
    c.box(0, 1, 12, 5, 'metal')
    for x in range(2, 11, 3): P(c, x, 2, c.r('metal', 4)); P(c, x, 4, c.r('metal', 1))
    c.box(12, 0, 15, 6, 'brass')
    P(c, 15, 3, hx('#9be8a0'))
    return c.outline().im
def strip(frames):
    w, h = frames[0].size; st = Image.new('RGBA', (w * len(frames), h), (0, 0, 0, 0))
    for i, f in enumerate(frames): st.paste(f, (i * w, 0))
    return st
S = {'walker': strip([knight(0), knight(1)]), 'hopper': strip([compass(0), compass(1)]),
     'flyer': strip([board(0), board(1)]), 'turret': calculator(), 'barrel': cbarrel()}
for k, v in S.items(): v.save(f'sp3_{k}.png')
Z = 8; board_ = Image.new('RGB', (1500, 330), '#0b0e1e'); d = ImageDraw.Draw(board_)
x = 20
for k, lab in [('walker', '量角器骑士'), ('hopper', '圆规跳跳'), ('flyer', '黑板飞贼'), ('turret', '计算器炮兵')]:
    sp = S[k]
    if k == 'turret':
        comp = Image.new('RGBA', (sp.width + 12, sp.height), (0, 0, 0, 0)); comp.alpha_composite(S['barrel'], (19, 5)); comp.alpha_composite(sp, (0, 0)); sp = comp
    z = 6 if sp.width > 40 else Z
    big = up(sp, z); board_.paste(big, (x, 20), big)
    d.text((x, 30 + big.height), lab, font=font(20), fill='#e8ecf2')
    x += big.width + 30
board_.save('enemies3_board.png'); print('ok')
