from math import log
import math
from time import perf_counter as P


def is_prime(n):
    if n < 2:
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


def primes(N):
    return [2]+[
        i
        for i in range(3, N, 2)
        if is_prime(i)
    ]


def fct1(arr) -> int:
    sol = 0
    for i in range(len(arr)):
        tmp = sum(arr[i:len(arr)-1])
        if (is_prime(tmp) is True) and (tmp > sol):
            sol = tmp
    return sol


def solb():
    prime_ls = []
    sol = 0
    tmp = 0
    i = 0

    while tmp < 1000000:
        sol = tmp
        if is_prime(i):
            prime_ls.append(i)
            tmp = fct1(prime_ls)
        i += 1
    return sol


def solb2():
    primesUpTo50K = [2]
    for i in range(3, 4000, 2):
        if is_prime(i):
            primesUpTo50K.append(i)
    terms = 0
    bestPrime = 0
    for i in range(len(primesUpTo50K)):
        for j in range(i, len(primesUpTo50K)):
            totalSum = sum(primesUpTo50K[i:j])
            if totalSum > 1000000:
                break
            if is_prime(totalSum):
                if j - i + 1 > terms:
                    terms = j - i + 1
                    bestPrime = totalSum
        return bestPrime


def PE050(M=10**6):
    def f(t): return t**2*(2*log(t)-1)-4*M
    def fp(t): return 4*t*log(t)  # fp is derivative of f, approx.
    x, y = M, M+2
    while y-x > 1:
        y, x = x, x-f(x)/fp(x)
    # Newton's method in order to find approx of pMax
    myBound = x*(log(x)+log(log(x)-1))

    prime = primes(int(myBound))
    # the crux, most of the time spent is here

    prSum = [0]  # let's do the cumulative sum
    pk = 0
    larg = 0
    while pk < M:
        pk += prime[larg]
        prSum.append(pk)
        larg += 1
    # larg<=len(prime) if not an error would have raised !
    # print((len(prime)-larg)/larg) # OK with 10% of marge

    # after that the answer will be found under 1ms
    res = 0
    pList = set()
    for j in range(larg-1, 0, -1):
        flag = j-res
        for i in range(larg-res+1):
            if i > flag:
                break
            pk = prSum[j] - prSum[i]
            if is_prime(pk):
                if j-i == res:
                    pList.add(pk)
                else:
                    res = j-i
                    pList = set()
                    pList.add(pk)
                flag = j-res
        if j < res:
            return pList


start = P()
p = PE050(10**9)
print(p)
elapsed_time = P()-start
print(f"Time taken to run: {elapsed_time:.6f} s")
