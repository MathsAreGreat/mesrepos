from time import perf_counter as P


def is_palindromic(c):
    return str(c) == str(c)[::-1]


start = P()

counter = 0
uniques = []
for i in range(1, 100):
    for j in range(1, 100):
        n = sum(int(e) for e in str(i**j))
        if n > counter:
            counter = n
            uniques = [i, j]

print(counter)
i, j = uniques
print(i**j)
elapsed_time = P()-start
print(f"Time taken to run: {elapsed_time:.6f} s")
