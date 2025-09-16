def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


num = den = 1
for i in range(10, 99):
    for j in range(i+1, 100):
        un = set(f"{i}").intersection(set(f"{j}"))
        if not un:
            continue
        l = list(un)[0]
        if int(l) == 0:
            continue
        a = int(str(i)[str(i).index(l)-1])
        b = int(str(j)[str(j).index(l)-1])
        if b and a/b == i/j:
            num *= a
            den *= b


p = pgcd(num, den)
print(den/p)
