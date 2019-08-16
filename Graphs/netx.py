import networkx as nx
from Support_Folders.timer import timeit
import sys
import numpy as np
import cython

# a = np.ones([60000, 60000], dtype=np.int8)  # 3.6 GB
# print(a.itemsize * a.size)

# a = np.ones([60000, 60000], dtype=np.int8)
# print(a.itemsize * a.size)

# b = np.packbits(np.ones([60000, 60000], dtype=np.int8), axis=-1)
# print(b.size * b.itemsize)

# a = '000101' * 10000000
# print(sys.getsizeof(a))
# # print(sys.getsizeof(a))
# a = int(a, 2)
# # print(a)
# print(sys.getsizeof(a))

# b = [x for x in range(10000)]
# print(sys.getsizeof(b))


# print(sys.getsizeof(1))
# print(sys.getsizeof('1'))
# print(sys.getsizeof(b'1'))
# print(sys.getsizeof(int('1', 2)))
# print(sys.getsizeof(True))
# print(sys.getsizeof(False))
# print(sys.getsizeof(None))
# print(sys.getsizeof(b'\0ff'))
# print(sys.getsizeof())
# import ctypes
# x = ctypes.c_ubyte(0xff)
# print(sys.getsizeof(x))
num = 10000
string = '1' * num
import zlib
# print(string.encode("utf-8"))
# print(sys.getsizeof(zlib.compress(string.encode("utf-8"))) * num)
# print(zlib.compress(string.encode("utf-8")))
# print(sys.getsizeof(string))
# print(sys.getsizeof(int(string, 2)))

# print(sys.getsizeof(string))
# print(sys.getsizeof(int(string, 2)))
# print(sys.getsizeof(int(string[:len(string)//1000], 2)))
# print(int(string[:len(string)//1000], 2))
#
# d = [1023 for i in range(10)]
# print(sys.getsizeof(d))


@cython.cclass
class Homogeneous:
    i = cython.declare(cython.int, visibility='public')
    j = cython.declare(cython.int, visibility='public')

    def __init__(self):
        print(type(self.i))

    @timeit
    def generate_graph(self, number_of_vertices):
        out = []
        for self.i in range(number_of_vertices):
            outout = ''
            for self.j in range(number_of_vertices):
                outout += '1'

        #     [out.append(int(outout, 2)) for outout in self.devide_binary_string(outout, number_of_vertices)]
        # print(out)
        # print(sys.getsizeof(out))

    @timeit
    def generate_graph_pure(self, number_of_vertices):
        out = []
        for i in range(number_of_vertices):
            outout = ''
            for j in range(number_of_vertices):
                outout += '1'

        #     [out.append(int(outout, 2)) for outout in self.devide_binary_string(outout, number_of_vertices)]
        # print(out)
        # print(sys.getsizeof(out))

        # return sys.getsizeof(out)

    def lfactor(self, num, depth=1):
        """returns the largest factor of num that isn't num"""

        counter = 0
        for i in range(num - 1, 0, -1):  # go backwards from num - 1 to 1
            if num % i == 0:  # if a number divides evenly
                counter += 1
                if counter == depth:
                    # print(i)
                    return i

    def devide_binary_string(self, string, number_of_vertices):
        devided_binary_string = []
        string_max_devider = self.lfactor(number_of_vertices, depth=1)
        for devided_string in [string[:string_max_devider]]:
            devided_binary_string.append(devided_string)
        return devided_binary_string




graph = Homogeneous()

# num = 100000
# # print(len(str(num)))
# string = '1' * num
# # print()
# print(sys.getsizeof(int(string[:len(string)//graph.lfactor(num, depth=len(str(num)) * 2) * graph.lfactor(num, depth=len(str(num)) * 2)], 2)))
number_vertex = 100
# string = '1' * number_vertex
# print(sys.getsizeof(string) * number_vertex)
# print(graph.generate_graph(number_vertex))
graph.generate_graph(number_vertex)
graph.generate_graph_pure(number_vertex)
