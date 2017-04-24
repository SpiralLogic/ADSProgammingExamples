# Partitions

This program takes a dictionary of 5 letter words and then partitions those words depending
on whether they can be reach one another in the following way:

Words are linked when they differ only by one letter:

house -> mouse -> moose -> loose

## Definitions
Partition: group of words that can reach each other
Vertex: a word in a partiton
Connected Components: How many partitions were found from the dictionary file

## Several options are available

Find and print all the vertices in the largest partition<br>
python task1.py [filename]

Print the connected components<br>
python task1.py [filename] -cc

Find and print the partitions and all their vertices<br>
python task1.py [filename] -p

Find and print the vertices and edges<br>
python task1.py [filename] -v

Find the distance between 2 words<br>
python task1.py [filename] [word1] [word2]