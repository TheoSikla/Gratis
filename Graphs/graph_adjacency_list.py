__author__ = "Theodoros Siklafidis"
__name__ = "Gratis"
__version__ = "1.0"
__license__ = "GNU General Public License v3.0"

from Graphs.graph import Graph
from Graphs.vertex import Vertex
from collections import OrderedDict


class AdjacencyListGraph(Graph):
    """Class for Adjacency List Graph objects."""

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
