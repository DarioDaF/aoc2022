
from utils import readInput, Pt, PQueue
import argparse, math, time

ap = argparse.ArgumentParser()
ap.add_argument('--test', action='store_true')
ap.add_argument('--nocheckdupe', action='store_true')
args = ap.parse_args()

if args.test:
    text = '''#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#'''
else:
    text = readInput()

# By design you can never blizard an entrance/exit so it's a square

def genBlizs():
    global size, bliz_xs, bliz_ys
    board = []
    for line in text.rstrip().split('\n')[1:-1]:
        board.append(line[1:-1])

    size = Pt(len(board[0]), len(board))

    bliz_ys = {}
    for y in range(size.y):
        bliz_r = [ board[y][x] == '>' for x in range(size.x) ]
        bliz_l = [ board[y][x] == '<' for x in range(size.x) ]
        bliz_ys[y] = bliz_r, bliz_l

    bliz_xs = {}
    for x in range(size.x):
        bliz_d = [ board[y][x] == 'v' for y in range(size.y) ]
        bliz_u = [ board[y][x] == '^' for y in range(size.y) ]
        bliz_xs[x] = bliz_d, bliz_u
genBlizs()

def getBlizPoint(p: Pt, t: int):
    global bliz_xs, bliz_ys, size
    # Out of bound exceptions
    if p == Pt(0, -1):
        return False # Start has never bliz
    if p == Pt(size.x - 1, size.y):
        return False # End has never bliz
    # Out of bound
    if p.x < 0 or p.x >= size.x:
        return True
    if p.y < 0 or p.y >= size.y:
        return True
    # In bound
    vd, vu = bliz_xs[p.x]
    hr, hl = bliz_ys[p.y]
    return (
        vd[(p.y - t) % size.y] or vu[(p.y + t) % size.y] or
        hr[(p.x - t) % size.x] or hl[(p.x + t) % size.x]
    )

def getSurrounding(p: Pt, t: int):
    for movement in [
        Pt(+1, 0), Pt(0, +1), # Heuristic, go down right!
        Pt(0, 0),
        Pt(-1, 0), Pt(0, -1),
    ]:
        dest = p + movement
        if not getBlizPoint(dest, t):
            yield dest

def minPath(st: Pt, end: Pt, t0: int = 0):
    global args
    toVisit = PQueue()
    toVisit.put(st, key=t0)

    # Use T modulo for this
    t_mod = math.lcm(size.x, size.y)
    alreadyVisited = set()

    parent = {}
    finish_time = -1

    while finish_time < 0 and not toVisit.empty():
        pos, t = toVisit.get()
        r = (t % t_mod, *pos.toTuple())
        if not args.nocheckdupe:
            if r in alreadyVisited:
                continue
        alreadyVisited.add(r)
        for option in getSurrounding(pos, t+1):
            if not args.nocheckdupe:
                r = ((t+1) % t_mod, *option.toTuple())
                if r in alreadyVisited:
                    continue
            parent[(t+1, *option.toTuple())] = (t, *pos.toTuple())
            toVisit.put(option, key=t+1)
            if option == end:
                finish_time = t+1
                break
    
    if finish_time < 0:
        return finish_time, []
    
    path = []
    endPoint = (finish_time, *end.toTuple())
    while endPoint in parent:
        path.append(endPoint)
        endPoint = parent[endPoint]
    path.append(endPoint)

    return finish_time, path[::-1]

t0 = time.monotonic()
st = Pt(0, -1)
end = Pt(size.x-1, size.y)
ft, p1 = minPath(st, end)
print(f'Time to go forward: {ft}')
ft, p2 = minPath(end, st, ft)
ft, p3 = minPath(st, end, ft)
print(f'With back and forw again trip: {ft}')
t1 = time.monotonic()

print(f'Total compute time: {t1-t0}')

total_path = p1 + p2[1:] + p3[1:]
print(total_path)
