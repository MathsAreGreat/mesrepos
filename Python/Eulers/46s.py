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


def odd_composite(x):
    if x % 2 == 0:
        return False
    elif not isPrime(x):
        return True


def conjecture(i):
    square = 1
    while (i > 2*square**2):
        remainder = i - 2*square**2
        if isPrime(remainder):
            return True
        square += 1
    return False


n = 9
s = P()

for i in range(9, 36000, 1):
    if not conjecture(i) and odd_composite(i):
        print(f'{i} is the first counter example of Goldbachs other conjecture')
        break


print(P()-s)
