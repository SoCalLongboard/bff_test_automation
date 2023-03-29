# Standard library imports
from random import choice
from string import ascii_uppercase, digits


UPPERCASE = ascii_uppercase
DIGITS = digits
ALPHANUMERIC = UPPERCASE + DIGITS

SAMPLE_FLOOR = 2
SAMPLE_CEILING = 6


def rand_char_str(size):
    chars = []
    for _ in range(size):
        chars.append(choice(ALPHANUMERIC))
    return "".join(chars)


def rand_alpha_str(size):
    chars = []
    for _ in range(size):
        chars.append(choice(UPPERCASE))
    return "".join(chars)


def rand_num_str(size):
    chars = []
    for _ in range(size):
        chars.append(choice(DIGITS))
    return "".join(chars)


def rand_boolean():
    return choice([True, False])


def get_sample_range(floor, ceiling):
    return range(floor, ceiling + 1)


def get_sample_value(floor, ceiling):
    sample_range = get_sample_range(floor, ceiling)

    return choice(sample_range)


def main():
    for index in range(1, 9):
        print(f"rand_char_str({index}) = {rand_char_str(index)}")
    print()

    for index in range(1, 9):
        print(f"rand_alpha_str({index}) = {rand_alpha_str(index)}")
    print()

    for index in range(1, 9):
        print(f"rand_num_str({index}) = {rand_num_str(index)}")
    print()

    for index in range(1, 9):
        print(f"rand_boolean() = {rand_boolean()}")
    print()


if __name__ == "__main__":
    main()
