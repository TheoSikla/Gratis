from Support_Folders.camel_case_spliter import *
from Generate.Generate import *
from Analyze.Analyze import *
import random
import sys


class ErdosRenyiGraph:
    """

        This class creates a Erdős–Rényi Graph (ER Graph) and a Custom ER Graph with specified connection probability.
        The difference between these two Graph models is that in the Custom one the user gets to choose the maximum
        number of edges the graph will have.


        |-----------------------------------------------------------------------------------------------------------|
        | The algorithms follows the following steps:                                                               |
        | ER Graph:                                                                                                 |
        |   1. Create a tank with all nodes in it.                                                                  |
        |   2. For each node try to connect with every other node with probability specified by the user, until all |
        |       nodes are tested.                                                                                   |
        |                                                                                                           |
        | Custom ER Graph:                                                                                          |
        |   1. Create a tank with all nodes in it.                                                                  |
        |   2. Each loop pick randomly a vertex x and a vertex y and try to connect them with probability of        |
        |      success specified by the user, until the maximum number of edges (specified by the user)             |
        |      that the graph must have is reached.                                                                 |
        |-----------------------------------------------------------------------------------------------------------|

    """

    def __init__(self):
        self.g = None

    def create_er_graph(self, adjacency_type, numOfVertices, probability, seed, thread):
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
            if thread.isStopped():  # --> Thread Status.
                sys.exit(0)

            self.g.add_vertex(Vertex(i))

        for newNode in range(numOfVertices):
            for adjacency_vertex in range(numOfVertices):

                Per = random.uniform(0, 1)

                if newNode == adjacency_vertex or adjacency_vertex >= numOfVertices:
                    pass

                elif probability >= Per:

                    if thread.isStopped():  # --> Thread Status.
                        sys.exit(0)

                    if not self.g.isAdjacent(newNode, adjacency_vertex):

                        self.g.add_edge_undirected(newNode, adjacency_vertex)

                        numOfEdges[newNode] += 1
                        numOfEdges[adjacency_vertex] += 1

        #                 print("Connected node {} ({}) edges with node {} ({}) edges with probability {} > {}"
        #                       .format(newNode, numOfEdges[newNode], adjacency_vertex, numOfEdges[adjacency_vertex],
        #                               probability, Per))
        # print()

        self.g.get_number_of_edges()

        generator.generate(adjacency_type, self.g, thread)

        if adjacency_type == "Matrix":
            analyzer.analyze_generated_graph(self.g.edges, adjacency_type, camel_case_split(self.__class__.__name__), numOfVertices, None,
                                            None, None, None, probability, seed)
        else:
            analyzer.analyze_generated_graph(self.g.neighbors, adjacency_type, camel_case_split(self.__class__.__name__), numOfVertices, None,
                                            None, None, None, probability, seed)

    def create_custom_er_graph(self, adjacency_type, numOfVertices, totalNumOfEdges, probability, seed, thread):

        """ Commented lines of code serve debugging purposes. """

        if adjacency_type == "Matrix":
            from Graphs.graph_adjacency_matrix import Graph, Vertex
        else:
            from Graphs.graph_adjacency_list import Graph, Vertex

        self.g = Graph()
        self.g.reset_graph()

        random.seed(seed)

        numOfEdges = [0] * numOfVertices
        numOfConnectedEdges = 0

        for i in range(numOfVertices):
            if thread.isStopped():  # --> Thread Status.
                sys.exit(0)

            self.g.add_vertex(Vertex(i))

        graph_vector = self.g.edge_indices.copy()

        while numOfConnectedEdges < totalNumOfEdges:

            newNode = int(random.choice(list(graph_vector.keys())))

            adjacency_vertex = int(random.choice(list(graph_vector.keys())))

            Per = random.uniform(0, 1)

            while newNode == adjacency_vertex or self.g.isAdjacent(newNode, adjacency_vertex):
                if thread.isStopped():  # --> Thread Status.
                    sys.exit(0)

                if len(graph_vector) > 1:
                    counter = 0
                    for w, l in graph_vector.items():

                        if self.g.isAdjacent(newNode, w) and newNode != w:
                            counter += 1

                    if counter == len(graph_vector) - 1:
                        break

                adjacency_vertex = int(random.choice(list(graph_vector.keys())))
                Per = random.uniform(0, 1)

            if probability > Per:
                if thread.isStopped():  # --> Thread Status.
                    sys.exit(0)

                self.g.add_edge_undirected(newNode, adjacency_vertex)
                numOfEdges[newNode] += 1
                numOfEdges[adjacency_vertex] += 1

                numOfConnectedEdges += 1

                # print("Connected node {} ({}) edges with node {} ({}) edges with probability {} > {}"
                #       .format(newNode, numOfEdges[newNode], adjacency_vertex, numOfEdges[adjacency_vertex],
                #               probability, Per))
                #
                # print("Number of connected edges {}".format(numOfConnectedEdges))

            if numOfEdges[newNode] >= numOfVertices - 1:
                try:
                    del graph_vector[str(newNode)]
                    # print("Removed node {} from play.".format(newNode))
                    # print(graph_vector)

                except KeyError:
                    pass

            elif numOfEdges[adjacency_vertex] >= numOfVertices - 1:
                try:
                    del graph_vector[str(adjacency_vertex)]
                    # print("Removed node {} from play.".format(adjacency_vertex))
                    # print(graph_vector)

                except KeyError:
                    pass

            elif len(graph_vector) == 1:
                last_node = random.choice(list(graph_vector.keys()))
                del graph_vector[last_node]
                # print("Removed node {} from play.".format(adjacency_vertex))
                # print(graph_vector)
                # print("Terminating...")
                break

        # print()

        self.g.get_number_of_edges()

        generator.generate(adjacency_type, self.g, thread)

        if adjacency_type == "Matrix":
            analyzer.analyze_generated_graph(self.g.edges, adjacency_type, f'Custom {camel_case_split(self.__class__.__name__)}', numOfVertices, None,
                                            totalNumOfEdges, None, None, probability, seed)
        else:
            analyzer.analyze_generated_graph(self.g.neighbors, adjacency_type, f'Custom {camel_case_split(self.__class__.__name__)}', numOfVertices, None,
                                            totalNumOfEdges, None, None, probability, seed)
