from functools import lru_cache
from time import perf_counter as P
from fractions import Fraction


def sqrt1(limit):
    prev = [3, 2]
    ans = 0
    cur = 1
    while cur <= limit:
        if len(str(prev[0])) > len(str(prev[1])):
            ans += 1
        prev = [prev[0]+2*prev[1], prev[0]+prev[1]]
        cur += 1
    return ans  # 4ms


def sqrt2(limit):
    a, b, result = 1, 2, 0
    for i in range(limit):
        a, b = b, 2 * b + a
        result += len(str(a + b)) > len((str(b)))
    return result  # 4ms


@lru_cache(maxsize=None)
def expansion(n: int) -> Fraction:
    if n == 1:
        return Fraction(1, 2)
    return Fraction(1, 2 + expansion(n - 1))


def sqrt3(limit):
    num = 0
    for i in range(1, limit+1):
        f = 1 + expansion(i)
        num += len(str(f.numerator)) > len(str(f.denominator))
    return num


limit = 1000
s = P()

print(P()-s)
