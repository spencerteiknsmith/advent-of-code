import numpy as np
from sys import stdin
from collections import deque as deq
from copy import copy
import functools as fntls
import itertools as ittls
import operator as op
import math
import re
import string
import heapq as q

e = enumerate
INF = float('inf')


def solve():
    h, d, a = 0, 0, 0
    for l in lines():
        dir, n = l.split()
        n = int(n)
        if dir[0] == 'f':
            h += n
            d += a * n
        elif dir[0] == 'd':
            a += n
        elif dir[0] == 'u':
            a -= n
    print(h * d)
    pass


def lines():
    return stdin.read().strip().split('\n')


def groups():
    return [g.split('\n') for g in stdin.read().strip().split('\n\n')]


def solvea(inp):
    #
    return None


def solveb(inp):
    #
    return None


def btwn(v, l, h):
    return (v > l and v < h) or (v < l and v > h)


def btwne(v, l, h):
    return (v >= l and v <= h) or (v <= l and v >= h)


def btwni(v, l, h):
    return v >= l and v < h


def valids(ijl, hii, hij):
    for i, j in ijl:
        if (btwni(i, -INF if hii == INF else 0, hii)
                and btwni(j, -INF if hii == INF else 0, hij)):
            yield (i, j)


def neigh4(i, j, hii=INF, hij=INF):
    yield from valids([(i - 1, j), \
                        (i + 1, j), \
                        (i, j - 1), \
                        (i, j + 1)], hii, hij)


def neigh8(i, j, hii=INF, hij=INF):
    yield from neigh4(i, j, hii, hij)
    yield from valids([(i - 1, j - 1), \
                        (i - 1, j + 1), \
                        (i + 1, j - 1), \
                        (i + 1, j + 1)], hii, hij)


if __name__ == '__main__':
    solve()
