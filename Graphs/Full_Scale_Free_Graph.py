__author__ = "Theodoros Siklafidis"
__name__ = "Gratis"
__version__ = "1.0"
__license__ = "GNU General Public License v3.0"

import random
from Analyze.Analyze import *
from Generate.Generate import *
from collections import OrderedDict
from Graphs.vertex import Vertex
from Graphs.graph_adjacency_list import AdjacencyListGraph
from Graphs.graph import GraphRepresentationType, GraphType
from Graphs.graph_adjacency_matrix import AdjacencyMatrixGraph


class FullScaleFree:
    """
        This class creates a Barabási-Albert Full Scale-Free graph who's nodes use the preferential attachment and
        incremental growth mechanism.

        |-----------------------------------------------------------------------------------------------------------|
        | The algorithm follows the following steps:                                                                |
        | Full Scale-Free Graph:                                                                                    |
        |   1. Generate a tank K with m0 initial nodes homogeneously connected and a tank L with all other nodes.   |
        |   2. For each node in tank L select randomly one node and place it into tank K creating edges with all    |
        |       other nodes with possibility of success Pi = ki/∑j kj                                               |
        |                                                                                                           |
        | Custom Full Scale-Free Graph:                                                                             |
        |   1. Generate a tank K with m0 initial nodes, connect them until the number of connected edges that       |
        |      m0 initial nodes have is equal to the number of initial edges specified by the user,                 |
        |      and a tank L with all other nodes.                                                                   |
        |   2. For each node in tank L select randomly one node and place it into tank K creating edges with all    |
        |      other nodes with possibility of success Pi = ki/∑j kj                                                |
        |-----------------------------------------------------------------------------------------------------------|

    """

    def __init__(self, graph_representation_type):
        if graph_representation_type == str(GraphRepresentationType.MATRIX):
            self.graph = AdjacencyMatrixGraph(GraphRepresentationType.MATRIX, GraphType.SCALE_FREE)
        else:
            self.graph = AdjacencyListGraph(GraphRepresentationType.LIST, GraphType.SCALE_FREE)

    def create_full_scale_free_graph(self, number_of_vertices, number_of_initial_nodes, seed, thread,
                                     number_of_initial_edges=None, **kwargs):
        """ Commented lines of code serve debugging purposes. """

        self.graph.reset_graph()

        if self.graph.graph_representation_type == "matrix":
            if kwargs.get('rle'):
                self.graph.mode = "memory efficient"

        number_of_edges = [0] * number_of_vertices
        number_of_connected_edges = 0
        random.seed(seed)
        graph_vector = {}

        # In case there is only one initial node.
        if number_of_initial_nodes == 1:
            number_of_connected_edges += 1

        # Generating tank with all nodes inside.
        for i in range(number_of_vertices):

            if thread.isStopped():  # --> Thread Status.
                sys.exit(0)

            graph_vector[str(i)] = i

        # Adding random mo initial nodes to the graph.
        # print("Initial nodes:")

        for i in range(number_of_initial_nodes):
            if thread.isStopped():  # --> Thread Status.
                sys.exit(0)

            random_node = random.choice(list(graph_vector.keys()))
            self.graph.add_vertex(Vertex(random_node))
            del graph_vector[random_node]

            # print(int(random_node) + 1)

        # Connecting all mo (initial nodes).
        if number_of_initial_nodes == 1:  # If number of initial node is one give the node a starting edge.
            for v, i in list(self.graph.edge_indices.items()):
                number_of_edges[int(v)] += 1

        for v, i in list(self.graph.edge_indices.items()):
            for b, j in list(self.graph.edge_indices.items()):
                if thread.isStopped():  # --> Thread Status.
                    sys.exit(0)

                # If Custom Full Scale-Free Graph is chosen.
                if number_of_initial_edges is not None and number_of_connected_edges >= number_of_initial_edges:
                    break

                if v != b and v < b:
                    self.graph.add_edge_undirected(v, b)
                    number_of_edges[int(v)] += 1
                    number_of_edges[int(b)] += 1
                    number_of_connected_edges += 1

            # If Custom Full Scale-Free Graph is chosen.
            if number_of_initial_edges is not None and number_of_connected_edges >= number_of_initial_edges:
                break

        #         print(f"""Connected node {int(v) + 1} ({number_of_edges[int(v)]}) edges with """
        #                 f"""node {int(b) + 1} ({number_of_edges[int(b)]}) edges with probability 1.0""")
        # print("Finished initial nodes.")

        # ======================================

        # Go for the rest nodes.
        while len(graph_vector) != 0:
            random_node = random.choice(list(graph_vector.keys()))  # random_node --> str
            self.graph.add_vertex(Vertex(random_node))
            del graph_vector[random_node]

            for v, i in list(self.graph.edge_indices.items()):
                if thread.isStopped():  # --> Thread Status.
                    sys.exit(0)

                if v != random_node:
                    probability = number_of_edges[int(v)] / number_of_connected_edges
                    probability_random = random.uniform(0, 1)

                    if probability > probability_random:
                        self.graph.add_edge_undirected(random_node, v)
                        number_of_edges[int(random_node)] += 1
                        number_of_edges[int(v)] += 1
                        number_of_connected_edges += 1

                        # print(f"""Connected node {int(random_node) + 1} ({number_of_edges[int(random_node)]}) """
                        #       f"""edges with node {int(v) + 1} ({number_of_edges[int(v)]}) edges with probability """
                        #       f"""{probability}""")

        graph_vector.clear()

        # Sort randomized graph order.

        # Method 1
        self.graph.edge_indices = {int(c): v for c, v in self.graph.edge_indices.items()}
        self.graph.edge_indices = OrderedDict(sorted(self.graph.edge_indices.items()))
        self.graph.edge_indices = {str(c): v for c, v in self.graph.edge_indices.items()}

        # self.graph.get_number_of_edges()

        generator.generate(self.graph.graph_representation_type, self.graph, thread)
        analyzer.analyze_generated_graph(self.graph.edges, self.graph.graph_representation_type,
                                         f'{"Custom " if number_of_initial_edges is not None else ""}'
                                         f'Full {self.graph.graph_type}',
                                         number_of_vertices, None, None, number_of_initial_edges, None, None, seed)
