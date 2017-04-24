"""
@author: Sol Jennings 26356015
@created: 2016-05-14
@description:

Will read in a give file of strings and then from this file perform computation depending on the
option chosen

Find and print all the vertices in the largest partition
python task1.py [filename]

Print the connected components
python task1.py [filename] -cc

Find and print the partitions and all their vertices
python task1.py [filename] -p

Find and print the vertices and edges
python task1.py [filename] -v

Find the distance between 2 words
python task1.py [filename] [word1] [word2]

"""
import sys, timeit


class Vertex:
    def __init__(self, word):
        """
        Vertex class for storing a vertex
        :param word: the word the vertex represents
        """
        self.word = word
        self.edges = set()
        self.partition = None

    def add_edge(self, vertex):
        """
        Add an edge to the vertex
        :param vertex: the vertex edge to add
        """
        if vertex is self:
            return
        if not isinstance(vertex, Vertex):
            raise TypeError("Cannot add an edge that isn't another Vertex")
        self.edges.add(vertex)

    def rotate_word(self):
        """
        Rotate the vertex word cylindrically, this is used in finding the edges
        e.g. word becomes ordw
        """
        self.word = self.word[-1] + self.word[:-1]

    def max_distance(self):
        """
        :return: the distance of the furthest Vertex to this Vertex
        """
        return self.distance(None)

    def distance(self, word_to_find=None):
        """
        Uses a BFS to find the distance from this vertex to another vertex word connected to the vertex
        If no word to find is provided then the distance to the furthest word is returned

        Each vertex needs have each of it's edges scanned this makes the
        Time complexity is O(|V| + |E|)

        :param word_to_find: the word to find
        :return: the distance to the word to find, -1 if the word was not found
        """
        Q = []  # Queue of all vertices in the set V
        dist = {}  # distances stored in python hashmap for O(1) lookup
        max_distance = -1
        visited = set()  # already visited vertices are stored in a python set for O(1) lookup
        dist[self.word] = 0  # distance form vertex to itself is 0
        Q.append(self)
        visited.add(self)
        while len(Q):
            x = Q.pop(0)
            for y in x.edges:
                if word_to_find is not None and y.word == word_to_find:
                    return dist[x.word] + 1

                if y not in visited:  # O(1) lookup provided by pythons sets
                    # O(1) lookup provided by pythons dictionary dictionary as hashmap
                    distance = dist[x.word] + 1
                    dist[y.word] = distance  # O(1) insert provided by python dictionary as hashmap

                    if distance > max_distance:
                        max_distance = distance

                    Q.append(y)
                    visited.add(y)  # O(1) insert provided by python set

        if word_to_find is not None:
            return -1
        return max_distance

    def __lt__(self, vertex):
        """
        Allow comparison for vertices, this is used in sorting

        :param vertex: vertex to compared
        :return: True this vertex is less than the vertex compared to
        """
        if not isinstance(vertex, Vertex):
            raise TypeError("Can only compare Vertex to Vertex")
        return self.word < vertex.word

    def __len__(self):
        """
        :return: The length of the vertex word
        """
        return len(self.word)

    def __str__(self):
        """
        :return: representation the vertex and all it's edges as a string
        """
        string = self.word + ": "
        for edge in self.edges:
            string += edge.word + ", "
        return string


class Partition:
    def __init__(self, number):
        """
        Partition class for storing vertex partitions
        :param number: partition number/name
        """
        self.vertices = []
        self.number = number
        self.diameter = None

    def add_vertex(self, vertex):
        """
        Add a vertex to the partition
        :param vertex:
        """
        if not isinstance(vertex, Vertex):
            raise TypeError("Can only add vertices to partitions")
        self.vertices.append(vertex)
        self.diameter = None

    def find_diameter(self):
        """
        Find the diameter of the partition

        Requires searching all of the vertices in the partition for their maximum distance to their furthest word
        in the partition.

        O(|V| * find_max_distance)
        = O(|V| * (|V| + |E|))
        = O(|V|^2 + |V||E|) it is possible for there to be an edge from every vertex to each other making |E|=|V|^2
        =O(|V|^3) in the worst case

        :return: the diameter of this partition
        """
        if self.diameter is not None:
            return self.diameter
        diameter = 0
        for j in self.vertices:
            distance = j.max_distance()
            if distance > diameter:
                diameter = distance
        self.diameter = diameter
        return self.diameter

    def __len__(self):
        """
        :return: the number of vertices in this partition
        """
        return len(self.vertices)

    def __str__(self):
        """
        :return: The total number of words in this partition and what each word is
        """
        string = "Partition " + str(self.number) + " has total words " + str(len(self)) + ": "
        for i in self.vertices:
            string += i.word + ", "
        return string


class Graph:
    def __init__(self):
        """
        Graph class to store a graphs vertices and partitions
        """
        self.vertices = []
        self.partitions = []
        self.largest_partition = None

    def read_file(self, filename):
        """
        Read a text file of strings and create vertices and edges for the graph
        :param filename: name of the file to read
        """
        word_length = None
        print("Reading file...")
        with open(filename, "r") as file:
            for line in file:
                word = Vertex(line.rstrip("\n"))

                if word_length is None:
                    word_length = len(word)

                if len(word) != word_length:
                    raise ValueError("Strings not all of the same size")

                self.vertices.append(word)

        print("Finding edges...")
        self.find_edges()

    def find_edges(self):
        """
        Find all of the edges for all of the vertices in the graph.
        Still has the same time complexity as comparing every vertex but this will only happen
        in the case when there is |V|^2 edges.

        This is done in the following way.
        1. First the list of words is sorted (using merge sort)
        2. An edge is added between every word that differs only by the last letter
        3. Each word is rotated cyclically. eg "word" becomes "dwor"
        4. Repeat step 1-3 for the lengths of the words

        Worst case Time complexity is:
        O(length_of_word * (sorting + finding edges))
        O(length_of_word * (|V|log|V| + |V|^2))
        O(|V|log|V| + |V|^2)
        O(|V|^2)

        Best Case is (there are no edges):
        O(length_of_word * (sorting + finding edges))
        O(length_of_word * (sorting))
        O(length_of_word * sorting)
        O(NlogN)
        """
        word_len = len(self.vertices[0].word)
        for _ in range(word_len):
            # self.vertices.sort(key=lambda vertex: vertex.word)
            merge_sort(self.vertices)
            edge_set = [self.vertices[0]]
            for i in range(1, len(self.vertices)):

                if self.vertices[i - 1].word[:word_len - 1] == self.vertices[i].word[:word_len - 1]:
                    edge_set.append(self.vertices[i])

                else:
                    self.addEdgeSet(edge_set)
                    edge_set = [self.vertices[i]]

            self.addEdgeSet(edge_set)

            for i in range(len(self.vertices)):
                self.vertices[i].rotate_word()

    def addEdgeSet(self, edge_set):
        """
        links a set of words together

        :param edge_set: the set of edges to link together
        :return:
        """
        if len(edge_set) == 1:
            return
        while len(edge_set):
            word1 = edge_set.pop(0)
            for word2 in edge_set:
                word1.add_edge(word2)
                word2.add_edge(word1)

    def assign_partitions(self):
        """
        Assign each of the vertices to a partition
        This is done in the following way:

        1. Find the first unpartitioned vertex
        2. From this vertex use BFS to find all vertices connected to it and assign them to the
        same partition
        3. repeat 1-2 until every vertex is assigned a partition

        Time complexity is:
        = O(BFS + time_to_find_unpartitioned)
        = O((|V| + |E|) + |V|)
        = O(|V| + |E|)

        """
        print("Assigning partitions...")
        num_to_partition = len(self.vertices)
        self.partitions = []

        # a python set is used to keep track of when each vertex is assigned a partition
        partitioned = set()
        start = self.vertices[0]
        start.partition = len(self.partitions)
        Q = [start]
        partitioned.add(start)
        current_partition = Partition(len(self.partitions))
        current_partition.add_vertex(start)

        # while there are still unpartitioned vertices
        while num_to_partition:
            while len(Q):  # BFS to find all vertices attached
                vertex = Q.pop(0)
                for edge in vertex.edges:
                    if edge not in partitioned:
                        edge.partition = len(self.partitions)
                        partitioned.add(edge)
                        current_partition.add_vertex(edge)
                        Q.append(edge)
                        num_to_partition -= 1

            # BFS done partition is complete, add it to the partition list
            self.partitions.append(current_partition)

            # find the next unpartitioned vertex
            next_vertex = self.find_next_unpartitioned()
            if next_vertex is None:
                break
            # create a new partition for this set of vertices
            current_partition = Partition(len(self.partitions))
            current_partition.add_vertex(next_vertex)
            Q.append(next_vertex)
            partitioned.add(next_vertex)
            next_vertex.partition = len(self.partitions)

    def find_next_unpartitioned(self):
        """
        :return: the next vertex which has not been assigned to a partition
        """
        for v in self.vertices:
            if v.partition is None:
                return v
        return None

    def word_distance(self, word1, word2):
        """
        Finds the distance between 2 words
        :param word1: word to start from
        :param word2: word to find distance to
        """
        word1_vertex = None
        for i in range(len(self.vertices)):
            if self.vertices[i].word == word1:
                word1_vertex = self.vertices[i]
                break
        if word1_vertex is None:
            raise ValueError(word1, " not in vertex list")

        distance = word1_vertex.distance(word2)
        if distance == -1:
            print(word2, "cannot be reached from", word1)
        else:
            print("Distance from", word1, "to", word2, ":", distance)

    def find_largest_diameter(self):
        """
        Find the partition with the largest diameter

        Time complexity:
        = O(|P| * find_partition_diameter)
        = O(|P| * |V|^3)
        """
        print("Finding largest partition diameter")
        largest_partition = None
        for partition in self.partitions:
            # skip any partitions that have less vertices than the largest current diameter as they won't have
            # a diameter larger
            if largest_partition is not None and len(
                    partition.vertices) - 1 <= largest_partition.diameter:
                continue
            diameter = partition.find_diameter()
            print("partition ", partition.number, "has diameter", diameter)
            if largest_partition is None:
                largest_partition = partition
            elif diameter > largest_partition.diameter:
                largest_partition = partition
        self.largest_partition = largest_partition
        return largest_partition

    def print_partitions(self):
        """
        Print all of the partitions in the graph
        """
        print("Number of partitions: ", len(self.partitions))
        for i in self.partitions:
            print(i)

    def print_vertices(self):
        """
        Print all of the vertices in the graph
        """
        for vertex in self.vertices:
            print(vertex)


def merge_sort(a_list):
    """
    Merge sort

    Time complexity:
    = O(merge * split)
    = O(|N| * log|N|)
    = O(|N|log|N|)

    :param a_list: list to sort
    """
    if len(a_list) > 1:
        mid = len(a_list) // 2
        left = a_list[:mid]
        right = a_list[mid:]

        merge_sort(left)
        merge_sort(right)
        i, j, k = 0, 0, 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                a_list[k] = left[i]
                i += 1
            else:
                a_list[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            a_list[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            a_list[k] = right[j]
            j += 1
            k += 1


def main():
    if len(sys.argv) == 1:
        print("Not enough arguments")
        exit()
    filename, word1, word2 = None, None, None
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    if len(sys.argv) == 3 or len(sys.argv) == 4:
        word1 = sys.argv[2]
    if len(sys.argv) == 4:
        word2 = sys.argv[3]
    g = Graph()
    try:

        g.read_file(filename)
        t1 = timeit.default_timer()
        g.find_edges()
        t2 = timeit.default_timer()
        print("Time to find edges ", t2 - t1)
    except IOError:
        print("File", filename, "could not be read")
        exit()
    except ValueError as e:
        print(e)
        exit()
    try:
        if word1 and word2:
            g.word_distance(word1, word2)
        elif word1 == '-cc':
            g.assign_partitions()
            print("There are", len(g.partitions), "partitions")
        elif word1 == '-p':
            g.assign_partitions()
            g.print_partitions()
        elif word1 == '-v':
            g.print_vertices()
        else:
            g.assign_partitions()
            t1 = timeit.default_timer()
            largest_partition = g.find_largest_diameter()
            t2 = timeit.default_timer()
            print(largest_partition)
            print("Largest partition is", largest_partition.number, "has diameter",
                  largest_partition.diameter)
            print("and has", len(largest_partition), 'vertices')
            print("with a time to find of", t2 - t1)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
