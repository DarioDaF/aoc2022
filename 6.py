
from utils import readInput

text = readInput()

i = 0
uniq = []
for c in text:
    i += 1
    uniq.append(c)
    uniq = uniq[-4:]
    if len(uniq) == 4 and len(set(uniq)) == 4:
        break

print(f'4len: {i}')

i = 0
uniq = []
for c in text:
    i += 1
    uniq.append(c)
    uniq = uniq[-14:]
    if len(uniq) == 14 and len(set(uniq)) == 14:
        break

print(f'14len: {i}')
