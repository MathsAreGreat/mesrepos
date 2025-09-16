from time import perf_counter as P
start = P()
# c = 0
# for i in range(9):
#     j = i+1
#     p = 1
#     while True:
#         result = j**p
#         if len(str(result)) < p:
#             break
#         if len(str(result)) == p:
#             c += 1
#         p += 1

c = len([(i, j, i ** j) for i in range(1, 10)
        for j in range(1, 100) if len(str(i ** j)) == j])

print(f"{c} : Answered in {P()-start}s")
