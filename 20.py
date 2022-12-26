
from utils import readInput
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('--test', action='store_true')
args = ap.parse_args()

if args.test:
    text = '''1
2
-3
3
-2
0
4'''
else:
    text = readInput()

data = [int(x) for x in text.strip().split('\n')]

dec_key = 811589153
dec_rounds = 10

'''
Fucked up analysis
Moving holes:
0, 1, 2, (3,) 4, 5
 o  o  o       o
0, 1, 2, 3, 4, (5)
 o  o  o  o  o?
(0,) 1, 2, 3, 4, 5
      o  o  o  o
take an object [i], it stands in hole i (corner case the border element stand in "fake" holes???)

Examples

When not overflowing it's fine
A, B, C, (D) -1
A, B, (D), C

(A), B, C, D +1
B, (A), C, D

A, B, (C), D +1
A, B, D, (C)

A, (B), C, D -1 # NOPE Seems like it's wonky this goes at the end of the list...
(B), A, C, D

When overflowing it CANNOT be in the hole of the opposite side!
A, B, C, (D) +1
A, (D), B, C

(A), B, C, D -1
B, C, (A), D

'''

def do_mix(data, start_placements = None, do_log = False):
    if start_placements == None:
        placements = [*range(len(data))]
    else:
        placements = start_placements
    for i in range(len(data)):
        start = placements.index(i)
        displace = data[i] # wrt the list with one less element!
        if displace != 0: # Corner case for modulo
            newPos = (start + displace - 1) % (len(data)-1) + 1
            if do_log:
                print(f'Moving {data[i]} from pos {start} to pos {newPos} in the stripped list')
            placements = placements[:start] + placements[start+1:]
            placements.insert(newPos, i)
    return placements

def apply_mix(data, placements):
    res = [0 for _ in range(len(data))]
    for i in range(len(data)):
        res[i] = data[placements[i]]
    return res

# Part 1

placements = do_mix(data)
old0pos = data.index(0)
new0pos = placements.index(old0pos)
vs = [
    data[placements[(new0pos + offset) % len(data)]] for offset in [1000, 2000, 3000]
]
print(f'Simple: {sum(vs)}')

# Part 2

dec_data = [i * dec_key for i in data]

compound_placements = [*range(len(data))] # Identity
for _ in range(dec_rounds):
    compound_placements = do_mix(dec_data, compound_placements)

old0pos = dec_data.index(0)
new0pos = compound_placements.index(old0pos)
vs = [
    dec_data[compound_placements[(new0pos + offset) % len(data)]] for offset in [1000, 2000, 3000]
]
print(f'Complex: {sum(vs)}')
