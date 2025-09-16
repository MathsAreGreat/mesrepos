from math import sqrt
from time import perf_counter as P


def structure(n, mx):
    mn = 0.0
    dn = 1.0
    a0 = int(sqrt(n))
    an = int(sqrt(n))
    periods = [a0]
    if a0 == sqrt(n):
        return periods
    while mx:
        mn = dn*an - mn
        dn = (n - mn**2)/dn
        an = int((a0 + mn)/dn)
        periods.append(an)
        mx -= 1
    return periods[::-1]


def get_e_periods(x=100):
    ps = [2]
    nb = 1
    i = 0
    while len(ps) < x:
        r = 1
        if i % 3 == 1:
            r = 2*nb
            nb += 1
        ps.append(r)
        i += 1
    return ps[::-1]


start = P()


sequence = [2, *(x for k in range(1, 34) for x in (1, 2 * k, 1))]

a, b = 1, sequence[-1]
for x in reversed(sequence[:-1]):
    a, b = x * a + b, a
print(sum(map(int, str(a))))


print(f"Answered in {P()-start}s")
