import math
from time import perf_counter as P


def isPrime(n):
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


def prime_factors(n):
    i = 2
    factors = {}
    while i * i <= n:
        if i not in factors:
            factors[i] = 0
        if n % i:
            i += 1
        else:
            n //= i
            factors[i] += 1
    if n > 1:
        if n not in factors:
            factors[n] = 0
        factors[n] += 1
    return {k: v for k, v in factors.items() if v > 0}


start = P()
i = 2
nb = 4
while True:
    i += 1
    infos = {}
    for j in range(nb):
        factors = prime_factors(i+j)
        if len(factors) != nb:
            break
        infos[i+j] = factors
    else:
        for k, v in infos.items():
            print(k, ":", v)
            break
        break
print(P()-start)
