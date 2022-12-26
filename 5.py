
from utils import readInput, deepcopy
import re

text = readInput()

drawing, moves = text.split('\n\n', 1)

drawing = drawing.split('\n')[:-1]
stacks = [[] for _ in range((len(drawing[0]) + 1) // 4)]
for line in reversed(drawing):
    for i in range(len(stacks)):
        content = line[i * 4 + 1]
        if content != ' ':
            stacks[i].append(content)

stacks2 = deepcopy(stacks)
rem = re.compile('move ([0-9]+) from ([0-9]+) to ([0-9]+)')

for line in moves.strip().split('\n'):
    q, src, dest = (int(x) for x in rem.match(line).groups())
    if src == dest:
        print('?')
        continue
    stacks[dest-1].extend(reversed(stacks[src-1][-q:]))
    stacks[src-1] = stacks[src-1][:-q]

print('9000: ' + ''.join(stack[-1] for stack in stacks))

for line in moves.strip().split('\n'):
    q, src, dest = (int(x) for x in rem.match(line).groups())
    if src == dest:
        print('?')
        continue
    stacks2[dest-1].extend(stacks2[src-1][-q:])
    stacks2[src-1] = stacks2[src-1][:-q]

print('9001: ' + ''.join(stack[-1] for stack in stacks2))
