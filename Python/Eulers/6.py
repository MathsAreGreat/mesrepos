# Sum Square Difference


def sum_square_difference(n):
    """Return the difference between the sum of the squares of the first n natural numbers and the square of their sum."""
    s2 = (n * (n + 1) * (2 * n + 1)) // 6
    s3 = ((n * (n + 1)) ** 2) // 4
    return s3-s2


print(sum_square_difference(100))
