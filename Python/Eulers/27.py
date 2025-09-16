

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


best = 0
els = []

# for a in range(-999, 1000):
#     for b in range(-999, 1000):
#         n = 0
#         prime_counter = 0
#         while True:
#             s = n**2+a*n+b
#             if s < 0:
#                 break
#             if is_prime(s):
#                 print(a, b, s, end="\r")
#                 prime_counter += 1
#             else:
#                 break
#             n += 1
#         if prime_counter > best:
#             best = prime_counter
#             els = [a, b]

# print(*els, best)

print(-61 * 971)
