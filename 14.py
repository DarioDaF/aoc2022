
from utils import readInput, deepcopy, Pt

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

field = Field(_tl, _br)

field[spawn] = '+'

# Paint walls
for strip in strips:
    field.drawStrip(strip)

# Dropping sand

# @TODO: Could be WAY more efficient cause each grain falls in the same line of the current
#        one and so you can backtrack to check where it goes instead of falling from the top
def dropGrain(field, spawn):
    cur_grain = deepcopy(spawn)
    settled = False
    while not settled:
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

tot_grains = 0
while dropGrain(field, spawn)[0]:
    tot_grains += 1

print(field)

print(f'Dropped {tot_grains} grains')

# Creating new map with floor

# Map sizes are on a pyramid centered at the source so:
_br += Pt(0, 2)
_leftmost = spawn.x - (_br.y - spawn.y)
_rightmost = spawn.x + (_br.y - spawn.y)

_tl = Pt(min(_tl.x, _leftmost), _tl.y)
_br = Pt(max(_br.x, _rightmost), _br.y)

field = Field(_tl, _br)

for strip in strips:
    field.drawStrip(strip)
field.drawStrip([ Pt(_tl.x, _br.y), _br ])

tot_grains = 0
while dropGrain(field, spawn)[1] != spawn:
    tot_grains += 1
tot_grains += 1 # COUNT THE ONE ON THE SPAWN!

print(field)
print(f'Dropped {tot_grains} grains')

# Probably reasonable to have all the flat lines count by carving triangles on their bottom
