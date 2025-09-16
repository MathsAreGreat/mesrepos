# Solves in 2 milliseconds

from time import perf_counter


def factoriel(n):
    p = 1
    if n > 1:
        for i in range(2, n+1):
            p *= i
    return p


def factoriels():
    return {
        f"{d}": factoriel(d)
        for d in range(10)
    }


n = 5
print("Time taken now !")
start = perf_counter()
fcts = factoriels()
sum_powers = 0

results = []
for digit in range(10, 1000_000):
    if sum(fcts[d] for d in str(digit)) == digit:
        results.append(digit)

end = perf_counter()

print(f"Time taken: {end - start:.10f} seconds")
print(sum(results))
