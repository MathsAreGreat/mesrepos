from time import perf_counter as P
start = P()

infos = {}

i = 2
while True:
    nb = i**3
    s = "".join(sorted(str(nb)))
    infos[s] = infos.get(s, {})
    infos[s][i] = nb
    if len(infos[s]) == 5:
        print(infos[s])
        break
    i += 1

print(f"Answered in {P()-start}s")
