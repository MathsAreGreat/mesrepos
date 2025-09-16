
import math


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


nb = 1
primes = []
i = 1
while i < 2000000:
    if is_prime(i):
        primes.append(i)
        nb = len(primes)
    if i % 100000 == 0:
        print(i, end="\r")
    i += 1

print(primes[0])
print(primes[-1])
print(sum(primes))
