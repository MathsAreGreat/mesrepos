
from time import perf_counter as P
cubes = {}
i = 10


def get_hash_rep(n):
    return ",".join(sorted(list(str(n))))


start = P()

while True:
    hash_rep = get_hash_rep(i**3)
    cubes.setdefault(hash_rep, []).append(i)
    if len(cubes[hash_rep]) == 5:
        break
    i += 1

ans = min(cubes[hash_rep]) ** 3

print(f"Your answer, Mr. Habip, is {ans} in {P()-start}s")
