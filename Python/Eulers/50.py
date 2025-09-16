import math
from time import perf_counter as P


def isPrime(n):
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


def prime_terms(number):
    j = 2
    primes = []
    while j < number:
        n = number
        i = j
        while i <= n:
            if isPrime(i):
                n -= i
                primes.append(i)
            i += 1
        if n == 0:
            break
        j += 1
        primes = []
    return primes


start = P()
infos = {}
NBR = 1000_000
numbers = [
    i
    for i in range(2, 4000)
    if isPrime(i)
]
print(len(numbers), "items !")

i = 0
infos = {}
while i < len(numbers)-1:
    somme = 0
    j = i
    temp = 0
    items = []
    length = 0
    while temp < NBR:
        if isPrime(temp):
            somme = temp
            length = len(items)
        items.append(numbers[j])
        temp = sum(items)
        j += 1
    if somme not in infos:
        infos[somme] = 0
    if infos[somme] < length:
        infos[somme] = length
    i += 1

p = max(infos.items(), key=lambda x: x[-1])
print(p)
print(P()-start)
