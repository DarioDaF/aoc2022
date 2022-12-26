
from utils import readInput, deque

text = readInput()

# Doing some graphs!

ground = [[*line] for line in text.strip().split('\n')]

h = len(ground)
w = len(ground[0])

s = (-1, -1)
e = (-1, -1)

for x in range(w):
    for y in range(h):
        v = ground[y][x]
        if v == 'S':
            s = (x, y)
            v = 'a'
        if v == 'E':
            e = (x, y)
            v = 'z'
        ground[y][x] = ord(v) - ord('a')

print(f'Start: {s} | End: {e}')

def sides(p):
    global w, h
    if p[0] > 0:
        yield (p[0]-1, p[1])
    if p[1] > 0:
        yield (p[0], p[1]-1)
    if p[0] < w-1:
        yield (p[0]+1, p[1])
    if p[1] < h-1:
        yield (p[0], p[1]+1)

def adj(p):
    global ground
    height = ground[p[1]][p[0]]
    for x, y in sides(p):
        if ground[y][x] <= height+1:
            yield x, y

def run1():
    global w, h, s, e
    dist = [[-1 for _ in range(w)] for _ in range(h)]
    todo = deque([s]) # QUEUE SO VISIT SMALLEST FIRST
    dist[s[1]][s[0]] = 0

    while len(todo) > 0:
        p0 = todo.popleft()
        for p1 in adj(p0):
            if dist[p1[1]][p1[0]] < 0:
                dist[p1[1]][p1[0]] = dist[p0[1]][p0[0]] + 1
                todo.append(p1)
            if p1 == e:
                return dist
    
    return dist # Nothing found...
dist = run1()

print(f'Distance SE: {dist[e[1]][e[0]]}')

def radj(p):
    global ground
    height = ground[p[1]][p[0]]
    for x, y in sides(p):
        if ground[y][x] >= height-1:
            yield x, y

def run2():
    global w, h, e, ground
    dist = [[-1 for _ in range(w)] for _ in range(h)]
    todo = deque([e]) # QUEUE SO VISIT SMALLEST FIRST
    dist[e[1]][e[0]] = 0 # Start from the end

    while len(todo) > 0:
        p0 = todo.popleft()
        for p1 in radj(p0):
            if dist[p1[1]][p1[0]] < 0:
                dist[p1[1]][p1[0]] = dist[p0[1]][p0[0]] + 1
                todo.append(p1)
            if ground[p1[1]][p1[0]] == 0: # Found a bottom tile
                return dist, p1
    
    return dist, (-1, -1) # Nothing found...
dist, best_s = run2()

print(f'Best Start: {best_s}')
print(f'Distance BSE: {dist[best_s[1]][best_s[0]]}')
