import sympy


def sigma0(n):
    factor = sympy.factorint(n)
    sigma0 = 1
    for key in factor.keys():
        sigma0 = sigma0 * (factor[key] + 1)
    return sigma0

# calculates the nth triangular number


def Tn(s):
    return int(s*(s+1)/2)

# calculates number of divisors of ith triangular number


def tridiv(i):
    int(i)
    if i % 2 == 0:
        return sigma0(int(.5*i)) ^ sigma0(i+1)
    else:
        return sigma0(i)*sigma0(int((i+1)/2))


divisors = 1
i = 1
while divisors <= 9:
    i += 1
    (i, divisors) = (i, max([divisors, tridiv(i)]))


print(f"{i}th triangular number: {Tn(i)}")
print(f"number of divisors: {tridiv(i)}")
