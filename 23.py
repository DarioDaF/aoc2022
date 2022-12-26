
from utils import readInput, Pt, count
import argparse, math

ap = argparse.ArgumentParser()
ap.add_argument('--test', action='store_true')
args = ap.parse_args()

if args.test:
    text = '''....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..'''
else:
    text = readInput()

elves = set()

y = 0
for line in text.split('\n'):
    x = 0
    for c in line:
        if c == '#':
            elves.add(Pt(x, y))
        x += 1
    y += 1

def _boundingBox(elves):
    topLeft = Pt(+math.inf, +math.inf)
    bottomRight = Pt(-math.inf, -math.inf)
    for elf in elves:
        topLeft = Pt(min(topLeft.x, elf.x), min(topLeft.y, elf.y))
        bottomRight = Pt(max(bottomRight.x, elf.x), max(bottomRight.y, elf.y))
    return topLeft, bottomRight

def _size(elves):
    a, b = _boundingBox(elves)
    return b - a + Pt(1, 1)

def _print(elves):
    a, b = _boundingBox(elves)
    for y in range(a.y, b.y + 1):
        print(''.join('#' if Pt(x, y) in elves else '.' for x in range(a.x, b.x + 1)))

print('START:')
_print(elves)

minimalConditionList = [
    Pt(-1, -1), Pt(0, -1), Pt(+1, -1),
    Pt(-1,  0),            Pt(+1,  0),
    Pt(-1, +1), Pt(0, +1), Pt(+1, +1),
]

decisionList = [
    (Pt(0, -1), [Pt(-1, -1), Pt(0, -1), Pt(+1, -1)]), # N
    (Pt(0, +1), [Pt(-1, +1), Pt(0, +1), Pt(+1, +1)]), # S
    (Pt(-1, 0), [Pt(-1, -1), Pt(-1, 0), Pt(-1, +1)]), # W
    (Pt(+1, 0), [Pt(+1, -1), Pt(+1, 0), Pt(+1, +1)]), # E
]
startDecisionIdx = 0

def _step():
    global elves, minimalConditionList, decisionList, startDecisionIdx
    proposals = {}
    voidProposals = set()

    # First step
    for elf in elves:
        if all(elf + condition not in elves for condition in minimalConditionList):
            continue # Don't move if noone around
        for movement, conditions in decisionList[startDecisionIdx:] + decisionList[:startDecisionIdx]:
            if all(elf + condition not in elves for condition in conditions): # No elves around
                if elf + movement in proposals:
                    voidProposals.add(elf + movement)
                else:
                    proposals[elf + movement] = elf
                break
    # Second step
    n_moves = 0
    for dest, src in proposals.items():
        if dest in voidProposals:
            continue
        elves.remove(src)
        elves.add(dest)
        n_moves += 1
    # Shuffle priorities
    startDecisionIdx += 1
    startDecisionIdx %= len(decisionList)
    return n_moves

for i in range(10):
    _step()
    print(f'Round {i+1}:')
    _print(elves)

# Check extremes
size = _size(elves)
print(f'Space in 10 round: {size.x * size.y - len(elves)}')

# Part 2
# @TODO: Define an update trigger only for elves near other elves, so the update set is smaller?
#        Probably reduces the time by very little...
print('Continue spreading...')

for i in count(start=10):
    if _step() == 0:
        break

print(f'Stable at: {i+1}')
