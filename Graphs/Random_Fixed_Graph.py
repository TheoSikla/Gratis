__author__ = "Theodoros Siklafidis"
__name__ = "Gratis"
__version__ = "1.0"
__license__ = "GNU General Public License v3.0"

import sys
import random
from Analyze.Analyze import *
from Generate.Generate import *
from Support_Folders.camel_case_spliter import *


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

    def create_random_fixed_graph(self, graph_respresentation_type, numOfVertices, connectivity, seed, thread):

        """ Commented lines of code serve debugging purposes. """

        if graph_respresentation_type == "Matrix":
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

                # print(f"Connecting node {int(v)} with others...")

                while numOfEdges[int(v)] < connectivity and len(graph_vector) != 0:

                    if thread.isStopped():
                        sys.exit(0)

                    random_node = random.choice(list(graph_vector.keys()))

                    if random_node == v and len(graph_vector) != 1:
                        while random_node == v:
                            random_node = random.choice(list(graph_vector.keys()))

                    if numOfEdges[int(random_node)] >= connectivity:
                        del graph_vector[random_node]
                        # print(f"Removed node {int(random_node)} from play.")
                        # print(graph_vector)

                    if numOfEdges[int(v)] >= connectivity:
                        try:
                            del graph_vector[v]
                            # print(f"Removed node {int(v) + 1} from play.")
                            # print(graph_vector)

                        except KeyError:
                            pass

                    if numOfEdges[int(random_node)] < connectivity and v != random_node \
                            and not self.g.isAdjacent(v, random_node):

                        self.g.add_edge_undirected(v, random_node)
                        numOfEdges[int(v)] += 1
                        numOfEdges[int(random_node)] += 1

                        # print(f"""Connected node {int(v)} ({numOfEdges[int(v)]}) """
                        #       f"""edges with node {int(random_node)} ({numOfEdges[int(random_node)]}) edges.""")

                        if numOfEdges[int(v)] >= connectivity:
                            try:
                                del graph_vector[v]
                                # print(f"Removed node {int(v)} from play.")
                                # print(graph_vector)

                            except KeyError:
                                pass

                        if numOfEdges[int(random_node)] >= connectivity:
                            del graph_vector[random_node]
                            # print(f"Removed node {int(random_node)} from play.")
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

        #                 print(f"""Connected node {int(v)} ({numOfEdges[int(v)]}) edges with """
        #                       f"""node {int(random_node)} ({numOfEdges[int(random_node)]}) edges.""")

        # print()

        self.g.get_number_of_edges()

        generator.generate(graph_respresentation_type, self.g, thread)

        if graph_respresentation_type == "Matrix":
            analyzer.analyze_generated_graph(self.g.edges, graph_respresentation_type, camel_case_split(self.__class__.__name__), numOfVertices, connectivity,
                                             None, None, None, None, seed)
        else:
            analyzer.analyze_generated_graph(self.g.neighbors, graph_respresentation_type, camel_case_split(self.__class__.__name__), numOfVertices, connectivity,
                                             None, None, None, None, seed)
