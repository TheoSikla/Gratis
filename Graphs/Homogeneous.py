__author__ = "Theodoros Siklafidis"
__name__ = "Gratis"
__version__ = "1.0"
__license__ = "GNU General Public License v3.0"

import sys
from Analyze.Analyze import *
from Generate.Generate import *


class Homogeneous:
    """
        This class creates a homogeneous graph and an adjacency matrix based on the number of vertices given by the
        user interface.
        Homogeneous graph is a graph that has all its vertices connected with each other.
    """

    def __init__(self):
        self.g = None

    def create_homogeneous_graph(self, graph_respresentation_type, numOfVertices, thread):
        if graph_respresentation_type == "Matrix":
            from Graphs.graph_adjacency_matrix import Graph, Vertex
        else:
            from Graphs.graph_adjacency_list import Graph, Vertex

        self.g = Graph()
        self.g.reset_graph()

        for i in range(numOfVertices):
            self.g.add_vertex(Vertex(str(i)))
            if thread.isStopped():
                sys.exit(0)

        for i in range(numOfVertices):
            for j in range(numOfVertices):
                if i != j and i < j:
                    self.g.add_edge_undirected(i, j)
                    if thread.isStopped():
                        sys.exit(0)

        generator.generate(graph_respresentation_type, self.g, thread)

        if graph_respresentation_type == "Matrix":
            analyzer.analyze_generated_graph(self.g.edges, graph_respresentation_type, self.__class__.__name__.replace("_", " "), numOfVertices)
        else:
            analyzer.analyze_generated_graph(self.g.neighbors, graph_respresentation_type, self.__class__.__name__.replace("_", " "), numOfVertices)
