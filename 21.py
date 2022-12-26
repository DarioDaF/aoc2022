
from utils import readInput, zip_longest
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('--test', action='store_true')
args = ap.parse_args()

if args.test:
    text = '''root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32'''
else:
    text = readInput()

ms = {}

for line in text.strip().split('\n'):
    mname, action = line.split(':')
    action = action.strip().split(' ')
    if len(action) == 1:
        action = int(action[0])
    assert mname not in ms
    ms[mname] = action

def compute(action):
    global ms
    if isinstance(action, int):
        return action
    return {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b
    }[action[1]](compute(ms[action[0]]), compute(ms[action[2]]))

res = compute(ms['root'])
print(f'Result root = {res}')

# Part 2 equation manipilation

ms['root'][1] = '='
ms['humn'] = 'x'

class MyPoly:
    def __init__(self, coeff = []):
        if isinstance(coeff, MyPoly):
            self.coeff = [*coeff.coeff]
        else:
            self.coeff = [*coeff]
    def __add__(self, other):
        return MyPoly(a + b for a, b in zip_longest(self.coeff, other.coeff, fillvalue=0))
    def __iadd__(self, other):
        if len(other.coeff) > len(self.coeff):
            self.coeff += [0 for _ in range(len(other.coeff) - len(self.coeff))]
        for i in range(len(other.coeff)):
            self.coeff[i] += other.coeff[i]
        return self
    def __sub__(self, other):
        return MyPoly(a - b for a, b in zip_longest(self.coeff, other.coeff, fillvalue=0))
    def __lshift__(self, x):
        return MyPoly([0 for _ in range(x)] + self.coeff)
    def __mul__(self, other):
        if isinstance(other, int):
            return MyPoly(other * a for a in self.coeff)
        res = MyPoly()
        for i, a in enumerate(self.coeff):
            res += (a * other) << i
        return res
    def __rmul__(self, other):
        return self * other
    def __repr__(self):
        return ' '.join(reversed([f'{a}x^{i}' for i, a in enumerate(self.coeff)]))

class MyPolyF:
    def __init__(self, num_coeff = [], den_coeff = [1]):
        self.num_coeff = MyPoly(num_coeff)
        self.den_coeff = MyPoly(den_coeff)
    def __add__(self, other):
        # @TODO: Simplify if equal?
        return MyPolyF(
            self.num_coeff * other.den_coeff + self.den_coeff * other.num_coeff,
            self.den_coeff * other.den_coeff
        )
    def __sub__(self, other):
        # @TODO: Simplify if equal?
        return MyPolyF(
            self.num_coeff * other.den_coeff - self.den_coeff * other.num_coeff,
            self.den_coeff * other.den_coeff
        )
    def __mul__(self, other):
        return MyPolyF(
            self.num_coeff * other.num_coeff,
            self.den_coeff * other.den_coeff
        )
    def __truediv__(self, other):
        return MyPolyF(
            self.num_coeff * other.den_coeff,
            self.den_coeff * other.num_coeff
        )
    def __repr__(self):
        nc = repr(self.num_coeff)
        dc = repr(self.den_coeff)
        sp = '-' * max(len(nc), len(dc))
        return nc + '\n' + sp + '\n' + dc


def computePoly(action):
    global ms
    if isinstance(action, int):
        return MyPolyF([action])
    if isinstance(action, str):
        if action == 'x':
            return MyPolyF([0, 1])
        else:
            raise NotImplemented()
    return {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b
    }[action[1]](computePoly(ms[action[0]]), computePoly(ms[action[2]]))

p1 = computePoly(ms[ms['root'][0]])
p2 = computePoly(ms[ms['root'][2]])
z = p1 - p2

print('Following fraction should be 0')
print(z)

assert len(z.num_coeff.coeff) == 2
assert len(z.den_coeff.coeff) == 1

res = -z.num_coeff.coeff[0] / z.num_coeff.coeff[1]

print(f'Result x = {res}')
