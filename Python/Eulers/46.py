import math
from time import perf_counter as P


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


n = 9
s = P()
while True:
    if not is_prime(n):
        for i in range(2, n):
            if is_prime(i):
                r = n-i
                if r % 2:
                    continue
                r //= 2
                if math.sqrt(r).is_integer():
                    break
        else:
            print(n)
            break
    n += 2


print(P()-s)
