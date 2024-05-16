# Modulo Operator
def is_even(number):
    return number % 2 == 0

# Bitwise AND Operator
def is_odd(number):
    return number & 1 == 1

# Division
def is_even_or_odd(number):
    return "Even" if number // 2 == number / 2 else "Odd"


# Test
num = 5
print(f"{num} is even: {is_even(num)}")
print(f"{num} is odd: {is_odd(num)}")
print(f"{num} is {is_even_or_odd(num)}")

