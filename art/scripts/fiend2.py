"""Boss 3 v2：函数怪（拟人化）——显示器头的疯狂数学教授（64×72，3 姿势 × 普通/愤怒）"""
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from enemies2 import C, hx, RAMP, OUT, WHITE
from pix import up
from PIL import Image
RAMP['robe']  = ['#1a0f2e', '#2e1a52', '#46287a', '#6a40a8', '#9a72d8']
RAMP['gold']  = ['#5e3a0a', '#a86a14', '#e0a030', '#ffd166', '#fff0c0']
RAMP['case']  = ['#1e2030', '#33364c', '#4d516e', '#727896', '#a9aec8']
RAMP['skin']  = ['#3a3f52', '#5c6278', '#868ca4', '#b4b9cc', '#e4e7f0']   # 金属手
RAMP['teal']  = ['#0a3a36', '#126a62', '#1fa898', '#48f0d8', '#c8fff6']
SCREEN = hx('#06231f'); SCAN = hx('#0b302a')
def P(c, x, y, col):
    c.px(int(x), int(y), col)
def seg(c, x0, y0, x1, y1, col, w=1):
    n = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 1
    for s in range(n + 1):
        x = x0 + (x1 - x0) * s / n; y = y0 + (y1 - y0) * s / n
        for dx in range(w): P(c, x + dx, y, col)
def fiend(pose, angry):
    c = C(64, 72)
    cx = 32
    eye = hx('#ff5a5a') if angry else hx('#48f0d8')
    eye2 = hx('#a3202c') if angry else hx('#1fa898')
    # ---- 长袍下摆：飘动的布条 + 青色光 ----
    for i, x in enumerate(range(19, 46, 4)):
        L = 5 + (i * 3) % 5
        for k in range(L):
            for dx in range(3):
                P(c, x + dx + (1 if k > 2 else 0), 62 + k, c.r('robe', 1 if dx == 2 else 2))
        P(c, x + 1, 62 + L, c.r('teal', 3)); P(c, x + 1, 63 + L, c.r('teal', 2))
    # ---- 长袍主体（梯形） ----
    for y in range(30, 63):
        half = 9 + (y - 30) * 0.33
        x0, x1 = int(cx - half), int(cx + half)
        for x in range(x0, x1 + 1):
            k = 2
            if x <= x0 + 1: k = 3
            elif x >= x1 - 1: k = 1
            elif x > cx + 2: k = 2 if (x - cx) < half * 0.6 else 1
            if y > 58: k = max(0, k - 1)
            P(c, x, y, c.r('robe', k))
        P(c, cx, y, c.r('gold', 3 if y < 50 else 2)); P(c, cx + 1, y, c.r('gold', 1))     # 前襟金边
    # 刺绣的粉笔公式（∑ 和 π）
    for (x, y) in [(24, 40), (25, 40), (26, 40), (24, 41), (25, 42), (24, 43), (24, 44), (25, 44), (26, 44)]: P(c, x, y, hx('#d8d0f0'))
    for (x, y) in [(37, 47), (38, 47), (39, 47), (40, 47), (38, 48), (38, 49), (38, 50), (40, 48), (40, 49), (40, 50)]: P(c, x, y, hx('#d8d0f0'))
    # 白色学者领
    for x in range(cx - 8, cx + 9):
        P(c, x, 30, c.r('case', 4)); P(c, x, 31, c.r('case', 3 if abs(x - cx) > 3 else 4))
    for x in range(cx - 5, cx + 6): P(c, x, 32, c.r('case', 2))
    # ---- 手臂 ----
    if pose == 'idle':
        back = [(cx - 9, 33), (cx - 15, 38), (cx - 20, 34)]          # 托着发光图像
        front = [(cx + 9, 33), (cx + 14, 40), (cx + 17, 46)]          # 握圆规
        orb = (cx - 21, 30); staff = (cx + 18, 46)
    elif pose == 'cast':
        back = [(cx - 9, 33), (cx - 16, 27), (cx - 20, 19)]
        front = [(cx + 9, 33), (cx + 16, 27), (cx + 20, 20)]
        orb = (cx - 21, 15); staff = (cx + 21, 20)
    else:   # dive：圆规向前下方刺出
        back = [(cx - 9, 33), (cx - 16, 36), (cx - 22, 40)]
        front = [(cx + 9, 33), (cx + 17, 38), (cx + 24, 44)]
        orb = None; staff = (cx + 25, 44)
    for pts in (back, front):
        for (a, b) in zip(pts, pts[1:]):
            seg(c, a[0], a[1], b[0], b[1], c.r('robe', 3), 2)
        hx_, hy_ = pts[-1]
        c.disc(hx_ + 0.5, hy_ + 0.5, 2.2, 'skin')                        # 金属手
    # 发光的函数图像（手上托着）
    if orb:
        ox, oy = orb
        for k in range(-6, 7):
            yy = oy - 3 * math.sin(k / 1.8)
            P(c, ox + k, yy, c.r('teal', 3)); P(c, ox + k, yy + 1, c.r('teal', 1))
        seg(c, ox - 7, oy + 4, ox + 7, oy + 4, c.r('teal', 2)); seg(c, ox, oy - 6, ox, oy + 5, c.r('teal', 2))
    # 巨大的绘图圆规（法杖）
    sx, sy = staff
    if pose == 'dive':
        seg(c, sx - 2, sy - 6, sx + 7, sy + 14, c.r('case', 4), 2)
        seg(c, sx + 2, sy - 6, sx + 11, sy + 12, c.r('case', 2), 2)
        P(c, sx + 8, sy + 15, WHITE)
    else:
        top = sy - 20 if pose != 'cast' else sy - 18
        seg(c, sx, top, sx - 3, sy + 22, c.r('case', 4), 2)             # 针脚
        seg(c, sx + 1, top, sx + 5, sy + 20, c.r('case', 2), 2)         # 笔脚
        P(c, sx - 3, sy + 23, WHITE); P(c, sx + 5, sy + 21, c.r('gold', 3))
        c.disc(sx + 1, top, 2.5, 'gold')                                  # 铰链
    # ---- 显示器头 ----
    hy = 9
    c.box(cx - 12, hy, cx + 12, hy + 19, 'case')
    for y in range(hy + 3, hy + 17):                                      # 屏幕
        for x in range(cx - 9, cx + 10):
            P(c, x, y, SCAN if y % 2 else SCREEN)
    P(c, cx - 9, hy + 3, c.r('teal', 1)); P(c, cx - 8, hy + 3, c.r('teal', 0))   # 屏幕反光
    for x in range(cx - 8, cx - 4): P(c, x, hy + 4, hx('#123f38'))
    # 脸：眉毛、眼睛、示波器嘴
    ey = hy + 8
    for side in (-1, 1):
        ex = cx + side * 5
        ew = 3 if pose != 'cast' else 4
        for dx in range(-ew // 2, ew - ew // 2):
            P(c, ex + dx, ey, eye); P(c, ex + dx, ey + 1, eye2)
            if pose == 'cast': P(c, ex + dx, ey - 1, eye)
        P(c, ex, ey, WHITE)
        # 眉毛（愤怒时向内下压）
        tilt = 1 if (angry or pose == 'dive') else 0
        for dx in range(-2, 3):
            P(c, ex + dx, ey - 3 + (tilt * (1 if dx * side < 0 else 0)) - (0 if pose != 'cast' else 1), eye2)
    my = hy + 13
    amp = 2 if pose == 'cast' else 1
    for k in range(-6, 7):
        yy = my - round(amp * math.sin(k * (1.2 if pose != 'dive' else 2.0)))
        P(c, cx + k, yy, eye)
    # 机壳细节：侧面旋钮 + 天线
    c.disc(cx - 13.5, hy + 9.5, 1.6, 'gold'); c.disc(cx + 14.5, hy + 9.5, 1.6, 'gold')
    for x in range(cx - 7, cx + 8, 3): P(c, x, hy + 18, c.r('case', 1))
    # ---- 学位帽 ----
    for y in range(0, 7):                                                  # 菱形帽顶
        w = 15 - abs(3 - y) * 3
        for x in range(cx - w, cx + w + 1):
            P(c, x, y + 1, c.r('robe', 1 if y > 3 else 0 if abs(x - cx) > w - 2 else 1))
    for x in range(cx - 15, cx + 16): P(c, x, 4, c.r('robe', 2))
    for x in range(cx - 8, cx + 9): P(c, x, 8, c.r('gold', 3)); P(c, x, 9, c.r('gold', 1))   # 金色帽箍
    P(c, cx, 4, c.r('gold', 4))
    seg(c, cx, 4, cx + 13, 6, c.r('gold', 3)); seg(c, cx + 13, 6, cx + 13, 14, c.r('gold', 2))   # 流苏
    for k in range(3): P(c, cx + 12 + k, 15, c.r('gold', 3)); P(c, cx + 12 + k, 16, c.r('gold', 2))
    return c.outline().im
poses = ['idle', 'cast', 'dive']
st = Image.new('RGBA', (64 * 6, 72), (0, 0, 0, 0))
for a in range(2):
    for i, p in enumerate(poses): st.paste(fiend(p, a == 1), ((a * 3 + i) * 64, 0))
st.save('sp_fiend2.png')
b = Image.new('RGB', (64 * 6 * 4 + 40, 72 * 4 + 40), '#0b0e1e'); big = up(st, 4); b.paste(big, (20, 20), big); b.save('fiend2_board.png')
print('ok')
