
from utils import readInput, deque, PQueue, deepcopy
import argparse, re, time

ap = argparse.ArgumentParser()
ap.add_argument('--test', action='store_true')
ap.add_argument('--part2', action='store_true')
ap.add_argument('--part3', action='store_true')
args = ap.parse_args()

if args.test:
    text = '''Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II'''
else:
    text = readInput()

START = 'AA'
if args.part3:
    # Just to see how fast it is
    TIME = 22
    USERS = 3
elif args.part2:
    TIME = 26
    USERS = 2
else:
    TIME = 30
    USERS = 1

valves = {}
m = re.compile('^Valve ([A-Za-z0-9]+) has flow rate=([0-9]+); tunnels? leads? to valves? (.+)$')
for line in text.strip().split('\n'):
    valve, flow, others = m.match(line).groups()
    flow = int(flow)
    others = [v.strip() for v in others.split(',')]
    valves[valve] = (flow, others)

# Precompute valve distances
#dist[(v1, v2)] = n
dist = {}
for valve in valves.keys():
    toVisit = deque()
    dist[(valve, valve)] = 0
    toVisit.appendleft(valve)
    while len(toVisit) > 0:
        x = toVisit.pop()
        for other in valves[x][1]:
            if (valve, other) not in dist:
                dist[(valve, other)] = dist[(valve, x)] + 1
                toVisit.appendleft(other)

good_valves = set(valve for valve, (flow, _) in valves.items() if flow > 0)

def getStates(paths, ts):
    return [(paths[i][-1], ts[i]) for i in range(len(ts))]

def getVisited(paths):
    return set(p for path in paths for p in path[1:])

def totPoints(path): # Not so important?
    global TIME, valves
    t = 0
    prev = path[0]
    tot = 0
    for p in path[1:]:
        t += dist[(prev, p)] + 1
        if t >= TIME:
            return -1
        tot += valves[p][0] * (TIME - t)
        prev = p
    return tot

def advance(state, v):
    global dist, valves, TIME
    sv, st = state
    st += dist[(sv, v)] + 1
    if st >= TIME:
        return -1, st
    return valves[v][0] * (TIME - st), st

def getChoices(states, visited):
    global good_valves, dist, valves, TIME
    
    # Break simmetries
    for u in range(len(states)):
        if states[u][1] == 0:
            # Must do this first
            pos, t = states[u]
            if u-1 >= 0:
                base = states[u-1][0]
            else:
                base = ''
            for valve in good_valves:
                if valve <= base:
                    continue
                newt = t + dist[(pos, valve)] + 1
                if newt < TIME:
                    yield u, valve
            return
    
    for u in range(len(states)):
        pos, t = states[u]
        for valve in good_valves - visited:
            newt = t + dist[(pos, valve)] + 1
            if newt < TIME:
                yield u, valve
# Remember: paths[i][1] < paths[j][1] for each i < j IS A CONSTRAINT to break simmetry

def heuristic(state, v):
    # Dumb minimal placeholder heuristic
    return advance(state, v)[0]

def upperBound(states, visited, choice = None):
    newstates = states
    newvisited = visited
    points = {}
    if choice != None:
        u, v = choice
        pos, t = states[u]
        pt, newt = advance((pos, t), v)
        points[choice] = pt
        newstates = states[:]
        newstates[u] = v, newt
        newvisited = visited | set([pos])
    for choice in getChoices(newstates, newvisited):
        u, v = choice
        ptc, _ = advance(newstates[u], v)
        if choice not in points or points[choice] < ptc:
            points[choice] = ptc
    return sum(points.values())

def rateFullState(fullState):
    paths, ts, pt = fullState
    mean_t = sum(ts) / len(ts)
    var_t = sum((t - mean_t) ** 2 for t in ts)
    return var_t

t0 = time.monotonic()

_paths = [[START] for _ in range(USERS)]
_ts = [0 for _ in range(USERS)]
_pt = 0

optimum = 0
toVisit = PQueue(key=rateFullState)
toVisit.put((_paths, _ts, _pt))

while not toVisit.empty():
    (paths, ts, pt), _ = toVisit.get()

    states = getStates(paths, ts)
    visited = getVisited(paths)

    ub = upperBound(states, visited)
    if pt + ub <= optimum:
        continue # Not optimal, cut branch

    choices = sorted([*getChoices(states, visited)], key=lambda c: heuristic(states[c[0]], c[1]), reverse=True)

    for u, v in choices:
        addpt, newt = advance(states[u], v)

        ub = upperBound(states, visited, (u, v))
        branchPtRange = (pt + addpt, pt + ub)
        if branchPtRange[1] <= optimum:
            continue # Not optimal, cut branch
        if branchPtRange[0] > optimum:
            optimum = branchPtRange[0] # New optimum
            t1 = time.monotonic()
            print(f'Value {optimum} found in {t1-t0} s: {paths} choosing {(u, v)}')

        newpaths = deepcopy(paths)
        newts = deepcopy(ts)
        newpaths[u].append(v)
        newts[u] = newt
        toVisit.put((newpaths, newts, branchPtRange[0]))

t1 = time.monotonic()

print(f'Completed in {t1-t0} s')
