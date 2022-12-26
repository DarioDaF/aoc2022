
from utils import readInput, dataclass, Pt, deque
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('--test', action='store_true')
args = ap.parse_args()

if args.test:
    text = '''        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5'''
    CUBE_SIZE = 4
else:
    text = readInput()
    CUBE_SIZE = 50

board = []

lines = text.rstrip().split('\n')
assert lines[-2] == ''
board = lines[:-2]
commands = lines[-1]

def command_iter(commands):
    n = 0
    for c in commands:
        if c >= '0' and c <= '9':
            n *= 10
            n += ord(c) - ord('0')
        if c in ['L', 'R']:
            if n > 0:
                yield n
                n = 0
            yield c
    if n > 0:
        yield n

def getPt(board, pt: Pt):
    if pt.x < 0 or pt.y < 0 or pt.y >= len(board) or pt.x >= len(board[pt.y]):
        return ' '
    return board[pt.y][pt.x]

direction = Pt(1, 0)
pos = Pt(board[0].index('.'), 0)
for cmd in command_iter(commands):
    #print(f'Command {cmd}: {pos} -> ', end='')
    if isinstance(cmd, int):
        for _ in range(cmd):
            newpos = pos + direction
            target = getPt(board, newpos)
            if target == ' ':
                while getPt(board, newpos - direction) != ' ':
                    newpos -= direction # Wrap around
                # Update target
                target = getPt(board, newpos)
            if target == '.':
                pos = newpos # No obstacle, do move
            else:
                break # Obstacle, no further moves required
    elif cmd == 'R':
        direction = Pt(-direction.y, direction.x)
    elif cmd == 'L':
        direction = Pt(direction.y, -direction.x)
    else:
        raise NotImplemented()
    #print(f'{pos}')

pos_int = 1000 * (pos.y+1) + 4 * (pos.x+1) + {
    (+1, 0): 0,
    (0, +1): 1,
    (-1, 0): 2,
    (0, -1): 3
}[direction.toTuple()]
print(f'On NON CUBE map: {pos_int}')

# Part 2

def direction2pt(d: str):
    return {
        '>': Pt(+1, 0),
        'v': Pt(0, +1),
        '<': Pt(-1, 0),
        '^': Pt(0, -1)
    }[d]

def get90s(d1, d2):
    '''Number of 90 turns to go from d1 to d2'''
    cw = '>v<^'
    return (cw.index(d2) - cw.index(d1)) % len(cw)
def apply90s(d, n):
    cw = '>v<^'
    return cw[(cw.index(d) + n) % len(cw)]

@dataclass
class Strip:
    origin: Pt
    direction: str
    length: int = 0 # >= 0, 0 means it's a rect and goes -inf, +inf
    def __contains__(self, other: Pt):
        if self.length > 0:
            x = self.proj(other)
            if x < 0 or x >= self.length:
                return False
        if self.direction in ['>', '<']:
            return other.y == self.origin.y
        if self.direction in ['v', '^']:
            return other.x == self.origin.x
    def proj(self, other: Pt):
        if self.direction == '>':
            return other.x - self.origin.x
        elif self.direction == '<':
            return self.origin.x - other.x
        if self.direction == 'v':
            return other.y - self.origin.y
        elif self.direction == '^':
            return self.origin.y - other.y
    def map(self, n: int):
        return self.origin + direction2pt(self.direction) * n

@dataclass
class Glue:
    s1: Strip
    s2: Strip
    def move(self, pt: Pt):
        if pt not in self.s1:
            raise ValueError('Point to be teleported is not part of the start strip')
        return self.s2.map(self.s1.proj(pt))
    def rotation(self):
        return get90s(self.s1.direction, self.s2.direction)

class CubePt:
    __glueMap: dict[int, dict[int, list[tuple[Glue, int]]]] = {} # Class variable
    def __initGlueMap(self):
        # Cube space is stored as 2 maps as a T
        #    0
        # (1)0111
        #    0
        if self.size not in self.__glueMap:
            print(f'[CubePt] Generating GlueMap for size {self.size}')
            self.__glueMap[self.size] = {
                0: [
                    (Glue(Strip(Pt(0, -1), '>'), Strip(Pt(2*self.size - 1, 0), '<')), 1),
                    (Glue(Strip(Pt(0, 3*self.size), '>'), Strip(Pt(2*self.size - 1, self.size - 1), '<')), 1),

                    (Glue(Strip(Pt(-1, 0), 'v', self.size), Strip(Pt(2*self.size, 0), '>')), 1),
                    (Glue(Strip(Pt(self.size, 0), 'v', self.size), Strip(Pt(self.size - 1, 0), '<')), 1),

                    (Glue(Strip(Pt(-1, self.size), 'v', self.size), Strip(Pt(3*self.size - 1, 0), 'v')), 1),
                    (Glue(Strip(Pt(self.size, self.size), 'v', self.size), Strip(Pt(0, 0), 'v')), 1),

                    (Glue(Strip(Pt(-1, 2*self.size), 'v', self.size), Strip(Pt(3*self.size - 1, self.size - 1), '<')), 1),
                    (Glue(Strip(Pt(self.size, 2*self.size), 'v', self.size), Strip(Pt(0, self.size - 1), '>')), 1),
                ],
                1: [
                    # Top lip
                    (Glue(Strip(Pt(0, -1), '>', self.size), Strip(Pt(self.size - 1, self.size - 1), '^')), 0),
                    (Glue(Strip(Pt(self.size, -1), '>', self.size), Strip(Pt(self.size - 1, 0), '<')), 0),
                    (Glue(Strip(Pt(2*self.size, -1), '>', self.size), Strip(Pt(0, 0), 'v')), 0),

                    # Bottom lip
                    (Glue(Strip(Pt(0, self.size), '>', self.size), Strip(Pt(self.size - 1, 2*self.size), 'v')), 0),
                    (Glue(Strip(Pt(self.size, self.size), '>', self.size), Strip(Pt(self.size - 1, 3*self.size - 1), '<')), 0),
                    (Glue(Strip(Pt(2*self.size, self.size), '>', self.size), Strip(Pt(0, 3*self.size - 1), '^')), 0),

                    # Sides
                    (Glue(Strip(Pt(-1, 0), 'v'), Strip(Pt(self.size - 1, self.size), 'v')), 0),
                    (Glue(Strip(Pt(3*self.size, 0), 'v'), Strip(Pt(0, self.size), 'v')), 0),
                ]
            }
    def __init__(self, size: int|tuple[int, int, int, int]):
        if isinstance(size, tuple):
            self.size, self._map, px, py = size
            self._pos = Pt(px, py)
        else:
            self.size = size
            self._pos = Pt(0, 0)
            self._map = 0
        self.__initGlueMap()
    def toTuple(self):
        return (self.size, self._map, *self._pos.toTuple())
    def move(self, direction: str):
        newdirection = direction
        self._pos += direction2pt(direction)
        for glue, dest in self.__glueMap[self.size][self._map]:
            if self._pos in glue.s1:
                self._pos = glue.move(self._pos)
                self._map = dest
                newdirection = apply90s(newdirection, glue.rotation())
                break
        return newdirection

# Convert board to cube
cube_map = {}
def cube2flat(p: CubePt):
    global cube_map
    return Pt(*cube_map[p.toTuple()][0])
def cube2rot(p: CubePt):
    global cube_map
    return cube_map[p.toTuple()][1]

to_visit = deque([(CubePt(CUBE_SIZE), Pt(board[0].index('.'), 0), 0)])
while len(to_visit) > 0:
    cpos, pos, rot = to_visit.pop()
    if cpos.toTuple() in cube_map:
        continue
    cube_map[cpos.toTuple()] = (pos.toTuple(), rot)

    for d in '>v<^':
        npos = pos + direction2pt(d)
        if getPt(board, npos) != ' ':
            ncpos = CubePt(cpos.toTuple())
            newrot = get90s(d, ncpos.move(apply90s(d, rot)))
            if ncpos.toTuple() not in cube_map:
                to_visit.appendleft((ncpos, npos, newrot))

# Try to print cubemap
#vs = set(p for p, _ in cube_map.values())
#for y in range(len(board)):
#    print(''.join('@' if (x, y) in vs else ' ' for x in range(len(board[y]))))
assert len(cube_map) == CUBE_SIZE * CUBE_SIZE * 6
assert len(set(p for p, _ in cube_map.values())) == len(cube_map)

direction = '>'
cpos = CubePt(CUBE_SIZE) # Origin maps to the question
for cmd in command_iter(commands):
    if isinstance(cmd, int):
        for _ in range(cmd):
            pos = cube2flat(cpos)
            #board[pos.y] = board[pos.y][:pos.x] + direction + board[pos.y][pos.x+1:]
            newcpos = CubePt(cpos.toTuple())
            newdirection = newcpos.move(direction)
            target = getPt(board, cube2flat(newcpos))
            #if target in ['.', '>', 'v', '<', '^']:
            if target == '.':
                cpos = newcpos # No obstacle, do move
                direction = newdirection
            else:
                break # Obstacle, no further moves required
    elif cmd == 'R':
        direction = apply90s(direction, 1)
    elif cmd == 'L':
        direction = apply90s(direction, -1)
    else:
        raise NotImplemented()

# Remap direction into base map?
flat_direction = apply90s(direction, -cube2rot(cpos))

pos = cube2flat(cpos)
pos_int = 1000 * (pos.y+1) + 4 * (pos.x+1) + '>v<^'.index(flat_direction)
print(f'On CUBE map: {pos_int} | {pos} {flat_direction}')

# Print normalized board
#print('Map0:')
#for y in range(3*CUBE_SIZE):
#    print(''.join(getPt(board, cube2flat(CubePt((CUBE_SIZE, 0, x, y)))) for x in range(CUBE_SIZE)))
#print('Map1:')
#for y in range(CUBE_SIZE):
#    print(''.join(getPt(board, cube2flat(CubePt((CUBE_SIZE, 1, x, y)))) for x in range(3*CUBE_SIZE)))
