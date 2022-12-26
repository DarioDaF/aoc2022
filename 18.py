
from utils import readInput, product
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('--test', action='store_true')
args = ap.parse_args()

if args.test:
    text = '''2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
'''
else:
    text = readInput()

dotList = []

maxDot = (0, 0, 0)

for line in text.strip().split('\n'):
    dot = tuple(map(int, line.split(',')))
    dotList.append(dot)
    maxDot = tuple(max(a, b) for a, b in zip(maxDot, dot))

maxDot = tuple(c + 1 for c in maxDot)
print(f'Grid size: {maxDot}')
grid = [[[False for _ in range(maxDot[2])] for _ in range(maxDot[1])] for _ in range(maxDot[0])]

for x, y, z in dotList:
    grid[x][y][z] = True

def getGrid(grid, dot, outside = False):
    sub = grid
    for c in dot:
        if c < 0 or c >= len(sub):
            return outside # Out of range
        sub = sub[c]
    return sub

def adj(dot):
    x, y, z = dot
    yield from [
        (x-1, y, z), (x+1, y, z),
        (x, y-1, z), (x, y+1, z),
        (x, y, z-1), (x, y, z+1),
    ]

surf = 0
for dot in dotList:
    # Check surface
    for adjDot in adj(dot):
        if not getGrid(grid, adjDot):
            surf += 1

print(f'Total Surface: {surf}')

# Filling outside
outsideGrid = [[[False for _ in range(maxDot[2])] for _ in range(maxDot[1])] for _ in range(maxDot[0])]
toBeFilled = set()
for x, y in product(range(maxDot[0]), range(maxDot[1])):
    toBeFilled.add((x, y, 0))
    toBeFilled.add((x, y, maxDot[2]-1))
for x, z in product(range(maxDot[0]), range(maxDot[2])):
    toBeFilled.add((x, 0, z))
    toBeFilled.add((x, maxDot[1]-1, z))
for y, z in product(range(maxDot[1]), range(maxDot[2])):
    toBeFilled.add((0, y, z))
    toBeFilled.add((maxDot[0]-1, y, z))

while len(toBeFilled) > 0:
    dot = toBeFilled.pop()
    if getGrid(outsideGrid, dot, True):
        continue
    if getGrid(grid, dot, True):
        continue
    outsideGrid[dot[0]][dot[1]][dot[2]] = True
    for adjDot in adj(dot):
        if getGrid(outsideGrid, adjDot, True):
            continue
        if getGrid(grid, adjDot, True):
            continue
        toBeFilled.add(adjDot)

surf = 0
for dot in dotList:
    # Check surface
    for adjDot in adj(dot):
        if getGrid(outsideGrid, adjDot, True):
            surf += 1

print(f'Outside Surface: {surf}')
