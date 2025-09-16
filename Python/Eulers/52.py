from time import perf_counter as P


start = P()
i = 10
while True:
    if "".join(sorted(str(2*i))) == "".join(sorted(str(i))):
        if "".join(sorted(str(3*i))) == "".join(sorted(str(i))):
            if "".join(sorted(str(4*i))) == "".join(sorted(str(i))):
                if "".join(sorted(str(5*i))) == "".join(sorted(str(i))):
                    if "".join(sorted(str(6*i))) == "".join(sorted(str(i))):
                        print(i)
                        break
    i += 1
elapsed_time = P()-start
print(f"Time taken to run: {elapsed_time:.6f} s")
