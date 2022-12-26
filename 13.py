
from utils import readInput

text = readInput()

def cmp(l, r):
    if isinstance(l, int) and isinstance(r, int):
        if l < r:
            return -1
        if l > r:
            return 1
        return 0
    if isinstance(l, int):
        l = [l]
    if isinstance(r, int):
        r = [r]
    minl = min(len(l), len(r))
    for i in range(minl):
        c = cmp(l[i], r[i])
        if c > 0:
            return 1
        if c < 0:
            return -1
    if len(l) == len(r):
        return 0 # Equal
    if len(l) < len(r):
        return -1
    return 1

class MyPacket:
    def __init__(self, val):
        self.val = val
    def __lt__(self, other):
        return cmp(self.val, other.val) < 0
    def __gt__(self, other):
        return cmp(self.val, other.val) > 0
    def __eq__(self, other):
        return cmp(self.val, other.val) == 0
    def __repr__(self):
        return repr(self.val)

packets = []

i = 1
tot = 0
for question in text.strip().split('\n\n'):
    l, r = question.split('\n')
    l = eval(l)
    r = eval(r)
    packets.append(MyPacket(l))
    packets.append(MyPacket(r))
    c = cmp(l, r)
    print(f'... Question {i} result: {c}')
    if c <= 0:
        tot += i
    i += 1

print(f'Number of sorted packets {tot}')

# Part 2
_DIV1 = MyPacket([[2]])
_DIV2 = MyPacket([[6]])
packets.append(_DIV1)
packets.append(_DIV2)

packets.sort()

_I1 = packets.index(_DIV1) + 1
_I2 = packets.index(_DIV2) + 1

print(f'Decoded key: {_I1 * _I2}')
