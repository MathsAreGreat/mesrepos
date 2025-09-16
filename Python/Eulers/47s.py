import numpy as np
import time

startTime = time.time()


def getPrimes(limit):
    dp = [0] * limit
    dp[0] = dp[1] = 1

    for i in range(2, limit):
        if 0 == dp[i]:
            for j in range(i, limit, i):
                dp[j] += 1
    return dp


def sols():
    limit = 1000000
    startTime = time.time()
    dp = getPrimes(limit)
    for i in range(2, limit - 4):

        if dp[i] >= 4 and dp[i + 1] >= 4 and dp[i + 2] >= 4 and dp[i + 3] >= 4:
            print(i)
            break
    print(time.time() - startTime)


def sols2():
    startTime = time.time()
    numfac = np.zeros((1000000,), dtype=np.uint8)
    for k in range(2, 1000):
        if numfac[k] == 0:
            numfac[k::k] += 1
    print(time.time() - startTime)
    print((np.lib.stride_tricks.sliding_window_view(
        numfac, (4,)) == 4).all(axis=1).argmax())


def primeFactors(n):
    prime_factors = {}
    factor = 2
    while factor ** 2 <= n:
        if n % factor:
            if factor != 2:
                factor += 2
            else:
                factor += 1
        else:
            prime_factors[factor] = prime_factors.get(factor, 0) + 1
            n //= factor
    if n > 1:
        prime_factors[n] = prime_factors.get(n, 0) + 1
    return prime_factors


n = 4
# Find first n consecutive integers to have m distinct prime factors each.
m = 4

i = 1
result = []
while True:
    prime_fac_store = []
    for j in range(n):
        prime_fac_store.append(primeFactors(i + j))
    if set([len(prime_fac) for prime_fac in prime_fac_store]) == {m}:
        result = [[i + j, list(prime_fac_store[j].keys())] for j in range(n)]
        break
    i += 1

print(result)
