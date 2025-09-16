from time import perf_counter as P


def powerful_digit_sum(limit):
    return max(sum(map(int, str(a ** b))) for a in range(1, limit) for b in range(1, limit))


start = P()
print(powerful_digit_sum(100))
elapsed_time = P()-start
print(f"Time taken to run: {elapsed_time:.6f} s")
