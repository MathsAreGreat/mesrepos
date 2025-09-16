from gmpy2 import mpz, next_prime, is_prime
import itertools


MAX = 10000


# Whether all concatenations of p with numbers from the iteratable it are prime
def conprime(p, it):
    return all(is_prime(int(str(p)+str(q))) and is_prime(int(str(q)+str(p)))
               for q in it)


# iterate over primes >p and <MAX which are equal to the remainder modulo 3
def p_iter(p, remainder):
    while p < MAX:
        p = next_prime(p)
        if p % 3 == remainder:
            yield p


for r in (1, 2):
    for p0 in itertools.chain([mpz(3)], p_iter(3, r)):
        for p1 in p_iter(p0, r):
            if conprime(p1, (p0,)):
                for p2 in p_iter(p1, r):
                    if conprime(p2, (p0, p1)):
                        for p3 in p_iter(p2, r):
                            if conprime(p3, (p0, p1, p2)):
                                for p4 in p_iter(p3, r):
                                    if conprime(p4, (p0, p1, p2, p3)):
                                        print(sum((p0, p1, p2, p3, p4)))
                                        exit(0)
