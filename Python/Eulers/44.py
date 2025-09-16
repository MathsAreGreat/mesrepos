from time import perf_counter as P
import math



def is_pentagonal(x):
    return ((math.sqrt(24*x+1)+1)/6).is_integer()


def pentagon(n):
    return n*(3*n-1)//2


def sols():
    nums = [1, 5, 12]
    n = 10
    Pn = 22
    while nums:
        #   for(var n = 10, Pn = 22; ; n+= 3, Pn+= n) {
        nums.append(Pn)
        for num in nums:
            a = Pn - num
            if is_pentagonal(a) and is_pentagonal(abs(a - num)):
                print(a-num)
                return 0
        n += 3
        Pn += n


s = P()
sols()
print(P()-s)
