import time

startTime = time.time()
somme = 0
for i in range(1, 1000):
    print(i, end="\r")
    somme += pow(i, i, 10**10)

print(somme % 10**10)
print(time.time()-startTime)
