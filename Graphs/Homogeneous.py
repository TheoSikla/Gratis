from Generate.Generate import *
from Analyze.Analyze import *
import sys


class Homogeneous:
    """
        This class creates a homogeneous graph and an adjacency matrix based on the number of vertices given by the
        user interface.
        Homogeneous graph is a graph that has all its vertices connected with each other.
    """

    def __init__(self):
        self.g = None

    def create_homogeneous_graph(self, adjacency_type, numOfVertices, thread):
        if adjacency_type == "Matrix":
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

        generator.generate(adjacency_type, self.g, thread)

        if adjacency_type == "Matrix":
            analyzer.analyze_matrix(self.g.edges, 'Homogeneous', numOfVertices)
        else:
            analyzer.analyze_list(self.g.neighbors, 'Homogeneous', numOfVertices)
