from cs50 import get_int

while True:
    # prompt user
    response = get_int("Height of Pyramid (between 0 and 23)?: ")
    if response >= 0 and response <= 23:
        break

for i in range(1, response + 1):

    # left space
    print(" " * (response - i), end="")

    # left pyramid
    print("#" * i, end="")

    # middle space
    print("  ", end="")

    # for right pyramid
    print("#" * i)