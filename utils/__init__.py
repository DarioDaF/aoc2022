
from dataclasses import dataclass
from math import prod, inf
import re
import bisect as bs
from copy import deepcopy
from collections import defaultdict, deque
from collections.abc import Iterator
from functools import reduce, total_ordering, lru_cache, cache, singledispatch
from queue import PriorityQueue
from typing import Callable, Generic, TypeVar
from itertools import product, permutations, zip_longest, count
import os

T = TypeVar('T')
K = TypeVar('K')

def clamp(x: T, _min: T, _max: T) -> T:
    return max(min(x, _max), _min)

def readInput():
    import __main__ as m
    #d = os.path.dirname(os.path.abspath(m.__file__))
    d = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bnf = os.path.basename(m.__file__)
    bnf = bnf.split('_')[0]
    bnf = bnf.split('.')[0]
    with open(os.path.join(d, 'input', bnf + '.txt'), 'r', encoding='utf-8') as fp:
        return fp.read()

def rfind(l: list, item):
    for i in reversed(range(len(l))):
        if l[i] == item:
            return i
    return -1

@dataclass(frozen=True, eq=True)
class Pt:
    x: int|float
    y: int|float
    def __add__(self, other: 'Pt'):
        return Pt(self.x + other.x, self.y + other.y)
    def __neg__(self):
        return Pt(-self.x, -self.y)
    def __sub__(self, other: 'Pt'):
        return self + (-other)
    def toDir(self):
        return Pt(clamp(self.x, -1, 1), clamp(self.y, -1, 1))
    def dist(self, n):
        return (abs(self.x) ** n + abs(self.y) ** n) ** (1/n)
    def toTuple(self):
        return (self.x, self.y)
    def __mul__(self, other: int|float):
        return Pt(self.x * other, self.y * other)
    def __truediv__(self, other: int|float):
        return Pt(self.x / other, self.y / other)

#@total_ordering
@dataclass
class KV(Generic[K, T]):
    key: K
    val: T
    def __lt__(self, other: 'KV'):
        return self.key < other.key
    def __getitem__(self, i: int):
        if i == 0:
            return self.key
        if i == 1:
            return self.val
        raise IndexError()

class PQueue(Generic[T, K]):
    def __init__(self, key: Callable[[T], K] = None):
        if key == None:
            key = lambda x: x # Use identity if no key function provided
        self.key = key
        self.pq = PriorityQueue()
    def empty(self):
        return self.pq.empty()
    def put(self, v: T, key: K = None):
        if key == None:
            key = self.key(v)
        self.pq.put_nowait(KV(key, v))
    def get(self) -> tuple[T, K]:
        key, val = self.pq.get_nowait()
        return val, key

re_pred = re.compile('(\w+)(?:\(([\w,]+)\))?')
def parseClingo(out):
    global re_pred
    res_type = ''
    res_str = ''

    last_line = ''
    in_answer = False
    for line in out.split('\n'):
        if in_answer and line == '':
            res_type = last_line
            in_answer = False
        if last_line.startswith('Answer: '):
            in_answer = True
            res_str = line
        last_line = line
    
    preds = []
    for m in re_pred.finditer(res_str):
        p, pargs = m.groups()
        if pargs == None:
            pargs = []
        else:
            pargs = pargs.split(',')
        preds.append((p, pargs))
    return res_type, preds
