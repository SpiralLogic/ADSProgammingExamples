# Eularian Circuit

This program takes an input of strings  of the same length and finds a eularian ciruit that connects them all
two strings are connected when the end of one string is the lame as the start of another

For example, these strings are connected (- is not part of the string):

Some Str---<br>
-ome Stri--<br>
--me Strin-<br>
---e String<br>

The output is the reconstruction of all of the strings from the input file

i.e.
Some Str
ome Stri
me Strin
e String

becomes: 
Some String


#### Example
python ecicuit.py substrings1.txt 

# Complexities

Space complexity of vertices:
------------------------------

O(|V|) space is used to store each vertex and it's associated string
O(|E|) space is used to store each of the edges in a linked list where each index of the list
represents the vertex number

Total space used: O(|V| + |E|)

if the graph is sparse and |V| > |E| then space complexity will be O(|V|)

if the graph is dense and |E| > |V| then space complexity will be O(|E|)

Time complexity of generating graph
-----------------------------------

Using a known property of the graph being a De Bruijn graph we know that each vertex will have
M edges. Using this property vertices can be generated in O(|V| * m) time. This is done by
sorting the vertices or in the case of this implementation, generate the vertices already
sorted.

For graphs that aren't De Bruijn then graph generation will take O(|V|^2) complexity. For example
when loading from a string file.



Time complexity of finding the circuit
--------------------------------------

Time complexity of finding the circuit is O(|E| * checking for disconnect)

I am using a BFS to detect a disconnect each time there are more than 2 edges for a
vertex. This checking for disconnect takes O(|V| + |E|) as we need to go to each vertex
and need to go to each edge.

This makes my total complexity
O(|E| * (|V| + |E|))
= O(|V||E| + |E|^2)
= O(|E|^2)              (if |V| == |E| then, O(2|E|^2) which is still O(|E|^2)

If there was only 1 edge per vertex then the BFS would never occur. Which allows us to assume
that |V| < |E| as each vertex would then have less than 2 edges. If there was only 1 edge per vertex
then time complexity would be O(|E|) as checking for a disconnect would never occur (giving it
a time complexity of O(1)).


If I was more ambitious and actually finished implementing Trajan's algorithm then I could work out
the bridges in advanced to make checking for a disconnect possible in O(1).

Space complexity of finding the circuit
--------------------------------------

Space complexity for finding e-circuit
O(|V| + |E|)

When finding the disconnects via BFS it will only add 1 extra copy of O(|V|+|E|) so the
space complexity will not change while searching
"""

