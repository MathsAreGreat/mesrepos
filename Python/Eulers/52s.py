"""Hmm. Well, one obvious optimization that immediately strikes me is
that I don't have to check every number - if we're looking for n
multiples, we need a number that is, at most, floor(10^d / n) for some
d. In the case of n = 2, that means less than 5 * 10^d - 1.

"""

from math import floor
from time import perf_counter


def permuted_multiples(n):
    """Find the lowest number which has n permuted multiples.

    """

    start = perf_counter()
    exponent = 0
    found = False
    permul = None
    while not found:
        smallest_to_check = 10 ** exponent
        for i in range(smallest_to_check, floor(smallest_to_check * 10 / n)):
            found = True
            for j in range(2, n + 1):
                if sorted(str(i)) != sorted(str(i * j)):
                    found = False
                    break
            # If we get this far and found has not been set to false,
            # then we have enough multiples.
            if found:
                permul = i
                break
            # else continue
        exponent += 1
    end = perf_counter()
    print(f"Smallest number with {n} permuted multiples is: {permul}")
    print(f"Time required: {end - start:0.4f} seconds")


start = perf_counter()
i = 1
while True:
    if sorted(str(i)) == sorted(str(2*i)) == sorted(str(3*i))\
            == sorted(str(4*i)) == sorted(str(5*i)) == sorted(str(6*i)):
        print(i)
        break
    i += 1
end = perf_counter()
print(f"Time required: {end - start:0.4f} seconds")
