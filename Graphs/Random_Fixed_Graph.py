from Generate.Generate import *
from Analyze.Analyze import *
import random
import sys


class RandomFixedGraph:
    """
        This class creates a Random Fixed Graph and an adjacency matrix based on the number of vertices, maximum node
        connectivity and seed given by the user interface.

       |-------------------------------------------------------------------------------------------------------------|
       | The algorithm follows the following steps:                                                                  |
       | 1. Generate the vertices and a matrix that holds the current number of edges for each vertex.               |
       | 2. For each Vertex start creating edges with other nodes randomly, until the number of edges of the current |
       |    Vertex is equal to the specified maximum number of edges that a Vertex can have. If so remove the        |
       |    current Vertex from 'play' and continue the process of connecting vertices until no Vertex left.         |
       |-------------------------------------------------------------------------------------------------------------|

    """

    def __init__(self):
        self.g = None

    def create_random_fixed_graph(self, adjacency_type, numOfVertices, connectivity, seed, thread):

        """ Commented lines of code serve debugging purposes. """

        if adjacency_type == "Matrix":
            from Graphs.graph_adjacency_matrix import Graph, Vertex
        else:
            from Graphs.graph_adjacency_list import Graph, Vertex

        self.g = Graph()
        self.g.reset_graph()

        random.seed(seed)
        numOfEdges = [0] * numOfVertices

        for i in range(numOfVertices):

            if thread.isStopped():
                sys.exit(0)

            self.g.add_vertex(Vertex(i))

        graph_vector = self.g.edge_indices.copy()

        for v, i in self.g.edge_indices.items():

            if v in graph_vector:

                # print("Connecting node {} with others...".format(int(v)))

                while numOfEdges[int(v)] < connectivity and len(graph_vector) != 0:

                    if thread.isStopped():
                        sys.exit(0)

                    random_node = random.choice(list(graph_vector.keys()))

                    if random_node == v and len(graph_vector) != 1:
                        while random_node == v:
                            random_node = random.choice(list(graph_vector.keys()))

                    if numOfEdges[int(random_node)] >= connectivity:
                        del graph_vector[random_node]
                        # print("Removed node {} from play.".format(int(random_node)))
                        # print(graph_vector)

                    if numOfEdges[int(v)] >= connectivity:
                        try:
                            del graph_vector[v]
                            # print("Removed node {} from play.".format(int(v) + 1))
                            # print(graph_vector)

                        except KeyError:
                            pass

                    if numOfEdges[int(random_node)] < connectivity and v != random_node \
                            and not self.g.isAdjacent(v, random_node):

                        self.g.add_edge_undirected(v, random_node)
                        numOfEdges[int(v)] += 1
                        numOfEdges[int(random_node)] += 1

                        # print("Connected node {} ({}) edges with node {} ({}) edges."
                        #       .format(int(v), numOfEdges[int(v)], int(random_node), numOfEdges[int(random_node)]))

                        if numOfEdges[int(v)] >= connectivity:
                            try:
                                del graph_vector[v]
                                # print("Removed node {} from play.".format(int(v)))
                                # print(graph_vector)

                            except KeyError:
                                pass

                        if numOfEdges[int(random_node)] >= connectivity:
                            del graph_vector[random_node]
                            # print("Removed node {} from play.".format(int(random_node)))
                            # print(graph_vector)

                    elif len(graph_vector) == 1:
                        break

                    elif len(graph_vector) > 1:
                        counter = 0
                        for w, l in graph_vector.items():

                            if self.g.isAdjacent(v, w) and v != w:
                                counter += 1

                        if counter == len(graph_vector) - 1:
                            break

                    elif not self.g.isAdjacent(v, random_node) and len(graph_vector) == 2 and v != random_node:
                        self.g.add_edge_directed(v, random_node)
                        numOfEdges[int(v)] += 1
                        numOfEdges[int(random_node)] += 1

                        # print("Connected node {} ({}) edges with node {} ({}) edges."
                        #       .format(int(v), numOfEdges[int(v)], int(random_node), numOfEdges[int(random_node)]))

        # print()

        self.g.get_number_of_edges()
        # self.g.print_graph()

        generator.generate(adjacency_type, self.g, thread)

        if adjacency_type == "Matrix":
            analyzer.analyze_matrix(self.g.edges, 'Random Fixed Graph', numOfVertices, connectivity,
                                    None, None, None, None, seed)
        else:
            analyzer.analyze_list(self.g.neighbors, 'Random Fixed Graph', numOfVertices, connectivity,
                                  None, None, None, None, seed)
