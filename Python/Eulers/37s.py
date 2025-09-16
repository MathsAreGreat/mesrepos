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


def generate_primes(input, adds):
    primes = []
    for e in adds:
        st = f"{input}{e}"
        rf = int(st)
        lf = int(st[1:])
        if is_prime(rf):
            # if is_prime(lf):
            primes.append(rf)
    return primes


mes_primes = [2, 3, 5, 7]
adds = [1, 3, 7, 9]
nb = 0

last = True
vb = 1000
while vb:
    last = []
    for prime in mes_primes[nb:]:
        last += generate_primes(prime, adds)
    if not last:
        break
    nb = len(mes_primes)
    mes_primes += last
    vb -= 1

mes_primes = [
    prime
    for prime in set(mes_primes)
    if prime > 9 and all(is_prime(int(str(prime)[nb:])) for nb in range(len(str(prime))))
]
print(vb, ":", len(mes_primes))
print()
print(mes_primes)
