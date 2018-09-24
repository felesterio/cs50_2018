from cs50 import get_float
import math
even_sum = 0
odd_sum = 0

while True:
    ccnum = get_float("Enter a credit card number: ")
    if ccnum > 0:
        break

# test 1, valid credit card
n = 1
index = 10**n
nDigits = math.floor(math.log10(abs(ccnum))) + 1
while n <= nDigits:
    # for even position digits
    if n % 2 == 0:
        position_a = ccnum % index
        index_minus = 10**(n - 1)
        digit_a = math.floor(position_a / index_minus)
        double_digit_a = 2 * digit_a
        if double_digit_a >= 10:
            one = double_digit_a % 10
            two = math.floor(double_digit_a / 10)
            double_digit_a = one + two
        even_sum = double_digit_a + even_sum

        # odd digits
    elif n % 2 != 0:
        position_b = ccnum % index
        index_minus = 10**(n - 1)
        digit_b = math.floor(position_b / index_minus)
        odd_sum = digit_b + odd_sum

    n += 1
    index = 10**n

final_sum = odd_sum + even_sum

if final_sum % 10 != 0:
    print("INVALID")

if final_sum % 10 == 0:
    first = math.floor(ccnum / (10**(nDigits - 2)))

    # amex
    if (first == 34 or first == 37) and nDigits == 15:
        print("AMEX")

    # mastercard
    elif (first == 51 or first == 52 or first == 53 or first == 54 or first == 55) and nDigits == 16:
        print("MASTERCARD")

    # visa
    elif math.floor(first / 10) == 4 and (nDigits == 13 or nDigits == 16):
        print("VISA")

    else:
        print("INVALID")