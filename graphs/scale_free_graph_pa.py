"""
                Copyright (C) 2020 Theodoros Siklafidis

    This file is part of GRATIS.

    GRATIS is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    GRATIS is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with GRATIS. If not, see <https://www.gnu.org/licenses/>.
"""
import random
from analyze.analyze import *
from generate.generate import *
from graphs.vertex import Vertex
from graphs.graph_adjacency_list import AdjacencyListGraph
from graphs.graph import GraphRepresentationType, GraphType
from graphs.graph_adjacency_matrix import AdjacencyMatrixGraph


class ScaleFreePA:
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

    def __init__(self, graph_representation_type):
        if graph_representation_type == str(GraphRepresentationType.MATRIX):
            self.graph = AdjacencyMatrixGraph(GraphRepresentationType.MATRIX, GraphType.SCALE_FREE)
        else:
            self.graph = AdjacencyListGraph(GraphRepresentationType.LIST, GraphType.SCALE_FREE)

    def create_scale_free_graph(self, number_of_vertices, seed, thread, **kwargs):
        """ Commented lines of code serve debugging purposes. """

        self.graph.reset_graph()

        if self.graph.graph_representation_type == "matrix":
            if kwargs.get('rle'):
                self.graph.mode = "memory efficient"

        number_of_edges = [0] * number_of_vertices
        number_of_connected_edges = 0

        random.seed(seed)

        # Generate the tank with all nodes and a support graph vector.
        for i in range(number_of_vertices):

            if thread.isStopped():  # --> Thread Status.
                sys.exit(0)

            self.graph.add_vertex(Vertex(i))

        graph_vector = self.graph.edge_indices.copy()

        # ======================================

        # Make a random initial connection.
        random_node1 = random.choice(list(self.graph.edge_indices.keys()))  # random_node1 --> str
        random_node2 = random.choice(list(self.graph.edge_indices.keys()))  # random_node2 --> str

        while random_node1 == random_node2:

            random_node2 = random.choice(list(self.graph.edge_indices.keys()))  # random_node2 --> str

        self.graph.add_edge_undirected(random_node1, random_node2)

        number_of_edges[int(random_node1)] += 1
        number_of_edges[int(random_node2)] += 1

        number_of_connected_edges += 1

        del graph_vector[random_node1]
        del graph_vector[random_node2]

        # print("Initial connection: ")
        # print(f"""Connected node {int(random_node1) + 1} ({number_of_edges[int(random_node1)]}) edges with """
        #       f"""node {int(random_node2) + 1} ({number_of_edges[int(random_node2)]}) edges.\n""")

        # ======================================

        # Connected the rest of the nodes with all other with specified probability.
        while len(graph_vector) != 0:

            if thread.isStopped():  # --> Thread Status.
                sys.exit(0)

            random_node3 = random.choice(list(graph_vector.keys()))

            # print(f"Connecting node {int(random_node3) + 1} with others...")

            for j in range(number_of_vertices):

                if thread.isStopped():  # --> Thread Status.
                    sys.exit(0)

                if int(random_node3) != j and number_of_edges[j] != 0:
                    probability = number_of_edges[j] / number_of_connected_edges
                    probability_random = random.uniform(0, 1)

                    if probability > probability_random:
                        self.graph.add_edge_undirected(int(random_node3), j)
                        number_of_edges[int(random_node3)] += 1
                        number_of_edges[j] += 1
                        number_of_connected_edges += 1

            #         print(f"""Connected node {int(random_node3) + 1} ({number_of_edges[int(random_node3)]}) """
            #               f"""edges with node {j + 1} ({number_of_edges[j]}) edges with probability {probability}""")
            # print()

            del graph_vector[random_node3]

        # ======================================

        # self.graph.get_number_of_edges()

        generator.generate(self.graph.graph_representation_type, self.graph, thread)

        analyzer.analyze_generated_graph(self.graph.edges, self.graph.graph_representation_type, self.graph.graph_type,
                                         number_of_vertices, None, None, None, None, None, seed)

    def create_custom_scale_free_graph(self, number_of_vertices, total_number_of_edges, seed, thread, **kwargs):
        """ Commented lines of code serve debugging purposes. """

        self.graph.reset_graph()

        if self.graph.graph_representation_type == "matrix":
            if kwargs.get('rle'):
                self.graph.mode = "memory efficient"

        number_of_edges = [0] * number_of_vertices
        number_of_connected_edges = 0

        random.seed(seed)

        # Generate the tank with all nodes and a support graph vector.
        for i in range(number_of_vertices):

            if thread.isStopped():  # --> Thread Status.
                sys.exit(0)

            self.graph.add_vertex(Vertex(i))

        graph_vector = self.graph.edge_indices.copy()

        # ======================================

        # Make a random initial connection.
        random_node1 = random.choice(list(self.graph.edge_indices.keys()))  # random_node1 --> str
        random_node2 = random.choice(list(self.graph.edge_indices.keys()))  # random_node2 --> str

        while random_node1 == random_node2:

            random_node2 = random.choice(list(self.graph.edge_indices.keys()))  # random_node2 --> str

        self.graph.add_edge_undirected(random_node1, random_node2)

        number_of_edges[int(random_node1)] += 1
        number_of_edges[int(random_node2)] += 1

        number_of_connected_edges += 1

        del graph_vector[random_node1]
        del graph_vector[random_node2]

        # print("Initial connection: ")
        # print(f"""Connected node {int(random_node1) + 1} ({number_of_edges[int(random_node1)]}) edges with """
        #       f"""node {int(random_node2) + 1} ({number_of_edges[int(random_node2)]}) edges.\n""")

        # ======================================

        # Connected the rest of the nodes with all other with specified probability.
        while len(graph_vector) != 0 and number_of_connected_edges < total_number_of_edges:

            if thread.isStopped():  # --> Thread Status.
                sys.exit(0)

            random_node3 = random.choice(list(graph_vector.keys()))

            # print(f"Connecting node {int(random_node3) + 1} with others...")

            for j in range(number_of_vertices):

                if thread.isStopped():  # --> Thread Status.
                    sys.exit(0)

                if int(random_node3) != j and number_of_edges[j] != 0:
                    probability = number_of_edges[j] / number_of_connected_edges
                    probability_random = random.uniform(0, 1)

                    if probability > probability_random:
                        self.graph.add_edge_undirected(int(random_node3), j)
                        number_of_edges[int(random_node3)] += 1
                        number_of_edges[j] += 1

                        number_of_connected_edges += 1

            #         print(f"""Connected node {int(random_node3) + 1} ({number_of_edges[int(random_node3)]}) """
            #               f"""edges with node {j + 1} ({number_of_edges[j]}) edges with probability {probability}""")
            # print()

            del graph_vector[random_node3]

        # ======================================

        # self.graph.get_number_of_edges()

        generator.generate(self.graph.graph_representation_type, self.graph, thread)
        analyzer.analyze_generated_graph(self.graph.edges, self.graph.graph_representation_type, self.graph.graph_type,
                                         number_of_vertices, None, total_number_of_edges, None, None, None, seed)
