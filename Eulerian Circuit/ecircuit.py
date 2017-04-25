"""
@author: Sol Jennings 26356015
@created: 2016-05-03
@description:

Works out the e-circuit for a string file or will generate a de bruijn graph and find an e-circuit
from a random vertex

Usage:

File Version:
ecircuit.py [filename]

De Bruijn
ecircuit.py [N] [M] [Start Vertex]

"""
import random
import string
import sys


# import timeit


class Vertex:
    def __init__(self, name):
        """
        Initialise a vertex
        :param name: Name of the vertex
        """
        self.name = name
        # counts how many incoming edges each node has
        self.incoming = 0

    def __str__(self):
        """
        Convert the vertex to a string representing its name, edges and incoming edge count
        :return:
        """
        return self.name


class Graph:
    def __init__(self):
        # the graph is stored as an adjacency list

        # stores the edges join vertices
        self.edges = []
        # stores the vertices so that their node value can be looked up later
        self.vertices = []
        # stores the graphs total edge count
        self.edge_count = 0

    def addVertex(self, vertex):
        """
        insert a vertex into the graph
        :param vertex: vertex name to insert
        """
        vertex = Vertex(vertex)
        self.vertices.append(vertex)
        self.edges.append([])

    def addEdge(self, vertex_from, vertex_to):
        """
        add an edge between 2 vertices
        :param vertex_from: the from vertex
        :param vertex_to:  the to vertex
        """
        # if this edge is a loop, add it to the start to make life easier later
        if vertex_from == vertex_to:
            self.edges[vertex_from] = [vertex_to] + self.edges[vertex_from]
        else:
            self.edges[vertex_from].append(vertex_to)
        # add to the total number of edges
        self.edge_count += 1
        self.vertices[vertex_to].incoming += 1

    def removeEdge(self, vertex_from, vertex_to):
        """
        remove an edge from the graph
        :param vertex_from: from vertex
        :param vertex_to: to vertex
        """
        self.edges[vertex_from].remove(vertex_to)


class Dgraph:
    def __init__(self):
        """
        initialise a dgraph
        """
        self.graph = Graph()
        self.e_circuit = None
        self.n = None
        self.m = None

    def create_vertices(self, n, m):
        """
        Get the permutations for the graph with an alphabet of size m and length of size n
        and create a Vertex for each permutation
        :param n: length
        :param m: alphabet size
        """
        print("Creating Vertices...")
        self.n = n
        self.m = m
        if m > 4 or m < 2:
            raise ValueError("M must be between 2 and 4")
        if n > 7 or n < 2:
            raise ValueError("N must be between 2 and 7")
        for i in self.vertex_generator(n, m):
            self.graph.addVertex(i)

    def vertex_generator(self, n, m):
        """
        generator to create each permutation of length n from the alphabet
        :param n: length
        :param m: alphabet size
        """
        alphabet = string.ascii_uppercase[:m]
        final = list(alphabet)
        for _ in range(n - 1):
            new_final = []
            for j in alphabet:
                for k in final:
                    new_final.append(j + k)
            final = new_final
        for i in final:
            yield i

    def create_edges(self):
        """
        generate the graph from the vertices. For each vertex when a new edge is found
        the number of vertices for that edge is increased
        Complexity: O(|V| * M)
        """
        print("Creating Edges...")
        current_position = 0
        total_vertices = len(self.graph.vertices)

        # for every vertex we know that it will have M edges based on a de bruijn graph
        # as these vertices are generated in alphabetical order we know the edges will occur in
        # order
        for i in range(total_vertices):
            new_position = current_position + self.m

            # do this to keep self edges at the start of the edge list
            for j in range(current_position, new_position):
                self.graph.addEdge(i, j)
            # we have reached the end of the list so restart the first position
            # tried to do this with a % but was always missing last vertex -.-
            if new_position == total_vertices:
                new_position = 0
            current_position = new_position

    def find_e_circuit(self, start=None):
        """
        Find the e-circuit for the graph starting from the vertex start
        if no start is supplied a random one will be chosen

        complexity for this is O(|E| * checking for disconnect)
        O(|E| * (|V| + |E|)) = O(|V||E| + |E|^2) = O(|E|^2)

        :param start: starting vertex
        """
        print("Finding circuit...")
        num_vertices = len(self.graph.vertices)
        if start is None:
            start = random.randint(0, num_vertices - 1)
        if start >= num_vertices:
            raise IndexError("Cannot start from vertex that doesn't exist")

        # how many vertices left to traverse
        edges_left = self.graph.edge_count
        vertices_left = num_vertices

        # starting vertex
        # list of edge transitions
        e_circuit = [start]
        u = start

        while True:
            num_edges_in_u = len(self.graph.edges[u])
            # store this to avoid looking up u in a list every time
            edges_in_u = self.graph.edges[u]
            if num_edges_in_u == 0:
                """
                the vertex u has no outgoing edges and all the edges in the graph have been visited:
                In this case TERMINATE the algorithm by printing “E-circuit found!” followed
                by the edges involved in the E-circuit.
                """
                if edges_left == 0:
                    print("E-circuit found!")
                    break
                """
                the vertex u has no outgoing edges, but there are still other untraversed edges
                remaining in the graph G: In this case, TERMINATE the algorithm by printing
                “E-circuit not found!”
                """
                if edges_left > 0:
                    print('E-circuit not found!')
                    break
            """
            the vertex u has exactly one outgoing edge: In this case, call the vertex at the
            other end of this edge as v. Traverse along this edge and add it to the current
            state of E-circuit. This will make v the current vertex. Then delete the edge
            (i.e., mark it as traversed) giving you a modified graph without/ignoring this edge.
            Furthermore, upon deletion of this edge, if u becomes disconnected∗
            in this modified graph, then delete the vertex u as well.
            """
            if num_edges_in_u == 1:
                v = edges_in_u.pop(0)

            """
            the vertex u has two or more outgoing edges: traverse along ANY of its outgoing
            edges under the constraint that the chosen edge hu, vi, when deleted from the current
            state of the graph, does NOT disconnect the vertex v. (If none of the outgoing edges
            at u satisfy this constraint, then there is no choice but to pick any one outgoing
            edge at u and traverse.) After traversal, v becomes the current vertex.
            """
            if num_edges_in_u > 1:
                # if the node has an edge to itself, use this first
                if edges_in_u[0] == u:
                    v = edges_in_u.pop(0)
                else:
                    # find next edge that doesn't result in a disconnect
                    i = 0
                    while i < num_edges_in_u:
                        # pop first edge off edge list this is O(1) for a linked list
                        v = edges_in_u.pop(0)

                        # we have reached the last edge so we will use this no matter what
                        if i == num_edges_in_u - 1:
                            break

                        # skip any nodes which have no outgoing edges
                        if len(self.graph.edges[v]) == 0:
                            i += 1
                            edges_in_u.append(v)
                            continue
                        # make sure the node we came from is still accessible
                        connected = self.still_connected(v, u, vertices_left)

                        # a disconnect and we can use this edge
                        if connected:
                            break
                        else:
                            # put the edge back at the end of the edge list
                            # this is O(1) for a linked list
                            edges_in_u.append(v)
                        i += 1

            # add the edge to the e-circuit
            e_circuit.append(v)
            edges_left -= 1
            u = v

            # decrease incoming edges of the new u
            self.graph.vertices[u].incoming -= 1
            # if there are no more incoming for u then it has been fully traversed
            if self.graph.vertices[u].incoming == 0:
                vertices_left -= 1
        self.e_circuit = e_circuit

    def print_e_circuit(self):
        """
        print the e-circuit for this graph
        """
        if self.e_circuit is None:
            self.find_e_circuit()
        string1 = ""
        for i in self.e_circuit:
            string1 += self.graph.vertices[i].name[0]
        print(self.e_circuit)
        print(string1 + self.graph.vertices[i].name[1:])

    def still_connected(self, u, return_vertex, vertices_left):
        """
        Perform a BFS to find if removing the edge has disconnected the vertex
        we came from
        Time complexity is O(|V|+|E|)
        :param u: node to start search from
        :param return_vertex: vertex we need to be able to return to
        :param vertices_left: number of vertices left in e-circuit
        :return: how many vertices were reachable
        """
        edges = []
        # need to create a deep copy of the list so python doesnt fuck my shit up
        # also set up a list to track the vertices that can be reached
        # sorry for the swearing
        # O(|V|+|E|)
        v_reachable = []
        for i in self.graph.edges:
            edges.append(list(i))
            v_reachable.append(False)
        to_travel = edges[u]
        # the node we are currently on is always reachable
        v_reachable[u] = True
        count = 1
        # while there are still edges to travel
        # O(|E|)
        while len(to_travel) and count < vertices_left:
            # remove a node from the queue
            edge = to_travel.pop(0)
            # we know we can get back to original vertex so return
            if edge == return_vertex:
                return True
            # we don't care about nodes we know we can already reach
            if v_reachable[edge]:
                continue
            else:
                # append the new edges to the search q, O(1) time with stack
                to_travel += edges[edge]
                v_reachable[edge] = True
                count += 1
        return count == vertices_left


class DgraphSpecial(Dgraph):
    def __init__(self):
        """
        Extends from the Dgraph ot read in a graph from a string file
        """
        super().__init__()

    def read_file(self, filename):
        """
        read in a file of strings to create d-graph from
        :param filename: file to read in
        """
        with open(filename, "r") as file:
            for line in file:
                self.graph.addVertex(line.rstrip("\n"))

    def create_edges(self):
        """
        generate the graph from the vertices. For each vertex when a new edge is found
        the number of vertices for that edge is increased
        """
        for i in range(len(self.graph.vertices)):
            for j in range(len(self.graph.vertices)):
                if self.graph.vertices[i].name[:-1] == self.graph.vertices[j].name[1:]:
                    self.graph.addEdge(j, i)

    def findStart(self):
        """
        Find the start of the graph by looking for the vertex with no incoming edges
        :return:
        """
        for i in range(len(self.graph.vertices)):
            if self.graph.vertices[i].incoming == 0:
                return i
        return None


if __name__ == "__main__":
    """
    read arguments of input and run appropriate version
    """
    if len(sys.argv) == 2:
        file = sys.argv[1]
        try:
            dg = DgraphSpecial()
            dg.read_file(file)
            dg.create_edges()
            start = dg.findStart()
            dg.find_e_circuit(start)
            dg.print_e_circuit()
        except IOError:
            print("Cannot read file: " + file)
        exit()
    elif len(sys.argv) > 2:
        try:
            n = int(sys.argv[1])
        except ValueError:
            print("N must be an Integer")
            exit()
        try:
            m = int(sys.argv[2])
        except ValueError:
            print("M must be an Integer")
            exit()
        start = None
        if len(sys.argv) > 3:
            try:
                start = int(sys.argv[3])
            except ValueError:
                print("Start must be an Integer")
        try:
            # average = 0
            # for i in range(n ** m):
            #    start = i
            dg = Dgraph()
            dg.create_vertices(n, m)
            dg.create_edges()
            #    t1 = timeit.default_timer()
            dg.find_e_circuit(start)
            #   t2 = timeit.default_timer()
            #   print("Time: ", t2 - t1)
            #   average += t2-t1
            dg.print_e_circuit()
            # print("Average: " , average/(n**m))
            exit()
        except (ValueError, IndexError) as e:
            print(e)
    else:
        print("Invalid arguments")
        print("Must be of form:")
        print("ecircuit.py [n] [m] [start vertex]")
        print("or")
        print("ecircuit.py filename")
        exit()

