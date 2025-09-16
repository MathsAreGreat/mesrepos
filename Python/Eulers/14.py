# Collatz Sequence

def collatz(nb):
    count = 1
    while nb > 1:
        count += 1
        if nb % 2 == 0:
            nb //= 2
        else:
            nb = 3*nb+1
    return count


best = 0
key = 0
infos = {}
for i in range(1, 1000_000):
    k = collatz(i)
    if k > best:
        best = k
        key = i

print(key, ":", best)
