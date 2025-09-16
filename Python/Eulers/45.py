from time import perf_counter as P
import math



def is_hexagonal(x):
    n = math.sqrt(8*x + 1)
    if not n.is_integer():
        return False
    q, r = divmod(n+1, 4)
    if r:
        return False
    return q


def is_pentagonal(x):
    n = math.sqrt(24*x+1)
    if not n.is_integer():
        return False
    q, r = divmod(n+1, 6)
    if r:
        return False
    return q


def pentagon(n):
    return n*(3*n-1)//2


def sols():
    n = 287
    c = 287
    while c:
        number = n*(n+1)//2
        n += 1
        p = is_pentagonal(number)
        if not p:
            continue
        h = is_hexagonal(number)
        if not h:
            continue
        print(f"T{n} = P{p} = H{h} = {number}")
        break


s = P()
sols()
print(P()-s)
