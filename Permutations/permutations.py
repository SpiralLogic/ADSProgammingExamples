"""
@author: Sol Jennings 26356015
@created: 2016-03-14
@Description: FIT2004 Prac 4 (Assignment 1)
"""
import string


def factorial(N):
    """
    :param N: The number to find the factorial of
    :return: The result
    """
    if N <= 0:
        return 1
    return N * factorial(N - 1)


def sumOfN(N):
    """
    Sum of N
    :param N: the integer to start summing from
    :return: summation
    """
    if N == 0:
        return 0
    return N + sumOfN(N - 1)


def permute(N):
    """
    Find the permutations for a given et of N elements and outputs the information to a file
    The information in the output will include
    The number of permutations
    the base_10, base_1, sum and permutation for each N!
    A frequency table for the sum of the base_! digits
    The weighted average of the frequencies

    :param N: The size of the set of elements

    """
    filename = "fit2004_lab4_output.txt"

    # So some basic validation
    try:
        N = int(N)
    except ValueError:
        raise ValueError("N must be an integer")
    if N < 0:
        raise ValueError("N must be greater than 0")

    # a list to store the sums of the digits
    digit_sums = []

    # a list to store the frequency of each digit sum
    frequency = []

    fact_N = factorial(N)

    # create a list of all the factorials of each digit so this
    # doesn't need to be generated many times
    digit_factorials = []
    for i in range(N - 1, -1, -1):
        digit_factorials.append(factorial(i))

    output_file = open(filename, "w")
    output_file.write("INPUT TO THE SCRIPT: N = " + str(N) + "\n")
    output_file.write("TOTAL NUMBER OF PERMUTATIONS = " + str(fact_N) + "\n")
    output_file.write("Base-10\tBase-!\tsum\tpermutation\n")

    # Iterate through all the permutations of N
    for i in range(fact_N):
        digit_sum = 0
        remainder = i
        perm = []

        # Convert from Base_10 to Base_!
        for j in digit_factorials:
            perm.append(remainder // j)
            remainder = remainder % j

        letters = list(string.ascii_lowercase[:N])
        string_perm = ""

        # Create the string from the Base_!
        for j in perm:
            digit = int(j)
            digit_sum += digit
            string_perm += letters.pop(digit)

        # Add the frequency to the frequency list
        try:
            frequency[digit_sum] += 1
        except IndexError:
            frequency.append(1)
        digit_sums.append(digit_sum)

        # turn the permutation into a string
        perm = "".join(str(x) for x in perm)

        output_file.write(
            "(" + str(i) + ")_10\t(" + perm + ")_!\t" + str(digit_sum) + "\t" + string_perm + "\n")

    # calculate the wreighted average for the frequency of the sums
    weight_average = sum(digit_sums) / len(digit_sums)

    # Output the calculated information to the output file
    output_file.write("\nFREQUENCY TABLE\n")
    output_file.write("-------------------\n")
    output_file.write("SUM\tFREQ.\n")
    for i in range(len(frequency)):
        output_file.write(str(i) + "\t" + str(frequency[i]) + "\n")
    output_file.write("Weighted average of sum = " + str(weight_average))
    output_file.close()
    print("Output written to: " + filename)


def min_trans(str1, str2):
    """
    Find the minimum transpositions needed to get from one string to another
    This uses the base_! number systems to calculate the transpositions. It will  work out
    where lexicographically each letter in str2 is compared to str1. And then use
    sum these base_! digits to find the minimum transpositions.

    :param str1: The first string
    :param str2: The second string
    :return: The minimum number of transpositions needed
    """
    if not str1.isalnum() or not str2.isalnum():
        print("Strings must be alphanumeric")
        return
    if len(str1) != len(str2):
        print("Lengths of string must be the same")
        return

    # create a list of available letters from the first string
    str1_letter_list = []
    for i in str(str1):
        str1_letter_list.append(i)
    number = 0
    for i in str(str2):
        try:
            # sum the positions of each letter in string2 compared to string1
            indx = str1_letter_list.index(i)
            number += indx
            # remove this letter from the list
            str1_letter_list.pop(indx)
        except ValueError:
            print("Strings are not the same composition of letters")
            return
    print("Number of swaps from " + str1 + " to " + str2 + ": " + str(number))


if __name__ == "__main__":
    """
    Menu when the program starts
    """
    print("1. Calculate permutations for a given N")
    print("2. Calculate the minimum transpositions between 2 strings")
    choice = input("Selection: ")
    if choice == "1":
        n = input("N: ")
        permute(n)
    elif choice == "2":
        string1 = input("String 1: ")
        string2 = input("String 2: ")
        min_trans(string1, string2)
    else:
        print("Incorrect or no option chosen")
        exit()

"""


D)
The weighted average is growing asymptotically as a function N^2

mathematically, the weighted average is half of the maximum. This is because the frequency is
normally distributed.
therefore

=(1/2)(N(N-1)/2)
= N(N-1)/4
= N^2/4 - N/4
=(1/4)(N^2 - N)

Therefore the weighted average is (1/4)(N^2 - N)

Which as a time complexity is O(N^2)

E)
The growth is the same as the time complexity of insertion sort, specifically the average case

We are working out sorting a list of elements of all possible permutations. Therefore
when we work out the weighted average we are working out the total number of transpositions
required for each permutation to be created from the sorted set of elements. Essentially
this is taking a sorted list and unsorting it to a specific permutation (or redefining what sorted
is).

This includes the best case of already sorted case  where "abcd" is sorted to "abcd"
which requires 0 inversions. This would have O(N) time complexity (Each N element is already
in the correct place)

It also includes the worst case of sorting over a set of elements that requires the
maximum number of inversions of N(N-1)/2. The example is the case "abcd" being sorted to "dcba"
This would have O(N^2) complexity.

As a result we are working out the average swaps of for every possible arrangement
of N! elements and we are transposing a sorted arrangement to be an out of order for each permutation.
By out of order we mean the elements of the set abcd are required to be in a new arrangement
with each new permutation and are sorted to this new permutation.
Because each elements new position is reached by swapping with the previous elements and the
beginning of the list remains sorted. this is equivalent to insertion sort.

Here a demonstration of the sort is shown, each desired element is swapped according to the
base_! permutation to it's correct position.

abcd -> acbd -> cabd -> cbad -> cbda
****    ****    -***    --**    ----

* shows the part of the list still unsorted
- shows thw part of the list that is now sorted


The weighted average of the transpositions will be the average case of sorting via insertion sort.
This is because we are determining the weighted average for all permutations of N!.

The other possibilities were bubble sort and selection sort. I will explain why I believe these
sorts aren't correct even though they have the same average O(N^2) and worst case O(N^2). With
 bubble sort having the same best case O(N)


It is not bubble sort because:
Bubble sort would swap each element in turn until the correct element was at the end of the list
then repeat this processes for all elements.

For example abcd -> cbda:

abcd -> bacd -> bcad -> bcda -> cbda
        **       **       **    **

* - the two elements swapped in each step

It is not selection sort because:
We would be selecting the next element and then swapping it into the correct place without
any intermediate steps

For example for cbda:

abcd -> cbad -> cbad -> cbda -> cbda
        * *      *        **       *

* - the two elements swapped in each step, (if only one * then the element was already in the correct
    place)


Therefore selection sort best describes the sort that is happening as each element that is needed
chosen by the permutation and then swapped until it is in it's correct place

For example for cbda:
abcd -> acbd -> cabd -> cbad -> cbda
         **     **       **       **

* - the two elements swapped in each step

Therefore selection sort best describes process of making swaps until an element is in the
correct position.



F)
N(N-1)/2, it is the sum of digits of the maximum transpositions in base_!

Therefore the range is [0, N(N-1)/2]


"""
