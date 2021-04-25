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

from analyze.analyze import *
from generate.generate import *
from graphs.vertex import Vertex
from graphs.graph_adjacency_list import AdjacencyListGraph
from graphs.graph import GraphRepresentationType, GraphType
from graphs.graph_adjacency_matrix import AdjacencyMatrixGraph


class Homogeneous:
    """
        This class creates a homogeneous graph and an adjacency matrix based on the number of vertices given by the
        user interface.
        Homogeneous graph is a graph that has all its vertices connected with each other.
    """

    def __init__(self, graph_representation_type):
        if graph_representation_type == GraphRepresentationType.MATRIX.value:
            self.graph = AdjacencyMatrixGraph(GraphRepresentationType.MATRIX, GraphType.HOMOGENEOUS)
        else:
            self.graph = AdjacencyListGraph(GraphRepresentationType.LIST, GraphType.HOMOGENEOUS)

    def create_homogeneous_graph(self, number_of_vertices, thread=None, **kwargs):
        self.graph.reset_graph()

        if self.graph.graph_representation_type == "matrix":
            if kwargs.get('rle'):
                self.graph.mode = "memory efficient"

        for i in range(number_of_vertices):
            self.graph.add_vertex(Vertex(str(i)))
            if thread and thread.isStopped():
                sys.exit(0)

        for i in range(number_of_vertices):
            for j in range(number_of_vertices):
                if i != j and i < j:
                    self.graph.add_edge_undirected(i, j)
                    if thread and thread.isStopped():
                        sys.exit(0)

        generator.generate(self.graph.graph_representation_type, self.graph, thread)
        analyzer.analyze_generated_graph(self.graph.edges, self.graph.graph_representation_type, self.graph.graph_type,
                                         number_of_vertices)
