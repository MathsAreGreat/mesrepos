from math import factorial
from time import perf_counter as P


def comb(n, r):
    return factorial(n) // (factorial(r) * factorial(n-r))


start = P()

counter = 0
for i in range(100):
    n = i+1
    for r in range(n):
        c = comb(n, r)
        if c > 1000_000:
            counter += 1
print(counter)
elapsed_time = P()-start
print(f"Time taken to run: {elapsed_time:.6f} s")
