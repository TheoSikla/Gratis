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

from graphs.graph import Graph
from graphs.vertex import Vertex
from collections import OrderedDict


class AdjacencyListGraph(Graph):
    """Class for Adjacency List Graph objects."""

    def __init__(self, repr_type, graph_type):
        super(AdjacencyListGraph, self).__init__(repr_type, graph_type)

    def __str__(self):
        out = ""
        out += "Graph = {\n"
        for vertex, neighbors in self.edges.items():
            out += (" " * 9) + "'{}': {}\n".format(vertex, str(neighbors))

        out += " " * 8 + "}\n"
        return out

    def add_vertex(self, vertex):
        if isinstance(vertex, Vertex) and vertex.name not in self.vertices:
            self.vertices[vertex.name] = vertex
            self.edge_indices[vertex.name] = len(self.edge_indices)
            self.edges[vertex.name] = []

            return True
        else:
            return False

    def remove_vertex(self, name):
        if str(name) in self.vertices:
            del self.vertices[str(name)]
            del self.edge_indices[str(name)]
            del self.edges[str(name)]

            for vertex, neighbors in self.edges.items():
                if str(name) in self.edges[vertex]:
                    self.edges[vertex].remove(str(name))
            return True
        else:
            return False

    def remove_neighbor(self, vertex, neighbor):
        if str(neighbor) in self.edges[str(vertex)]:
            self.edges[str(vertex)].remove(str(neighbor))
            self.edges[str(neighbor)].remove(str(vertex))
            return True
        else:
            return False

    def add_edge_directed(self, vertex, neighbor):
        if str(neighbor) not in self.edges[str(vertex)]:
            self.edges[str(vertex)].append(str(neighbor))
            return True
        else:
            return False

    def add_edge_undirected(self, vertex, neighbor):
        if str(neighbor) not in self.edges[str(vertex)]:
            self.edges[str(vertex)].append(str(neighbor))
            self.edges[str(neighbor)].append(str(vertex))
            return True
        else:
            return False

    def isAdjacent(self, vertex1, vertex2):
        if str(vertex1) in self.edges[str(vertex2)]:
            return True
        elif str(vertex2) in self.edges[str(vertex1)]:
            return True
        else:
            return False

    def reset_graph(self):
        self.vertices.clear()
        self.edge_indices.clear()
        self.edges.clear()
        self.vertices = {}
        self.edge_indices = {}
        self.edges = {}

    def get_number_of_edges(self):
        self.edges = {int(c): v for c, v in self.edges.items()}
        self.edges = OrderedDict(sorted(self.edges.items()))
        self.edges = {str(c): v for c, v in self.edges.items()}
        for vertex, neighbors in self.edges.items():
            print("Node {:>{}} has {:>{}} edges {}".format(int(vertex) + 1, len(str(len(self.edges))),
                                                           len(self.edges[vertex]), len(str(len(self.edges))),
                                                           ("*" * len(self.edges[vertex]))))
        print()
