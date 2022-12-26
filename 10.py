
from utils import readInput

text = readInput()

def runProgram():
    t = 1
    x = 1
    yield (t, x)
    for inst in text.strip().split('\n'):
        args = inst.split(' ')
        if args[0] == 'noop':
            t += 1
            yield (t, x)
        if args[0] == 'addx':
            t += 1
            yield (t, x)
            t += 1
            x += int(args[1])
            yield (t, x)

res = 0
for t, x in runProgram():
    if (t - 20) % 40 == 0:
        res += t * x

print(f'Points: {res}')

crt = [[' ' for i in range(40)] for j in range(6)]

for t, x in runProgram():
    pos = ((t-1) % 40, (t-1) // 40 % 6)
    if abs(pos[0] - x) <= 1:
        crt[pos[1]][pos[0]] = '#'

print('\n'.join(''.join(l) for l in crt))
