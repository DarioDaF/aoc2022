
from utils import readInput
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('--test', action='store_true')
args = ap.parse_args()

if args.test:
    text = '''1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122'''
else:
    text = readInput()

def snafu2int(snafu):
    digits = '012=-'
    res = 0
    for c in snafu:
        res *= 5
        d = digits.index(c)
        if d > 2:
            d = d - 5
        res += d
    return res

def int2snafu(i):
    digits = '012=-'
    res = ''
    while i > 0:
        d = i % 5
        res = digits[d] + res
        if d > 2:
            i += 5 - d
        i //= 5
    return res

tot = 0
for line in text.strip().split('\n'):
    assert line == int2snafu(snafu2int(line)) # Just for debug
    tot += snafu2int(line)

print(f'Sum: {int2snafu(tot)}')
