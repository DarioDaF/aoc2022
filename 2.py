
from utils import readInput

text = readInput()

def rps(s):
    if s == 'A' or s == 'X':
        return 1
    if s == 'B' or s == 'Y':
        return 2
    if s == 'C' or s == 'Z':
        return 3
    return 0

def rpsBack(i):
    return ['C', 'A', 'B'][i % 3]

def score(s1, s2):
    s1 = rps(s1)
    s2 = rps(s2)
    st = (s2 - s1) % 3
    return (
        s2 + # my shape
        [3, 6, 0][st] # won?
    )

t = 0
for round in text.split('\n'):
    if round == '':
        continue
    enemy, my = round.split(' ')
    t += score(enemy, my)

print(f'Score1: {t}')

t = 0
for round in text.split('\n'):
    if round == '':
        continue
    enemy, my_st = round.split(' ')
    my = ''
    if my_st == 'Y': # draw
        my = enemy
    elif my_st == 'Z': # win
        my = rpsBack(rps(enemy) + 1)
    elif my_st == 'X': # loose
        my = rpsBack(rps(enemy) - 1)
    t += score(enemy, my)

print(f'Score2: {t}')
