__author__ = "Theodoros Siklafidis"
__name__ = "Gratis"
__version__ = "1.0"
__license__ = "GNU General Public License v3.0"

from collections import OrderedDict


class Vertex:
    def __init__(self, name):
        self.name = str(name)


class Graph:
    vertices = {}
    edge_indices = {}
    neighbors = {}

    def __str__(self):
        out = ""
        out += "Graph = {\n"
        for vertex, neighbors in self.neighbors.items():
            out += (" " * 9) + "'{}': {}\n".format(vertex, str(neighbors))

        out += " " * 8 + "}\n"
        return out

    def add_vertex(self, vertex):
        if isinstance(vertex, Vertex) and vertex.name not in self.vertices:
            self.vertices[vertex.name] = vertex
            self.edge_indices[vertex.name] = len(self.edge_indices)
            self.neighbors[vertex.name] = []

            return True
        else:
            return False

    def remove_vertex(self, name):
        if str(name) in self.vertices:
            del self.vertices[str(name)]
            del self.edge_indices[str(name)]
            del self.neighbors[str(name)]

            for vertex, neighbors in self.neighbors.items():
                if str(name) in self.neighbors[vertex]:
                    self.neighbors[vertex].remove(str(name))
            return True
        else:
            return False

    def remove_neighbor(self, vertex, neighbor):
        if str(neighbor) in self.neighbors[str(vertex)]:
            self.neighbors[str(vertex)].remove(str(neighbor))
            self.neighbors[str(neighbor)].remove(str(vertex))
            return True
        else:
            return False

    def add_edge_directed(self, vertex, neighbor):
        if str(neighbor) not in self.neighbors[str(vertex)]:
            self.neighbors[str(vertex)].append(str(neighbor))
            return True
        else:
            return False

    def add_edge_undirected(self, vertex, neighbor):
        if str(neighbor) not in self.neighbors[str(vertex)]:
            self.neighbors[str(vertex)].append(str(neighbor))
            self.neighbors[str(neighbor)].append(str(vertex))
            return True
        else:
            return False

    def isAdjacent(self, vertex1, vertex2):
        if str(vertex1) in self.neighbors[str(vertex2)]:
            return True
        elif str(vertex2) in self.neighbors[str(vertex1)]:
            return True
        else:
            return False

    def reset_graph(self):
        self.vertices.clear()
        self.edge_indices.clear()
        self.neighbors.clear()
        self.vertices = {}
        self.edge_indices = {}
        self.neighbors = {}

    def get_number_of_edges(self):
        self.neighbors = {int(c): v for c, v in self.neighbors.items()}
        self.neighbors = OrderedDict(sorted(self.neighbors.items()))
        self.neighbors = {str(c): v for c, v in self.neighbors.items()}
        for vertex, neighbors in self.neighbors.items():
            print("Node {:>{}} has {:>{}} edges {}".format(int(vertex) + 1, len(str(len(self.neighbors))),
                                                           len(self.neighbors[vertex]), len(str(len(self.neighbors))),
                                                           ("*" * len(self.neighbors[vertex]))))
        print()
