"""
--- Day 4: Secure Container ---

You arrive at the Venus fuel depot only to discover it's protected by a password. The Elves had written the password on a sticky note, but someone threw it out.

However, they do remember a few key facts about the password:

    It is a six-digit number.
    The value is within the range given in your puzzle input.
    Two adjacent digits are the same (like 22 in 122345).
    Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).

Other than the range rule, the following are true:

    111111 meets these criteria (double 11, never decreases).
    223450 does not meet these criteria (decreasing pair of digits 50).
    123789 does not meet these criteria (no double).

How many different passwords within the range given in your puzzle input meet these criteria?
"""

import re

with open("input/day4.txt") as input_file:
    [low, high] = [int(x) for x in input_file.readline().split("-")]


# part 1: 

# check for double digits
pattern = r"(\d)\1"

# check if two digits are increasing or the same; the higher digits will have a higher ordenance
# print(ord("1"))
# print(ord("9"))
# Another way to check this is sorting, which might be faster but definitely looks cleaner
# if the number as a list is the same as its sorted string, the digits are all increasing.
# print(sorted(str(124789)) == ([x for x in str(124789)]))


def part_1():
    total = 0
    for i in range(low, high+1):
        match = re.search(pattern, str(i))
        if match:
            if ([x for x in str(i)] == sorted(str(i))):
                total += 1
    return total

print(part_1())

"""
--- Part Two ---

An Elf just remembered one more important detail: the two adjacent matching digits are not part of a larger group of matching digits.

Given this additional criterion, but still ignoring the range rule, the following are now true:

    112233 meets these criteria because the digits never decrease and all repeated digits are exactly two digits long.
    123444 no longer meets the criteria (the repeated 44 is part of a larger group of 444).
    111122 meets the criteria (even though 1 is repeated more than twice, it still contains a double 22).

How many different passwords within the range given in your puzzle input meet all of the criteria?
"""

# part 2 is similar to part 1, but with an extra condition.
# I'll simply add a pattern that checks for 3 or more of the same digits
pattern_2 = r"(\d)(\1){2,}"
# the next step is to see if the two patterns overlap
# if at least 1 match on the first pattern does not overlap with a match on the second pattern, that is still OK

def part_2():
    total = 0
    for i in range(low, high+1):
        match = re.search(pattern, str(i))
        if match:
            # Check if one digit is in the string exactly twice
            if 2 in [str(i).count(digit) for digit in str(i)]:
                if ([x for x in str(i)] == sorted(str(i))):
                    total += 1

    return total

print(part_2())