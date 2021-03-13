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


class RandomFixed:
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

    def __init__(self, graph_representation_type):
        if graph_representation_type == GraphRepresentationType.MATRIX.value:
            self.graph = AdjacencyMatrixGraph(GraphRepresentationType.MATRIX, GraphType.RANDOM_FIXED)
        else:
            self.graph = AdjacencyListGraph(GraphRepresentationType.LIST, GraphType.RANDOM_FIXED)

    def create_random_fixed_graph(self, number_of_vertices, graph_degree, seed, thread=None, **kwargs):
        """ Commented lines of code serve debugging purposes. """

        self.graph.reset_graph()

        if self.graph.graph_representation_type == "matrix":
            if kwargs.get('rle'):
                self.graph.mode = "memory efficient"

        random.seed(seed)
        number_of_edges = [0] * number_of_vertices

        for i in range(number_of_vertices):

            if thread and thread.isStopped():
                sys.exit(0)

            self.graph.add_vertex(Vertex(i))

        graph_vector = self.graph.edge_indices.copy()

        for v, i in self.graph.edge_indices.items():

            if v in graph_vector:

                # print(f"Connecting node {int(v)} with others...")

                while number_of_edges[int(v)] < graph_degree and len(graph_vector) != 0:

                    if thread and thread.isStopped():
                        sys.exit(0)

                    random_node = random.choice(list(graph_vector.keys()))

                    if random_node == v and len(graph_vector) != 1:
                        while random_node == v:
                            random_node = random.choice(list(graph_vector.keys()))

                    if number_of_edges[int(random_node)] >= graph_degree:
                        del graph_vector[random_node]
                        # print(f"Removed node {int(random_node)} from play.")
                        # print(graph_vector)

                    if number_of_edges[int(v)] >= graph_degree:
                        try:
                            del graph_vector[v]
                            # print(f"Removed node {int(v) + 1} from play.")
                            # print(graph_vector)

                        except KeyError:
                            pass

                    if number_of_edges[int(random_node)] < graph_degree and v != random_node \
                            and not self.graph.isAdjacent(v, random_node):

                        self.graph.add_edge_undirected(v, random_node)
                        number_of_edges[int(v)] += 1
                        number_of_edges[int(random_node)] += 1

                        # print(f"""Connected node {int(v)} ({number_of_edges[int(v)]}) """
                        #       f"""edges with node {int(random_node)} ({number_of_edges[int(random_node)]}) edges.""")

                        if number_of_edges[int(v)] >= graph_degree:
                            try:
                                del graph_vector[v]
                                # print(f"Removed node {int(v)} from play.")
                                # print(graph_vector)

                            except KeyError:
                                pass

                        if number_of_edges[int(random_node)] >= graph_degree:
                            del graph_vector[random_node]
                            # print(f"Removed node {int(random_node)} from play.")
                            # print(graph_vector)

                    elif len(graph_vector) == 1:
                        break

                    elif len(graph_vector) > 1:
                        counter = 0
                        for w, l in graph_vector.items():

                            if self.graph.isAdjacent(v, w) and v != w:
                                counter += 1

                        if counter == len(graph_vector) - 1:
                            break

                    elif not self.graph.isAdjacent(v, random_node) and len(graph_vector) == 2 and v != random_node:
                        self.graph.add_edge_directed(v, random_node)
                        number_of_edges[int(v)] += 1
                        number_of_edges[int(random_node)] += 1

        #                 print(f"""Connected node {int(v)} ({number_of_edges[int(v)]}) edges with """
        #                       f"""node {int(random_node)} ({number_of_edges[int(random_node)]}) edges.""")

        # print()

        # self.graph.get_number_of_edges()

        generator.generate(self.graph.graph_representation_type, self.graph, thread)
        analyzer.analyze_generated_graph(self.graph.edges, self.graph.graph_representation_type,
                                         self.graph.graph_type,
                                         number_of_vertices, graph_degree, None, None, None, None, seed)
