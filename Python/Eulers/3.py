

import math
import time


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


nb = 600851475143

i = 2

primes = []
large = 2


i = 2
s = time.time()

while i <= nb:
    if not is_prime(i):
        i += 1
        continue
    primes.append(i)
    if nb % i == 0:
        nb //= i
        large = i
    else:
        i += 1

print(large, "#", time.time()-s)
