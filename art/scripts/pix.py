"""像素画小工具：字符网格精灵 + 放大渲染 + 中文标注"""
from PIL import Image, ImageDraw, ImageFont
PAL = {
 'K':'#101a2b','B':'#4fc3f7','L':'#b8ecff','b':'#2a86c2','D':'#1d3b5e','d':'#13283f',
 'Y':'#fff59d','y':'#f2c94c','W':'#ffffff','G':'#9aa6b8','g':'#5d6880','O':'#ff9f43','o':'#c46a1c',
 'C':'#7fffd4','R':'#ff6b6b','r':'#b83b4b',
}
FONT='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
def font(sz): return ImageFont.truetype(FONT, sz)
def sprite(rows, w=24, pal=PAL):
    h=len(rows); im=Image.new('RGBA',(w,h),(0,0,0,0))
    for y,row in enumerate(rows):
        assert len(row)<=w, (y,len(row),row)
        for x,c in enumerate(row):
            if c!='.' and c!=' ': im.putpixel((x,y), Image.new('RGB',(1,1),pal[c]).getpixel((0,0))+(255,))
    return im
def up(im,k): return im.resize((im.width*k, im.height*k), Image.NEAREST)
def flip(im): return im.transpose(Image.FLIP_LEFT_RIGHT)
