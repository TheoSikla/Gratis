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

from Graphs.vertex import Vertex
from Graphs.graph import Graph


class AdjacencyMatrixGraph(Graph):
    """Class for Adjacency Matrix Graph objects."""

    def __init__(self, repr_type, graph_type, mode="normal"):
        self.mode = mode
        super(AdjacencyMatrixGraph, self).__init__(repr_type, graph_type)

    def __str__(self):
        """ Prints a well formatted output of the graph's adjacency matrix. """
        out = ""
        out += "{:>{}}\n".format("Vertices", len(str(len(self.edge_indices))) + 9)
        out += "{:<{}}".format("", len(str(len(self.edge_indices))) + 1)
        for v, i in self.edge_indices.items():
            out += "{:<{}}".format(int(v) + 1, len(str(len(self.edge_indices))) + 1)
        out += "\n"

        for v, i in self.edge_indices.items():
            out += "{:<{}}".format(str((int(v) + 1)), len(str(len(self.edge_indices))) + 1)
            for j in range(len(self.edges)):
                out += "{:<{}}".format(self.edges[i][j], len(str(len(self.edge_indices))) + 1)
            out += "\n"

        return out

    def add_vertex(self, vertex):
        """ Adds a vertex to the dictionaries 'vertices' and 'edge_indices' and extends the list of
            the edges allocating memory space with 0's. """

        if isinstance(vertex, Vertex) and vertex.name not in self.vertices:
            self.vertices[vertex.name] = vertex
            for row in self.edges:
                row.append(0)
            self.edges.append([0] * (len(self.edges) + 1))
            self.edge_indices[vertex.name] = len(self.edge_indices)
            return True
        else:
            return False

    def remove_vertex(self, name):
        """ Removes a vertex from the 'vertices' dictionary. """

        if str(name) in self.vertices:
            del self.vertices[str(name)]
            del self.edge_indices[str(name)]
            return True
        else:
            return False

    def add_edge_directed(self, u, v, weight=1):
        """ Adds a one-way directed edge from point u to v (u,v) to the adjacency matrix. """

        if str(u) in self.vertices and str(v) in self.vertices:
            self.edges[self.edge_indices[str(u)]][self.edge_indices[str(v)]] = weight
            return True
        else:
            return False

    def add_edge_undirected(self, u, v, weight=1):
        """ Adds a two-way directed edge from point u to v (u,v) to the adjacency matrix. """

        if str(u) in self.vertices and str(v) in self.vertices:
            try:
                self.edges[self.edge_indices[str(u)]][self.edge_indices[str(v)]] = weight
                self.edges[self.edge_indices[str(v)]][self.edge_indices[str(u)]] = weight

            except IndexError:
                self.reset_graph()

            return True
        else:
            return False

    def isAdjacent(self, vertex1, vertex2):
        """ Checks if two vertexes are adjacent based on the adjacency matrix. """

        if isinstance(vertex1, Vertex) and isinstance(vertex2, Vertex):
            index1, index2 = int(vertex1.name), int(vertex2.name)

            if index1 < 0 or index1 >= len(self.vertices) or index2 < 0 or index2 >= len(self.vertices):
                return False
            if self.edges[index1][index2] == 0 and self.edges[index2][index1] == 0:
                return False
            else:
                return True
        else:
            index1, index2 = int(vertex1), int(vertex2)
            if index1 < 0 or index1 >= len(self.vertices) or index2 < 0 or index2 >= len(self.vertices):
                return False
            if self.edges[index1][index2] == 0 and self.edges[index2][index1] == 0:
                return False
            else:
                return True

    def reset_graph(self):
        """ Resets the graph variables so that a new graph will be ready to be generated. """

        self.vertices.clear()
        self.edges.clear()
        self.edge_indices.clear()
        self.vertices = {}
        self.edges = []
        self.edge_indices = {}

    def get_number_of_edges(self):
        node_edges = 0
        for v, i in self.edge_indices.items():
            for j in range(len(self.edges)):
                if self.edges[i][j] == 1:
                    node_edges += 1
            print("Node {:>{}} has {:>{}} edges. ".format(int(v) + 1, len(str(len(self.edge_indices))),
                                                          node_edges, len(str(len(self.edge_indices))))
                  + "*" * node_edges)
            node_edges = 0
        print()
