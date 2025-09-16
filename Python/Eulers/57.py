from time import perf_counter as P
from fractions import Fraction


def sqrt2(nb):
    res = 1+Fraction(1, 2)
    while nb:
        res = 1+1/(1+res)
        nb -= 1
    return res


s = P()
counter = 0
for i in range(1000):
    numerator = str(sqrt2(i).numerator)
    denominator = str(sqrt2(i).denominator)
    if len(numerator) > len(denominator):
        counter += 1
print(P()-s)
print(counter)
