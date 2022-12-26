
from utils import readInput

text = readInput()

def prio(s):
    if s >= 'a' and s <= 'z':
        return ord(s) - ord('a') + 1
    if s >= 'A' and s <= 'Z':
        return ord(s) - ord('A') + 27


t = 0
for line in text.strip().split('\n'):
    clen = len(line) // 2
    x = set(line[clen:]).intersection(set(line[:clen]))
    assert len(x) == 1
    t += prio(x.pop())

print(f'Single pack: {t}')


from itertools import zip_longest

def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks.

    >>> grouper('ABCDEFG', 3, 'x')
    ['ABC', 'DEF', 'Gxx']

    https://stackoverflow.com/questions/4998427/how-to-group-elements-in-python-by-n-elements
    """
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

t = 0
for e1, e2, e3 in grouper(text.strip().split('\n'), 3):
    x = set(e1).intersection(set(e2)).intersection(set(e3))
    assert len(x) == 1
    t += prio(x.pop())

print(f'Single pack: {t}')


