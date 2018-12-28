from Generate.Generate import *
from Analyze.Analyze import *
import random
from collections import OrderedDict
import sys


class Full_Scale_Free_Graph:
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

    def __init__(self):
        self.g = None

    def create_full_scale_free_graph(self, adjacency_type, numOfVertices, numOfInitialNodes, seed, thread,
                                     numOfInitialEdges=None):

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

        graph_vector = {}

        # In case there is only one initial node.
        if numOfInitialNodes == 1:
            numOfConnectedEdges += 1

        # ======================================

        # Generating tank with all nodes inside.
        for i in range(numOfVertices):

            if thread.isStopped():  # --> Thread Status.
                sys.exit(0)

            graph_vector[str(i)] = i

        # ======================================

        # Adding random mo initial nodes to the graph.
        # print("Initial nodes:")
        # self.g.edge_indices.clear()

        for i in range(numOfInitialNodes):

            if thread.isStopped():  # --> Thread Status.
                sys.exit(0)

            random_node = random.choice(list(graph_vector.keys()))
            self.g.add_vertex(Vertex(random_node))
            del graph_vector[random_node]

            # print(int(random_node) + 1)

        # ======================================

        # Connecting all mo (initial nodes).
        if numOfInitialNodes == 1:  # If number of initial node is one give the node a starting edge.
            for v, i in list(self.g.edge_indices.items()):
                numOfEdges[int(v)] += 1

        for v, i in list(self.g.edge_indices.items()):

            for b, j in list(self.g.edge_indices.items()):

                if thread.isStopped():  # --> Thread Status.
                    sys.exit(0)

                # If Custom Full Scale-Free Graph is chosen.
                if numOfInitialEdges is not None and numOfConnectedEdges >= numOfInitialEdges:
                    break
                # ======================================

                if v != b and v < b:
                    self.g.add_edge_undirected(v, b)
                    numOfEdges[int(v)] += 1
                    numOfEdges[int(b)] += 1
                    numOfConnectedEdges += 1

            # If Custom Full Scale-Free Graph is chosen.
            if numOfInitialEdges is not None and numOfConnectedEdges >= numOfInitialEdges:
                break
            # ======================================

        #             print("Connected node {} ({}) edges with node {} ({}) edges with probability 1.0"
        #                   .format(int(v)+1, numOfEdges[int(v)], int(b)+1, numOfEdges[int(b)]))
        # print("Finished initial nodes.")

        # ======================================

        # Go for the rest nodes.
        while len(graph_vector) != 0:

            random_node = random.choice(list(graph_vector.keys()))  # random_node --> str
            self.g.add_vertex(Vertex(random_node))
            del graph_vector[random_node]

            for v, i in list(self.g.edge_indices.items()):

                if thread.isStopped():  # --> Thread Status.
                    sys.exit(0)

                if v != random_node:
                    P = numOfEdges[int(v)] / numOfConnectedEdges
                    prandom = random.uniform(0, 1)

                    if P > prandom:
                        self.g.add_edge_undirected(random_node, v)
                        numOfEdges[int(random_node)] += 1
                        numOfEdges[int(v)] += 1
                        numOfConnectedEdges += 1

                        # print("Connected node {} ({}) edges with node {} ({}) edges with probability {}"
                        #       .format(int(random_node)+1, numOfEdges[int(random_node)],
                        #               int(v)+1, numOfEdges[int(v)], P))

        # ======================================
        graph_vector.clear()

        # ==============================================================================================================
        # ==> Simple reference for dictionary sorting, no need though... Things are sorted before printed. <==

        # Sort randomized graph order.

        # Method 1
        self.g.edge_indices = {int(c): v for c, v in self.g.edge_indices.items()}
        self.g.edge_indices = OrderedDict(sorted(self.g.edge_indices.items()))
        self.g.edge_indices = {str(c): v for c, v in self.g.edge_indices.items()}

        # Method 2
        # self.g.edge_indices = sorted(self.g.edge_indices.items(), key=lambda kv: kv[0])
        # self.g.edge_indices = dict(self.g.edge_indices)
        # ==============================================================================================================

        # self.g.print_graph()
        self.g.get_number_of_edges()

        generator.generate(adjacency_type, self.g, thread)

        if adjacency_type == "Matrix":
            analyzer.analyze_matrix(self.g.edges, 'Full Scale-Free Graph', numOfVertices, None, None, numOfInitialNodes,
                                    numOfInitialEdges, None, seed)
        else:
            analyzer.analyze_list(self.g.neighbors, 'Full Scale-Free Graph', numOfVertices, None, None,
                                  numOfInitialNodes, numOfInitialEdges, None, seed)
