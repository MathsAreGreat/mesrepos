# Solves in 2 milliseconds

from time import perf_counter


def power(n):
    return {d: d**n for d in range(10)}


def power_sums(n):
    lower_bound, upper_bound = determine_bounds(n)
    powers = power(n)
    res = []
    for i in range(lower_bound, upper_bound):
        digits = list(map(int, str(i)))
        sum_num = sum(powers[d] for d in digits)
        if sum_num == i:
            res.append(i)
    return res


def determine_bounds(n):
    """Given a power n > 1, return the lower and upper bounds in which to search"""
    nine_power, digit_count = 9 ** n, 1
    while True:
        upper = digit_count * nine_power
        new_count = len(str(upper))
        if new_count == digit_count:
            return max(10, 2 ** n), upper+1
        digit_count = new_count


def is_digit_power_sum(i, n):
    return sum(int(d) ** n for d in str(i)) == i


def find_equal_digit_power_sum(n):
    """Find all numbers i between lower_bound and upper_bound (inclusive) that have a digit sum of n"""
    lower_bound, upper_bound = determine_bounds(n)
    # Print the range of numbers with the given digit sum
    print(
        f"Numbers between {lower_bound} and {upper_bound} with a digit sum of {n}:")
    numbers = []
    for i in range(lower_bound, upper_bound):
        if is_digit_power_sum(i, n):
            numbers.append(i)
    return numbers


n = 5
print("Time taken now !")
start = perf_counter()
# numbers = find_equal_digit_power_sum(n)
numbers = sum(power_sums(n))
print(numbers)

end = perf_counter()

print(f"Time taken: {end - start:.10f} seconds")
