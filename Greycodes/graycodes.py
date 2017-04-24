"""
@author: Sol Jennings 26356015
@created: 2016-05-14
@description:

Given a parameter n, enumerates all subsets of a set containing n elements in the order prescribed


usage:
python task3.py [n]

"""
import string

import sys


def generate_gray_code(n):
    """
    Generates all of the gray codes of size n

    It does this by converting unsigned binary numbers using bitwise operators

    >> shift right
    ^ XOR

    Time complexity:
    = O(2^n)

    :param n: the number of sets to create
    :return: a list of all of the grey codes in order
    """
    list = []
    for i in range(2 ** n):
        list.append(i ^ (i >> 1))
    return list


def generate_set(codes):
    # set = []
    """
    Generates a set from the gray codes as positions

    for example

    000=  []
    001 = [a]
    011 = [ab]

    The bit position determines whether the character form lowercase ascii should be in the set or not

    This is done using bitwise operations on each of the grey codes to determine whether a character should exist in
    the set

    Time complexity:
    O(codes)

    :param codes: binary code to generate each permutations from
    """
    for i in codes:
        next_set = []
        letter = 0
        while i > 0:
            if i & 1:
                next_set.append(string.ascii_lowercase[letter])
            i >>= 1
            letter += 1
        print(str(next_set))
        # set.append(next_set)
        # return set


def main():
    if len(sys.argv) != 2:
        print("Invalid number of arguments")
        exit()
    try:
        n = int(sys.argv[1])
    except ValueError:
        print("Invalid arguments")
    try:
        generate_set(generate_gray_code(n))
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()


"""

my current best evaluations:


3. Space

O(2^|N|) where n is the number of elements
"""
