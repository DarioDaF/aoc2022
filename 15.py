
from utils import readInput, Pt
import math, re, argparse

ap = argparse.ArgumentParser()
ap.add_argument('--test', action='store_true')
ap.add_argument('--slow2', action='store_true')
args = ap.parse_args()

if args.test:
    text = '''Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3'''
    TARGET_Y = 10
else:
    text = readInput()
    TARGET_Y = 2000000

def squash(segs: list[tuple[int, int]]):
    res = 0
    start = -math.inf
    for seg in sorted(segs, key=lambda seg: seg[0]):
        real_start = max(start, seg[0])
        s = seg[1] - real_start + 1
        if s > 0: # If not completely eaten
            res += s
            start = seg[1] + 1
    return res

def findHole(segs: list[tuple[int, int]], searchSpace: tuple[int, int]):
    start = searchSpace[0]
    for seg in sorted(segs, key=lambda seg: seg[0]):
        if seg[0] > start:
            return start
        real_start = max(start, seg[0])
        s = seg[1] - real_start + 1
        if s > 0: # If not completely eaten
            start = seg[1] + 1
            if start > searchSpace[1]:
                return None
    #if start <= searchSpace[1]: # Always true if searchSpace is not empty
    return start

pairs: list[tuple[Pt, Pt]] = []
m = re.compile('^Sensor at x=(-?[0-9]+), y=(-?[0-9]+): closest beacon is at x=(-?[0-9]+), y=(-?[0-9]+)$')
for line in text.strip().split('\n'):
    gs = [int(c) for c in m.match(line).groups()]
    s = Pt(*gs[0:2]); b = Pt(*gs[2:4])
    pairs.append((s, b))

# Part 1

segs = []
alligned_beacons = set()

for s, b in pairs:
    # Keep aligned beacons list
    if b.y == TARGET_Y:
        alligned_beacons.add(b)
    # Generate segment where beacon CANNOT be
    manhattan = (s - b).dist(1)
    dy = abs(TARGET_Y - s.y)
    occ = manhattan - dy
    if occ >= 0:
        seg = (s.x - occ, s.x + occ)
        segs.append(seg)

tot = squash(segs)
print(f'Squashed distance at y={TARGET_Y}: {tot-len(alligned_beacons)}')

# Part 2

BOX_BORDERS = (0, 4000000)

if args.slow2:
    # Do like part 1 for each y
    for y in range(*BOX_BORDERS):
        segs = []
        for s, b in pairs:
            # Generate segment where beacon CANNOT be
            manhattan = (s - b).dist(1)
            dy = abs(y - s.y)
            occ = manhattan - dy
            if occ >= 0:
                seg = (s.x - occ, s.x + occ)
                segs.append(seg)
        hole = findHole(segs, (BOX_BORDERS[0], BOX_BORDERS[1]-1))
        if hole != None:
            hole_p = Pt(hole, y)
            print(f'Found: {hole_p} | Freq: {hole_p.x * (BOX_BORDERS[1] - BOX_BORDERS[0]) + hole_p.y}')
            break
        if y % 100000 == 0:
            print(f'... {y}')
else:
    # Diamonds intersections

    def roundInDir(x: float, d: int):
        if d > 0:
            return math.ceil(x)
        if d < 0:
            return math.floor(x)
        return x
    def roundInDirPt(p: Pt, d: Pt):
        return Pt(roundInDir(p.x, d.x), roundInDir(p.y, d.y))

    def diagIntersect(p0, d0, p1, d1):
        m0 = -d0.y / d0.x
        m1 = -d1.y / d1.x
        x = ((p1.y - p0.y) - (p1.x * m1 - p0.x * m0)) / (m0 - m1)
        y = (x - p0.x) * m0 + p0.y
        res = Pt(x, y)
        return res

    def possibleIntersections():
        yield from [
            (Pt(+1, +1), Pt(+1, -1)),
            (Pt(+1, +1), Pt(-1, +1)),
            (Pt(-1, -1), Pt(+1, -1)),
            (Pt(-1, -1), Pt(-1, +1))
        ]

    def getMultiIntPt(p: Pt):
        if math.isclose(abs(math.fmod(p.x, 1.0)), 0.5, abs_tol=0.1):
            yield from getMultiIntPt(Pt(math.floor(p.x), p.y))
            yield from getMultiIntPt(Pt(math.ceil(p.x), p.y))
            return
        if math.isclose(abs(math.fmod(p.y, 1.0)), 0.5, abs_tol=0.1):
            yield from getMultiIntPt(Pt(p.x, math.floor(p.y)))
            yield from getMultiIntPt(Pt(p.x, math.ceil(p.y)))
            return
        yield p

    def checkPt(p: Pt):
        global pairs
        for s, b in pairs:
            if (p - s).dist(1) <= (s - b).dist(1):
                return False
        return True

    n_ints = 0
    for s1, b1 in pairs:
        d1 = (s1 - b1).dist(1)
        for s2, b2 in pairs:
            d2 = (s2 - b2).dist(1)
            # Intersections: (they are squares)
            v = s1 - s2
            vd = v.dist(1)
            if vd <= 0:
                continue # The same
            if vd > d1 + d2:
                continue # Too far
            for dir1, dir2 in possibleIntersections():
                i = diagIntersect(s1 + Pt(dir1.x * d1, 0), dir1, s2 + Pt(dir2.x * d2, 0), dir2)
                dircomb = (dir1 + dir2) / 2
                i += dircomb
                i = roundInDirPt(i, dircomb)
                for target in getMultiIntPt(i):
                    # Check target
                    if target.x not in range(*BOX_BORDERS) or target.y not in range(*BOX_BORDERS):
                        continue
                    n_ints += 1
                    if checkPt(target):
                        print(f'Found: {target} | Freq: {target.x * (BOX_BORDERS[1] - BOX_BORDERS[0]) + target.y}')
                    if n_ints % 100 == 0:
                        print(f'... {n_ints}')
