# Permutations

Creates a permutation of a given set of letters.

The permutation will find each possible permutation of the set of letters and list them in order such that only one letter changes with each permutation.
A second option on input is to calculate the minimum transpositions between strings
i.e<br>
abcd<br>
abdc<br>
acbd<br>
acdb <br>

etc.

A Factorial based number system is used to achieve this

Permutations Example
--
<code>python permutations.py</code>
<pre>1. Calculate permutations for a given N
2. Calculate the minimum transpositions between 2 strings
Selection: 1
N: 6
Output written to: permutations.txt
</pre>

Transpositions Example
--
<code>python permutations.py</code>
<pre>1. Calculate permutations for a given N
2. Calculate the minimum transpositions between 2 strings
Selection: 2
String 1: stuff
String 2: ftufs
Number of swaps from stuff to ftufs: 6
</pre>

# Other Information

###### How is this weighted average growing asymptotically as a function of N? Justify your answer with a clear reasoning.
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

###### This growth informs the complexity of a certain sorting algorithm we discussed specifically in weeks 2 and 3. Which one and what case – Best, Average or Worst?


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

<pre>
abcd -> acbd -> cabd -> cbad -> cbda
****    ****    -***    --**    ----

* shows the part of the list still unsorted
- shows thw part of the list that is now sorted
</pre>


The weighted average of the transpositions will be the average case of sorting via insertion sort.
This is because we are determining the weighted average for all permutations of N!.

The other possibilities were bubble sort and selection sort. I will explain why I believe these
sorts aren't correct even though they have the same average O(N^2) and worst case O(N^2). With
 bubble sort having the same best case O(N)


It is not bubble sort because:
Bubble sort would swap each element in turn until the correct element was at the end of the list
then repeat this processes for all elements.

For example abcd -> cbda:

<pre>
abcd -> bacd -> bcad -> bcda -> cbda
        **       **       **    **

* - the two elements swapped in each step
</pre>

It is not selection sort because:
We would be selecting the next element and then swapping it into the correct place without
any intermediate steps

For example for cbda:
<pre>
abcd -> cbad -> cbad -> cbda -> cbda
        * *      *        **       *

* - the two elements swapped in each step, (if only one * then the element was already in the correct
    place)
</pre>

Therefore selection sort best describes the sort that is happening as each element that is needed
chosen by the permutation and then swapped until it is in it's correct place

For example for cbda:
<pre>

abcd -> acbd -> cabd -> cbad -> cbda
         **     **       **       **

* - the two elements swapped in each step
</pre>

Therefore selection sort best describes process of making swaps until an element is in the
correct position.


###### For any arbitrary N, what range of values does the sum of the base-! digits take? Why?

N(N-1)/2, it is the sum of digits of the maximum transpositions in base_!

Therefore the range is [0, N(N-1)/2]
