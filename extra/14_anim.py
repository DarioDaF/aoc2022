
from utils import readInput, deepcopy, Pt
from PIL import Image
import argparse, os

ap = argparse.ArgumentParser()
ap.add_argument('--ground', action='store_true')
args = ap.parse_args()

text = readInput()

spawn = Pt(500, 0)
strips = []

_tl = deepcopy(spawn)
_br = deepcopy(spawn)

for line in text.strip().split('\n'):
    strip = []
    for p_str in line.split(' -> '):
        p = Pt(*(int(c) for c in p_str.split(',')))
        _tl = Pt(min(p.x, _tl.x), min(p.y, _tl.y))
        _br = Pt(max(p.x, _br.x), max(p.y, _br.y))
        strip.append(p)
    strips.append(strip)

_tl += Pt(-1, 0)
_br += Pt(+1, 0)

class Field:
    def __init__(self, tl: Pt, br: Pt):
        self.tl = tl
        self.br = br
        self.size = br - tl + Pt(1, 1)
        self._field = [ ['.' for _ in range(self.size.x)] for _ in range(self.size.y) ] # field[y][x]
    def drawStrip(self, strip):
        oldp = strip[0]
        self[oldp] = '#'
        for p in strip[1:]:
            d = (p - oldp).toDir()
            while oldp != p:
                oldp += d
                self[oldp] = '#'
    def __getitem__(self, key: Pt):
        rel = key - self.tl
        return self._field[rel.y][rel.x]
    def __setitem__(self, key: Pt, val: str):
        rel = (key - self.tl)
        self._field[rel.y][rel.x] = val
    def __repr__(self):
        return '\n'.join(''.join(line) for line in self._field)
    def img(self):
        palette = {
            '#': (0, 0, 0),
            '.': (255, 255, 255),
            '+': (255, 0, 0),
            'o': (255, 255, 0),
        }
        img = Image.new('RGB', self.size.toTuple(), (255, 255, 255))
        img.putdata([palette[c] for line in self._field for c in line])
        return img

# Dropping sand

# @TODO: Could be WAY more efficient cause each grain falls in the same line of the current
#        one and so you can backtrack to check where it goes instead of falling from the top
def dropGrainIt(field, spawn):
    cur_grain = deepcopy(spawn)
    settled = False
    while not settled:
        yield settled, cur_grain
        if cur_grain.y == _br.y:
            break
        new_grain = cur_grain + Pt(0, 1)
        if field[new_grain] == '.':
            cur_grain = new_grain
            continue
        new_grain = cur_grain + Pt(-1, 1)
        if field[new_grain] == '.':
            cur_grain = new_grain
            continue
        new_grain = cur_grain + Pt(+1, 1)
        if field[new_grain] == '.':
            cur_grain = new_grain
            continue
        settled = True
    if settled:
        field[cur_grain] = 'o'
    return settled, cur_grain

# Creating new map with floor

if args.ground:
    # Map sizes are on a pyramid centered at the source so:
    _br += Pt(0, 2)
    _leftmost = spawn.x - (_br.y - spawn.y)
    _rightmost = spawn.x + (_br.y - spawn.y)

    _tl = Pt(min(_tl.x, _leftmost), _tl.y)
    _br = Pt(max(_br.x, _rightmost), _br.y)

field = Field(_tl, _br)
field[spawn] = '+'

for strip in strips:
    field.drawStrip(strip)
if args.ground:
    field.drawStrip([ Pt(_tl.x, _br.y) + Pt(+1, 0), _br + Pt(-1, 0)])

# @TODO: If you follow above simplification you can have only 1 grain and print
#        in blue the backtrack stack
def play():
    global field, spawn

    i = 0
    grains = []
    while True:
        # Add a grain at each step
        grains.append(iter(dropGrainIt(field, spawn)))
        # Process grains
        moving = []
        for grain in grains[:]: # Need to work on a copy cause it's altered
            try:
                settled, cur_grain = next(grain)
                if cur_grain.y == _br.y:
                    return # Overflow
                moving.append(cur_grain)
            except StopIteration as e:
                grains.remove(grain)
                settled, cur_grain = e.value
                if cur_grain == spawn:
                    return # Spawn blocked
        img = field.img()
        for p in moving:
            img.putpixel((p - field.tl).toTuple(), (0, 255, 255))
        #img.save(f'{_PBASE}/imgout/{i}.png')
        yield img
        i += 1
        if i % 1000 == 0:
            print(f'... {i}')
imgs = iter(play())
img0 = next(imgs)

os.makedirs('_output', exist_ok=True)
img0.save(f'_output/14_anim{"_withground" if args.ground else "_noground"}.gif', save_all=True, append_images=imgs, duration=20) # 20 seems to be the fastest?
