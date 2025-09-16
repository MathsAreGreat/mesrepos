from time import perf_counter as P


def is_palindromic(c):
    return str(c) == str(c)[::-1]


start = P()

counter = 0
uniques = set()
for i in range(10, 10000):
    n = i
    if n in uniques:
        continue
    temp = set()
    for j in range(50):
        if n in uniques:
            break
        if j:
            temp.add(n)
        n += int(str(n)[::-1])
        if is_palindromic(n):
            uniques.update(temp)
            break
    else:
        counter += 1

print(counter)
elapsed_time = P()-start
print(f"Time taken to run: {elapsed_time:.6f} s")
