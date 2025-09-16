from collections import deque
import math
from time import perf_counter


def is_prime(n):
    if n == 1:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    if n < 9:
        return True
    if n % 3 == 0:
        return False
    mx = int(math.sqrt(n))+1
    for i in range(5, mx, 6):
        if n % i == 0:
            return False
        if n % (i+2) == 0:
            return False
    return True


def rotations(v):
    nb = len(v)
    if nb == 1:
        return [int(v)]
    d = deque(v)
    res = []
    for i in range(nb):
        v = int("".join(d))
        res.append(v)
        d.rotate(1)
    return list(set(res))


# rs = rotations("1234")
# print(rs)

def valid(i):
    if i < 10:
        return True
    ns = sorted(int(e) for e in str(i))
    if ns[0] % 2 == 0 or ns[0] % 5 == 0 or sum(ns) % 3 == 0:
        return False
    return True


primes = []

start = perf_counter()

for i in range(2, 1_000_000):
    if not valid(i):
        continue
    if i in primes:
        continue
    rs = rotations(f"{i}")
    if all(is_prime(e) for e in rs):
        primes += rs
end = perf_counter()

print(f"Time taken: {end - start:.3f} seconds")
print(len(primes))
print(primes)
