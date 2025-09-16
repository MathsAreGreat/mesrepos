# Even Fibonacci Numbers
s = 0
a, b = 0, 1
while b < 4000000:
    if b % 2 == 0:
        s += b
    a, b = b, a+b

print(s)
