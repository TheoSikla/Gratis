from Graphs.cython.homogeneous import generate_graph
from Graphs.cython.pp import generate_graph_pure
from Support_Folders.timer import timeit
from Support_Folders.run_length_encoder import RunLengthEncoder
import sys

x = 10000

@timeit
def t():
    graph_matrix = generate_graph(x)
    # graph_matrix = generate_graph_2(x)
    # print(a[0])
    # print(f"size of graph {sys.getsizeof(graph_matrix)}")
    # print(f"size of row {sys.getsizeof(graph_matrix[0])}")
    # print(graph_matrix)
    # print(graph_matrix[0])
    # enc = encoder.encode([''.join(str(_) for _ in graph_matrix[0])][0])
    # print(enc)
    # print(len(enc))
    # dec = encoder.decode(enc)
    # print(dec)
    # print(sys.getsizeof(1.0))
    # print(sys.getsizeof([1 for _ in range(30000)]) * 30000)
    # print(sys.getsizeof('1' * 30000) * 30000)



@timeit
def r():
    generate_graph_pure(x)


encoder = RunLengthEncoder()

t()
# r()