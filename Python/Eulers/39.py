def count_integer_right_triangles(p_limit):
    max_solutions = 0
    max_p = 0

    for p in range(3, p_limit + 1):
        num_solutions = 0
        for a in range(1, p // 2 + 1):
            if p * (p - 2 * a) % (2 * (p - a)) == 0:
                num_solutions += 1

        if num_solutions > max_solutions:
            max_solutions = num_solutions
            max_p = p
    return max_p


p_limit = 10000
result = count_integer_right_triangles(p_limit)
print("Max solutions:", result)
