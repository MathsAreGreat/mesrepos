from functools import lru_cache


@lru_cache(maxsize=None)
def fibonnacci(n):
    if n < 3:
        return 1
    else:
        return fibonnacci(n-1) + fibonnacci(n-2)


i = 0
while True:
    fn = fibonnacci(i)
    if len(str(fn)) == 1000:
        break
    i += 1
print(i, ":", fn)
