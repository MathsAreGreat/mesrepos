def PandigitalProduct_1_9(n):
    i = 1
    while i * i <= n:
        q, r = divmod(n, i)
        if r == 0 and isPandigital(f"{n}{i}{q}"):
            return n
        i += 1
    return False


def isPandigital(Str):
    if len(Str) != 9:
        return False
    ch = "".join(sorted(Str))
    if ch == "123456789":
        return True
    else:
        return False


res = []
for i in range(200, 10**5):
    print(i, end="\r")
    if sorted(f"{i}") != sorted(set(f"{i}")):
        continue
    r = PandigitalProduct_1_9(i)
    if r:
        res.append(r)

print(sum(res))
