

def all_perms(str):
    if len(str) <= 1:
        yield str
    else:
        for perm in all_perms(str[1:]):
            for i in range(len(perm)+1):
                yield perm[:i] + str[0:1] + perm[i:]


products = set()

for p in all_perms('123456789'):

    lhs = p[:5]
    rhs = p[5:]

    size = len(lhs)
    allowedPositions = [1, 3]
    for multiplyPos in allowedPositions:
        factor1 = lhs[:multiplyPos]
        factor2 = lhs[multiplyPos:]
        if int(factor1) * int(factor2) == int(rhs):
            products.add(int(rhs))

print(products)
