from PIL import Image, ImageDraw, ImageFont

FONT = ImageFont.truetype('Consolas.ttf', 14)


class Slider:
    def __init__(self, label='value', min_value=0.0, max_value=100.0, value=0.0):
        self.base = min_value
        self.lng = max_value - min_value
        self.t = label + ':'
        self.v = min(max(value, self.base), self.base + self.lng)
        self.fmt = '%.2f'

        self.action = None
        self.height = 21
        self.img = Image.new('RGB', (400, 21))
        self.draw = ImageDraw.Draw(self.img)
        self.draw.font = FONT

        self.top = 0
        self.texture = None
        self.tx = 88 - self.draw.textsize(self.t)[0]
        self.cx = min(max(100 + int(200 * (self.v - self.base) / self.lng), 100), 300)
        self.cc = '#fff'
        self.drag = False

    def redraw(self):
        self.draw.rectangle((0, 0, 400, 21), '#fff')
        self.draw.text((self.tx, 4), self.t, '#000')
        self.draw.line((100, 10, 300, 10), '#000')
        self.draw.rectangle((self.cx - 4, 0, self.cx + 4, 20), self.cc, '#000')
        self.draw.text((312, 4), self.fmt % self.v, '#000')
        if self.texture:
            self.texture.write(self.img.tobytes(), (0, self.top, 400, 21))

    def mouse(self, mx, my, state):
        redraw = False
        hit = self.top <= my < self.top + 21 and abs(self.cx - mx) <= 4

        cc = '#fff'
        if state < 2:
            if hit:
                cc = '#eee'
        elif state == 2:
            if self.drag:
                cc = '#ddd'

        if state == 1 and hit:
            self.drag = True

        if self.drag:
            cx = min(max(mx, 100), 300)
            if self.cx != cx:
                self.cx = cx
                self.v = self.base + self.lng * (cx - 100) / 200
                if self.action:
                    self.action(self.v)
                redraw = True

        res = self.drag

        if state == 3:
            self.drag = False

        if self.cc != cc:
            self.cc = cc
            redraw = True

        if redraw:
            self.redraw()

        return res

    @property
    def value(self):
        return self.v

    @value.setter
    def value(self, value):
        self.v = min(max(value, self.base), self.base + self.lng)
        self.cx = min(max(100 + int(200 * (self.v - self.base) / self.lng), 100), 300)
        self.redraw()

    @property
    def limits(self):
        return (self.base, self.base + self.lng)

    @limits.setter
    def limits(self, value):
        min_v, max_v = value
        self.base = min_v
        self.lng = max_v - min_v
        self.cx = min(max(100 + int(200 * (self.v - self.base) / self.lng), 100), 300)
        self.v = min(max(self.v, self.base), self.base + self.lng)
        self.redraw()

    @property
    def label(self):
        return self.t[:-1]

    @label.setter
    def label(self, value):
        self.t = value + ':'
        self.tx = 88 - self.draw.textsize(self.t)[0]
        self.redraw()


class Button:
    def __init__(self, label='button', text='button'):
        self.t = label + ':'
        self.b = text

        self.action = None
        self.height = 21
        self.img = Image.new('RGB', (400, 21))
        self.draw = ImageDraw.Draw(self.img)
        self.draw.font = FONT

        self.top = 0
        self.texture = None
        self.tx = 88 - self.draw.textsize(self.t)[0]
        self.bx = 200 - self.draw.textsize(self.b)[0] // 2
        self.bc = '#fff'
        self.drag = False

    def redraw(self):
        self.draw.rectangle((0, 0, 400, 21), '#fff')
        self.draw.text((self.tx, 4), self.t, '#000')
        self.draw.rectangle((120, 0, 280, 20), self.bc, '#000')
        self.draw.text((self.bx, 4), self.b, '#000')
        if self.texture:
            self.texture.write(self.img.tobytes(), (0, self.top, 400, 21))

    def mouse(self, mx, my, state):
        redraw = False
        hit = self.top <= my < self.top + 21 and 120 <= mx <= 280

        bc = '#fff'
        if state < 2:
            if hit:
                bc = '#eee'
        elif state == 2:
            if self.drag:
                bc = '#ddd'

        if state == 1 and hit:
            self.drag = True

        res = self.drag

        if state == 3:
            if hit and self.action:
                self.action()

            self.drag = False

        if self.bc != bc:
            self.bc = bc
            redraw = True

        if redraw:
            self.redraw()

        return res

    @property
    def label(self):
        return self.t[:-1]

    @label.setter
    def label(self, value):
        self.t = value + ':'
        self.tx = 88 - self.draw.textsize(self.t)[0]
        self.redraw()

    @property
    def text(self):
        return self.b

    @text.setter
    def text(self, value):
        self.b = value
        self.bx = 200 - self.draw.textsize(self.b)[0] // 2
        self.redraw()


class Options:
    def __init__(self, label='options', options=('on', 'off'), selected=0):
        self.t = label + ':'
        self.s = selected
        self.op = options
        self.b = self.op[self.s]

        self.action = None
        self.height = 21
        self.img = Image.new('RGB', (400, 21))
        self.draw = ImageDraw.Draw(self.img)
        self.draw.font = FONT

        self.top = 0
        self.texture = None
        self.tx = 88 - self.draw.textsize(self.t)[0]
        self.bx = 200 - self.draw.textsize(self.b)[0] // 2
        self.pc = '#fff'
        self.nc = '#fff'
        self.drag = 0

    def redraw(self):
        self.draw.rectangle((0, 0, 400, 21), '#fff')
        self.draw.text((self.tx, 4), self.t, '#000')
        self.draw.rectangle((140, 0, 260, 20), '#fff', '#000')
        self.draw.rectangle((110, 0, 130, 20), self.pc, '#000')
        self.draw.rectangle((270, 0, 290, 20), self.nc, '#000')
        self.draw.text((116, 4), '<', '#000')
        self.draw.text((276, 4), '>', '#000')
        self.draw.text((self.bx, 4), self.b, '#000')
        if self.texture:
            self.texture.write(self.img.tobytes(), (0, self.top, 400, 21))

    def mouse(self, mx, my, state):
        redraw = False
        hit1 = self.top <= my < self.top + 21 and 110 <= mx <= 130
        hit2 = self.top <= my < self.top + 21 and 270 <= mx <= 290

        pc = '#fff'
        nc = '#fff'

        if state < 2:
            if hit1:
                pc = '#eee'
            if hit2:
                nc = '#eee'
        elif state == 2:
            if self.drag == 1:
                pc = '#ddd'
            if self.drag == 2:
                nc = '#ddd'

        if state == 1:
            if hit1:
                self.drag = 1
            if hit2:
                self.drag = 2

        res = self.drag

        if state == 3:
            if self.drag == 1 and hit1:
                if self.s > 0:
                    self.s -= 1
                    self.b = self.op[self.s]
                    self.bx = 200 - self.draw.textsize(self.b)[0] // 2
                    if self.action:
                        self.action(self.b)
                    redraw = True

            if self.drag == 2 and hit2:
                if self.s < len(self.op) - 1:
                    self.s += 1
                    self.b = self.op[self.s]
                    self.bx = 200 - self.draw.textsize(self.b)[0] // 2
                    if self.action:
                        self.action(self.b)
                    redraw = True

            self.drag = 0

        if self.pc != pc:
            self.pc = pc
            redraw = True

        if self.nc != nc:
            self.nc = nc
            redraw = True

        if redraw:
            self.redraw()

        return res

    @property
    def value(self):
        return self.b

    @value.setter
    def value(self, value):
        self.s = self.op.index(value)
        self.b = self.op[self.s]
        self.bx = 200 - self.draw.textsize(self.b)[0] // 2
        self.redraw()

    @property
    def label(self):
        return self.t[:-1]

    @label.setter
    def label(self, value):
        self.t = value + ':'
        self.tx = 88 - self.draw.textsize(self.t)[0]
        self.redraw()


class ColorSlider:
    def __init__(self, label='color', value=(0, 0, 0)):
        self.t = label + ':'
        r, g, b = value
        r = min(max(int(r), 0), 255)
        g = min(max(int(g), 0), 255)
        b = min(max(int(b), 0), 255)
        self.v = (r, g, b)
        self.fmt = '%d'

        self.action = None
        self.height = 65
        self.img = Image.new('RGB', (400, 65))
        self.draw = ImageDraw.Draw(self.img)
        self.draw.font = FONT

        self.top = 0
        self.texture = None
        self.tx = 88 - self.draw.textsize(self.t)[0]
        self.rx = min(max(100 + 200 * self.v[0] // 255, 100), 300)
        self.gx = min(max(100 + 200 * self.v[1] // 255, 100), 300)
        self.bx = min(max(100 + 200 * self.v[2] // 255, 100), 300)
        self.drag = 0

        self.rc = '#fff'
        self.gc = '#fff'
        self.bc = '#fff'

    def redraw(self):
        self.draw.rectangle((0, 0, 400, 65), '#fff')
        self.draw.text((self.tx, 25), self.t, '#000')
        self.draw.line((100, 10, 300, 10), '#000')
        self.draw.line((100, 31, 300, 31), '#000')
        self.draw.line((100, 52, 300, 52), '#000')
        self.draw.rectangle((self.rx - 4, 0, self.rx + 4, 20), self.rc, '#000')
        self.draw.rectangle((self.gx - 4, 22, self.gx + 4, 42), self.gc, '#000')
        self.draw.rectangle((self.bx - 4, 44, self.bx + 4, 64), self.bc, '#000')
        self.draw.rectangle((348, 12, 388, 52), self.v, '#000')
        self.draw.text((312, 4), self.fmt % self.v[0], '#000')
        self.draw.text((312, 25), self.fmt % self.v[1], '#000')
        self.draw.text((312, 46), self.fmt % self.v[2], '#000')
        if self.texture:
            self.texture.write(self.img.tobytes(), (0, self.top, 400, 65))

    def mouse(self, mx, my, state):
        redraw = True
        hit1 = self.top <= my < self.top + 21 and abs(self.rx - mx) <= 4
        hit2 = self.top + 22 <= my < self.top + 43 and abs(self.gx - mx) <= 4
        hit3 = self.top + 44 <= my < self.top + 65 and abs(self.bx - mx) <= 4

        rc = '#fff'
        gc = '#fff'
        bc = '#fff'

        if state < 2:
            if hit1:
                rc = '#eee'
            if hit2:
                gc = '#eee'
            if hit3:
                bc = '#eee'

        elif state == 2:
            if self.drag == 1:
                rc = '#ddd'
            if self.drag == 2:
                gc = '#ddd'
            if self.drag == 3:
                bc = '#ddd'

        if state == 1:
            if hit1:
                self.drag = 1
            if hit2:
                self.drag = 2
            if hit3:
                self.drag = 3

        if self.drag == 1:
            rx = min(max(mx, 100), 300)
            if self.rx != rx:
                self.rx = rx
                self.v = (int(255 * (rx - 100) / 200), self.v[1], self.v[2])
                if self.action:
                    self.action(self.v)
                redraw = True

        if self.drag == 2:
            gx = min(max(mx, 100), 300)
            if self.gx != gx:
                self.gx = gx
                self.v = (self.v[0], int(255 * (gx - 100) / 200), self.v[2])
                if self.action:
                    self.action(self.v)
                redraw = True

        if self.drag == 3:
            bx = min(max(mx, 100), 300)
            if self.bx != bx:
                self.bx = bx
                self.v = (self.v[0], self.v[1], int(255 * (bx - 100) / 200))
                if self.action:
                    self.action(self.v)
                redraw = True

        res = self.drag

        if state == 3:
            self.drag = 0

        if self.rc != rc:
            self.rc = rc
            redraw = True

        if self.gc != gc:
            self.gc = gc
            redraw = True

        if self.bc != bc:
            self.bc = bc
            redraw = True

        if redraw:
            self.redraw()

        return res

    @property
    def value(self):
        return self.v

    @value.setter
    def value(self, value):
        r, g, b = value
        r = min(max(int(r), 0), 255)
        g = min(max(int(g), 0), 255)
        b = min(max(int(b), 0), 255)
        self.v = (r, g, b)
        self.rx = min(max(100 + 200 * self.v[0] // 255, 100), 300)
        self.gx = min(max(100 + 200 * self.v[1] // 255, 100), 300)
        self.bx = min(max(100 + 200 * self.v[2] // 255, 100), 300)
        self.redraw()

    @property
    def label(self):
        return self.t[:-1]

    @label.setter
    def label(self, value):
        self.t = value + ':'
        self.tx = 88 - self.draw.textsize(self.t)[0]
        self.redraw()


class Settings:
    def __init__(self, texture, items):
        self.items = items
        self.selected = None
        top = 8
        for item in self.items:
            item.top = top
            item.texture = texture
            top += item.height + 8

    def mouse(self, mx, my, state):
        if self.selected and self.selected.mouse(mx, my, state):
            return

        for item in self.items:
            if item.top <= my and my < item.top + item.height:
                if self.selected != item:
                    self.selected = item
                    self.selected.mouse(mx, my, state)
                return


import os
import GLWindow
import ModernGL
import struct
import numpy as np
from ModernGL.ext.obj import Obj
from pyrr import Matrix44, Vector4
from PIL import Image, ImageDraw, ImageFont

wnd = GLWindow.create_window()
ctx = ModernGL.create_context()

prog = ctx.program([
    ctx.vertex_shader('''
        #version 330

        in vec2 in_vert;
        in vec2 in_text;

        out vec2 v_text;

        void main() {
            v_text = in_text;
            gl_Position = vec4(in_vert, 0.0, 1.0);
        }
    '''),
    ctx.fragment_shader('''
        #version 330

        uniform sampler2D Texture;

        in vec2 v_text;

        out vec4 f_color;

        void main() {
            f_color = texture(Texture, v_text);
        }
    '''),
])

vbo = ctx.buffer(reserve=64)

def foobar(x, y, w, h, mw=400, mh=600):
    x1 = x * 2.0 / wnd.width - 1.0
    y1 = 1.0 - y * 2.0 / wnd.height
    x2 = x1 + w * 2.0 / wnd.width
    y2 = y1 - h * 2.0 / wnd.height
    return struct.pack('4f4f4f4f',
         x1, y1, 0.0, 0.0,
         x1, y2, 0.0, h / mh,
         x2, y1, w / mw, 0.0,
         x2, y2, w / mw, h / mh,
    )

vao = ctx.simple_vertex_array(prog, vbo, ['in_vert', 'in_text'])
texture = ctx.texture((400, 600), 3, b'\xff' * 400 * 600 * 3)

settings = Settings(texture, [
    ColorSlider('color', (100, 200, 300)),
    Slider('value', -10.0, 200.0, 10.0),
    Slider('value', -10.0, 200.0, 40.0),
    Button('button', 'button'),
    Options('hello', ('apple', 'pear', 'potato', 'tomato')),
])

for item in settings.items:
    item.label = 'abc'
    item.redraw()

while wnd.update():
    mouse = wnd.mouse
    mx, my = mouse[0], wnd.height - mouse[1] - 1

    state = 0
    if wnd.key_pressed(1):
        state = 1
    elif wnd.key_released(1):
        state = 3
    elif wnd.key_down(1):
        state = 2

    if wnd.key_pressed(' '):
        settings.items[4].action = lambda x: print(x)
        settings.items[4].value = 'tomato'

    settings.mouse(mx, my, state)

    ctx.enable_only(ModernGL.BLEND)
    vbo.write(foobar(0, 0, 400, 600))
    texture.use()
    vao.render(ModernGL.TRIANGLE_STRIP)
