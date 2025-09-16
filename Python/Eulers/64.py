from math import sqrt
from time import perf_counter as P


def structure(n):
    mn = 0.0
    dn = 1.0
    a0 = int(sqrt(n))
    an = int(sqrt(n))
    period = 0
    if a0 == sqrt(n):
        return period
    while an != 2*a0:
        mn = dn*an - mn
        dn = (n - mn**2)/dn
        an = int((a0 + mn)/dn)
        period += 1
    return period


start = P()

c = 0
for i in range(10_000):
    r = structure(i)
    if r % 2:
        c += 1

print(f"Answered in {P()-start}s")
print(c)
