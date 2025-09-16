s = 0
for i in range(1000):
    if i % 3 == 0:
        s += i
        continue
    if i % 5 == 0:
        s += i

print(s)
