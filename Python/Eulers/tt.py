# for i in range(1, 20):
#     print(1/i)

def cycle_length(n):
    rem = 1 % n
    rems = {}
    pos = 0
    while rem and rem not in rems:
        rems[rem] = pos
        rem = (10*rem) % n
        pos += 1
    if rem == 0:
        return 0
    return pos-rems[rem]


max_length = 0
number = 0
for i in range(1, 1000):
    c = cycle_length(i)
    if c > max_length:
        max_length = c
        number = i

print(number, ':', max_length)
