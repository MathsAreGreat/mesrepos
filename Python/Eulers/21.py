
import math


def find_proper_divisors(n):
    divisors = set()  # Using a set to avoid duplicate divisors
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divisors.add(i)  # Add the divisor
            divisors.add(n // i)  # Add its complement divisor
    divisors.remove(n)
    return divisors


# start = P()
# n = 220
# r = d(n)
# print(*sorted(r.values()), sep=", ")
# print(f"Answered in {P()-start}s")

n = 220
factor = find_proper_divisors(n)
print(sum(factor))
