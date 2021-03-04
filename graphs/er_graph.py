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


class ErdosRenyi:
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

    def __init__(self, graph_representation_type):
        if graph_representation_type == str(GraphRepresentationType.MATRIX):
            self.graph = AdjacencyMatrixGraph(GraphRepresentationType.MATRIX, GraphType.ER)
        else:
            self.graph = AdjacencyListGraph(GraphRepresentationType.LIST, GraphType.ER)

    def create_er_graph(self, number_of_vertices, probability, seed, thread, **kwargs):
        """ Commented lines of code serve debugging purposes. """

        self.graph.reset_graph()

        if self.graph.graph_representation_type == "matrix":
            if kwargs.get('rle'):
                self.graph.mode = "memory efficient"

        random.seed(seed)

        number_of_edges = [0] * number_of_vertices

        for i in range(number_of_vertices):
            if thread.isStopped():  # --> Thread Status.
                sys.exit(0)

            self.graph.add_vertex(Vertex(i))

        for new_node in range(number_of_vertices):
            for adjacency_vertex in range(number_of_vertices):

                per = random.uniform(0, 1)

                if new_node == adjacency_vertex or adjacency_vertex >= number_of_vertices:
                    pass

                elif probability >= per:

                    if thread.isStopped():  # --> Thread Status.
                        sys.exit(0)

                    if not self.graph.isAdjacent(new_node, adjacency_vertex):

                        self.graph.add_edge_undirected(new_node, adjacency_vertex)

                        number_of_edges[new_node] += 1
                        number_of_edges[adjacency_vertex] += 1

                        # print(f"""Connected node {new_node} ({number_of_edges[new_node]}) edges with """
                        #       f"""node {adjacency_vertex} ({number_of_edges[adjacency_vertex]})
                        #       edges with probability {probability} > {per}""")
        # print()

        # self.graph.get_number_of_edges()

        generator.generate(self.graph.graph_representation_type, self.graph, thread)
        analyzer.analyze_generated_graph(self.graph.edges, self.graph.graph_representation_type, self.graph.graph_type,
                                         number_of_vertices, None, None, None, None, probability, seed)

    def create_custom_er_graph(self, number_of_vertices, total_number_of_edges, probability,
                               seed, thread, **kwargs):
        """ Commented lines of code serve debugging purposes. """

        self.graph.reset_graph()

        if self.graph.graph_representation_type == "matrix":
            if kwargs.get('rle'):
                self.graph.mode = "memory efficient"

        random.seed(seed)

        number_of_edges = [0] * number_of_vertices
        number_of_connected_edges = 0

        for i in range(number_of_vertices):
            if thread.isStopped():  # --> Thread Status.
                sys.exit(0)

            self.graph.add_vertex(Vertex(i))

        graph_vector = self.graph.edge_indices.copy()

        while number_of_connected_edges < total_number_of_edges:

            new_node = int(random.choice(list(graph_vector.keys())))

            adjacency_vertex = int(random.choice(list(graph_vector.keys())))

            per = random.uniform(0, 1)

            while new_node == adjacency_vertex or self.graph.isAdjacent(new_node, adjacency_vertex):
                if thread.isStopped():  # --> Thread Status.
                    sys.exit(0)

                if len(graph_vector) > 1:
                    counter = 0
                    for w, l in graph_vector.items():

                        if self.graph.isAdjacent(new_node, w) and new_node != w:
                            counter += 1

                    if counter == len(graph_vector) - 1:
                        break

                adjacency_vertex = int(random.choice(list(graph_vector.keys())))
                per = random.uniform(0, 1)

            if probability > per:
                if thread.isStopped():  # --> Thread Status.
                    sys.exit(0)

                self.graph.add_edge_undirected(new_node, adjacency_vertex)
                number_of_edges[new_node] += 1
                number_of_edges[adjacency_vertex] += 1

                number_of_connected_edges += 1

                # print(f"""Connected node {new_node} ({number_of_edges[new_node]}) edges with """
                #       f"""node {adjacency_vertex} ({number_of_edges[adjacency_vertex]}) edges with probability
                #       {probability} > {per}""")
                
                # print(f"Number of connected edges {number_of_connected_edges}")

            if number_of_edges[new_node] >= number_of_vertices - 1:
                try:
                    del graph_vector[str(new_node)]
                    # print(f"Removed node {new_node} from play.")
                    # print(graph_vector)

                except KeyError:
                    pass

            elif number_of_edges[adjacency_vertex] >= number_of_vertices - 1:
                try:
                    del graph_vector[str(adjacency_vertex)]
                    # print(f"Removed node {adjacency_vertex} from play.")
                    # print(graph_vector)

                except KeyError:
                    pass

            elif len(graph_vector) == 1:
                last_node = random.choice(list(graph_vector.keys()))
                del graph_vector[last_node]
                # print(f"Removed node {adjacency_vertex} from play.")
                # print(graph_vector)
                # print("Terminating...")
                break

        # print()

        # self.graph.get_number_of_edges()

        generator.generate(self.graph.graph_representation_type, self.graph, thread)
        analyzer.analyze_generated_graph(self.graph.edges, self.graph.graph_representation_type, self.graph.graph_type,
                                         number_of_vertices, None, total_number_of_edges, None, None, probability, seed)
