
from utils import readInput

text = readInput()

trees = []

for line in text.strip().split('\n'):
    trees.append([int(c) for c in line])

w = len(trees[0])
h = len(trees)

visibility = [[False for i in range(w)] for j in range(h)]

def markVis(l, getf, markf):
    tallest = -1
    for i in range(l):
        v = getf(i)
        if v > tallest:
            tallest = v
            markf(i)

for j in range(h):    
    def _m(i): visibility[j][i] = True
    markVis(w, lambda i: trees[j][i], _m)

    def _m(i): visibility[j][-i-1] = True
    markVis(w, lambda i: trees[j][-i-1], _m)

for j in range(w):
    def _m(i): visibility[i][j] = True
    markVis(h, lambda i: trees[i][j], _m)

    def _m(i): visibility[-i-1][j] = True
    markVis(h, lambda i: trees[-i-1][j], _m)

print(sum(sum(l) for l in visibility))

def countLower(v, lst):
    i = 0
    for x in lst:
        i += 1
        if x >= v:
            break
    return i

maxscore = 0
for i in range(h):
    for j in range(w):
        score = 1
        # For each tree
        v = trees[i][j]
        score *= countLower(v, trees[i][j+1:])
        score *= countLower(v, reversed(trees[i][:j]))
        score *= countLower(v, [x[j] for x in trees[i+1:]])
        score *= countLower(v, [x[j] for x in reversed(trees[:i])])
        if score > maxscore:
            maxscore = score

print(f'Max scenic score: {maxscore}')
