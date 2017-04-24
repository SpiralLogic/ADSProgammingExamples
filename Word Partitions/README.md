# Partitions

This program takes a dictionary of words with the same number of letters and then partitions those words depending
on whether they can be reach one another in the following way:

Words are linked when they differ only by one letter:

house -> mouse -> moose -> loose

## Definitions
Partition: group of words that can reach each other<br>
Vertex: a word in a partiton<br>
Connected Components: How many partitions were found from the dictionary file<br>

## Several options are available

Find and print all the vertices in the largest partition<br>
python permutations.py [filename]

Print the connected components<br>
python permutations.py [filename] -cc

Find and print the partitions and all their vertices<br>
python permutations.py [filename] -p

Find and print the vertices and edges<br>
python permutations.py [filename] -v

Find the distance between 2 words<br>
python permutations.py [filename] [word1] [word2]

# Complexities

Space Complexity of distance between any 2 given vertex:<br>
O(|V| +|E|)

Space complexity of partitions:<br>
O(|V| + |P| + |E|)

Space for finding diameter of the partitions:<br>
O(|V| + |E| + |P|)
