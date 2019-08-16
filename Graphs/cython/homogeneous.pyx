"""
from math import exp
import numpy as np

def rbf_network(double[:, :] X,  double[:] beta, double theta):

    cdef int N = X.shape[0]
    cdef int D = X.shape[1]
    cdef double[:] Y = np.zeros(N)
    cdef int i, j, d
    cdef double r = 0

    for i in range(N):
        for j in range(N):
            r = 0
            for d in range(D):
                r += (X[j, d] - X[i, d]) ** 2
            r = r**0.5
            Y[i] += beta[j] * exp(-(r * theta)**2)

    return Y
"""


# class Homogeneous:
#
#     def __init__(self):
#         pass
#
#     @timeit
#     def generate_graph(self, number_of_vertices):
#         cdef int i, j
#         out = []
#         for self.i in range(number_of_vertices):
#             outout = ''
#             for self.j in range(number_of_vertices):
#                 outout += '1'
#
#         #     [out.append(int(outout, 2)) for outout in self.devide_binary_string(outout, number_of_vertices)]
#         # print(out)
#         # print(sys.getsizeof(out))
#
#     @timeit
#     def generate_graph_pure(self, number_of_vertices):
#         out = []
#         for i in range(number_of_vertices):
#             outout = ''
#             for j in range(number_of_vertices):
#                 outout += '1'
#
#         #     [out.append(int(outout, 2)) for outout in self.devide_binary_string(outout, number_of_vertices)]
#         # print(out)
#         # print(sys.getsizeof(out))
#
#         # return sys.getsizeof(out)
#
#     def lfactor(self, num, depth=1):
#         """returns the largest factor of num that isn't num"""
#
#         counter = 0
#         for i in range(num - 1, 0, -1):  # go backwards from num - 1 to 1
#             if num % i == 0:  # if a number divides evenly
#                 counter += 1
#                 if counter == depth:
#                     # print(i)
#                     return i
#
#     def devide_binary_string(self, string, number_of_vertices):
#         devided_binary_string = []
#         string_max_devider = self.lfactor(number_of_vertices, depth=1)
#         for devided_string in [string[:string_max_devider]]:
#             devided_binary_string.append(devided_string)
#         return devided_binary_string


cpdef list generate_graph(int number_of_vertices):
    cdef int i, j
    cdef list arr=[]
    cdef list outout=[]
    cdef str outout2= ''

    for i in range(number_of_vertices):
        outout=[]
        # outout2=''
        for j in range(number_of_vertices):
            outout.append(1)
            # outout2 += '1'
        # print(outout2)
        arr.append(outout)
        # arr.append(outout2)
    return arr


# graph = Homogeneous()
#
# number_vertex = 100

# graph.generate_graph(number_vertex)
# graph.generate_graph_pure(number_vertex)
