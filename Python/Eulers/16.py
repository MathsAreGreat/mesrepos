from functools import lru_cache


def goo(nbr):
    ways = []
    way = [(0, 0)]
    segs = []
    i = 0
    j = 0
    cc = 10
    cx = 1
    while True:
        if i < nbr:
            c = (i+1, j)
            seg = (way[-1], c)
            if seg not in segs:
                segs.append(seg)
                way.append(c)
                i, j = c
                continue
        if j < nbr:
            c = (i, j+1)
            seg = (way[-1], c)
            if seg not in segs:
                segs.append(seg)
                way.append(c)
                i, j = c
                continue

        segs = [(s, t) for s, t in segs if s != way[-1]]
        if len(way) == 2*nbr+1:
            ways.append(way)
            print(end="\r")
            print(cx, ":", way)
            cx += 1
        way = way[:-1]
        if not way:
            break
        i, j = way[-1]


@lru_cache(maxsize=None)
def countRoutes(m, n):
    if n == 0 or m == 0:
        return 1
    return countRoutes(m-1, n)+countRoutes(m, n-1)


def countRoutes2(m, n):
    grid = [[0 if j else 1 for j in range(n)] for _ in range(m)]
    for j in range(1, n):
        grid[0][j] = 1

    for i in range(m):
        for j in range(n):
            grid[i+1][j+1] = grid[i][j+1] + grid[i+1][j]
    return grid[m-1][n-1]

# for n in range(1, 21):
#     print(n, ":", math.comb(2*n, n))


n = 20
ss = countRoutes2(n, n)
print(ss)
