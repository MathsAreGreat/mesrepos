# Assuming the fifth_power list and functions are already defined
from time import perf_counter


fifth_power = [i ** 5 for i in range(10)]


def individual_digits(n):
    digits = []  # Initialize a new list for this number
    while n > 0:
        digits.append(n % 10)  # Append the last digit
        n //= 10  # Reduce the number by removing the last digit
    return digits[::-1]  # Return the digits in the correct order


def sum_of_fifth_powers(n, fifth_p):
    digits = individual_digits(n)  # Extract the digits of the number
    sum_powers = 0  # Initialize the sum of fifth powers
    for digit in digits:  # Loop through each digit
        # Add the fifth power of the digit to the sum
        sum_powers += fifth_p[digit]
    return sum_powers  # Return the sum of fifth powers


start = perf_counter()
# Set the upper limit
upper_limit = 6 * (9 ** 5)

# Initialize a list to store valid numbers
valid_numbers = []

# Loop through the numbers from 2 to upper_limit
for number in range(2, upper_limit):
    if number == sum_of_fifth_powers(number, fifth_power):
        valid_numbers.append(number)

# Calculate the sum of all valid numbers
result = sum(valid_numbers)


end = perf_counter()

print(f"Time taken: {end - start:.10f} seconds")
# Output the result
print("Sum of all numbers that can be written as the sum of the fifth powers of their digits:", result)
