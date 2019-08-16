from Graphs.cython.homogeneous import generate_graph
from Graphs.cython.pp import generate_graph_pure
from Support_Folders.timer import timeit
import random
import sys
import re
from enum import Enum


class RunLengthEncoder:
    REPEATS_RE = re.compile(r'(.)\1*')
    NUMBERS_RE = re.compile(r'(\d+)(.)')

    def __init__(self):
        self.mode = None

    def check_input(self, string):
        self.mode = "binary" if all(_ in '01' for _ in string) else "normal"

    def to_numbers(self, match):
        length = len(match.group(0))
        return (
            str(length) + match.group(1)
            if length > 1
            else match.group(1)
        )

    def from_numbers(self, match):
        return int(match.group(1)) * match.group(2)

    def encode(self, string):
        self.check_input(string)
        if self.mode == 'normal':
            return self.REPEATS_RE.sub(self.to_numbers, string)
        string = ''.join([chr(int(char)) for char in string])
        # print(string)
        return self.REPEATS_RE.sub(self.to_numbers, string)

    def decode(self, string):
        if self.mode == 'normal':
            return self.NUMBERS_RE.sub(self.from_numbers, string)
        # print(string)
        return ''.join([''.join(str(ord(digit))) for digit in self.NUMBERS_RE.sub(self.from_numbers, string)])


x = 10000


@timeit
def t():
    string = generate_graph(x)
    # print(a[0])
    print(sys.getsizeof(string))
    # print(string[0])
    enc = encode([''.join(str(_) for _ in string[0])][0])
    print(enc)
    dec = decode(enc)
    print(dec)
    # print(len(dec))
    # print(sys.getsizeof(encode([''.join(str(_) for _ in string[0])][0])))
    # import zib
    #     # print([''.join(str(_) for _ in string[0])][0].encode("utf-8"))
    #     # # print(type([''.join(str(_) for _ in string[0])][0]))
    #     # st = [''.join(str(_) for _ in string[0])][0]
    #     # print(sys.getsizeof(zlib.compress(st.encode("utf-8"))) * 10000)
    #     # print(zlib.compress(st.encode("utf-8")))lib
    # print([''.join(str(_) for _ in string[0])][0].encode("utf-8"))
    # # print(type([''.join(str(_) for _ in string[0])][0]))
    # st = [''.join(str(_) for _ in string[0])][0]
    # print(sys.getsizeof(zlib.compress(st.encode("utf-8"))) * 10000)
    # print(zlib.compress(st.encode("utf-8")))


@timeit
def r():
    generate_graph_pure(x)


# t()
# r()

encoder = RunLengthEncoder()


random_string = ''
for j in range(1000):
    for i in range(1000):
        random_string += str(random.randint(0, 1))

    # print(random_string)
    # print(all(c in '01' for c in random_string))
    # random_string = 'aaaaabbhhnaaasssdd'
    enc = encoder.encode(random_string)
    # print(enc)
    # print(len(enc))
    dec = encoder.decode(enc)
    assert random_string == dec
    # print(dec)
    # # print(len(dec))
    # print(''.join([''.join(str(ord(digit))) for digit in random_string]))
    # assert ''.join([''.join(str(ord(digit))) for digit in random_string]) == dec
    random_string = ''
    # print()


# random_string = 'aaaaabbhhnaaasssdd'
# print(random_string)
# enc = encode(random_string)
# print(enc)
# dec = decode(enc)
# print(dec)