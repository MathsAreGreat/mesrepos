from time import perf_counter as P
from itertools import permutations
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


# start = P()
# print(max(int(''.join(i for i in x)) for x in permutations(str(1234567))
#       if all(int(''.join(i for i in x)) % p > 0 for p in range(2, int(10 ** 3.5) + 1))))
# print(P()-start)
start = P()
st = "123456789"
while st:
    res = []
    for perm in permutations(st):
        str_num = ''.join(perm)
        if str_num[-1] not in "1379":
            continue
        num = int(str_num)
        if is_prime(num):
            res.append(num)
    if res:
        print(max(res))
        break
    st = st[:-1]
print(P()-start)
