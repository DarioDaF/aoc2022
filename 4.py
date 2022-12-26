
from utils import readInput

text = readInput()

def rinc(rbig, rsmall):
    return rsmall[0] >= rbig[0] and rsmall[1] <= rbig[1]
def rincsym(r1, r2):
    return rinc(r1, r2) or rinc(r2, r1)

t = 0
for line in text.strip().split('\n'):
    e1, e2 = [[int(y) for y in x.split('-')] for x in line.split(',')]
    if rincsym(e1, e2):
        t += 1

print(f'Full: {t}')

def roverlap(r1, r2):
    return r1[0] <= r2[1] and r1[1] >= r2[0]
    #return (r1[0] - r2[1]) * (r1[1] - r2[0]) <= 0

t = 0
for line in text.strip().split('\n'):
    e1, e2 = [[int(y) for y in x.split('-')] for x in line.split(',')]
    if roverlap(e1, e2):
        t += 1

print(f'Any: {t}')