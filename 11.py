
from utils import readInput, deque, deepcopy, prod
import math

text = readInput()

class Monkey:
    def __init__(self, data: str):
        sdata = data.split('\n')
        self.id = int(sdata[0].split(' ')[-1][:-1])
        self.items = deque(int(i) for i in sdata[1].split(':')[-1].split(','))

        assign = sdata[2].split(':')[-1].strip().split(' = ')[1]
        t1, action, t2 = assign.split(' ')
        if action == '+':
            self._op = lambda old: self._term(t1, old) + self._term(t2, old)
        if action == '*':
            self._op = lambda old: self._term(t1, old) * self._term(t2, old)
        
        self._test = int(sdata[3].split(':')[-1].strip().split(' ')[-1])
        self._actions = {
            True: int(sdata[4].split(':')[-1].strip().split(' ')[-1]),
            False: int(sdata[5].split(':')[-1].strip().split(' ')[-1])
        }
    def _term(self, t, old: int):
        if t == 'old':
            return old
        return int(t)
    def runOp(self, old: int):
        return self._op(old)
    def test(self, x: int):
        return x % self._test == 0
    def target(self, test: bool):
        return self._actions[test]
    def process(self, div3: bool = True, modulocap: int = 0):
        while len(self.items) > 0:
            item = self.items.popleft()
            item = self.runOp(item)
            if div3:
                item //= 3
            if modulocap != 0:
                item %= modulocap
            target = self.target(self.test(item))
            yield item, target
    def __repr__(self):
        return f'Monkey({self.id})'

monkeys = [Monkey(data) for data in text.split('\n\n')]

for i in range(len(monkeys)):
    monkey = monkeys[i]
    assert monkey.id == i
    monkey.inspections = 0

ms1 = deepcopy(monkeys)

for i in range(20):
    for monkey in ms1:
        for item, target in monkey.process(True):
            monkey.inspections += 1
            ms1[target].items.append(item)

x = sorted(ms1, key=lambda m: m.inspections, reverse=True)
print(prod(m.inspections for m in x[:2]))

ms2 = deepcopy(monkeys)

# Analyzing modulocap
modulocap = math.lcm(*(m._test for m in ms2))
print(f'Modulo: {modulocap}')

for i in range(10000):
    for monkey in ms2:
        for item, target in monkey.process(False, modulocap):
            monkey.inspections += 1
            ms2[target].items.append(item)
    if i % 1000 == 0:
        print(f'... {100 * i / 10000}%')

x = sorted(ms2, key=lambda m: m.inspections, reverse=True)
print(prod(m.inspections for m in x[:2]))
