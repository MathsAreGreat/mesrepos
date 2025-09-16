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


def jrb():
    st = "0123456789"
    primes = [2, 3, 5, 7, 11, 13, 17]
    somme = 0
    for perm in permutations(st):
        str_num = ''.join(perm)
        if str_num[5] != "5":
            continue
        for i, prime in enumerate(primes, start=1):
            number = int(str_num[i:i+3])
            if number % prime > 0:
                break
        else:
            somme += int(str_num)
    print(somme)


def jrb2():
    pandigital_num = permutations(
        {"1", "2", "3", "4", "5", "6", "7", "8", "9", "0"})
    res = [
        int("".join(p))
        for p in pandigital_num
        if p[5] == "5"
        and p[3] in {"0", "2", "4", "6", "8"}
        and int(p[7] + p[8] + p[9]) % 17 == 0
        and int(p[6] + p[7] + p[8]) % 13 == 0
        and int(p[5] + p[6] + p[7]) % 11 == 0
        and int(p[4] + p[5] + p[6]) % 7 == 0
        and int(p[2] + p[3] + p[4]) % 3 == 0
    ]
    print(sum(res))


start = P()
jrb()
end = P()-start
print(end)
