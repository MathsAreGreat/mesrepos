# Smallest Multiple

import math


def smallest_multiple(n):
    """Return the smallest positive integer that is a multiple of all integers from 1 to n inclusive."""
    return math.lcm(*list(range(1, n+1)))


print(smallest_multiple(20))
