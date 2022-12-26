
from utils import readInput

text = readInput()

def sign(x):
    if x == 0:
        return 0
    return 1 if x > 0 else -1

def moveTail(head, oldTail):
    dx = head[0] - oldTail[0]
    dy = head[1] - oldTail[1]
    if abs(dx) <= 1 and abs(dy) <= 1:
        return oldTail # Not moved
    return (oldTail[0] + sign(dx), oldTail[1] + sign(dy))

def getMove(dir):
    return {
        'U': (0, +1),
        'D': (0, -1),
        'R': (+1, 0),
        'L': (-1, 0)
    }[dir]

visited = set()
head = (0, 0)
tail = (0, 0)
for line in text.strip().split('\n'):
    dir, q = line.split(' ')
    q = int(q)
    d = getMove(dir)
    for i in range(q):
        head = (head[0] + d[0], head[1] + d[1])
        tail = moveTail(head, tail)
        visited.add(tail)

print(f'Rope2: {len(visited)}')

# Big rope
visited = set()
head = (0, 0)
tails = [(0, 0) for i in range(9)]
for line in text.strip().split('\n'):
    dir, q = line.split(' ')
    q = int(q)
    d = getMove(dir)
    for i in range(q):
        head = (head[0] + d[0], head[1] + d[1])
        tmpHead = head
        for ti in range(len(tails)):
            tails[ti] = moveTail(tmpHead, tails[ti])
            tmpHead = tails[ti]
        visited.add(tails[-1])

print(f'Rope10: {len(visited)}')