# Genome and Radix Sort

This program operates in 2 parts<br>

1. generateKmers.py takes a text file of a genetic genome and produces a kmer file representing it<br>
2. radixLSD.py sorts the genome using a radix sort and outputs it into a file

This program can be used to find similar genetic sequences within a genetic string

Example Output
--
<code>python generateKmers.py 16 generateKmers.py exampleKmerFile.txt</code>
<pre>
Generating from generateKmers.py with window size 16...
kmer file exampleKmerFile.txt created!
</pre>

<code>python radixLSD.py "example output\exampleKmerFile.txt"</code>
<pre>
Reading in kmer file
Sorting kmer file using radix LSD sort...
Sorting with window size:  16
Sorting pass: 4
Sorting pass: 3
Sorting pass: 2
Sorting pass: 1
Creating sorted kmer file
kmer file kmers_sorted.txt created!
</pre>

# Complexities

Time complexity (n is number of genome segments, k is the length of those segments):<br>
O(n * k)<br>


