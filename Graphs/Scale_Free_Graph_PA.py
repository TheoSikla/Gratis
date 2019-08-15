__author__ = "Theodoros Siklafidis"
__name__ = "Gratis"
__version__ = "1.0"
__license__ = "GNU General Public License v3.0"

import sys
import random
from Analyze.Analyze import *
from Generate.Generate import *
from Support_Folders.camel_case_spliter import *


class ScaleFreeGraphPA:
    """
        This class creates a Barabási-Albert Scale-Free or Custom Scale-Free graph who's nodes use
        the Preferential Attachment (PA) mechanism.

        |----------------------------------------------------------------------------------------------------|
        | The algorithm follows the following steps:                                                         |
        | Scale-Free PA:                                                                                     |
        |   1. Generate the vertices, a support tank-graph and make a random initial connection.             |
        |   2. For each node create an edge with all other nodes with possibility of success Pi = ki/∑j kj   |
        |                                                                                                    |
        | Custom Scale-Free PA:                                                                              |
        |   1. Generate the vertices, a support tank-graph and make a random initial connection.             |
        |   2. For each node create an edge with all other nodes with possibility of success Pi = ki/∑j kj,  |
        |      until the maximum number of edges specified by the user is reached.                           |
        |----------------------------------------------------------------------------------------------------|

    """

    def __init__(self):
        self.g = None

    def create_scale_free_graph(self, adjacency_type, numOfVertices, seed, thread):

        """ Commented lines of code serve debugging purposes. """

        if adjacency_type == "Matrix":
            from Graphs.graph_adjacency_matrix import Graph, Vertex
        else:
            from Graphs.graph_adjacency_list import Graph, Vertex

        self.g = Graph()
        self.g.reset_graph()

        numOfEdges = [0] * numOfVertices
        numOfConnectedEdges = 0

        random.seed(seed)

        # Generate the tank with all nodes and a support graph vector.
        for i in range(numOfVertices):

            if thread.isStopped():  # --> Thread Status.
                sys.exit(0)

            self.g.add_vertex(Vertex(i))

        graph_vector = self.g.edge_indices.copy()

        # ======================================

        # Make a random initial connection.
        random_node1 = random.choice(list(self.g.edge_indices.keys()))  # random_node1 --> str
        random_node2 = random.choice(list(self.g.edge_indices.keys()))  # random_node2 --> str

        while random_node1 == random_node2:

            random_node2 = random.choice(list(self.g.edge_indices.keys()))  # random_node2 --> str

        self.g.add_edge_undirected(random_node1, random_node2)

        numOfEdges[int(random_node1)] += 1
        numOfEdges[int(random_node2)] += 1

        numOfConnectedEdges += 1

        del graph_vector[random_node1]
        del graph_vector[random_node2]

        print("Initial connection: ")
        print(f"""Connected node {int(random_node1) + 1} ({numOfEdges[int(random_node1)]}) edges with """
              f"""node {int(random_node2) + 1} ({numOfEdges[int(random_node2)]}) edges.\n""")

        # ======================================

        # Connected the rest of the nodes with all other with specified probability.
        while len(graph_vector) != 0:

            if thread.isStopped():  # --> Thread Status.
                sys.exit(0)

            random_node3 = random.choice(list(graph_vector.keys()))

            # print(f"Connecting node {int(random_node3) + 1} with others...")

            for j in range(numOfVertices):

                if thread.isStopped():  # --> Thread Status.
                    sys.exit(0)

                if int(random_node3) != j and numOfEdges[j] != 0:
                    P = numOfEdges[j] / numOfConnectedEdges
                    prandom = random.uniform(0, 1)

                    if P > prandom:
                        self.g.add_edge_undirected(int(random_node3), j)
                        numOfEdges[int(random_node3)] += 1
                        numOfEdges[j] += 1
                        numOfConnectedEdges += 1

            #         print(f"""Connected node {int(random_node3) + 1} ({numOfEdges[int(random_node3)]}) edges with """
            #               f"""node {j + 1} ({numOfEdges[j]}) edges with probability {P}""")
            # print()

            del graph_vector[random_node3]

        # ======================================

        self.g.get_number_of_edges()

        generator.generate(adjacency_type, self.g, thread)

        if adjacency_type == "Matrix":
            analyzer.analyze_generated_graph(self.g.edges, adjacency_type,
                                            f'{camel_case_split(self.__class__.__name__[:-2])} with Preferential Attachment', numOfVertices, None,
                                            None, None, None, None, seed)
        else:
            analyzer.analyze_generated_graph(self.g.neighbors, adjacency_type,
                                             f'{camel_case_split(self.__class__.__name__[:-2])} with Preferential Attachment', numOfVertices, None,
                                             None, None, None, None, seed)

    def create_custom_scale_free_graph(self, adjacency_type, numOfVertices, totalNumOfEdges, seed, thread):

        """ Commented lines of code serve debugging purposes. """

        if adjacency_type == "Matrix":
            from Graphs.graph_adjacency_matrix import Graph, Vertex
        else:
            from Graphs.graph_adjacency_list import Graph, Vertex

        self.g = Graph()
        self.g.reset_graph()

        numOfEdges = [0] * numOfVertices
        numOfConnectedEdges = 0

        random.seed(seed)

        # Generate the tank with all nodes and a support graph vector.
        for i in range(numOfVertices):

            if thread.isStopped():  # --> Thread Status.
                sys.exit(0)

            self.g.add_vertex(Vertex(i))

        graph_vector = self.g.edge_indices.copy()

        # ======================================

        # Make a random initial connection.
        random_node1 = random.choice(list(self.g.edge_indices.keys()))  # random_node1 --> str
        random_node2 = random.choice(list(self.g.edge_indices.keys()))  # random_node2 --> str

        while random_node1 == random_node2:

            random_node2 = random.choice(list(self.g.edge_indices.keys()))  # random_node2 --> str

        self.g.add_edge_undirected(random_node1, random_node2)

        numOfEdges[int(random_node1)] += 1
        numOfEdges[int(random_node2)] += 1

        numOfConnectedEdges += 1

        del graph_vector[random_node1]
        del graph_vector[random_node2]

        print("Initial connection: ")
        print(f"""Connected node {int(random_node1) + 1} ({numOfEdges[int(random_node1)]}) edges with """
              f"""node {int(random_node2) + 1} ({numOfEdges[int(random_node2)]}) edges.\n""")

        # ======================================

        # Connected the rest of the nodes with all other with specified probability.
        while len(graph_vector) != 0 and numOfConnectedEdges < totalNumOfEdges:

            if thread.isStopped():  # --> Thread Status.
                sys.exit(0)

            random_node3 = random.choice(list(graph_vector.keys()))

            # print(f"Connecting node {int(random_node3) + 1} with others...")

            for j in range(numOfVertices):

                if thread.isStopped():  # --> Thread Status.
                    sys.exit(0)

                if int(random_node3) != j and numOfEdges[j] != 0:
                    P = numOfEdges[j] / numOfConnectedEdges
                    prandom = random.uniform(0, 1)

                    if P > prandom:
                        self.g.add_edge_undirected(int(random_node3), j)
                        numOfEdges[int(random_node3)] += 1
                        numOfEdges[j] += 1

                        numOfConnectedEdges += 1

            #         print(f"""Connected node {int(random_node3) + 1} ({numOfEdges[int(random_node3)]}) edges with """
            #               f"""node {j + 1} ({numOfEdges[j]}) edges with probability {P}""")
            # print()

            del graph_vector[random_node3]

        # ======================================

        self.g.get_number_of_edges()

        generator.generate(adjacency_type, self.g, thread)

        if adjacency_type == "Matrix":
            analyzer.analyze_generated_graph(self.g.edges, adjacency_type,
                                            f'Custom {camel_case_split(self.__class__.__name__[:-2])} with Preferential Attachment', numOfVertices, None,
                                            totalNumOfEdges, None, None, None, seed)
        else:
            analyzer.analyze_generated_graph(self.g.neighbors, adjacency_type,
                                            f'Custom {camel_case_split(self.__class__.__name__[:-2])} with Preferential Attachment', numOfVertices, None,
                                            totalNumOfEdges, None, None, None, seed)
