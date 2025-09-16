from numba import jit
from time import perf_counter as P


@jit(nopython=True)  # 8.6 seconds without this
def myfunc():
    res = [0, 0]
    for p in range(3, 10001):
        counter = 0
        for a in range(1, p):
            for b in range(a, p-a):
                c = p-a-b
                if a*a + b*b == c*c:
                    counter += 1
        if res[0] < counter:
            res[0] = counter
            res[1] = p
    print(res)


start = P()
myfunc()
print(P()-start)

start = P()
myfunc()
print(P()-start)
